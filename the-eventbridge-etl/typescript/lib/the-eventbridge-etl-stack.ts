import * as cdk from '@aws-cdk/core';
import s3 = require('@aws-cdk/aws-s3');
import s3n = require("@aws-cdk/aws-s3-notifications");
import sqs = require('@aws-cdk/aws-sqs');
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';
import lambda = require('@aws-cdk/aws-lambda');

export class TheEventbridgeEtlStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Queue that listens for S3 Bucket events
     */
    const queue = new sqs.Queue(this, 'newObjectInLandingBucketEventQueue', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    /**
     * S3 Landing Bucket
     */
    let bucket = new s3.Bucket(this, 'LandingBucket', {
    });

    bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.SqsDestination(queue));

    /**
     * Lambda that subscribes to newObjectInLandingBucketEventQueue
     */

    // defines an AWS Lambda resource to pull from our queue
    const sqsSubscribeLambda = new lambda.Function(this, 'SQSSubscribeLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas/subscribe'),  // code loaded from the "lambdas/subscribe" directory
      handler: 'newObjectInLandingBucketEventQueue.handler',                // file is "lambda", function is "handler"
      reservedConcurrentExecutions: 2 // throttle lambda to 2 concurrent invocations
    });
    queue.grantConsumeMessages(sqsSubscribeLambda);
    sqsSubscribeLambda.addEventSource(new SqsEventSource(queue, {}));
  }
}
