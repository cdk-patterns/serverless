import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda-nodejs');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigatewayv2');
const path = require('path');

export class TheLambdaCircuitBreakerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //DynamoDB Table To Hold Circuitbreaker State
    const table = new dynamodb.Table(this, 'CircuitBreakerTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });

    // Create a Lambda Function with unreliable code
    const unreliableLambda = new lambda.NodejsFunction(this, 'UnreliableLambdaHandler', {
      entry: path.join(__dirname, '../lambda-fns/unreliable.ts'),
      handler: 'handler',
      environment: {
        CIRCUITBREAKER_TABLE: table.tableName
      }
    });

    // grant the lambda role read/write permissions to our table
    table.grantReadWriteData(unreliableLambda);

    // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
    let api = new apigw.HttpApi(this, 'CircuitBreakerGateway', {
      defaultIntegration: new apigw.LambdaProxyIntegration({
        handler: unreliableLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
