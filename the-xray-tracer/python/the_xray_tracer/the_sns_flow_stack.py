from aws_cdk import (
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    core
)


class TheSnsFlowStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, sns_topic_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # SNS Topic creation
        topic = sns.Topic(self, 'TheXRayTracerSnsTopic', display_name='The XRay Tracer CDK Pattern Topic')

        sns_lambda = _lambda.Function(self, "snsLambdaHandler",
                                      runtime=_lambda.Runtime.NODEJS_12_X,
                                      handler="sns_publish.handler",
                                      code=_lambda.Code.from_asset("lambda_fns"),
                                      tracing=_lambda.Tracing.ACTIVE,
                                      environment={
                                          "TOPIC_ARN": topic.topic_arn
                                      }
                                      )
        topic.grant_publish(sns_lambda)
        apigw_topic = sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic_arn)
        apigw_topic.add_subscription(subscriptions.LambdaSubscription(sns_lambda))

        sns_subscriber_lambda = _lambda.Function(self, "snsSubscriptionLambdaHandler",
                                                 runtime=_lambda.Runtime.NODEJS_12_X,
                                                 handler="sns_subscribe.handler",
                                                 code=_lambda.Code.from_asset("lambda_fns"),
                                                 tracing=_lambda.Tracing.ACTIVE
                                                 )
        topic.add_subscription(subscriptions.LambdaSubscription(sns_subscriber_lambda))
