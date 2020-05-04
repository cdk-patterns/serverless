import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSqsFlow = require('../lib/the-sqs-flow-stack');

test('SQS Queue Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::SQS::Queue", {
    }));
  });

test('SQS Send Message Lambda Created - Tracing Enabled', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Handler": "sqs.handler",
        "Runtime": "nodejs12.x",
        "TracingConfig": {
            "Mode": "Active"
        }
      }
      ));
  });

test('SQS Send Message IAM Policy Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
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
                    "Action": [
                    "sqs:SendMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl"
                    ],
                    "Effect": "Allow"
                }
            
            ]
        }
    }
    ));
});

test('SQS Subscribe Lambda Created - Tracing Enabled', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Handler": "sqs_subscribe.handler",
        "Runtime": "nodejs12.x",
        "TracingConfig": {
            "Mode": "Active"
        }
      }
      ));
  });

test('SQS recieve Message IAM Policy Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
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
                    "Action": [
                        "sqs:ReceiveMessage",
                        "sqs:ChangeMessageVisibility",
                        "sqs:GetQueueUrl",
                        "sqs:DeleteMessage",
                        "sqs:GetQueueAttributes"
                    ],
                    "Effect": "Allow"
                }
            
            ]
        }
    }
    ));
});

test('SNS Lambda Subscription Created', () => {
    const app = new cdk.App();
    const topicARN = 'arn:1234:1234:1234:1234:1234';
    // WHEN
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
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
    const stack = new TheSqsFlow.TheSqsFlowStack(app, 'TheSqsFlowStack', {
        snsTopicARN: topicARN
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Permission", {
        "Action": "lambda:InvokeFunction",
        "Principal": "sns.amazonaws.com"
    }
    ));
});