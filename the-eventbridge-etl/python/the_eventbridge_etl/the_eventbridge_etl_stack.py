from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as _event,
    aws_dynamodb as dynamo_db,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_events as events,
    aws_events_targets as targets,
    core
)
import json


class TheEventbridgeEtlStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # If left unchecked this pattern could "fan out" on the transform and load
        # lambdas to the point that it consumes all resources on the account. This is
        # why we are limiting concurrency to 2 on all 3 lambdas. Feel free to raise this.
        lambda_throttle_size = 2

        ####
        # DynamoDB Table
        # This is where our transformed data ends up
        ####
        table = dynamo_db.Table(self, "TransformedData",
                                partition_key=dynamo_db.Attribute(name="id", type=dynamo_db.AttributeType.STRING)
                                )

        ####
        # S3 Landing Bucket
        # This is where the user uploads the file to be transformed
        ####
        bucket = s3.Bucket(self, "LandingBucket")

        ####
        # Queue that listens for S3 Bucket events
        ####
        queue = sqs.Queue(self, 'newObjectInLandingBucketEventQueue', visibility_timeout=core.Duration.seconds(300))

        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.SqsDestination(queue))

        # EventBridge Permissions
        event_bridge_put_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW, resources=['*'], actions=['events:PutEvents'])

        ####
        # Fargate ECS Task Creation to pull data from S3
        #
        # Fargate is used here because if you had a seriously large file,
        # you could stream the data to fargate for as long as needed before
        # putting the data onto eventbridge or up the memory/storage to
        # download the whole file. Lambda has limitations on runtime and
        # memory/storage
        ####
        vpc = ec2.Vpc(self, "Vpc", max_azs=2)

        logging = ecs.AwsLogDriver(stream_prefix='TheEventBridgeETL', log_retention=logs.RetentionDays.ONE_WEEK)

        cluster = ecs.Cluster(self, 'Ec2Cluster', vpc=vpc)

        task_definition = ecs.TaskDefinition(self, 'FargateTaskDefinition',
                                             memory_mib="512",
                                             cpu="256",
                                             compatibility=ecs.Compatibility.FARGATE)

        # We need to give our fargate container permission to put events on our EventBridge
        task_definition.add_to_task_role_policy(event_bridge_put_policy)
        # Grant fargate container access to the object that was uploaded to s3
        bucket.grant_read(task_definition.task_role)

        container = task_definition.add_container('AppContainer',
                                                  image=ecs.ContainerImage.from_asset('container/s3DataExtractionTask'),
                                                  logging=logging,
                                                  environment={
                                                      'S3_BUCKET_NAME': bucket.bucket_name,
                                                      'S3_OBJECT_KEY': ''
                                                  })

        ####
        # Lambdas
        #
        # These are used for 4 phases:
        #
        # Extract    - kicks of ecs fargate task to download data and splinter to eventbridge events
        # Transform  - takes the two comma separated strings and produces a json object
        # Load       - inserts the data into dynamodb
        # Observe    - This is a lambda that subscribes to all events and logs them centrally
        ####

        subnet_ids = []
        for subnet in vpc.private_subnets:
            subnet_ids.append(subnet.subnet_id)

        ####
        # Extract
        # defines an AWS Lambda resource to trigger our fargate ecs task
        ####
        extract_lambda = _lambda.Function(self, "extractLambdaHandler",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="s3SqsEventConsumer.handler",
                                          code=_lambda.Code.from_asset("lambda_fns/extract"),
                                          reserved_concurrent_executions=lambda_throttle_size,
                                          environment={
                                              "CLUSTER_NAME": cluster.cluster_name,
                                              "TASK_DEFINITION": task_definition.task_definition_arn,
                                              "SUBNETS": json.dumps(subnet_ids),
                                              "CONTAINER_NAME": container.container_name
                                          }
                                          )
        queue.grant_consume_messages(extract_lambda)
        extract_lambda.add_event_source(_event.SqsEventSource(queue=queue))
        extract_lambda.add_to_role_policy(event_bridge_put_policy)

        run_task_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW, resources=[task_definition.task_definition_arn], actions=['ecs:RunTask'])
        extract_lambda.add_to_role_policy(run_task_policy_statement)

        task_execution_role_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=[task_definition.obtain_execution_role().role_arn,
                       task_definition.task_role.role_arn],
            actions=['iam:PassRole'])
        extract_lambda.add_to_role_policy(task_execution_role_policy_statement)

        ####
        # Transform
        # defines a lambda to transform the data that was extracted from s3
        ####

        transform_lambda = _lambda.Function(self, "TransformLambdaHandler",
                                            runtime=_lambda.Runtime.NODEJS_12_X,
                                            handler="transform.handler",
                                            code=_lambda.Code.from_asset("lambda_fns/transform"),
                                            reserved_concurrent_executions=lambda_throttle_size,
                                            timeout=core.Duration.seconds(3)
                                            )
        transform_lambda.add_to_role_policy(event_bridge_put_policy)

        # Create EventBridge rule to route extraction events
        transform_rule = events.Rule(self, 'transformRule',
                                     description='Data extracted from S3, Needs transformed',
                                     event_pattern=events.EventPattern(source=['cdkpatterns.the-eventbridge-etl'],
                                                                       detail_type=['s3RecordExtraction'],
                                                                       detail={
                                                                           "status": ["extracted"]
                                                                       }))
        transform_rule.add_target(targets.LambdaFunction(handler=transform_lambda))

        ####
        # Load
        # load the transformed data in dynamodb
        ####

        load_lambda = _lambda.Function(self, "LoadLambdaHandler",
                                       runtime=_lambda.Runtime.NODEJS_12_X,
                                       handler="load.handler",
                                       code=_lambda.Code.from_asset("lambda_fns/load"),
                                       reserved_concurrent_executions=lambda_throttle_size,
                                       timeout=core.Duration.seconds(3),
                                       environment={
                                           "TABLE_NAME": table.table_name
                                       }
                                       )
        load_lambda.add_to_role_policy(event_bridge_put_policy)
        table.grant_read_write_data(load_lambda)

        load_rule = events.Rule(self, 'loadRule',
                                description='Data transformed, Needs loaded into dynamodb',
                                event_pattern=events.EventPattern(source=['cdkpatterns.the-eventbridge-etl'],
                                                                  detail_type=['transform'],
                                                                  detail={
                                                                      "status": ["transformed"]
                                                                  }))
        load_rule.add_target(targets.LambdaFunction(handler=load_lambda))

        ####
        # Observe
        # Watch for all cdkpatterns.the-eventbridge-etl events and log them centrally
        ####

        observe_lambda = _lambda.Function(self, "ObserveLambdaHandler",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="observe.handler",
                                          code=_lambda.Code.from_asset("lambda_fns/observe"),
                                          reserved_concurrent_executions=lambda_throttle_size,
                                          timeout=core.Duration.seconds(3)
                                          )

        observe_rule = events.Rule(self, 'observeRule',
                                   description='all events are caught here and logged centrally',
                                   event_pattern=events.EventPattern(source=['cdkpatterns.the-eventbridge-etl']))

        observe_rule.add_target(targets.LambdaFunction(handler=observe_lambda))
