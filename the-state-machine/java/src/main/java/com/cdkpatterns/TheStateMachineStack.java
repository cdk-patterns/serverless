package com.cdkpatterns;

import java.util.Map;

import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Duration;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.stepfunctions.tasks.LambdaInvoke;
import software.amazon.awscdk.services.stepfunctions.Fail;
import software.amazon.awscdk.services.stepfunctions.Pass;
import software.amazon.awscdk.services.stepfunctions.Chain;
import software.amazon.awscdk.services.stepfunctions.Choice;
import software.amazon.awscdk.services.stepfunctions.Condition;
import software.amazon.awscdk.services.stepfunctions.StateMachine;
import software.amazon.awscdk.services.sqs.Queue;
import software.amazon.awscdk.services.apigateway.LambdaRestApi;

public class TheStateMachineStack extends Stack {
    public TheStateMachineStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheStateMachineStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        // Step Function Starts Here

        // The first thing we need to do is see if they are asking for pineapple on a pizza
        Function pineappleCheckHandler = Function.Builder.create(this, "pineappleCheckLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.code(Code.fromAsset("lambda_fns")) // code loaded from the "lambda_fns" directory
        		.handler("orderPizza.handler") // file is "orderPizza", function is "handler"
        		.build();
        
        /*
         * Step functions are built up of steps, we need to define our first step
         * This step was refactored due to Deprecated function
         */
        LambdaInvoke orderPizzaTask = LambdaInvoke.Builder.create(this, "Order Pizza Job")
        		.lambdaFunction(pineappleCheckHandler)
        		.inputPath("$.flavour")
        		.resultPath("$.pineappleAnalysis")
        		.payloadResponseOnly(true)
        		.build();
        
        // Pizza Order failure step defined
        Fail jobFailed = Fail.Builder.create(this, "Sorry, We Dont add Pineapple")
        		.cause("Failed To Make Pizza")
        		.error("They asked for Pineapple")
        		.build();
        
        // If they didn't ask for pineapple let's cook the pizza
        Pass cookPizza = Pass.Builder.create(this, "Lets make your pizza")
        		.build();
        
        
        // If they ask for a pizza with pineapple, fail. Otherwise cook the pizza
        Chain chainDefinition = Chain
        		.start(orderPizzaTask)
        		.next(Choice.Builder.create(this, "With Pineapple?") // Logical choice added to flow
        				.build()
        				// Look at the "status" field
        				.when(Condition.booleanEquals("$.pineappleAnalysis.containsPineapple", true), jobFailed) // Fail for pineapple
        				.otherwise(cookPizza));
        
        // Building the state machine
        StateMachine stateMachine = StateMachine.Builder.create(this, "StateMachine")
        		.definition(chainDefinition)
        		.timeout(Duration.minutes(5))
        		.build();
        
        /*
         * Dead Letter Queue Setup
         * SQS creation
         * https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
         */
        Queue deadLetterQueue = Queue.Builder.create(this, "stateMachineLambdaDLQ")
        		.visibilityTimeout(Duration.seconds(300))
        		.build();
        
        // defines an AWS Lambda resource to connect to our API Gateway
        Function stateMachineHandler = Function.Builder.create(this, "stateMachineLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.code(Code.fromAsset("lambda_fns")) // code loaded from the "lambda_fns" directory
        		.handler("stateMachineLambda.handler") // file is "stateMachineLambda", function is "handler
        		.deadLetterQueue(deadLetterQueue)
        		.environment(Map.of(
        				"statemachine_arn", stateMachine.getStateMachineArn()
        				))
        		.build();
        
        
        // Grants to state machine execution
        stateMachine.grantStartExecution(stateMachineHandler);

        /*
         * Simple API Gateway proxy integration
         */
        // defines an API Gateway REST API resource backed by our "sqs_publish_lambda" function.
        LambdaRestApi.Builder.create(this, "Endpoint")
	        .handler(stateMachineHandler)
	        .build();
    }
}
