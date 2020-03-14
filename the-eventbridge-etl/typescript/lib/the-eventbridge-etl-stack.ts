import * as cdk from '@aws-cdk/core';
import s3 = require('@aws-cdk/aws-s3');
import s3n = require("@aws-cdk/aws-s3-notifications");
import sqs = require('@aws-cdk/aws-sqs');

export class TheEventbridgeEtlStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const queue = new sqs.Queue(this, 'newObjectInLandingBucketEventQueue', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    let bucket = new s3.Bucket(this, 'LandingBucket', {
    });

    bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.SqsDestination(queue))
  }
}
