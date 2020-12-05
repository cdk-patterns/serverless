from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    core
)
import os


class ThePredictiveLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # defines an AWS  Lambda resource
        model_folder = os.path.dirname(os.path.realpath(__file__)) + "/../model"
        predictive_lambda = _lambda.DockerImageFunction(self, 'PredictiveLambda',
                                                        code=_lambda.DockerImageCode.from_image_asset(model_folder),
                                                        memory_size=4096,
                                                        timeout=core.Duration.seconds(15))
        # defines an API Gateway Http API resource backed by our "PredictiveLambda" function.
        api = api_gw.HttpApi(self, 'PredictiveLambdaEndpoint',
                             default_integration=integrations.LambdaProxyIntegration(handler=predictive_lambda));

        core.CfnOutput(self, 'HTTP API Url', value=api.url);
