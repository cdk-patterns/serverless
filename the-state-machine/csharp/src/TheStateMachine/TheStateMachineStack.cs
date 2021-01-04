using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using SQS = Amazon.CDK.AWS.SQS;
using APIGateway = Amazon.CDK.AWS.APIGateway;
using StepFunction = Amazon.CDK.AWS.StepFunctions;
using StepFuncionTasks = Amazon.CDK.AWS.StepFunctions.Tasks;
using System.Collections.Generic;

namespace TheStateMachine
{
    public class TheStateMachineStack : Stack
    {

        readonly private Lambda.Function _pineppaleCheckHandler;
        readonly private Lambda.Function _stateMachineHandler;
        readonly private StepFuncionTasks.LambdaInvoke _orderPizzaTask;
        readonly private StepFunction.Fail _jobFailed;
        readonly private StepFunction.Pass _cookPizza;
        readonly private StepFunction.Chain _chainDefinition;
        readonly private StepFunction.StateMachine _stateMachine;
        readonly private SQS.Queue _deadeLetterQueue;

        internal TheStateMachineStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {

            // Step Function Starts Here

            // The first thing we need to do is see if they are asking for pineapple on a pizza
            _pineppaleCheckHandler = new Lambda.Function(this, "pineappleCheckLambdaHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Code = Lambda.Code.FromAsset("lambda_fns"),
                Handler = "orderPizza.handler"
            });

            /*
             * Step functions are built up of steps, we need to define our first step
             * This step was refactored due to Deprecated function
             */
            _orderPizzaTask = new StepFuncionTasks.LambdaInvoke(this, "Order Pizza Job", new StepFuncionTasks.LambdaInvokeProps
            {
                LambdaFunction = _pineppaleCheckHandler,
                InputPath = "$.flavour",
                ResultPath = "$.pineappleAnalysis",
                PayloadResponseOnly = true
            });

            // Pizza Order failure step defined
            _jobFailed = new StepFunction.Fail(this, "Sorry, We Dont add Pineapple", new StepFunction.FailProps
            {
                Cause = "Failed To Make Pizza",
                Error = "They asked for Pineapple"
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
                Timeout = Duration.Minutes(5)
            });

            /**
             * Dead Letter Queue Setup
             * SQS creation
             * https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
             */
            _deadeLetterQueue = new SQS.Queue(this, "stateMachineLambdaDLQ", new SQS.QueueProps
            {
                VisibilityTimeout = Duration.Seconds(300)
            });

            // defines an AWS Lambda resource to connect to our API Gateway
            _stateMachineHandler = new Lambda.Function(this, "stateMachineLambdaHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X,
                Code = Lambda.Code.FromAsset("lambda_fns"),
                Handler = "stateMachineLambda.handler",
                DeadLetterQueue = _deadeLetterQueue,
                Environment = new Dictionary<string, string>
                {
                    { "statemachine_arn", _stateMachine.StateMachineArn }
                }
            });

            // Grants to state machine execution
            _stateMachine.GrantStartExecution(_stateMachineHandler);

            /*
             * Simple API Gateway proxy integration
             */
            // defines an API Gateway REST API resource backed by our "sqs_publish_lambda" function.
            new APIGateway.LambdaRestApi(this, "Endpoint", new APIGateway.LambdaRestApiProps
            {
                Handler = _stateMachineHandler
            });
        }
    }
}
