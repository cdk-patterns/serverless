from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    aws_sqs as sqs,
    core
)


class TheScalableWebhookStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        # This is standing in for what is RDS on the diagram due to simpler/cheaper setup
        table = dynamo_db.Table(self, "Messages",
                                partition_key=dynamo_db.Attribute(name="id", type=dynamo_db.AttributeType.STRING)
                                )

        # Queue Setup
        sqs_queue = sqs.Queue(self, 'RDSPublishQueue', visibility_timeout=core.Duration.seconds(300))

        # defines an AWS  Lambda resource to publish to our sqs_queue
        sqs_publish_lambda = _lambda.Function(self, "SQSPublishLambdaHandler",
                                              runtime=_lambda.Runtime.NODEJS_12_X,              # execution environment
                                              handler="lambda.handler",                         # file is "lambda", function is "handler"
                                              code=_lambda.Code.from_asset("lambda_fns/publish"),  # Code loaded from the lambda_fns/publish dir
                                              environment={
                                                  'queueURL': sqs_queue.queue_url
                                              }
                                              )
        sqs_queue.grant_send_messages(sqs_publish_lambda)

        # defines an AWS  Lambda resource to pull from our sqs_queue
        sqs_subscribe_lambda = _lambda.Function(self, "SQSSubscribeLambdaHandler",
                                                runtime=_lambda.Runtime.NODEJS_12_X,              # execution environment
                                                handler="lambda.handler",                         # file is "lambda", function is "handler"
                                                code=_lambda.Code.from_asset("lambda_fns/subscribe"),# Code loaded from the lambda_fns/subscribe dir
                                                environment={
                                                  'queueURL': sqs_queue.queue_url,
                                                  'tableName': table.table_name
                                                },
                                                reserved_concurrent_executions=2
                                              )
        sqs_queue.grant_consume_messages(sqs_subscribe_lambda)
        sqs_subscribe_lambda.add_event_source(lambda_event.SqsEventSource(sqs_queue))
        table.grant_read_write_data(sqs_subscribe_lambda)

        # defines an API Gateway REST API resource backed by our "sqs_publish_lambda" function.
        api_gw.LambdaRestApi(self, 'Endpoint',
                             handler=sqs_publish_lambda
                             )
