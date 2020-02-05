import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

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

    // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: stateMachineLambda
    });
  }
}
