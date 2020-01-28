import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheDynamoStreamer = require('../lib/the-dynamo-streamer-stack');

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "message",
        "KeyType": "HASH"
      }
    ],
    "StreamSpecification": {
      "StreamViewType": "NEW_IMAGE"
    }}
  ));
});

test('DynamoDB Stream Read IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
          "Action": "dynamodb:ListStreams",
          "Effect": "Allow"
        },
        {
          "Action": [
            "dynamodb:DescribeStream",
            "dynamodb:GetRecords",
            "dynamodb:GetShardIterator"
          ],
          "Effect": "Allow"
        }
      ]
    }
  }
  ));
});
