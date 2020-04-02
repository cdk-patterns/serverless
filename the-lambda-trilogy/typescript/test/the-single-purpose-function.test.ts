import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSinglePurposeFunctionStack = require('../lib/the-single-purpose-function-stack');


test('Add Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSinglePurposeFunctionStack.TheSinglePurposeFunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "add.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Subtract Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSinglePurposeFunctionStack.TheSinglePurposeFunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "subtract.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Multiply Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSinglePurposeFunctionStack.TheSinglePurposeFunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "multiply.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('API Gateway add path Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSinglePurposeFunctionStack.TheSinglePurposeFunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "add"
  }
  ));
});

test('API Gateway multiply path Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSinglePurposeFunctionStack.TheSinglePurposeFunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "multiply"
  }
  ));
});

test('API Gateway subtract path Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSinglePurposeFunctionStack.TheSinglePurposeFunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "subtract"
  }
  ));
});
