import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import sfn = require('@aws-cdk/aws-stepfunctions');
import tasks = require('@aws-cdk/aws-stepfunctions-tasks');
import sqs = require('@aws-cdk/aws-sqs');

export class TheStateMachineStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Step Function Starts Here
     */
     
    //The first thing we need to do is see if they are asking for pineapple on a pizza
    let pineappleCheckLambda = new lambda.Function(this, 'pineappleCheckLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
      handler: 'orderPizza.handler'
    });

    // Step functions are built up of steps, we need to define our first step
    const orderPizza = new tasks.LambdaInvoke(this, "Order Pizza Job", {
      lambdaFunction: pineappleCheckLambda,
      inputPath: '$.flavour',
      resultPath: '$.pineappleAnalysis',
      payloadResponseOnly: true
    })

    // Pizza Order failure step defined
    const jobFailed = new sfn.Fail(this, 'Sorry, We Dont add Pineapple', {
      cause: 'Failed To Make Pizza',
      error: 'They asked for Pineapple',
    });

    // If they didnt ask for pineapple let's cook the pizza
    const cookPizza = new sfn.Pass(this, 'Lets make your pizza');

    //Step function definition
    const definition = sfn.Chain
    .start(orderPizza)
    .next(new sfn.Choice(this, 'With Pineapple?') // Logical choice added to flow
        // Look at the "status" field
        .when(sfn.Condition.booleanEquals('$.pineappleAnalysis.containsPineapple', true), jobFailed) // Fail for pineapple
        .otherwise(cookPizza));

    let stateMachine = new sfn.StateMachine(this, 'StateMachine', {
      definition,
      timeout: cdk.Duration.minutes(5)
    });

    /**
     * Dead Letter Queue Setup
     * SQS creation
     * https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
     */
    const dlq = new sqs.Queue(this, 'stateMachineLambdaDLQ', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    // defines an AWS Lambda resource to connect to our API Gateway
    const stateMachineLambda = new lambda.Function(this, 'stateMachineLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
      handler: 'stateMachineLambda.handler',
      deadLetterQueue:dlq,
      environment: {
        statemachine_arn: stateMachine.stateMachineArn
      }
    });

    stateMachine.grantStartExecution(stateMachineLambda);

    /**
     * Simple API Gateway proxy integration
     */
    // defines an API Gateway REST API resource backed by our "stateMachineLambda" function.
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: stateMachineLambda
    });
  }
}
