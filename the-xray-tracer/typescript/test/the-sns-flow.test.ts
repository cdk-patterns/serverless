import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSnsFlow = require('../lib/the-sns-flow-stack');

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