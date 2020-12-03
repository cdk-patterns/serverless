import { expect as expectCDK, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as ThePredictiveLambda from '../lib/the-predictive-lambda-stack';

test('Predictive Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new ThePredictiveLambda.ThePredictiveLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "MemorySize": 4096,
    "PackageType": "Image"
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new ThePredictiveLambda.ThePredictiveLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});

