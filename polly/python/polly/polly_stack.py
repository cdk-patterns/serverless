from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_iam as iam,
    core
)


class PollyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lambda Function that takes in text and returns a polly voice synthesis
        polly_lambda = _lambda.Function(self, 'pollyHandler',
                                        runtime=_lambda.Runtime.PYTHON_3_8,
                                        code=_lambda.Code.from_asset('lambda_fns'),
                                        handler='polly.handler')

        # https://docs.aws.amazon.com/polly/latest/dg/api-permissions-reference.html
        # https://docs.aws.amazon.com/translate/latest/dg/translate-api-permissions-ref.html
        polly_policy = iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                           resources=['*'],
                                           actions=['translate:TranslateText',
                                                    'polly:SynthesizeSpeech'])
        polly_lambda.add_to_role_policy(polly_policy)

        # defines an API Gateway Http API resource backed by our "efs_lambda" function.
        api = api_gw.HttpApi(self, 'Polly',
                             default_integration=integrations.LambdaProxyIntegration(handler=polly_lambda))

        core.CfnOutput(self, 'HTTP API Url', value=api.url)
