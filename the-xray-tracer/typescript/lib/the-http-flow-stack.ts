import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import sns_sub = require('@aws-cdk/aws-sns-subscriptions');
import sns = require('@aws-cdk/aws-sns');

export interface HttpFlowStackProps extends cdk.StackProps{
    readonly snsTopicARN: string;
}

export class TheHttpFlowStack extends cdk.Stack {

    httpLambda: lambda.Function;
    constructor(scope: cdk.Construct, id: string, props: HttpFlowStackProps) {
        super(scope, id, props);

        // defines an AWS Lambda resource
        this.httpLambda = new lambda.Function(this, 'httpLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'http.handler',
            tracing: lambda.Tracing.ACTIVE
        });

        let topic = sns.Topic.fromTopicArn(this, 'SNSTopic', props.snsTopicARN);
        topic.addSubscription(new sns_sub.LambdaSubscription(this.httpLambda));
    }
}
