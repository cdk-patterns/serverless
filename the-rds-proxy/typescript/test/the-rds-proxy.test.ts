import { expect as expectCDK, matchTemplate, MatchStyle, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheRdsProxy from '../lib/the-rds-proxy-stack';

test('VPC Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::VPC", {
  }
  ));
});

test('Lambda to RDS Proxy Security Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
    "GroupDescription": "MyTestStack/Lambda to RDS Proxy Connection"
  }
  ));
});

test('RDS Proxy to MySQL Security Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
    "GroupDescription": "MyTestStack/Proxy to DB Connection"
  }
  ));
});

test('MySQL Ingress Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroupIngress", {
    "IpProtocol": "tcp",
    "Description": "allow db connection",
    "FromPort": 3306
  }
  ));
});

test('Lambda -> Proxy Ingress Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroupIngress", {
    "IpProtocol": "tcp",
    "Description": "allow lambda connection",
    "FromPort": 3306
  }
  ));
});

test('Store username/password in Secrets Manager', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SecretsManager::Secret", {
    "GenerateSecretString": {
      ExcludePunctuation: true,
      GenerateStringKey: "password",
      IncludeSpace: false,
      SecretStringTemplate: '{"username":"syscdk"}'
    }
  }
  ));
});

test('RDS DB Subnet Group created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::RDS::DBSubnetGroup", {
  }
  ));
});

test('RDS MySQL DB created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::RDS::DBInstance", {
    DBInstanceClass: "db.t2.small",
    Engine: "mysql"
  }
  ));
});

test('IAM Policy to allow secret access from Lambda Fn created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
    PolicyDocument: {
      Statement: [
        {
          Action: [
            "secretsmanager:GetSecretValue",
            "secretsmanager:DescribeSecret"
          ],
          Effect: "Allow"
        }
      ]
    }
  }
  ));
});

test('RDS Proxy created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::RDS::DBProxy", {
    DBProxyName: "MyTestStack-proxy",
    EngineFamily: "MYSQL",
    DebugLogging: true,
    RequireTLS: true
  }
  ));
});

test('Lambda Function created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    Handler: "rdsLambda.handler",
    Runtime: "nodejs12.x",
    Environment: {
      Variables: {
        PROXY_ENDPOINT:{},
        "RDS_SECRET_NAME": "MyTestStack-rds-credentials"
      }
    },
    "VpcConfig": {}
  }
  ));
});

test('API Gateway Http API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheRdsProxy.TheRdsProxyStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGatewayV2::Api", {
    "ProtocolType": "HTTP"
  }
  ));
});