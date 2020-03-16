import { expect as expectCDK, matchTemplate, MatchStyle, haveResourceLike, haveResource } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeEtl = require('../lib/the-eventbridge-etl-stack');

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "id",
        "KeyType": "HASH"
      }
    ]}
  ));
});

test('Landing Bucket Created', () => {
  //GIVEN
  const app = new cdk.App();

  //WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  
  // THEN
  expectCDK(stack).to(haveResource('AWS::S3::Bucket'));
});

test('SQS Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResource("AWS::SQS::Queue"));
});

test('PutBucketNotification IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument":{
      "Statement": [
        {
          "Action": "s3:PutBucketNotification",
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }
  }
  ));
});

test('Custom::S3BucketNotifications LambdaCreated', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Description": "AWS CloudFormation handler for \"Custom::S3BucketNotifications\" resources (@aws-cdk/aws-s3)"
  }
  ));
});

test('EventBridge IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
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

test('VPC Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResource("AWS::EC2::VPC"));
});

test('ECS Cluster Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResource("AWS::ECS::Cluster"));
});

test('ECS Task Definition Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ECS::TaskDefinition", {
    "ContainerDefinitions":[
      {
        "Environment": [
          {
            "Name": "S3_BUCKET_NAME"
          },
          {
            "Name": "S3_OBJECT_KEY"
          }
        ],
        "LogConfiguration": {
          "LogDriver": "awslogs",
          "Options": {
            "awslogs-stream-prefix": "TheEventBridgeETL"
          }
        }
      }
    ],
    "Cpu": "256",
    "Memory": "512",
    "NetworkMode": "awsvpc",
    "RequiresCompatibilities": ["FARGATE"]
  }
  ));
});

test('Extract Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "s3SqsEventConsumer.handler",
    "Runtime": "nodejs12.x",
    "ReservedConcurrentExecutions": 2,
    "Environment": {
      "Variables": {
        "CLUSTER_NAME": {},
        "TASK_DEFINITION": {},
        "SUBNETS": {}
      }
    }
    }
  ));
});

test('Extract Lambda IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument":{
      "Statement": [
        {
          "Action": [
            "sqs:ReceiveMessage",
            "sqs:ChangeMessageVisibility",
            "sqs:GetQueueUrl",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
          ],
          "Effect": "Allow",
          "Resource": {}
        },
        {
          "Action": "events:PutEvents",
          "Effect": "Allow",
          "Resource": "*"
        },
        {
          "Action": "ecs:RunTask",
          "Effect": "Allow",
          "Resource": {}
        },
        {
          "Action": "iam:PassRole",
          "Effect": "Allow"
        }
      ]
    }
  }
  ));
});

test('Transform Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "transform.handler",
    "Runtime": "nodejs12.x",
    "ReservedConcurrentExecutions": 2
    }
  ));
});

test('Transform EventBridge Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "Description": "Data extracted from S3, Needs transformed",
    "EventPattern": {
      "source": [
        "cdkpatterns.the-eventbridge-etl"
      ],
      "detail-type": [
        "s3RecordExtraction"
      ],
      "detail": {
        "status": [
          "extracted"
        ]
      }
    },
    "State": "ENABLED",
    }
  ));
});

test('Load Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "load.handler",
    "Runtime": "nodejs12.x",
    "ReservedConcurrentExecutions": 2,
    "Environment": {
      "Variables": {
        "TABLE_NAME": {}
      }
    }
    }
  ));
});

test('Load Lambda IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    "PolicyDocument":{
      "Statement": [
        {
          "Action": "events:PutEvents",
          "Effect": "Allow",
          "Resource": "*"
        },
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
        }
      ]
    }
  }
  ));
});

test('Load EventBridge Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "Description": "Data transformed, Needs loaded into dynamodb",
    "EventPattern": {
      "source": [
        "cdkpatterns.the-eventbridge-etl"
      ],
      "detail-type": [
        "transform"
      ],
      "detail": {
        "status": [
          "transformed"
        ]
      }
    },
    "State": "ENABLED",
    }
  ));
});

test('Observe Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "observe.handler",
    "Runtime": "nodejs12.x"
    }
  ));
});

test('Observe EventBridge Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Events::Rule", {
    "Description": "all events are caught here and logged centrally",
    "EventPattern": {
      "source": [
        "cdkpatterns.the-eventbridge-etl"
      ]
    },
    "State": "ENABLED",
    }
  ));
});