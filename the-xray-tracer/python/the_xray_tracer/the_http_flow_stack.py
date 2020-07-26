from aws_cdk import (
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    core
)


class TheHttpFlowStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, sns_topic_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        http_lambda = _lambda.Function(self, "httpLambdaHandler",
                                       runtime=_lambda.Runtime.NODEJS_12_X,
                                       handler="http.handler",
                                       code=_lambda.Code.from_asset("lambda_fns"),
                                       tracing=_lambda.Tracing.ACTIVE
                                       )

        topic = sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic_arn)
        topic.add_subscription(subscriptions.LambdaSubscription(http_lambda))
