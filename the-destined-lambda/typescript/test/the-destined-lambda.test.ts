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

test('EventBridge PUT Permissions IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument":{
      "Statement": [
        {
          "Action": "events:PutEvents",
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }
  }
  ));
});

test('SNS Lambda Invoke Permissions Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Permission", {
    "Action": "lambda:InvokeFunction",
    "Principal": "sns.amazonaws.com"
  }
  ));
});

test('SNS Subscription Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SNS::Subscription", {
    "Protocol": "lambda"
  }
  ));
});

test('Success Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "success.handler",
    "Runtime": "nodejs12.x"
    }
  ));
});

test('Eventbridge Invoke Success Lambda Permissions Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Permission", {
    "Action": "lambda:InvokeFunction",
    "Principal": "events.amazonaws.com"
  }
  ));
});

test('Success Lambda EventBridge Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDestinedLambda.TheDestinedLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "Description": "all success events are caught here and logged centrally",
    "EventPattern": {
      "detail": {
        "requestContext": {
          "condition": ["Success"]
        },
        "responsePayload": {
          "source": ["cdkpatterns.the-destined-lambda"],
          "action": ["message"]
        }
      }
    },
    "State": "ENABLED",
    }
  ));
});