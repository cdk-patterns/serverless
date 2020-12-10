import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import integrations = require('@aws-cdk/aws-apigatewayv2-integrations');
const { execSync } = require('child_process');

export class TheLambdaCircuitBreakerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //DynamoDB Table To Hold Circuitbreaker State
    const table = new dynamodb.Table(this, 'CircuitBreakerTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    
    // Install Dependencies and Compile Lambda Function
    execSync('cd lambda-fns && npm i && npm run build');

    // Create a Lambda Function with unreliable code
    const unreliableLambda = new lambda.Function(this, 'UnreliableLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
      handler: 'unreliable.handler', 
      environment: {
        CIRCUITBREAKER_TABLE: table.tableName
      }
    });

    // grant the lambda role read/write permissions to our table
    table.grantReadWriteData(unreliableLambda);

    // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
    let api = new apigw.HttpApi(this, 'CircuitBreakerGateway', {
      defaultIntegration: new integrations.LambdaProxyIntegration({
        handler: unreliableLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
