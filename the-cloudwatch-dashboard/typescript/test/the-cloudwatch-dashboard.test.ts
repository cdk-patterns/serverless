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

test('CloudWatch Dashboard Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResource("AWS::CloudWatch::Dashboard"));
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
    }],
    "Threshold": 1
  }
  ));
});

test('>0 API Gateway 5xx Errors Alarm Created', () => {
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

test('p99 Latency > 1 second API Gateway Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "MetricName": "Latency",
    "ExtendedStatistic": "p99",
    "Namespace": "AWS/ApiGateway",
    "Threshold": 1000
  }
  ));
});

test('% of invocations that errored, last 5 mins Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "Metrics": [{
      "Expression": "e / i * 100",
      "Label": "% of invocations that errored, last 5 mins"
    }, 
    {
      "Id": "i",
      "MetricStat": {
        "Metric": {
          "MetricName": "Invocations",
          "Namespace": "AWS/Lambda"
        }
      }
    },
    {
      "Id": "e",
      "MetricStat": {
        "Metric": {
          "MetricName": "Errors",
          "Namespace": "AWS/Lambda"
        }
      }
    }],
    "Threshold": 2
  }
  ));
});

test('Dynamo Lambda p99 Long Duration Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "MetricName": "Duration",
    "ExtendedStatistic": "p99",
    "Namespace": "AWS/Lambda",
    "Threshold": 1000
  }
  ));
});

test('% of throttled requests, last 30 mins Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "Metrics": [{
      "Expression": "t / (i + t) * 100",
      "Label": "% of throttled requests, last 30 mins"
    }, 
    {
      "Id": "i",
      "MetricStat": {
        "Metric": {
          "MetricName": "Invocations",
          "Namespace": "AWS/Lambda"
        }
      }
    },
    {
      "Id": "t",
      "MetricStat": {
        "Metric": {
          "MetricName": "Throttles",
          "Namespace": "AWS/Lambda"
        }
      }
    }],
    "Threshold": 2
  }
  ));
});

test('DynamoDB Throttles Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "Metrics": [{
      "Expression": "m1 + m2",
      "Label": "DynamoDB Throttles"
    }, 
    {
      "Id": "m1",
      "MetricStat": {
        "Metric": {
          "MetricName": "ReadThrottleEvents",
          "Namespace": "AWS/DynamoDB"
        }
      }
    },
    {
      "Id": "m2",
      "MetricStat": {
        "Metric": {
          "MetricName": "WriteThrottleEvents",
          "Namespace": "AWS/DynamoDB"
        }
      }
    }],
    "Threshold": 1
  }
  ));
});

test('DynamoDB Errors Alarm Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::CloudWatch::Alarm", {
    "Metrics": [{
      "Expression": "m1 + m2",
      "Label": "DynamoDB Errors"
    }, 
    {
      "Id": "m1",
      "MetricStat": {
        "Metric": {
          "MetricName": "UserErrors",
          "Namespace": "AWS/DynamoDB"
        }
      }
    },
    {
      "Expression": "getitem + batchgetitem + scan + query + getrecords + putitem + deleteitem + updateitem + batchwriteitem",
      "Id": "m2",
      "Label": "Sum of errors across all operations",
      "ReturnData": false
    }],
    "Threshold": 0
  }
  ));
});