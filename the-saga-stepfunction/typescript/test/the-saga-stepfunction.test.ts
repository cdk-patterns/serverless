import { expect as expectCDK, haveResourceLike, countResourcesLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSagaStepfunction = require('../lib/the-saga-stepfunction-stack');

test('API Gateway Proxy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}"
  }
  ));
});

test('Saga Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "sagaLambda.handler"
  }
  ));
});

test('Saga Lambda Permissions To Execute StepFunction', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [{
        "Action": "states:StartExecution",
        "Effect": "Allow"
      }]
    }
  }
  ));
});

test('Saga State Machine Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::StepFunctions::StateMachine", {
     "DefinitionString": {
          "Fn::Join": [
            "",
            [
              "{\"StartAt\":\"BookHotel\",\"States\":{\"BookHotel\":{\"Next\":\"BookFlight\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.BookHotelError\",\"Next\":\"CancelHotel\"}],\"Type\":\"Task\",\"Resource\":\"",
              {},
              "\",\"ResultPath\":\"$.BookHotelResult\"},\"BookFlight\":{\"Next\":\"BookRental\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.CancelFlightError\",\"Next\":\"CancelFlight\"}],\"Type\":\"Task\",\"Resource\":\"",
              {},
              "\",\"ResultPath\":\"$.BookFlightResult\"},\"BookRental\":{\"Next\":\"We have made your booking!\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.CancelRentalError\",\"Next\":\"CancelRental\"}],\"Type\":\"Task\",\"Resource\":\"",
              {},
              "\",\"ResultPath\":\"$.BookRentalResult\"},\"We have made your booking!\":{\"Type\":\"Succeed\"},\"CancelRental\":{\"Next\":\"CancelFlight\",\"Retry\":[{\"ErrorEquals\":[\"States.ALL\"],\"MaxAttempts\":3}],\"Type\":\"Task\",\"Resource\":\"",
              {},
              "\",\"ResultPath\":\"$.CancelRentalResult\"},\"CancelFlight\":{\"Next\":\"CancelHotel\",\"Retry\":[{\"ErrorEquals\":[\"States.ALL\"],\"MaxAttempts\":3}],\"Type\":\"Task\",\"Resource\":\"",
              {},
              "\",\"ResultPath\":\"$.CancelFlightResult\"},\"CancelHotel\":{\"Next\":\"Sorry, We Couldn't make the booking\",\"Retry\":[{\"ErrorEquals\":[\"States.ALL\"],\"MaxAttempts\":3}],\"Type\":\"Task\",\"Resource\":\"",
              {},
              "\",\"ResultPath\":\"$.CancelHotelResult\"},\"Sorry, We Couldn't make the booking\":{\"Type\":\"Fail\"}},\"TimeoutSeconds\":300}"
            ]
          ]
        }
  }
  ));
});

test('6 Separate DynamoDB Read/Write IAM Policies Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(countResourcesLike("AWS::IAM::Policy", 6, {
    "PolicyDocument": {
      "Statement": [
        {
        "Action": [
          "dynamodb:BatchGetItem",
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:Query",
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ],
        "Effect": "Allow"  
      }]
    }
  }
  ));
});

test('3 DynamoDB Tables Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(countResourcesLike("AWS::DynamoDB::Table", 3, {
    "KeySchema": [
      {
        "AttributeName": "trip_id",
        "KeyType": "HASH"
      }
    ]}
  ));
});

test('Hotel Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "bookHotel.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Cancel Hotel Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "cancelHotel.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Flight Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "bookFlight.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Cancel Flight Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "cancelFlight.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Rental Car Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "bookRental.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Cancel Rental Car Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "cancelRental.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});
