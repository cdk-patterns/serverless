import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

export class TheFatLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Lambdas defined individually even though code is all in one file
     */

    const addLambda = new lambda.Function(this, 'addLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/fat-lambda'),
      handler: 'fat-lambda.add',                
    });

    const subtractLambda = new lambda.Function(this, 'subtractLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/fat-lambda'),
      handler: 'fat-lambda.subtract',                
    });

    const multiplyLambda = new lambda.Function(this, 'multiplyLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/fat-lambda'),
      handler: 'fat-lambda.multiply',                
    });


    /**
     * Routes defined individually on API Gateway
     */
    
    let gateway = new apigw.LambdaRestApi(this, 'FatLambdaAPI', {
      handler: addLambda,
      proxy: false
    });

    gateway.root.resourceForPath('add').addMethod('GET', new apigw.LambdaIntegration(addLambda));
    gateway.root.resourceForPath('subtract').addMethod('GET', new apigw.LambdaIntegration(subtractLambda));
    gateway.root.resourceForPath('multiply').addMethod('GET', new apigw.LambdaIntegration(multiplyLambda));
  }
}
