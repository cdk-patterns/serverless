import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import destinations = require('@aws-cdk/aws-lambda-destinations');
import events = require('@aws-cdk/aws-events');
import events_targets = require('@aws-cdk/aws-events-targets');
import apigw = require('@aws-cdk/aws-apigateway');
import sns = require('@aws-cdk/aws-sns');
import sns_sub = require('@aws-cdk/aws-sns-subscriptions');
import iam = require('@aws-cdk/aws-iam');

export class TheDestinedLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Let's create our own Event Bus for this rather than using default
     */
    const bus = new events.EventBus(this, 'DestinedEventBus', {
      eventBusName: 'the-destined-lambda'
    })

    /**
     * Destinations need invoked Asynchronously so let's use SNS
     */
    const topic = new sns.Topic(this, 'theDestinedLambdaTopic',
    {
      displayName: "The Destined Lambda CDK Pattern Topic"
    });

    /**
     * Lambda configured with success and failure destinations
     * 
     * Note the actual lambda has no EventBridge code inside it
     */
    const destinedLambda = new lambda.Function(this, 'destinedLambda', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
      handler: 'destinedLambda.handler',
      retryAttempts: 0,
      onSuccess: new destinations.EventBridgeDestination(bus),
      onFailure: new destinations.EventBridgeDestination(bus)
    });

    topic.addSubscription(new sns_sub.LambdaSubscription(destinedLambda))

    /**
     * This is a lambda that will be called by onSuccess for destinedLambda
     * 
     * It simply prints the event it receives to the cloudwatch logs
     */
    const successLambda = new lambda.Function(this, 'SuccessLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
      handler: 'success.handler',
      timeout: cdk.Duration.seconds(3)
    });

    // Notice how we can still do event filtering based on the json payload returned
    // by the actual lambda
    const successRule = new events.Rule(this, 'successRule', {
      eventBus: bus,
      description: 'all success events are caught here and logged centrally',
      eventPattern:
      {
        "detail": {
          "requestContext": {
            "condition": ["Success"]
          },
          "responsePayload": {
            "source": ["cdkpatterns.the-destined-lambda"],
            "action": ["message"]
          }
        }
      }
    });

    successRule.addTarget(new events_targets.LambdaFunction(successLambda));

    /**
     * This Lambda catches all failed events in our DestinedEventBus
     * It simply prints the event it receives to the cloudwatch logs.
     * 
     * Notice how it includes the message that came into destined lambda to make it fail so you have
     * everything you need to do retries or manually investigate
     */
    const failureLambda = new lambda.Function(this, 'FailureLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns'),
      handler: 'failure.handler',
      timeout: cdk.Duration.seconds(3)
    });

    // Create EventBridge rule to route events
    const failureRule = new events.Rule(this, 'failureRule', {
      eventBus: bus,
      description: 'all failure events are caught here and logged centrally',
      eventPattern:
      {
        "detail": {
          "responsePayload": {
            "errorType": ["Error"]
          }
        }
      }
    });

    failureRule.addTarget(new events_targets.LambdaFunction(failureLambda));

    /**
     * API Gateway Creation
     * 
     * This is a VTL integration to SNS so most of the below is boilerplate
     * 
     * This looks complicated because it transforms the incoming json payload into a query string url
     * this url is used to post the payload to sns without a lambda inbetween 
     */
    let gateway = new apigw.RestApi(this, 'theDestinedLambdaAPI', {
      deployOptions: {
        metricsEnabled: true,
        loggingLevel: apigw.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        stageName: 'prod'
      }
    });

    //Give our gateway permissions to interact with SNS
    let apigwSnsRole = new iam.Role(this, 'ApiGatewaySnsRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com')
    });
    topic.grantPublish(apigwSnsRole);

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

    //Create an endpoint '/SendEvent' which accepts a mode query param on a GET verb
    gateway.root.addResource('SendEvent')
      .addMethod('GET', new apigw.Integration({
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
                              "Message=please $input.params().querystring.get('mode')&"+
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
              'application/json': JSON.stringify({ message: 'Message added to SNS topic'})
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
