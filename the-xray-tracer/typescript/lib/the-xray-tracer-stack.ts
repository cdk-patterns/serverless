import * as cdk from '@aws-cdk/core';
import apigw = require('@aws-cdk/aws-apigateway');
import sns = require('@aws-cdk/aws-sns');
import iam = require('@aws-cdk/aws-iam');

export class TheXrayTracerStack extends cdk.Stack {
  public snsTopicARN: string;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const topic = new sns.Topic(this, 'TheXRayTracerSnsFanOutTopic', {
      displayName: "The XRay Tracer Fan Out Topic",
    });
    this.snsTopicARN = topic.topicArn;

    /**
     * API Gateway Creation
     * This is complicated because it is a direct SNS integration through VTL not a proxy integration
     * Tracing is enabled for X-Ray
     */

    let gateway = new apigw.RestApi(this, 'xrayTracerAPI', {
      deployOptions: {
        metricsEnabled: true,
        loggingLevel: apigw.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        tracingEnabled: true,
        stageName: 'prod'
      }
    });

    // We need a role to let our gateway publish to SNS
    let apigwSnsRole = new iam.Role(this, 'ApiGatewaySNSRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com')
    });
    topic.grantPublish(apigwSnsRole);

    // This is our direct VTL integration with SNS
    let snsIntegration = new apigw.Integration({
      type: apigw.IntegrationType.AWS, //native aws integration
      integrationHttpMethod: "POST",
      uri: 'arn:aws:apigateway:us-east-1:sns:path//', // This is how we setup an SNS Topic publish operation.
      options: {
        credentialsRole: apigwSnsRole,
        requestParameters: {
          'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'" // Tell api gw to send our payload as query params
        },
        requestTemplates: {
        // This is the VTL to transform our incoming request to post to our SNS topic
        // Check: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        'application/json': "Action=Publish&"+
                            "TargetArn=$util.urlEncode('"+topic.topicArn+"')&"+
                            "Message=$util.urlEncode($context.path)&"+
                            "Version=2010-03-31"
      },
      passthroughBehavior: apigw.PassthroughBehavior.NEVER,
      integrationResponses: [
        {
          // Tells APIGW which response to use based on the returned code from the service
          statusCode: "200",
          responseTemplates: {
            // Just respond with a generic message
            // Check https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
            'application/json': JSON.stringify({ message: 'message added to SNS topic'})
          }
        },
        {
          // For errors, we check if the response contains the words BadRequest
          selectionPattern: '^\[Error\].*',
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
    });

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

    let methodOptions: apigw.MethodOptions = {
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
    }

    // Integration for users hitting / endpoint
    gateway.root
      .addMethod('GET', snsIntegration, methodOptions);

    //Create a /{proxy+} endpoint where the URL is used as the payload for all processes
    gateway.root.addResource('{proxy+}')
      .addMethod('GET', snsIntegration, methodOptions);
  }
}
