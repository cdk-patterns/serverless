from aws_cdk import (
    aws_lambda as _lambda,
    aws_stepfunctions as step_fn,
    aws_stepfunctions_tasks as step_fn_tasks,
    aws_sqs as sqs,
    aws_apigateway as api_gw,
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
        job_failed = step_fn.Fail(self, 'Sorry, We Dont add Pineapple',
                                  cause='Failed To Make Pizza',
                                  error='They asked for Pineapple')

        # If they didnt ask for pineapple let's cook the pizza
        cook_pizza = step_fn.Pass(self, 'Lets make your pizza')

        # If they ask for a pizza with pineapple, fail. Otherwise cook the pizza
        definition = step_fn.Chain \
            .start(order_pizza) \
            .next(step_fn.Choice(self, 'With Pineapple?') \
                  .when(step_fn.Condition.boolean_equals('$.pineappleAnalysis.containsPineapple', True), job_failed) \
                  .otherwise(cook_pizza))

        state_machine = step_fn.StateMachine(self, 'StateMachine', definition=definition, timeout=core.Duration.minutes(5))

        # Dead Letter Queue Setup
        # https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
        dlq = sqs.Queue(self, 'stateMachineLambdaDLQ', visibility_timeout=core.Duration.seconds(300))

        # defines an AWS Lambda resource to connect to our API Gateway
        state_machine_lambda = _lambda.Function(self, "stateMachineLambdaHandler",
                                                runtime=_lambda.Runtime.NODEJS_12_X,
                                                handler="stateMachineLambda.handler",
                                                code=_lambda.Code.from_asset("lambda_fns"),
                                                environment={
                                                    'statemachine_arn': state_machine.state_machine_arn
                                                }
                                                )

        state_machine.grant_start_execution(state_machine_lambda)

        # Simple API Gateway proxy integration
        # defines an API Gateway REST API resource backed by our "state_machine_lambda" function.
        api_gw.LambdaRestApi(self, 'Endpoint',
                             handler=state_machine_lambda
                             )
