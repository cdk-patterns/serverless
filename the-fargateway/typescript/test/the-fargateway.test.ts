import { expect as expectCDK, matchTemplate, MatchStyle, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheFargateway from '../lib/the-fargateway-stack';

test('VPC Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheFargateway.TheFargatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::VPC", {
  }
  ));
});

test('Fargate Security Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheFargateway.TheFargatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
    "GroupDescription": "MyTestStack/fargateway/SecurityGroup"
  }
  ));
});

test('Fargate Ingress Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheFargateway.TheFargatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroupIngress", {
    "IpProtocol": "tcp",
    "Description": "from MyTestStackapi725F2A80:API to Fargate",
    "FromPort": 80,
    "ToPort": 80,
    "SourceSecurityGroupId": {
      "Fn::GetAtt": [
        "apiC8550315",
        "GroupId"
      ]
    },
  }
  ));
});

test('API Gateway Security Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheFargateway.TheFargatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
    "GroupDescription": "MyTestStack/api"
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheFargateway.TheFargatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});