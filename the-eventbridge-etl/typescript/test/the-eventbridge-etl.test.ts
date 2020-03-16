import { expect as expectCDK, matchTemplate, MatchStyle, haveResourceLike, haveResource } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeEtl = require('../lib/the-eventbridge-etl-stack');

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
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

test('Landing Bucket Created', () => {
  //GIVEN
  const app = new cdk.App();

  //WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  
  // THEN
  expectCDK(stack).to(haveResource('AWS::S3::Bucket'));
});

test('SQS Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
expectCDK(stack).to(haveResource("AWS::SQS::Queue"));
});
