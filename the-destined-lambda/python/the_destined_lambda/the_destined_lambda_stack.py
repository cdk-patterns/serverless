from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_destinations as destinations,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    core
)


class TheDestinedLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # Let's create our own Event Bus for this rather than using default
        ###
        bus = events.EventBus(self, 'DestinedEventBus', event_bus_name='the-destined-lambda')

        ###
        # Destinations need invoked Asynchronously so let's use SNS
        ###
        topic = sns.Topic(self, 'theDestinedLambdaTopic', display_name='The Destined Lambda CDK Pattern Topic')

        ###
        # Lambda configured with success and failure destinations
        # Note the actual lambda has no EventBridge code inside it
        ###
        destined_lambda = _lambda.Function(self, "destinedLambda",
                                           runtime=_lambda.Runtime.NODEJS_12_X,
                                           handler="destinedLambda.handler",
                                           code=_lambda.Code.from_asset("lambdas"),
                                           retry_attempts=0,
                                           on_success=destinations.EventBridgeDestination(event_bus=bus),
                                           on_failure=destinations.EventBridgeDestination(event_bus=bus)
                                           )
        topic.add_subscription(subscriptions.LambdaSubscription(destined_lambda))

        ###
        # This is a lambda that will be called by onSuccess for destinedLambda
        # It simply prints the event it receives to the cloudwatch logs
        ###
        success_lambda = _lambda.Function(self, "successLambda",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="success.handler",
                                          code=_lambda.Code.from_asset("lambdas"),
                                          timeout=core.Duration.seconds(3)
                                          )
        ###
        # EventBridge Rule to send events to our success lambda
        # Notice how we can still do event filtering based on the json payload returned by the destined lambda
        ###
        success_rule = events.Rule(self, 'successRule',
                                   event_bus=bus,
                                   description='all success events are caught here and logged centrally',
                                   event_pattern=events.EventPattern(
                                       detail={
                                           "requestContext": {
                                               "condition": ["Success"]
                                           },
                                           "responsePayload": {
                                               "source": ["cdkpatterns.the-destined-lambda"],
                                               "action": ["message"]
                                           }
                                       }))
        success_rule.add_target(targets.LambdaFunction(success_lambda))

        ###
        # This is a lambda that will be called by onFailure for destinedLambda
        # It simply prints the event it receives to the cloudwatch logs.
        # Notice how it includes the message that came into destined lambda to make it fail so you have
        # everything you need to do retries
        ###
        failure_lambda = _lambda.Function(self, "failureLambda",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="failure.handler",
                                          code=_lambda.Code.from_asset("lambdas"),
                                          timeout=core.Duration.seconds(3)
                                          )

        ###
        # EventBridge Rule to send events to our failure lambda
        ###
        failure_rule = events.Rule(self, 'failureRule',
                                   event_bus=bus,
                                   description='all failure events are caught here and logged centrally',
                                   event_pattern=events.EventPattern(
                                       detail={
                                           "responsePayload": {
                                               "errorType": ["Error"]
                                           }
                                       }))
        failure_rule.add_target(targets.LambdaFunction(failure_lambda))
