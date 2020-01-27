import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import iam = require('@aws-cdk/aws-iam');

export class TheDynamoStreamerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //DynamoDB Table
    const table = new dynamodb.Table(this, 'Hits', {
      partitionKey: { name: 'message', type: dynamodb.AttributeType.STRING }
    });

     // defines an AWS Lambda resource
     /*const dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambda'),  // code loaded from the "lambda" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      environment: {
        HITS_TABLE_NAME: table.tableName
    }
    });*/

    // grant the lambda role read/write permissions to our table
    //table.grantReadWriteData(dynamoLambda);

    let gateway = new apigw.RestApi(this, 'DynamoStreamerAPI', {

    });

    let apigwDynamoRole = new iam.Role(this, 'DefaultLambdaHanderRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com')
    });

    table.grantReadWriteData(apigwDynamoRole);

    gateway.root.addProxy({
       defaultIntegration: new apigw.Integration({
         type: apigw.IntegrationType.AWS,
         uri: 'arn:aws:apigateway:us-east-1:DynamoDB:action/PutItem',
         options: {
           credentialsRole: apigwDynamoRole
         }
       })
     })
  }
}
