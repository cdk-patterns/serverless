import { expect as expectCDK, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheEfsLambda from '../lib/the-efs-lambda-stack';

test('VPC Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEfsLambda.TheEfsLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::VPC", {
  }
  ));
});

test('EFS File System Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEfsLambda.TheEfsLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EFS::FileSystem", {
  }
  ));
});

test('EFS Access Point Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEfsLambda.TheEfsLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EFS::AccessPoint", {
    PosixUser:{
      Gid: "1001",
      Uid: "1001"
    },
    RootDirectory:{
      CreationInfo:{
        OwnerGid: "1001",
        OwnerUid: "1001",
        Permissions: "750"
      },
      Path: "/export/lambda"
    }
  }
  ));
});



test('IAM Policy to allow EFS Access', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEfsLambda.TheEfsLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    PolicyDocument: {
      Statement: [
        {
          Action: "elasticfilesystem:ClientMount",
          Effect: "Allow"
        },
        {
          Action: "elasticfilesystem:ClientWrite",
          Effect: "Allow"
        }
      ]
    }
  }
  ));
});

test('Lambda Function created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEfsLambda.TheEfsLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    Handler: "message_wall.lambda_handler",
    Runtime: "python3.8",
    "VpcConfig": {}
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheEfsLambda.TheEfsLambdaStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});