import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheBigFan = require('../lib/the-big-fan-stack');

test('SNS Topic Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SNS::Topic", {
    "DisplayName": "The Big Fan CDK Pattern Topic"
  }));
});

test('StatusCreatedSubscriber SQS Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SQS::Queue", {
    "QueueName": "BigFanTopicStatusCreatedSubscriberQueue"
  }));
});

test('AnyOtherStatusSubscriber SQS Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SQS::Queue", {
    "QueueName": "BigFanTopicAnyOtherStatusSubscriberQueue"
  }));
});

test('Status Created SNS Message Subscription', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SNS::Subscription", {
    "Protocol": "sqs",
    "FilterPolicy": {
        "status": ["created"]
    }
  }));
});

test('Any Other Status SNS Message Subscription', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SNS::Subscription", {
    "Protocol": "sqs",
    "FilterPolicy": {
        "status":  [
          {
            "anything-but": [
              "created"
            ]
          }
        ]
    }
  }));
});

test('SQS ReceiveMessage IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
          "Action": [
            "sqs:ReceiveMessage",
            "sqs:ChangeMessageVisibility",
            "sqs:GetQueueUrl",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
          ],
          "Effect": "Allow"
        }]
    }
  }
  ));
});

test('createdStatus SQS Subscriber Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "createdStatus.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('anyOtherStatus SQS Subscriber Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "anyOtherStatus.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Lambda Event Source Mapping Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::EventSourceMapping", {
  }));
});

test('API Gateway /SendEvent Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "SendEvent",
  }
  ));
});

test('API Gateway Method + VTL Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Method", {
    "HttpMethod": "POST",
    "AuthorizationType": "NONE",
    "Integration": {
      "IntegrationHttpMethod": "POST",
      "IntegrationResponses": [
        {
          "ResponseTemplates": {
            "application/json": "{\"message\":\"message added to topic\"}"
          },
          "StatusCode": "200"
        },
        {
          "ResponseParameters": {
            "method.response.header.Content-Type": "'application/json'",
            "method.response.header.Access-Control-Allow-Origin": "'*'",
            "method.response.header.Access-Control-Allow-Credentials": "'true'"
          },
          "ResponseTemplates": {
            "application/json": "{\"state\":\"error\",\"message\":\"$util.escapeJavaScript($input.path('$.errorMessage'))\"}"
          },
          "SelectionPattern": "^\[Error\].*",
          "StatusCode": "400"
        }
      ],
      "RequestTemplates": {
        "application/json": {
          "Fn::Join": [
            "",
            [
              "Action=Publish&TargetArn=$util.urlEncode('",
              {},
              "')&Message=$util.urlEncode($input.path('$.message'))&Version=2010-03-31&MessageAttributes.entry.1.Name=status&MessageAttributes.entry.1.Value.DataType=String&MessageAttributes.entry.1.Value.StringValue=$util.urlEncode($input.path('$.status'))"
            ]
          ]
        }
      },
      "Type": "AWS",
    },
    "MethodResponses": [
      {
        "ResponseParameters": {
          "method.response.header.Content-Type": true,
          "method.response.header.Access-Control-Allow-Origin": true,
          "method.response.header.Access-Control-Allow-Credentials": true
        },
        "StatusCode": "200"
      },
      {
        "ResponseParameters": {
          "method.response.header.Content-Type": true,
          "method.response.header.Access-Control-Allow-Origin": true,
          "method.response.header.Access-Control-Allow-Credentials": true
        },
        "StatusCode": "400"
      }
    ]
  }
  ));
});

test('API Gateway Model Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBigFan.TheBigFanStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Model", {
    "ContentType": "application/json",
    "Name": "ResponseModel",
    "Schema": {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "pollResponse",
      "type": "object",
      "properties": {
        "message": {
          "type": "string"
        }
      }
    }
  }
  ));
});
