import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheLambdalithStack = require('../lib/the-lambda-lith-stack');


test('Lambda-lith Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheLambdalithStack.TheLambdalithStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambdalith.main",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('API Gateway Proxy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheLambdalithStack.TheLambdalithStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}"
  }
  ));
});
