from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    core
)


class TheEventbridgeAtmStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #
        # Producer Lambda
        #
        atm_producer_lambda = _lambda.Function(self, "atmProducerLambda",
                                               runtime=_lambda.Runtime.NODEJS_12_X,
                                               handler="handler.lambdaHandler",
                                               code=_lambda.Code.from_asset("lambda_fns/atmProducer")
                                               )

        event_policy = iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=['*'], actions=['events:PutEvents'])

        atm_producer_lambda.add_to_role_policy(event_policy)

        #
        # Approved Transaction Consumer
        #
        atm_consumer1_lambda = _lambda.Function(self, "atmConsumer1Lambda",
                                                runtime=_lambda.Runtime.NODEJS_12_X,
                                                handler="handler.case1Handler",
                                                code=_lambda.Code.from_asset("lambda_fns/atmConsumer")
                                                )

        atm_consumer1_rule = events.Rule(self, 'atmConsumer1LambdaRule',
                                         description='Approved Transactions',
                                         event_pattern=events.EventPattern(source=['custom.myATMapp'],
                                                                           detail_type=['transaction'],
                                                                           detail={
                                                                              "result": ["approved"]
                                                                            }))

        atm_consumer1_rule.add_target(targets.LambdaFunction(handler=atm_consumer1_lambda))

        #
        # NY Prefix Consumer
        #
        atm_consumer2_lambda = _lambda.Function(self, "atmConsumer2Lambda",
                                                runtime=_lambda.Runtime.NODEJS_12_X,
                                                handler="handler.case2Handler",
                                                code=_lambda.Code.from_asset("lambda_fns/atmConsumer")
                                                )

        atm_consumer2_rule = events.Rule(self, 'atmConsumer2LambdaRule',
                                         event_pattern=events.EventPattern(source=['custom.myATMapp'],
                                                                           detail_type=['transaction'],
                                                                           detail={
                                                                               "location": [{"prefix": "NY-"}]
                                                                           }))

        atm_consumer2_rule.add_target(targets.LambdaFunction(handler=atm_consumer2_lambda))

        #
        # Not Approved Consumer
        #
        atm_consumer3_lambda = _lambda.Function(self, "atmConsumer3Lambda",
                                                runtime=_lambda.Runtime.NODEJS_12_X,
                                                handler="handler.case3Handler",
                                                code=_lambda.Code.from_asset("lambda_fns/atmConsumer")
                                                )

        atm_consumer3_rule = events.Rule(self, 'atmConsumer3LambdaRule',
                                         event_pattern=events.EventPattern(source=['custom.myATMapp'],
                                                                           detail_type=['transaction'],
                                                                           detail={
                                                                               "result": [{"anything-but": "approved"}]
                                                                           }))

        atm_consumer3_rule.add_target(targets.LambdaFunction(handler=atm_consumer3_lambda))

        # defines an API Gateway REST API resource backed by our "atm_producer_lambda" function.
        api_gw.LambdaRestApi(self, 'Endpoint',
                             handler=atm_producer_lambda
                             )
