from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as dynamo_db,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    core
)


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