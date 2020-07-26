from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    core
)


class TheSinglePurposeFunctionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # We have 3 separate lambda functions, all coming from separate files
        ###

        add_lambda = _lambda.Function(self, "addLambdaHandler",
                                      runtime=_lambda.Runtime.PYTHON_3_8,
                                      handler="add.handler",
                                      code=_lambda.Code.from_asset("lambda_fns/the_single_purpose_function")
                                      )

        subtract_lambda = _lambda.Function(self, "subtractLambdaHandler",
                                           runtime=_lambda.Runtime.PYTHON_3_8,
                                           handler="subtract.handler",
                                           code=_lambda.Code.from_asset("lambda_fns/the_single_purpose_function")
                                           )

        multiply_lambda = _lambda.Function(self, "multiplyLambdaHandler",
                                           runtime=_lambda.Runtime.PYTHON_3_8,
                                           handler="multiply.handler",
                                           code=_lambda.Code.from_asset("lambda_fns/the_single_purpose_function")
                                           )

        ###
        # All functions have their own endpoint defined on our gateway
        ##

        api = api_gw.LambdaRestApi(self, 'singlePurposeFunctionAPI',
                                   handler=add_lambda,
                                   proxy=False
                                   )

        api.root.resource_for_path('add').add_method('GET', api_gw.LambdaIntegration(add_lambda))
        api.root.resource_for_path('subtract').add_method('GET', api_gw.LambdaIntegration(subtract_lambda))
        api.root.resource_for_path('multiply').add_method('GET', api_gw.LambdaIntegration(multiply_lambda))