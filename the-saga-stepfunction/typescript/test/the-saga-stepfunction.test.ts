import { expect as expectCDK, haveResourceLike, countResourcesLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSagaStepfunction = require('../lib/the-saga-stepfunction-single-table-stack');

test('API Gateway Proxy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "{proxy+}"
  }
  ));
});

test('Saga Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "sagaLambda.handler"
  }
  ));
});

test('Saga Lambda Permissions To Execute StepFunction', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
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
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::StepFunctions::StateMachine", {
     "DefinitionString": {
      "Fn::Join": [
        "",
        [
          "{\"StartAt\":\"ReserveHotel\",\"States\":{\"ReserveHotel\":{\"Next\":\"ReserveFlight\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.ReserveHotelError\",\"Next\":\"CancelHotelReservation\"}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.ReserveHotelResult\"},\"ReserveFlight\":{\"Next\":\"TakePayment\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.ReserveFlightError\",\"Next\":\"CancelFlightReservation\"}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.ReserveFlightResult\"},\"TakePayment\":{\"Next\":\"ConfirmHotelBooking\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.TakePaymentError\",\"Next\":\"RefundPayment\"}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.TakePaymentResult\"},\"ConfirmHotelBooking\":{\"Next\":\"ConfirmFlight\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.ConfirmHotelBookingError\",\"Next\":\"RefundPayment\"}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.ConfirmHotelBookingResult\"},\"ConfirmFlight\":{\"Next\":\"We have made your booking!\",\"Catch\":[{\"ErrorEquals\":[\"States.ALL\"],\"ResultPath\":\"$.ConfirmFlightError\",\"Next\":\"RefundPayment\"}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.ConfirmFlightResult\"},\"We have made your booking!\":{\"Type\":\"Succeed\"},\"RefundPayment\":{\"Next\":\"CancelFlightReservation\",\"Retry\":[{\"ErrorEquals\":[\"States.ALL\"],\"MaxAttempts\":3}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.RefundPaymentResult\"},\"CancelFlightReservation\":{\"Next\":\"CancelHotelReservation\",\"Retry\":[{\"ErrorEquals\":[\"States.ALL\"],\"MaxAttempts\":3}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.CancelFlightReservationResult\"},\"CancelHotelReservation\":{\"Next\":\"Sorry, We Couldn't make the booking\",\"Retry\":[{\"ErrorEquals\":[\"States.ALL\"],\"MaxAttempts\":3}],\"Parameters\":{\"FunctionName\":\"",
          {},
          "\",\"Payload.$\":\"$\"},\"Type\":\"Task\",\"Resource\":\"arn:",
          {},
          ":states:::lambda:invoke\",\"ResultPath\":\"$.CancelHotelReservationResult\"},\"Sorry, We Couldn't make the booking\":{\"Type\":\"Fail\"}},\"TimeoutSeconds\":300}"
        ]
      ]
    }
  }
  ));
});

test('8 Separate DynamoDB Read/Write IAM Policies Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(countResourcesLike("AWS::IAM::Policy", 8, {
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

test('1 DynamoDB Table Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(countResourcesLike("AWS::DynamoDB::Table", 1, {
    "KeySchema": [
      {
        "AttributeName": "pk",
        "KeyType": "HASH"
      },
      {
        "AttributeName": "sk",
        "KeyType": "RANGE"
      }
    ],
    "AttributeDefinitions": [
      {
        "AttributeName": "pk",
        "AttributeType": "S"
      },
      {
        "AttributeName": "sk",
        "AttributeType": "S"
      }
    ]}
  ));
});

test('Hotel Reservation Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "hotel/reserveHotel.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Confirm Hotel Reservation Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "hotel/confirmHotel.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Cancel Hotel Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "hotel/cancelHotel.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Flight Reservation Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "flights/reserveFlight.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Confirm Flight Reservation Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "flights/confirmFlight.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Cancel Flight Booking Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "flights/cancelFlight.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Payment Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "payment/takePayment.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Cancel Payment Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSagaStepfunction.TheSagaStepfunctionSingleTableStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "payment/refundPayment.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});
