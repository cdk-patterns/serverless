from aws_cdk import (
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_dynamodb as dynamo_db,
    core
)


class TheDynamoFlowStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, sns_topic_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamo_db.Table(self, "Hits",
                                partition_key=dynamo_db.Attribute(name="path", type=dynamo_db.AttributeType.STRING)
                                )

        dynamo_lambda = _lambda.Function(self, "DynamoLambdaHandler",
                                         runtime=_lambda.Runtime.NODEJS_12_X,
                                         handler="dynamo.handler",
                                         code=_lambda.Code.from_asset("lambda_fns"),
                                         tracing=_lambda.Tracing.ACTIVE,
                                         environment={
                                             "HITS_TABLE_NAME": table.table_name
                                         }
                                         )
        # grant the lambda role read/write permissions to our table
        table.grant_read_write_data(dynamo_lambda)

        topic = sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic_arn)
        topic.add_subscription(subscriptions.LambdaSubscription(dynamo_lambda))
