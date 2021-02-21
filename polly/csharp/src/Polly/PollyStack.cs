using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using APIGatewayV2 = Amazon.CDK.AWS.APIGatewayv2;
using APIGatewayV2Integrations = Amazon.CDK.AWS.APIGatewayv2.Integrations;
using IAM = Amazon.CDK.AWS.IAM;

namespace Polly
{
    public class PollyStack : Stack
    {

        private readonly Lambda.Function _pollyFunction;
        private readonly IAM.PolicyStatement _pollyPolicy;
        private readonly APIGatewayV2.HttpApi _httpApi;


        internal PollyStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            // Lambda Function that takes in text and returns a polly voice synthesis
            _pollyFunction = new Lambda.Function(this, "pollyHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.PYTHON_3_8,
                Code = Lambda.Code.FromAsset("lambda_fns"),
                Handler = "polly.handler"
            });

            // https://docs.aws.amazon.com/polly/latest/dg/api-permissions-reference.html
            // https://docs.aws.amazon.com/translate/latest/dg/translate-api-permissions-ref.html
            _pollyPolicy = new IAM.PolicyStatement(new IAM.PolicyStatementProps
            {
                Effect = IAM.Effect.ALLOW,
                Resources = new[] { "*" },
                Actions = new[]
                {
                    "translate:TranslateText", "polly:SynthesizeSpeech"
                }
            });

            _pollyFunction.AddToRolePolicy(_pollyPolicy);

            // defines an API Gateway Http API resource backed by our "pollyHandler" function.
            _httpApi = new APIGatewayV2.HttpApi(this, "Polly", new APIGatewayV2.HttpApiProps
            {
                DefaultIntegration = new APIGatewayV2Integrations.LambdaProxyIntegration(
                    new APIGatewayV2Integrations.LambdaProxyIntegrationProps
                    {
                        Handler = _pollyFunction
                    })
            });

            new CfnOutput(this, "HTTP API Url", new CfnOutputProps
            {
                Value = _httpApi.Url
            });
        }
    }
}
