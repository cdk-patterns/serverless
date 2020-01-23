import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import sns = require('@aws-cdk/aws-sns');
import subs = require('@aws-cdk/aws-sns-subscriptions');
import sqs = require('@aws-cdk/aws-sqs');

export class TheScalableWebhookStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

     // defines an AWS Lambda resource
     const sqsPublishLambda = new lambda.Function(this, 'SQSPublishLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas/publish'),  // code loaded from the "lambda" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      environment: {
    }
    });

    // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: sqsPublishLambda
    });
    
    //SNS/SQS
    const queue = new sqs.Queue(this, 'RDSPublishQueue', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    const topic = new sns.Topic(this, 'RDSPublishTopic');

    topic.addSubscription(new subs.SqsSubscription(queue));
  }
}
