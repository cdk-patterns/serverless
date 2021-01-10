using Amazon.CDK;
using System.Collections.Generic;
using Lambda = Amazon.CDK.AWS.Lambda;
using SAM = Amazon.CDK.AWS.SAM;

namespace TheLambdaPowerTuner
{
    public class TheLambdaPowerTunerStack : Stack
    {

        readonly private Lambda.Function _functionExample;
        readonly private string _powerValues = "128,256,512,1024,1536,3008";
        readonly private string _lambdaResource = "*";

        internal TheLambdaPowerTunerStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {

            //  An example lambda that can be used to test the powertuner
            _functionExample = new Lambda.Function(this, "exampleLambda", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Handler = "index.handler",
                Code = Lambda.Code.FromInline("exports.handler = function(event, ctx, cb) { return cb(null, 'hi'); }"),
            });

            // uncomment to only allow this power tuner to manipulate this defined function
            //var _lambdaResource = _functionExample.FunctionArn;

            // Output the Lambda function ARN in the deploy logs to ease testing
            new CfnOutput(this, "LambdaARN", new CfnOutputProps
            {
                Value = _functionExample.FunctionArn
            });

            // Deploy the aws-lambda-powertuning application from the Serverless Application Repository
            // https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning
            new SAM.CfnApplication(this, "powerTuner", new SAM.CfnApplicationProps
            {
                Location = new SAM.CfnApplication.ApplicationLocationProperty
                {
                    ApplicationId = "arn:aws:serverlessrepo:us-east-1:451282441545:applications/aws-lambda-power-tuning",
                    SemanticVersion = "3.4.0"
                },
                Parameters = new Dictionary<string, object>
                {
                    { "lambdaResource", _lambdaResource },
                    { "PowerValues", _powerValues }
                }
            });

        }
    }
}
