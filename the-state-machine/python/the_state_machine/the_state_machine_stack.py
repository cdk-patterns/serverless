from aws_cdk import (
    aws_lambda as _lambda,
    aws_stepfunctions as step_fn,
    aws_stepfunctions_tasks as step_fn_tasks,
    aws_iam as iam,
    aws_apigatewayv2 as api_gw,
    core
)


class TheStateMachineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Step Function Starts Here

        # The first thing we need to do is see if they are asking for pineapple on a pizza
        pineapple_check_lambda = _lambda.Function(self, "pineappleCheckLambdaHandler",
                                                  runtime=_lambda.Runtime.NODEJS_12_X,
                                                  handler="orderPizza.handler",
                                                  code=_lambda.Code.from_asset("lambda_fns"),
                                                  )

        # Step functions are built up of steps, we need to define our first step
        order_pizza = step_fn_tasks.LambdaInvoke(self, 'Order Pizza Job',
                                                 lambda_function=pineapple_check_lambda,
                                                 input_path='$.flavour',
                                                 result_path='$.pineappleAnalysis',
                                                 payload_response_only=True)

        # Pizza Order failure step defined
        pineapple_detected = step_fn.Fail(self, 'Sorry, We Dont add Pineapple',
                                          cause='They asked for Pineapple',
                                          error='Failed To Make Pizza')

        # If they didnt ask for pineapple let's cook the pizza
        cook_pizza = step_fn.Succeed(self, 'Lets make your pizza', output_path='$.pineappleAnalysis')

        # If they ask for a pizza with pineapple, fail. Otherwise cook the pizza
        definition = step_fn.Chain \
            .start(order_pizza) \
            .next(step_fn.Choice(self, 'With Pineapple?')
                  .when(step_fn.Condition.boolean_equals('$.pineappleAnalysis.containsPineapple', True),
                        pineapple_detected)
                  .otherwise(cook_pizza))

        state_machine = step_fn.StateMachine(self, 'StateMachine', definition=definition,
                                             timeout=core.Duration.minutes(5),
                                             tracing_enabled=True, state_machine_type=step_fn.StateMachineType.EXPRESS)

        # HTTP API Definition

        # Give our gateway permissions to interact with SNS
        http_api_role = iam.Role(self, 'HttpApiRole',
                                 assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'),
                                 inline_policies={
                                     "AllowSFNExec": iam.PolicyDocument(statements=[iam.PolicyStatement(
                                         actions=["states:StartSyncExecution"],
                                         effect=iam.Effect.ALLOW,
                                         resources=[state_machine.state_machine_arn]
                                     )])
                                 })

        api = api_gw.HttpApi(self, 'the_state_machine_api', create_default_stage=True)

        # create an AWS_PROXY integration between the HTTP API and our Step Function
        integ = api_gw.CfnIntegration(self, 'Integ', api_id=api.http_api_id, integration_type='AWS_PROXY',
                                      connection_type='INTERNET',
                                      integration_subtype='StepFunctions-StartSyncExecution',
                                      credentials_arn=http_api_role.role_arn,
                                      request_parameters={"Input": "$request.body",
                                                          "StateMachineArn": state_machine.state_machine_arn},
                                      payload_format_version="1.0",
                                      timeout_in_millis=10000)

        api_gw.CfnRoute(self, 'DefaultRoute', api_id=api.http_api_id, route_key=api_gw.HttpRouteKey.DEFAULT.key,
                        target="integrations/" + integ.ref)

        core.CfnOutput(self, 'HTTP API URL', value=api.url)
