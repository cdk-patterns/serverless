import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import sqs = require('@aws-cdk/aws-sqs');
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';

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

     // defines an AWS Lambda resource
     const httpLambda = new lambda.Function(this, 'httpLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'http.handler',
      tracing: lambda.Tracing.ACTIVE
    });

    /**
     * Queue Setup
     * SQS creation
     */
    const queue = new sqs.Queue(this, 'RDSPublishQueue', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    // defines an AWS Lambda resource
    const sqslambda = new lambda.Function(this, 'sqsLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'sqs.handler',
      environment: {
        SQS_URL: queue.queueUrl
      },
      tracing: lambda.Tracing.ACTIVE
    });
    queue.grantSendMessages(sqslambda);

    // defines an AWS Lambda resource to pull from our queue
    const sqsSubscribeLambda = new lambda.Function(this, 'SQSSubscribeLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas'),  // code loaded from the "lambdas/subscribe" directory
      handler: 'sqs_subscribe.handler',                // file is "lambda", function is "handler"
      reservedConcurrentExecutions: 2, // throttle lambda to 2 concurrent invocations
      environment: {
        queueURL: queue.queueUrl
      },
    });
    queue.grantConsumeMessages(sqsSubscribeLambda);
    sqsSubscribeLambda.addEventSource(new SqsEventSource(queue, {}));

     // defines an AWS Lambda resource
     const orchLambda = new lambda.Function(this, 'OrchLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'orchestrator.handler',
      timeout: cdk.Duration.seconds(30),
      environment: {
        DYNAMO_FN_ARN: dynamoLambda.functionArn,
        HTTP_FN_ARN: httpLambda.functionArn,
        SQS_FN_ARN: sqslambda.functionArn
      },
      tracing: lambda.Tracing.ACTIVE
    });
    dynamoLambda.grantInvoke(orchLambda);
    httpLambda.grantInvoke(orchLambda);
    sqslambda.grantInvoke(orchLambda)

    // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
    new apigw.LambdaRestApi(this, 'X-Ray_Endpoint', {
      handler: orchLambda,
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
