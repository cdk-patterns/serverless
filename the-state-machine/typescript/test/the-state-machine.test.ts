import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheStateMachine = require('../lib/the-state-machine-stack');

test('API Gateway Proxy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheStateMachine.TheStateMachineStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}"
  }
  ));
});


test('State Machine Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheStateMachine.TheStateMachineStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::StepFunctions::StateMachine", {
     "DefinitionString": {
          "Fn::Join": [
            "",
            [
              "{\"StartAt\":\"Order Pizza Job\",\"States\":{\"Order Pizza Job\":{\"Next\":\"With Pineapple?\",\"Retry\":[{\"ErrorEquals\":[\"Lambda.ServiceException\",\"Lambda.AWSLambdaException\",\"Lambda.SdkClientException\"],\"IntervalSeconds\":2,\"MaxAttempts\":6,\"BackoffRate\":2}],\"Type\":\"Task\",\"InputPath\":\"$.flavour\",\"ResultPath\":\"$.pineappleAnalysis\",\"Resource\":\"",
              {
              },
              "\"},\"With Pineapple?\":{\"Type\":\"Choice\",\"Choices\":[{\"Variable\":\"$.pineappleAnalysis.containsPineapple\",\"BooleanEquals\":true,\"Next\":\"Sorry, We Dont add Pineapple\"}],\"Default\":\"Lets make your pizza\"},\"Lets make your pizza\":{\"Type\":\"Pass\",\"End\":true},\"Sorry, We Dont add Pineapple\":{\"Type\":\"Fail\",\"Error\":\"They asked for Pineapple\",\"Cause\":\"Failed To Make Pizza\"}},\"TimeoutSeconds\":300}"
            ]
          ]
        }
  }
  ));
});

test('Order Pizza Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheStateMachine.TheStateMachineStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "orderPizza.handler"
  }
  ));
});

test('State Machine Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheStateMachine.TheStateMachineStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "stateMachineLambda.handler"
  }
  ));
});

test('DLQ Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheStateMachine.TheStateMachineStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SQS::Queue", {
    "VisibilityTimeout": 300
  }
  ));
});
