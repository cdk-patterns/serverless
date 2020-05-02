import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import sns = require('@aws-cdk/aws-sns');
import sns_sub = require('@aws-cdk/aws-sns-subscriptions');
import iam = require('@aws-cdk/aws-iam');

export interface XrayTraceStackProps extends cdk.StackProps{
  readonly lambdasToInvoke: lambda.Function[];
}

export class TheXrayTracerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: XrayTraceStackProps) {
    super(scope, id, props);

    const topic = new sns.Topic(this, 'TheXRayTracerSnsTopic', {
      displayName: "The XRay Tracer CDK Pattern Topic",
    });

    for(let lambda of props.lambdasToInvoke) {
      topic.addSubscription(new sns_sub.LambdaSubscription(lambda));
    }

    /**
     * API Gateway Creation
     * This is complicated because it transforms the incoming json payload into a query string url
     * this url is used to post the payload to sns without a lambda inbetween 
     */
    let gateway = new apigw.RestApi(this, 'theBigFanAPI', {
      deployOptions: {
        metricsEnabled: true,
        loggingLevel: apigw.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        tracingEnabled: true,
        stageName: 'prod'
      }
    });

    //Give our gateway permissions to interact with SNS
    let apigwSnsRole = new iam.Role(this, 'DefaultLambdaHanderRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com')
    });
    topic.grantPublish(apigwSnsRole);

    gateway.root.addProxy({
      defaultIntegration: new apigw.Integration({
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
                              "Version=2010-03-31&"+
                              "MessageAttributes.entry.1.Name=status&"+
                              "MessageAttributes.entry.1.Value.DataType=String&"+
                              "MessageAttributes.entry.1.Value.StringValue=$util.urlEncode($input.path('$.status'))"
        },
        passthroughBehavior: apigw.PassthroughBehavior.NEVER,
        integrationResponses: [
          {
            // Tells APIGW which response to use based on the returned code from the service
            statusCode: "200",
            responseTemplates: {
              // Just respond with a generic message
              // Check https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
              'application/json': JSON.stringify({ message: 'message added to topic'})
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
      })
    });
  }
}
