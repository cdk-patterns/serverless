import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import sns = require('@aws-cdk/aws-sns');
import sns_sub = require('@aws-cdk/aws-sns-subscriptions');

export interface SNSFlowStackProps extends cdk.StackProps{
    readonly snsTopicARN: string;
}

export class TheSnsFlowStack extends cdk.Stack {
    snsLambda: lambda.Function;
    constructor(scope: cdk.Construct, id: string, props: SNSFlowStackProps) {
        super(scope, id, props);

        // Create an SNS Topic
        const topic = new sns.Topic(this, 'TheXRayTracerSnsTopic', {
                displayName: "The XRay Tracer CDK Pattern Topic",
        });

        // defines an AWS Lambda resource
        this.snsLambda = new lambda.Function(this, 'snsLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'sns_publish.handler',
            environment: {
                TOPIC_ARN: topic.topicArn
            },
            tracing: lambda.Tracing.ACTIVE
        });
        topic.grantPublish(this.snsLambda);
        let apigwTopic = sns.Topic.fromTopicArn(this, 'SNSTopic', props.snsTopicARN);
        apigwTopic.addSubscription(new sns_sub.LambdaSubscription(this.snsLambda));

        // Have a Lambda subscribe to our topic
        let snsSubscribeLambda = new lambda.Function(this, 'snsSubscriptionLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'sns_subscribe.handler',
            tracing: lambda.Tracing.ACTIVE
        });
        topic.addSubscription(new sns_sub.LambdaSubscription(snsSubscribeLambda));
    }
}
