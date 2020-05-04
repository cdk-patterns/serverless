import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheHttpFlow = require('../lib/the-http-flow-stack');

test('Http Lambda Created - Tracing Enabled', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheHttpFlow.TheHttpFlowStack(app, 'TheHttpFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Handler": "http.handler",
        "Runtime": "nodejs12.x",
        "TracingConfig": {
            "Mode": "Active"
        }
      }
      ));
  });