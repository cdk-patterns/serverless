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
      deployOptions: {
        metricsEnabled: true,
        loggingLevel: apigw.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        stageName: 'prod'
      }
    });

    let apigwDynamoRole = new iam.Role(this, 'DefaultLambdaHanderRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com')
    });

    table.grantReadWriteData(apigwDynamoRole);
    
    const responseModel = gateway.addModel('ResponseModel', {
      contentType: 'application/json',
      modelName: 'ResponseModel',
      schema: { 'schema': apigw.JsonSchemaVersion.DRAFT4, 'title': 'pollResponse', 'type': apigw.JsonSchemaType.OBJECT, 'properties': { 'message': { 'type': apigw.JsonSchemaType.STRING } } }
    });

    gateway.root.addResource('InsertItem')
      .addMethod('POST', new apigw.Integration({
        type: apigw.IntegrationType.AWS,
        integrationHttpMethod: "POST",
        uri: 'arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
        options: {
          credentialsRole: apigwDynamoRole,
          requestTemplates: {
          // You can define a mapping that will build a payload for your integration, based
          //  on the integration parameters that you have specified
          // Check: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
          'application/json': JSON.stringify({"TableName": table.tableName, "Item": {"message": { "S": "$input.path('$.message')"}}})
        },
        integrationResponses: [
          {
            // Successful response from the Lambda function, no filter defined
            //  - the selectionPattern filter only tests the error message
            // We will set the response status code to 200
            statusCode: "200",
            responseTemplates: {
              // This template takes the "message" result from the Lambda function, adn embeds it in a JSON response
              // Check https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
              'application/json': JSON.stringify({ message: 'item added to db'})
            }
          }
        ]
        }
      }),
      {
        methodResponses: [
          {
            // Successful response from the integration
            statusCode: '200',
            // Define what parameters are allowed or not
            responseParameters: {
              'method.response.header.Content-Type': true,
              'method.response.header.Access-Control-Allow-Origin': true,
              'method.response.header.Access-Control-Allow-Credentials': true
            },
            // Validate the schema on the response
            responseModels: {
              'application/json': responseModel
            }
          }
        ]
      })
  }
}
