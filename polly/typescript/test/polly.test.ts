import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as Polly from '../lib/polly-stack';

test('Polly Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Polly.PollyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "polly.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Polly IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Polly.PollyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
        "Action": [
          "translate:TranslateText",
          "polly:SynthesizeSpeech"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }]
    }
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Polly.PollyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});