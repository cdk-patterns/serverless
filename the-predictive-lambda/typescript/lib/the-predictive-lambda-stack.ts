import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import integrations = require('@aws-cdk/aws-apigatewayv2-integrations');
import * as path from 'path';

export class ThePredictiveLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // defines an AWS Lambda resource
    const predictiveLambda = new lambda.DockerImageFunction(this, 'PredictiveLambda', {
      code: lambda.DockerImageCode.fromImageAsset(path.join(__dirname, '../model')),
      memorySize:4096,
      timeout: cdk.Duration.seconds(15)
    })

   // defines an API Gateway Http API resource backed by our "PredictiveLambda" function.
   const api = new apigw.HttpApi(this, 'Predictive Endpoint', {
     defaultIntegration: new integrations.LambdaProxyIntegration({
       handler: predictiveLambda
     })
   });

   new cdk.CfnOutput(this, 'HTTP API Url', {
    value: api.url ?? 'Something went wrong with the deploy'
  });
  }
}
