import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import iam = require('@aws-cdk/aws-iam');
import { DynamoEventSource } from '@aws-cdk/aws-lambda-event-sources';

export class TheDynamoStreamerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * DynamoDB Creation
     * Streaming is enabled to send the whole new object down the pipe
     */
    const table = new dynamodb.Table(this, 'TheDynamoStreamer', {
      partitionKey: { name: 'message', type: dynamodb.AttributeType.STRING },
      stream: dynamodb.StreamViewType.NEW_IMAGE
    });
    
    /**
     * Lambda Dynamo Stream Subscriber Creation
     */
    const dynamoStreamSubscriberLambda = new lambda.Function(this, 'dynamoStreamSubscriberLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.fromAsset('lambda-fns/subscribe'),  // code loaded from the "lambdas/subscribe" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      environment: {
      },
    });
    // subscribe our lambda to the stream
    dynamoStreamSubscriberLambda.addEventSource(new DynamoEventSource(table, {startingPosition: lambda.StartingPosition.LATEST}));

    /**
     * API Gateway Creation
     */
    let gateway = new apigw.RestApi(this, 'DynamoStreamerAPI', {
      deployOptions: {
        metricsEnabled: true,
        loggingLevel: apigw.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        stageName: 'prod'
      }
    });

    //Give our gateway permissions to interact with dynamodb
    let apigwDynamoRole = new iam.Role(this, 'DefaultLambdaHanderRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com')
    });
    table.grantReadWriteData(apigwDynamoRole);
    
    //Because this isn't a proxy integration, we need to define our response model
    const responseModel = gateway.addModel('ResponseModel', {
      contentType: 'application/json',
      modelName: 'ResponseModel',
      schema: { 'schema': apigw.JsonSchemaVersion.DRAFT4, 'title': 'pollResponse', 'type': apigw.JsonSchemaType.OBJECT, 'properties': { 'message': { 'type': apigw.JsonSchemaType.STRING } } }
    });
    
    // We define the JSON Schema for the transformed error response
    const errorResponseModel = gateway.addModel('ErrorResponseModel', {
      contentType: 'application/json',
      modelName: 'ErrorResponseModel',
      schema: { 'schema': apigw.JsonSchemaVersion.DRAFT4, 'title': 'errorResponse', 'type': apigw.JsonSchemaType.OBJECT, 'properties': { 'state': { 'type': apigw.JsonSchemaType.STRING }, 'message': { 'type': apigw.JsonSchemaType.STRING } } }
    });

    //Create an endpoint '/InsertItem' which accepts a JSON payload on a POST verb
    gateway.root.addResource('InsertItem')
      .addMethod('POST', new apigw.Integration({
        type: apigw.IntegrationType.AWS, //native aws integration
        integrationHttpMethod: "POST",
        uri: 'arn:aws:apigateway:us-east-1:dynamodb:action/PutItem', // This is how we setup a dynamo insert operation.
        options: {
          credentialsRole: apigwDynamoRole,
          requestTemplates: {
          // This is the VTL to transform our incoming JSON to a Dynamo Insert query
          // Check: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
          'application/json': JSON.stringify({"TableName": table.tableName, "Item": {"message": { "S": "$input.path('$.message')"}}})
        },
        passthroughBehavior: apigw.PassthroughBehavior.NEVER,
        integrationResponses: [
          {
            // Tells APIGW which response to use based on the returned code from the service
            statusCode: "200",
            responseTemplates: {
              // Just respond with a generic message
              // Check https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
              'application/json': JSON.stringify({ message: 'item added to db'})
            }
          },
          {
            // For errors, we check if the response contains the words BadRequest
            selectionPattern: '^\[BadRequest\].*',
            statusCode: "400",
            responseTemplates: {
                'application/json': JSON.stringify({ state: 'error', message: "$util.escapeJavaScript($input.path('$.errorMessage'))" })
            },
            responseParameters: {
                'method.response.header.Content-Type': "'application/json'",
                'method.response.header.Access-Control-Allow-Origin': "'*'",
                'method.response.header.Access-Control-Allow-Credentials': "'true'"
            }
          }
        ]
        }
      }),
      {
        methodResponses: [ //We need to define what models are allowed on our method response
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
          },
          {
            // Same thing for the error responses
            statusCode: '400',
            responseParameters: {
              'method.response.header.Content-Type': true,
              'method.response.header.Access-Control-Allow-Origin': true,
              'method.response.header.Access-Control-Allow-Credentials': true
            },
            responseModels: {
              'application/json': errorResponseModel
            }
          }
        ]
      })
  }
}
