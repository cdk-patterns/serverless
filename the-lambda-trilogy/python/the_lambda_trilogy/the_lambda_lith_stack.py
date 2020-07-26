from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    core
)


class TheLambdalithStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_lith = _lambda.Function(self, "lambdalithHandler",
                                       runtime=_lambda.Runtime.PYTHON_3_8,
                                       handler="lambdalith.handler",
                                       code=_lambda.Code.from_asset("lambda_fns/the_lambda_lith/flask")
                                       )

        # defines an API Gateway REST API resource backed by our "lambda_lith" function.
        api_gw.LambdaRestApi(self, 'LambdalithAPI',
                             handler=lambda_lith
                             )
