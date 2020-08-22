import {expect as expectCDK, matchTemplate, MatchStyle, haveResourceLike} from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheBasicMQ from '../lib/the-basic-mq-stack';

test('VPC Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::VPC", {}
  ));
});

test('MQ Instances Security Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
      "GroupDescription": "MyTestStack/mqGroup"
    }
  ));
});

test('Bastion to MQ Instances Security Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
      "GroupDescription": "MyTestStack/bastionToMQGroup"
    }
  ));
});

test('MQ Group Ingress Rule Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroup", {
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "Description": "allow OpenWire communication within VPC",
          "FromPort": TheBasicMQ.brokerPort,
          "CidrIp": TheBasicMQ.vpcCidr,
        },
        {
          "IpProtocol": "tcp",
          "Description": "allow communication on ActiveMQ console port within VPC",
          "FromPort": TheBasicMQ.mqConsolePort,
          "CidrIp": TheBasicMQ.vpcCidr,
        }]
    }
  ));

  expectCDK(stack).to(haveResourceLike("AWS::EC2::SecurityGroupIngress", {
      "IpProtocol": "tcp",
      "Description": "allow communication from nlb and other brokers",
      "FromPort": 0,
    }
  ));
});

test('Store username/password in ssm parameter', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::SSM::Parameter", {
    "Type": "String"
    }
  ));
});

test('MQ Instances Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AmazonMQ::Broker", {
      "PubliclyAccessible": false,
      "Users": [
        {
          "ConsoleAccess": true
        }
      ]
    }
  ));
});

test('NLB Target Group Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ElasticLoadBalancingV2::TargetGroup", {
      "HealthCheckEnabled": true,
      "HealthCheckPort": TheBasicMQ.mqConsolePort.toString(),
      "Port": TheBasicMQ.brokerPort,
    }
  ));
});

test('NLB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ElasticLoadBalancingV2::LoadBalancer", {
      "Scheme": "internet-facing",
    }
  ));
});

test('NLB Listener Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ElasticLoadBalancingV2::Listener", {
      "Port": TheBasicMQ.brokerPort,
      "Protocol": "TLS",
    }
  ));
});

test('Alias Record Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Route53::RecordSet", {
      "Name": `${TheBasicMQ.subdomainName}.${TheBasicMQ.zoneName}.`,
      "Type": "A",
    }
  ));
});

test('Bastion Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheBasicMQ.TheBasicMQStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::EC2::Instance", {
    }
  ));
});