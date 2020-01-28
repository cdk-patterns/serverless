import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheDynamoStreamer = require('../lib/the-dynamo-streamer-stack');

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "message",
        "KeyType": "HASH"
      }
    ],
    "StreamSpecification": {
      "StreamViewType": "NEW_IMAGE"
    }}
  ));
});

test('DynamoDB Stream Read IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument": {
      "Statement": [
        {
          "Action": "dynamodb:ListStreams",
          "Effect": "Allow"
        },
        {
          "Action": [
            "dynamodb:DescribeStream",
            "dynamodb:GetRecords",
            "dynamodb:GetShardIterator"
          ],
          "Effect": "Allow"
        }
      ]
    }
  }
  ));
});

test('Lambda Event Source Mapping Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::EventSourceMapping", {
    "BatchSize": 100,
    "StartingPosition": "LATEST"
  }));
});


test('API Gateway /InsertItem Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "InsertItem",
  }
  ));
});

test('API Gateway Method + VTL Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Method", {
    "HttpMethod": "POST",
    "AuthorizationType": "NONE",
    "Integration": {
      "IntegrationHttpMethod": "POST",
          "IntegrationResponses": [
            {
              "ResponseTemplates": {
                "application/json": "{\"message\":\"item added to db\"}"
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
              "SelectionPattern": "^\[BadRequest\].*",
              "StatusCode": "400"
            }
          ],
          "RequestTemplates": {
            "application/json": {
              "Fn::Join": [
                "",
                [
                  "{\"TableName\":\"",
                  {
                    "Ref": "TheDynamoStreamer641C5E5B"
                  },
                  "\",\"Item\":{\"message\":{\"S\":\"$input.path('$.message')\"}}}"
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
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
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

test('API Gateway -> DynamoDB Read/Write IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamoStreamer.TheDynamoStreamerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
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