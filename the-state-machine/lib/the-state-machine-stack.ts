import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import sfn = require('@aws-cdk/aws-stepfunctions');
import tasks = require('@aws-cdk/aws-stepfunctions-tasks');

export class TheStateMachineStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Step Function definition

    // defines an AWS Lambda resource
    const stateMachineLambda = new lambda.Function(this, 'stateMachineLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas'),  // code loaded from the "lambda" directory
      handler: 'stateMachineLambda.handler'                // file is "lambda", function is "handler"
    });

    const orderPizzaLambda = new lambda.Function(this, 'orderPizzaLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas'),  // code loaded from the "lambda" directory
      handler: 'orderPizza.handler'                // file is "lambda", function is "handler"
    });

    const orderPizza = new sfn.Task(this, 'Order Pizza Job', {
      task: new tasks.InvokeFunction(orderPizzaLambda),
      // Put Lambda's result here in the execution's state object
      resultPath: '$.type',
    });

    const jobFailed = new sfn.Fail(this, 'Sorry, We Dont add Pineapple', {
      cause: 'Failed To Make Pizza',
      error: 'They asked for Pineapple',
    });

    const cookPizza = new sfn.Pass(this, 'Lets make your pizza');

    const definition = sfn.Chain
    .start(orderPizza)
    .next(new sfn.Choice(this, 'With Pineapple?')
        // Look at the "status" field
        .when(sfn.Condition.stringEquals('$.type', 'Pineapple'), jobFailed)
        .otherwise(cookPizza));

    new sfn.StateMachine(this, 'StateMachine', {
      definition,
      timeout: cdk.Duration.minutes(5)
    });

    // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: stateMachineLambda
    });
  }
}