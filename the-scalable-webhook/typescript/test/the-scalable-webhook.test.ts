import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheScalableWebhook = require('../lib/the-scalable-webhook-stack');

test('SQS Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
    // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SQS::Queue", {}));
});

test('DynamoDB Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
    // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "id",
        "KeyType": "HASH"
      }
    ]}
  ));
});

test('DynamoDB Read/Write and SQS Read/Delete IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
          "Action": [
            "sqs:ReceiveMessage",
            "sqs:ChangeMessageVisibility",
            "sqs:GetQueueUrl",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
          ],
          "Effect": "Allow"
        },
        {
        "Action": [
          "dynamodb:BatchGetItem",
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:Query",
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ],
        "Effect": "Allow"  
      }]
    }
  }
  ));
});

test('SQS Send IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
          "Action": [
            "sqs:SendMessage",
            "sqs:GetQueueAttributes",
            "sqs:GetQueueUrl"
          ],
          "Effect": "Allow"
        }]
    }
  }
  ));
});

test('Throttled Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambda.handler",
    "Runtime": "nodejs12.x",
    "ReservedConcurrentExecutions": 2
  }
  ));
});

test('Publisher Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambda.handler",
    "Runtime": "nodejs12.x",
    "Environment": {
      "Variables": {
        "queueURL": {
        }
      }
    }
  }
  ));
});

test('API Gateway Proxy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}"
  }
  ));
});