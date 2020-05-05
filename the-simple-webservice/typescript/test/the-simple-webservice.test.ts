import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSimpleWebservice = require('../lib/the-simple-webservice-stack');

test('DynamoDB Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheSimpleWebservice.TheSimpleWebserviceStack(app, 'MyTestStack');
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

test('DynamoDB Read/Write IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleWebservice.TheSimpleWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
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

test('DynamoDB Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleWebservice.TheSimpleWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambda.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleWebservice.TheSimpleWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});
