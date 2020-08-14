using System.Collections.Generic;
using Amazon.CDK;
using Amazon.CDK.AWS.APIGateway;
using Amazon.CDK.AWS.Events;
using Amazon.CDK.AWS.Events.Targets;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;

namespace TheEventbridgeAtm
{
    public class TheEventbridgeAtmStack : Stack
    {
        public TheEventbridgeAtmStack(Construct scope, string id, IStackProps props = null) 
            : base(scope, id, props)
        {
            //Producer Lambda
            var atmProducerLambda = new Function(this, "atmProducerLambda", new FunctionProps
            {
                Runtime = Runtime.NODEJS_12_X,
                Code = Code.FromAsset("lambda-fns/atmProducer"),
                Handler = "handler.lambdaHandler"
            });

            var eventPolicy = new PolicyStatement(new PolicyStatementProps
            {
                Effect = Effect.ALLOW,
                Resources = new[] { "*" },
                Actions = new[] { "events:PutEvents" }
            });

            atmProducerLambda.AddToRolePolicy(eventPolicy);

            //Approved Transaction Consumer
            var atmConsumer1Lambda = new Function(this, "atmConsumer1Lambda", new FunctionProps
            {
                Runtime = Runtime.NODEJS_12_X,
                Code = Code.FromAsset("lambda-fns/atmConsumer"),
                Handler = "handler.case1Handler"
            });

            var atmConsumer1LambdaRule = new Rule(this, "atmConsumer1LambdaRule", new RuleProps
            {
                Description = "Approved transactions",
                EventPattern = new EventPattern
                {
                    Source = new[] { "custom.myATMapp" },
                    DetailType = new[] { "transaction" },
                    Detail = new Dictionary<string, object>
                    {
                        ["result"] = new[] { "approved" }
                    }
                }
            });

            atmConsumer1LambdaRule.AddTarget(new LambdaFunction(atmConsumer1Lambda));

            //NY Prefix Consumer
            var atmConsumer2Lambda = new Function(this, "atmConsumer2Lambda", new FunctionProps
            {
                Runtime = Runtime.NODEJS_12_X,
                Code = Code.FromAsset("lambda-fns/atmConsumer"),
                Handler = "handler.case2Handler"
            });

            var atmConsumer2LambdaRule = new Rule(this, "atmConsumer2LambdaRule", new RuleProps
            {
                Description = "Transactions with NY- prefix",
                EventPattern = new EventPattern
                {
                    Source = new[] { "custom.myATMapp" },
                    DetailType = new[] { "transaction" },
                    Detail = new Dictionary<string, object>
                    {
                        ["location"] = new []
                        {
                            new Dictionary<string, string>
                            {
                                ["prefix"] =  "NY-"
                            }
                        }
                    }
                }
            });

            atmConsumer2LambdaRule.AddTarget(new LambdaFunction(atmConsumer2Lambda));

            //Not Approved Consumer
            var atmConsumer3Lambda = new Function(this, "atmConsumer3Lambda", new FunctionProps
            {
                Runtime = Runtime.NODEJS_12_X,
                Code = Code.FromAsset("lambda-fns/atmConsumer"),
                Handler = "handler.case3Handler"
            });

            var atmConsumer3LambdaRule = new Rule(this, "atmConsumer3LambdaRule", new RuleProps
            {
                Description = "Not approved transactions",
                EventPattern = new EventPattern
                {
                    Source = new[] { "custom.myATMapp" },
                    DetailType = new[] { "transaction" },
                    Detail = new Dictionary<string, object>
                    {
                        ["result"] = new[]
                        {
                            new Dictionary<string, object>
                            {
                                ["anything-but"] = "approved"
                            }
                        }
                    }
                }
            });

            atmConsumer3LambdaRule.AddTarget(new LambdaFunction(atmConsumer3Lambda));

            //API Gateway proxy integration
            // defines an API Gateway REST API resource backed by our "atmProducerLambda" function.
            new LambdaRestApi(this, "Endpoint", new LambdaRestApiProps
            {
                Handler = atmProducerLambda
            });
        }
    }
}
