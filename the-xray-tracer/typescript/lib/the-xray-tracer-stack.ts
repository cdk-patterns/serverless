import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import dynamodb = require('@aws-cdk/aws-dynamodb');

export class TheXrayTracerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //DynamoDB Table
    const table = new dynamodb.Table(this, 'Hits', {
      partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
    });

     // defines an AWS Lambda resource
     const dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'dynamo.handler',
      environment: {
        HITS_TABLE_NAME: table.tableName
      },
      tracing: lambda.Tracing.ACTIVE
    });

     // grant the lambda role read/write permissions to our table
     table.grantReadWriteData(dynamoLambda);

    // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
    new apigw.LambdaRestApi(this, 'X-Ray_Endpoint', {
      handler: dynamoLambda,
      options: {
        deployOptions: {
          loggingLevel: apigw.MethodLoggingLevel.INFO,
          dataTraceEnabled: true,
          metricsEnabled: true,
          tracingEnabled: true
        }
      }
    });
  }
}
