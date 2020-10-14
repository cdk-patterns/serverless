import { expect as expectCDK, matchTemplate, haveResourceLike,MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheLambdaCircuitBreaker from '../lib/the-lambda-circuit-breaker-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheLambdaCircuitBreaker.TheLambdaCircuitBreakerStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheLambdaCircuitBreaker.TheLambdaCircuitBreakerStack(app, 'MyTestStack');
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

test('DynamoDB Read/Write IAM Policy Created', () => {
const app = new cdk.App();
// WHEN
const stack = new TheLambdaCircuitBreaker.TheLambdaCircuitBreakerStack(app, 'MyTestStack');
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
const stack = new TheLambdaCircuitBreaker.TheLambdaCircuitBreakerStack(app, 'MyTestStack');
// THEN
expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
  "Handler": "index.handler",
  "Runtime": "nodejs12.x"
}
));
});

test('API Gateway Http API Created', () => {
const app = new cdk.App();
// WHEN
const stack = new TheLambdaCircuitBreaker.TheLambdaCircuitBreakerStack(app, 'MyTestStack');
// THEN
expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
  "ProtocolType": "HTTP"
}
));
});
