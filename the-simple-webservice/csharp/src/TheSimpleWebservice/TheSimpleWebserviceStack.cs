using System.Collections.Generic;
using Amazon.CDK;
using Amazon.CDK.AWS.APIGatewayv2;
using Amazon.CDK.AWS.APIGatewayv2.Integrations;
using Amazon.CDK.AWS.DynamoDB;
using Amazon.CDK.AWS.Lambda;

namespace TheSimpleWebservice
{
    public class TheSimpleWebserviceStack : Stack
    {
        internal TheSimpleWebserviceStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            //DynamoDB Table
            var table = new Table(this, "Hits", new TableProps
            {
                PartitionKey = new Attribute
                {
                    Name = "path",
                    Type = AttributeType.STRING
                }
            });
            
            // defines an AWS Lambda resource
            var dynamoLambda = new Function(this, "DynamoLambdaHandler", new FunctionProps
            {
                Runtime = Runtime.NODEJS_12_X,                // execution environment
                Code = Code.FromAsset("lambda-fns"),    //code loaded from the "lambda" directory
                Handler = "lambda.handler",                   //code loaded from the "lambda" directory
                Environment = new Dictionary<string, string>
                {
                    { "HITS_TABLE_NAME", table.TableName }
                }
            });
            
            // grant the lambda role read/write permissions to our table
            table.GrantReadWriteData(dynamoLambda);

            
            // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
            var api = new HttpApi(this, "Endpoint", new HttpApiProps
            {
                DefaultIntegration = new LambdaProxyIntegration(new LambdaProxyIntegrationProps
                {
                    Handler = dynamoLambda
                })
            });

            new CfnOutput(this, "HTTP API Url", new CfnOutputProps
            {
                Value = api.Url ?? "Something went wrong with the deploy"
            });
        }
    }
}
