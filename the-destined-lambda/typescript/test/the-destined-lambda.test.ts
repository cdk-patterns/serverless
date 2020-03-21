import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheDestinedLambda = require('../lib/the-destined-lambda-stack');


test('EventBus Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::EventBus", {
    "Name": "the-destined-lambda"
  }
  ));
});

test('SNS Topic Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SNS::Topic", {
    "DisplayName": "The Destined Lambda CDK Pattern Topic"
  }
  ));
});

test('Destined Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "destinedLambda.handler",
    "Runtime": "nodejs12.x"
    }
  ));
});


test('Lambda Destinations Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::EventInvokeConfig", {
    "DestinationConfig": {
      OnFailure: {
        Destination: {}
      },
      OnSuccess: {
        Destination: {}
      }
    }
  }
  ));
});