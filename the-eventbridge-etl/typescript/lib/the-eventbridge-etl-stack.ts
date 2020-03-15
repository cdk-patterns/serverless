import * as cdk from '@aws-cdk/core';
import s3 = require('@aws-cdk/aws-s3');
import s3n = require("@aws-cdk/aws-s3-notifications");
import sqs = require('@aws-cdk/aws-sqs');
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';
import lambda = require('@aws-cdk/aws-lambda');
import ec2 = require('@aws-cdk/aws-ec2');
import ecs = require('@aws-cdk/aws-ecs');
import logs = require('@aws-cdk/aws-logs');
import iam = require('@aws-cdk/aws-iam');

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
     * Fargate ECS Task Creation to pull data from S3
     */
    // Producer definition, launch is done through a lambda function
    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2, // Default is all AZs in the region
    });

    const logging = new ecs.AwsLogDriver({
      streamPrefix: 'TheEventBridgeETL',
      logRetention: logs.RetentionDays.ONE_WEEK,
    });

    const cluster = new ecs.Cluster(this, 'Ec2Cluster', {
      vpc: vpc
    });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'ProducerTaskDefinition', {
      memoryLimitMiB: 512,
      cpu: 256
    });

    let container = taskDefinition.addContainer('AppContainer', {
      image: ecs.ContainerImage.fromAsset('container/s3DataExtractionTask'),
      logging,
      environment: { // clear text, not for sensitive data
        'S3_BUCKET_NAME': bucket.bucketName,
        'S3_OBJECT_KEY': '',
        'STREAM_NAME': '',
      },
    });

    // Grant task access to new uploaded assets
    bucket.grantRead(taskDefinition.taskRole);

    const runTaskPolicyStatement = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'ecs:RunTask'
      ],
      resources: [
        taskDefinition.taskDefinitionArn,
      ]
    });

    const taskExecutionRolePolicyStatement = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'iam:PassRole',
      ],
      resources: [
        taskDefinition.obtainExecutionRole().roleArn,
        taskDefinition.taskRole.roleArn,
      ]
    });

    /**
     * Lambda that subscribes to newObjectInLandingBucketEventQueue
     */

    // Create a command line launcher for the fargate task. It is based on lambda.
    const lambdaEnv = {
      CLUSTER_NAME: cluster.clusterName,
      TASK_DEFINITION: taskDefinition.taskDefinitionArn,
      SUBNETS: JSON.stringify(Array.from(vpc.privateSubnets, x => x.subnetId)),
      CONTAINER_NAME: container.containerName
    };

    // defines an AWS Lambda resource to pull from our queue
    const sqsSubscribeLambda = new lambda.Function(this, 'SQSSubscribeLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas/subscribe'),  // code loaded from the "lambdas/subscribe" directory
      handler: 'newObjectInLandingBucketEventQueue.handler',                // file is "lambda", function is "handler"
      reservedConcurrentExecutions: 2, // throttle lambda to 2 concurrent invocations
      environment: lambdaEnv
    });
    queue.grantConsumeMessages(sqsSubscribeLambda);
    sqsSubscribeLambda.addEventSource(new SqsEventSource(queue, {}));
    sqsSubscribeLambda.addToRolePolicy(runTaskPolicyStatement);
    sqsSubscribeLambda.addToRolePolicy(taskExecutionRolePolicyStatement);
  }
}
