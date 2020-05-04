import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheDynamoFlow = require('../lib/the-dynamo-flow-stack');

test('Dynamo Lambda Created - Tracing Enabled', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheDynamoFlow.TheDynamoFlowStack(app, 'TheDynamoFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Handler": "dynamo.handler",
        "Runtime": "nodejs12.x",
        "TracingConfig": {
            "Mode": "Active"
        }
      }
      ));
  });

test('DynamoDB Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheDynamoFlow.TheDynamoFlowStack(app, 'TheDynamoFlowStack', {
        snsTopicARN: 'arn:1234:1234:1234:1234:1234'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
      "KeySchema": [
        {
          "AttributeName": "path",
          "KeyType": "HASH"
        }
      ]}
    ));
  });