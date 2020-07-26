from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_sqs as sqs,
    core
)


class TheSqsFlowStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, sns_topic_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Queue Setup
        sqs_queue = sqs.Queue(self, 'RDSPublishQueue', visibility_timeout=core.Duration.seconds(300))

        sqs_lambda = _lambda.Function(self, "sqsLambdaHandler",
                                      runtime=_lambda.Runtime.NODEJS_12_X,
                                      handler="sqs.handler",
                                      code=_lambda.Code.from_asset("lambda_fns"),
                                      tracing=_lambda.Tracing.ACTIVE,
                                      environment={
                                          "SQS_URL": sqs_queue.queue_url
                                      }
                                      )
        sqs_queue.grant_send_messages(sqs_lambda)

        topic = sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic_arn)
        topic.add_subscription(subscriptions.LambdaSubscription(sqs_lambda))

        sqs_subscribe_lambda = _lambda.Function(self, "sqsSubscribeLambdaHandler",
                                                runtime=_lambda.Runtime.NODEJS_12_X,
                                                handler="sqs_subscribe.handler",
                                                code=_lambda.Code.from_asset("lambda_fns"),
                                                tracing=_lambda.Tracing.ACTIVE
                                                )
        sqs_queue.grant_consume_messages(sqs_subscribe_lambda)
        sqs_subscribe_lambda.add_event_source(lambda_event.SqsEventSource(sqs_queue))

