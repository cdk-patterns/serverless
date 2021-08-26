using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using APIGateway = Amazon.CDK.AWS.APIGatewayv2;
using StepFunction = Amazon.CDK.AWS.StepFunctions;
using StepFunctionTasks = Amazon.CDK.AWS.StepFunctions.Tasks;
using IAM = Amazon.CDK.AWS.IAM;
using System.Collections.Generic;

namespace TheStateMachine
{
    public class TheStateMachineStack : Stack
    {

        readonly private Lambda.Function _pineappleCheckHandler;
        readonly private StepFunctionTasks.LambdaInvoke _orderPizzaTask;
        readonly private StepFunction.Fail _jobFailed;
        readonly private StepFunction.Pass _cookPizza;
        readonly private StepFunction.Chain _chainDefinition;
        readonly private StepFunction.StateMachine _stateMachine;
        readonly private IAM.Role _httpApiRole;
        readonly private APIGateway.HttpApi _api;
        readonly private APIGateway.CfnIntegration _integration;

        internal TheStateMachineStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {

            // Step Function Starts Here

            // The first thing we need to do is see if they are asking for pineapple on a pizza
            _pineappleCheckHandler = new Lambda.Function(this, "pineappleCheckHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Code = Lambda.Code.FromAsset("lambda_fns"),
                Handler = "orderPizza.handler"
            });

            /*
             * Step functions are built up of steps, we need to define our first step
             * This step was refactored due to Deprecated function
             */
            _orderPizzaTask = new StepFunctionTasks.LambdaInvoke(this, "Order Pizza Job", new StepFunctionTasks.LambdaInvokeProps
            {
                LambdaFunction = _pineappleCheckHandler,
                InputPath = "$.flavour",
                ResultPath = "$.pineappleAnalysis",
                PayloadResponseOnly = true
            });

            // Pizza Order failure step defined
            _jobFailed = new StepFunction.Fail(this, "Sorry, We Dont add Pineapple", new StepFunction.FailProps
            {
                Cause = "They asked for Pineapple",
                Error = "Failed To Make Pizza"
            });

            // If they didnt ask for pineapple let's cook the pizza
            _cookPizza = new StepFunction.Pass(this, "Lets make your pizza");

            // If they ask for a pizza with pineapple, fail. Otherwise cook the pizza
            _chainDefinition = StepFunction.Chain
                .Start(_orderPizzaTask)
                .Next(new StepFunction.Choice(this, "With Pineapple?") // Logical choice added to flow
                .When(StepFunction.Condition.BooleanEquals("$.pineappleAnalysis.containsPineapple", true), _jobFailed)
                .Otherwise(_cookPizza));

            // Building the state machine
            _stateMachine = new StepFunction.StateMachine(this, "StateMachine", new StepFunction.StateMachineProps
            {
                Definition = _chainDefinition,
                Timeout = Duration.Minutes(5),
                TracingEnabled = true,
                StateMachineType = StepFunction.StateMachineType.EXPRESS
            });

            /**
            * HTTP API Definition
            **/

            // We need to give our HTTP API permission to invoke our step function
            _httpApiRole = new IAM.Role(this, "HttpAPIRole", new IAM.RoleProps
            {
                AssumedBy = new IAM.ServicePrincipal("apigateway.amazonaws.com"),
                InlinePolicies = new Dictionary<string, IAM.PolicyDocument>
                {
                    {"AllowSFNExec", new IAM.PolicyDocument(new IAM.PolicyDocumentProps
                        {
                            Statements = new IAM.PolicyStatement[]
                            {
                                new IAM.PolicyStatement(new IAM.PolicyStatementProps
                                {
                                    Actions = new string[] {"states:StartSyncExecution"},
                                    Effect = IAM.Effect.ALLOW,
                                    Resources = new string[] {_stateMachine.StateMachineArn}
                                })
                            }
                        })
                    }
                }
            });

            _api = new APIGateway.HttpApi(this, "TheStateMachineAPI", new APIGateway.HttpApiProps 
            {
                CreateDefaultStage = true
            });

            _integration = new APIGateway.CfnIntegration(this, "Integration", new APIGateway.CfnIntegrationProps 
            {
                ApiId = _api.HttpApiId,
                IntegrationType = "AWS_PROXY",
                ConnectionType = "INTERNET",
                IntegrationSubtype = "StepFunctions-StartSyncExecution",
                CredentialsArn = _httpApiRole.RoleArn,
                RequestParameters = new Dictionary<string, string>
                {
                    {"Input", "$request.body"}, {"StateMachineArn", _stateMachine.StateMachineArn}
                },
                PayloadFormatVersion = "1.0",
                TimeoutInMillis = 10000
            });

            new APIGateway.CfnRoute(this, "DefaultRoute", new APIGateway.CfnRouteProps
            {
                ApiId = _api.HttpApiId,
                RouteKey = APIGateway.HttpRouteKey.DEFAULT.Key,
                Target = "integrations/"+_integration.Ref
            });

            new Amazon.CDK.CfnOutput(this, "HTTP API Url", new Amazon.CDK.CfnOutputProps
            {
                Value = _api.Url
            });
        }
    }
}
