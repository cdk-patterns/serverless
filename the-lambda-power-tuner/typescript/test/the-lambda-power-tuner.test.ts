import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheLambdaPowerTuner from '../lib/the-lambda-power-tuner-stack';

test('SQS Queue Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheLambdaPowerTuner.TheLambdaPowerTunerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Serverless::Application", {
  }));
});