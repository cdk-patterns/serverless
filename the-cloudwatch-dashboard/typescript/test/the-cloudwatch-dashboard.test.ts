import { expect as expectCDK, matchTemplate, haveResource, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheCloudwatchDashboard from '../lib/the-cloudwatch-dashboard-stack';

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "path",
        "KeyType": "HASH"
      }
    ]}
  ));
});

test('DynamoDB Read/Write IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
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

test('DynamoDB Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "lambda.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});

test('SNS Topic Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResource("AWS::SNS::Topic"));
});

test('% API Gateway 4xx Errors Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "Metrics": [{
      "Expression": "m1/m2*100",
      "Label": "% API Gateway 4xx Errors"
    }, 
    {
      "Id": "m1",
      "MetricStat": {
        "Metric": {
          "MetricName": "4XXError",
          "Namespace": "AWS/ApiGateway"
        }
      }
    },
    {
      "Id": "m2",
      "MetricStat": {
        "Metric": {
          "MetricName": "Count",
          "Namespace": "AWS/ApiGateway"
        }
      }
    }]
  }
  ));
});

test('% API Gateway 5xx Errors Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "MetricName": "5XXError",
    "Namespace": "AWS/ApiGateway",
    "Threshold": 0
  }
  ));
});