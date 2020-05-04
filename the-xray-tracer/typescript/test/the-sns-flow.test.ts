import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSnsFlow = require('../lib/the-sns-flow-stack');

test('SNS Topic Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSnsFlow.TheSnsFlowStack(app, 'TheSnsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::SNS::Topic", {
    }));
  });


test('SNS Publish IAM Policy Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSnsFlow.TheSnsFlowStack(app, 'TheSnsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
        "PolicyDocument": {
        "Statement": [
            {
                "Action": [
                  "xray:PutTraceSegments",
                  "xray:PutTelemetryRecords"
                ],
                "Effect": "Allow"
            },
            {
                "Action": "sns:Publish",
                "Effect": "Allow"
            }]
        }
    }
    ));
});

test('SNS Publish Lambda Created - Tracing Enabled', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSnsFlow.TheSnsFlowStack(app, 'TheSnsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Handler": "sns_publish.handler",
        "Runtime": "nodejs12.x",
        "TracingConfig": {
            "Mode": "Active"
        }
      }
      ));
  });

test('SNS Lambda Subscription Created', () => {
    const app = new cdk.App();
    const topicARN = 'arn:1234:1234:1234:1234:1234';
    // WHEN
    const stack = new TheSnsFlow.TheSnsFlowStack(app, 'TheSnsFlowStack', {
        snsTopicARN: topicARN
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::SNS::Subscription", {
        "Protocol": "lambda",
        "TopicArn": topicARN
    }
    ));
});

test('SNS Given Lambda Invoke Permissions', () => {
    const app = new cdk.App();
    const topicARN = 'arn:1234:1234:1234:1234:1234';
    // WHEN
    const stack = new TheSnsFlow.TheSnsFlowStack(app, 'TheSnsFlowStack', {
        snsTopicARN: topicARN
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Permission", {
        "Action": "lambda:InvokeFunction",
        "Principal": "sns.amazonaws.com"
    }
    ));
});

test('SNS Subscribe Lambda Created - Tracing Enabled', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSnsFlow.TheSnsFlowStack(app, 'TheSnsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Handler": "sns_subscribe.handler",
        "Runtime": "nodejs12.x",
        "TracingConfig": {
            "Mode": "Active"
        }
      }
      ));
});