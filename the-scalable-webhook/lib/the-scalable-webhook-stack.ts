import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import sns = require('@aws-cdk/aws-sns');
import subs = require('@aws-cdk/aws-sns-subscriptions');
import sqs = require('@aws-cdk/aws-sqs');
import {DatabaseInstance, DatabaseInstanceEngine, StorageType} from '@aws-cdk/aws-rds';
import {ISecret, Secret} from '@aws-cdk/aws-secretsmanager';
import {InstanceClass, InstanceSize, InstanceType, Peer, SubnetType, Vpc} from "@aws-cdk/aws-ec2";

export class TheScalableWebhookStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Basic VPC Setup (RDS has to be in a VPC)
    /*const vpc = new Vpc(this, 'TheVPC', {
      cidr: "10.0.0.0/16"
    })*/

    /**
     * RDS Database Setup
     * MySQL Database / Auto Generated Password Setup
     */
    /*let secret = new Secret(this, 'secret', {
      description: 'rds password',
      secretName: 'rds-password',
      generateSecretString: {
          excludePunctuation: true,
          excludeCharacters: '/@" '
      }
    })
    
    let mySQLRDSInstance = new DatabaseInstance(this, 'mysql-rds-instance', {
        engine: DatabaseInstanceEngine.MYSQL,
        instanceClass: InstanceType.of(InstanceClass.T2, InstanceSize.SMALL),
        vpc,
        vpcPlacement: {subnetType: SubnetType.PRIVATE},
        storageEncrypted: true,
        multiAz: false,
        autoMinorVersionUpgrade: false,
        allocatedStorage: 25,
        storageType: StorageType.GP2,
        backupRetention: cdk.Duration.days(3),
        deletionProtection: false,
        masterUsername: 'Admin',
        databaseName: 'webhook',
        masterUserPassword: secret.secretValue,
        port: 3306
    });*/

    /**
     * Queue Setup
     * SNS/SQS creation
     */
    const queue = new sqs.Queue(this, 'RDSPublishQueue', {
      visibilityTimeout: cdk.Duration.seconds(300)
    });

    /*const topic = new sns.Topic(this, 'RDSPublishTopic');

    topic.addSubscription(new subs.SqsSubscription(queue));*/

    /**
     * Lambdas
     * Both publisher and subscriber from pattern
     */

    // defines an AWS Lambda resource to publish to our queue
    const sqsPublishLambda = new lambda.Function(this, 'SQSPublishLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas/publish'),  // code loaded from the "lambdas/publish" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      environment: {
        queueURL: queue.queueUrl
      }
    });
    
    queue.grantSendMessages(sqsPublishLambda);

    // defines an AWS Lambda resource to pull from our queue
    const sqsSubscribeLambda = new lambda.Function(this, 'SQSSubscribeLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.asset('lambdas/subscribe'),  // code loaded from the "lambdas/subscribe" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      reservedConcurrentExecutions: 2, // throttle lambda to 2 concurrent invocations
      environment: {
        queueURL: queue.queueUrl
      }
    });

    queue.grantConsumeMessages(sqsSubscribeLambda);

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
