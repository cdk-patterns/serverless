import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import iam = require('@aws-cdk/aws-iam');

export class PollyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda Function that takes in text and returns a polly voice synthesis
    const pollyLambda = new lambda.Function(this, 'PollyHandler', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.asset('lambdas'), 
      handler: 'polly.handler'
    });
    
    // https://docs.aws.amazon.com/polly/latest/dg/api-permissions-reference.html
    const pollyStatement = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: [
        'polly:SynthesizeSpeech'
      ]
    });
    pollyLambda.addToRolePolicy(pollyStatement);

    // defines an API Gateway Http API resource backed by our "pollyLambda" function.
    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new apigw.LambdaProxyIntegration({
        handler: pollyLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
