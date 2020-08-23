import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import sqs = require('@aws-cdk/aws-sqs');
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';
import sns_sub = require('@aws-cdk/aws-sns-subscriptions');
import sns = require('@aws-cdk/aws-sns');

export interface SQSFlowStackProps extends cdk.StackProps{
    readonly snsTopicARN: string;
}

export class TheSqsFlowStack extends cdk.Stack {
    sqslambda: lambda.Function;
    constructor(scope: cdk.Construct, id: string, props: SQSFlowStackProps) {
        super(scope, id, props);

        /**
         * SQS Flow
         * SQS creation
         */
        const queue = new sqs.Queue(this, 'Queue', {
            visibilityTimeout: cdk.Duration.seconds(300)
        });

        // defines an AWS Lambda resource
        this.sqslambda = new lambda.Function(this, 'sqsLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'sqs.handler',
            environment: {
                SQS_URL: queue.queueUrl
            },
            tracing: lambda.Tracing.ACTIVE
        });
        queue.grantSendMessages(this.sqslambda);

        let topic = sns.Topic.fromTopicArn(this, 'SNSTopic', props.snsTopicARN);
        topic.addSubscription(new sns_sub.LambdaSubscription(this.sqslambda));

        // defines an AWS Lambda resource to pull from our queue
        const sqsSubscribeLambda = new lambda.Function(this, 'sqsSubscribeLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'sqs_subscribe.handler', 
            tracing: lambda.Tracing.ACTIVE
        });
        queue.grantConsumeMessages(sqsSubscribeLambda);
        sqsSubscribeLambda.addEventSource(new SqsEventSource(queue, {}));
    }
}
