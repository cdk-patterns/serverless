import { expect as expectCDK, countResourcesLike, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheXrayTracer = require('../lib/the-xray-tracer-stack');

test('SNS Topic Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheXrayTracer.TheXrayTracerStack(app, 'TheXrayTracerStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SNS::Topic", {
  }));
});

test('SNS Publish IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheXrayTracer.TheXrayTracerStack(app, 'TheXrayTracerStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
          "Action": "sns:Publish",
          "Effect": "Allow"
        }]
    }
  }
  ));
});

test('API Gateway /{proxy+} URL Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheXrayTracer.TheXrayTracerStack(app, 'TheXrayTracerStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}",
  }
  ));
});

test('Two API Gateway Methods Created, one for / and one for {proxy+}', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheXrayTracer.TheXrayTracerStack(app, 'TheXrayTracerStack');
  // THEN
  expectCDK(stack).to(countResourcesLike("AWS::ApiGateway::Method", 2, {}))
});

test('API Gateway Tracing Enabled', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheXrayTracer.TheXrayTracerStack(app, 'TheXrayTracerStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Stage", {
    "MethodSettings": [{
      "DataTraceEnabled": true,
      "HttpMethod": "*",
      "LoggingLevel": "INFO",
      "MetricsEnabled": true,
      "ResourcePath": "/*"
    }],
    "TracingEnabled": true
  }
  ));
});