from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    core
)


class TheFatLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        add_lambda = _lambda.Function(self, "fatLambdaHandler",
                                      runtime=_lambda.Runtime.PYTHON_3_8,
                                      handler="fatlambda.add",
                                      code=_lambda.Code.from_asset("lambdas/the_fat_lambda")
                                      )

        # defines an API Gateway REST API resource backed by our "lambda_lith" function.
        api_gw.LambdaRestApi(self, 'fatLambdaAPI',
                             handler=add_lambda
                             )
