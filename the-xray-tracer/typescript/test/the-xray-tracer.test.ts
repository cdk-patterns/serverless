import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheXrayTracer from '../lib/the-xray-tracer-stack';
import lambda = require('@aws-cdk/aws-lambda'); 

test('Empty Stack', () => {
    const app = new cdk.App();

    let mockFunction = new lambda.Function(app, 'TestFunction', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.inline(''),
      handler: 'test'
    });

    // WHEN
    const stack = new TheXrayTracer.TheXrayTracerStack(app, 'MyTestStack', {
      dynamoFlowLambda: mockFunction,
      httpFlowLambda: mockFunction,
      sqsFlowLambda: mockFunction
  });
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
