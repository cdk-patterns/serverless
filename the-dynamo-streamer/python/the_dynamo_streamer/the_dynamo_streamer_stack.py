from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as _event,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    aws_iam as iam,
    core
)


class TheDynamoStreamerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        # Streaming is enabled to send the whole new object down the pipe
        table = dynamo_db.Table(self, "TheDynamoStreamer",
                                partition_key=dynamo_db.Attribute(name="message",
                                                                  type=dynamo_db.AttributeType.STRING),
                                stream=dynamo_db.StreamViewType.NEW_IMAGE
                                )

        # defines an AWS  Lambda resource
        subscriber_lambda = _lambda.Function(self, "DynamoLambdaHandler",
                                             runtime=_lambda.Runtime.NODEJS_12_X,
                                             handler="lambda.handler",
                                             code=_lambda.Code.from_asset("lambdas/subscribe")
                                             )

        subscriber_lambda.add_event_source(_event.DynamoEventSource(table=table,
                                                                    starting_position=_lambda.StartingPosition.LATEST))

        # API Gateway Creation
        gateway = api_gw.RestApi(self, 'DynamoStreamerAPI',
                                 deploy_options=api_gw.StageOptions(metrics_enabled=True,
                                                                    logging_level=api_gw.MethodLoggingLevel.INFO,
                                                                    data_trace_enabled=True,
                                                                    stage_name='prod'
                                                                    ))

        # Give our gateway permissions to interact with dynamodb
        api_gw_dynamo_role = iam.Role(self, 'DefaultLambdaHanderRole',
                                      assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))
        table.grant_read_write_data(api_gw_dynamo_role)
