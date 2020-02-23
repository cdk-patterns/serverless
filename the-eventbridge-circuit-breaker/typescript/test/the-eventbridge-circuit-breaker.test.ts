import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeCircuitBreaker = require('../lib/the-eventbridge-circuit-breaker-stack');

test('Webservice Integration Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeCircuitBreaker.TheEventbridgeCircuitBreakerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambda.handler",
    "Runtime": "nodejs12.x",
    "Timeout": 20
    }
  ));
});

test('Error Handler Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeCircuitBreaker.TheEventbridgeCircuitBreakerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambda.handler",
    "Runtime": "nodejs12.x",
    "Timeout": 3
    }
  ));
});

test('Error DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeCircuitBreaker.TheEventbridgeCircuitBreakerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "RequestID",
        "KeyType": "HASH"
      },
      {
        "AttributeName": "ExpirationTime",
        "KeyType": "RANGE"
      }
    ],
    "AttributeDefinitions": [
      {
        "AttributeName": "RequestID",
        "AttributeType": "S"
      },
      {
        "AttributeName": "ExpirationTime",
        "AttributeType": "N"
      },
      {
        "AttributeName": "SiteUrl",
        "AttributeType": "S"
      }
    ],
    "GlobalSecondaryIndexes": [
      {
        "IndexName": "UrlIndex",
        "KeySchema": [
          {
            "AttributeName": "SiteUrl",
            "KeyType": "HASH"
          },
          {
            "AttributeName": "ExpirationTime",
            "KeyType": "RANGE"
          }
        ],
        "Projection": {
          "ProjectionType": "ALL"
        },
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        }
      }
    ],
    "TimeToLiveSpecification": {
      "AttributeName": "ExpirationTime",
      "Enabled": true
    }}
  ));
});

test('Error Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeCircuitBreaker.TheEventbridgeCircuitBreakerStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "Description": "Failed Webservice Call",
    "EventPattern": {
      "source": [
        "cdkpatterns.eventbridge.circuitbreaker"
      ],
      "detail-type": [
        "httpcall"
      ],
      "detail": {
        "status": [
          "fail"
        ]
      }
    },
    "State": "ENABLED",
    }
  ));
});
