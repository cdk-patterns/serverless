import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

export class TheSinglePurposeFunctionStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Lambdas defined individually, each handler is in individual file
     */

    const addLambda = new lambda.Function(this, 'addLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/single-purpose-function'),
      handler: 'add.handler',                
    });

    const subtractLambda = new lambda.Function(this, 'subtractLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/single-purpose-function'),
      handler: 'subtract.handler',                
    });

    const multiplyLambda = new lambda.Function(this, 'multiplyLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/single-purpose-function'),
      handler: 'multiply.handler',                
    });


    /**
     * Routes defined individually on API Gateway
     */
    
    let gateway = new apigw.LambdaRestApi(this, 'SinglePurposeFunctionAPI', {
      handler: addLambda,
      proxy: false
    });

    gateway.root.resourceForPath('add').addMethod('GET', new apigw.LambdaIntegration(addLambda));
    gateway.root.resourceForPath('subtract').addMethod('GET', new apigw.LambdaIntegration(subtractLambda));
    gateway.root.resourceForPath('multiply').addMethod('GET', new apigw.LambdaIntegration(multiplyLambda));
  }
}
