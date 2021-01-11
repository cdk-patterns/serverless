import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import sqs = require('@aws-cdk/aws-sqs');
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';
import dynamodb = require('@aws-cdk/aws-dynamodb');

export class TheScalableWebhookStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Dynamo Setup
     * This is standing in for what is RDS on the diagram due to simpler/cheaper setup
     */
    const table = new dynamodb.Table(this, 'Messages', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING } //the key being id means we squash duplicate sqs messages
    });

    /**
     * Queue Setup
     * SQS creation
     */
    const queue = new sqs.Queue(this, 'RDSPublishQueue', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    /**
     * Lambdas
     * Both publisher and subscriber from pattern
     */

    // defines an AWS Lambda resource to publish to our queue
    const sqsPublishLambda = new lambda.Function(this, 'SQSPublishLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.fromAsset('lambda-fns/publish'),  // code loaded from the "lambda-fns/publish" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      environment: {
        queueURL: queue.queueUrl
      }
    });
    
    queue.grantSendMessages(sqsPublishLambda);

    // defines an AWS Lambda resource to pull from our queue
    const sqsSubscribeLambda = new lambda.Function(this, 'SQSSubscribeLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.fromAsset('lambda-fns/subscribe'),  // code loaded from the "lambda-fns/subscribe" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      reservedConcurrentExecutions: 2, // throttle lambda to 2 concurrent invocations
      environment: {
        queueURL: queue.queueUrl,
        tableName: table.tableName
      },
    });
    queue.grantConsumeMessages(sqsSubscribeLambda);
    sqsSubscribeLambda.addEventSource(new SqsEventSource(queue, {}));
    table.grantReadWriteData(sqsSubscribeLambda);

  
    /**
     * API Gateway Proxy
     * Used to expose the webhook through a URL
     */

    // defines an API Gateway REST API resource backed by our "sqsPublishLambda" function.
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: sqsPublishLambda
    });
    
  }
}
