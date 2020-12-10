import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

export class ApigatewayStack extends cdk.Stack {
  apiGatewayARN:string;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Lambda Function Creation
     * returns "Hello World!" when called
     */
    const helloWorldLambda = new lambda.Function(this, 'HelloWorldHandler', {
        runtime: lambda.Runtime.NODEJS_12_X,
        code: lambda.Code.fromAsset('lambda-fns'),
        handler: 'helloworld.handler'
    });

    /**
     * API Gateway Creation
     * sets up a /prod/helloworld endpoint
     */
    let gateway = new apigw.RestApi(this, 'WafGatewayAPI', {
        endpointTypes: [apigw.EndpointType.REGIONAL],
        deployOptions: {
          metricsEnabled: true,
          loggingLevel: apigw.MethodLoggingLevel.INFO,
          dataTraceEnabled: true,
          stageName: 'prod',
          methodOptions: {
              "/*/*": {
                throttlingRateLimit: 100,
                throttlingBurstLimit: 200
              }
          }
        }
    });

    const basePath = gateway.root.addResource('helloworld');

    let lambdaIntegration = new apigw.LambdaIntegration(helloWorldLambda, {
        proxy: false,
        integrationResponses: [
            {
                statusCode: '200',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            }
        ]
    });

    basePath.addMethod('GET', lambdaIntegration, {
        methodResponses: [
            {
                statusCode: '200',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Origin': true
                }
            }
        ]
    });

    //store the gateway ARN for use with our WAF stack
    this.apiGatewayARN = `arn:aws:apigateway:${cdk.Stack.of(this).region}::/restapis/${gateway.restApiId}/stages/${gateway.deploymentStage.stageName}`
  }
}
