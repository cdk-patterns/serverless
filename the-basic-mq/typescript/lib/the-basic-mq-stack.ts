import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as mq from '@aws-cdk/aws-amazonmq';
import * as secrets from '@aws-cdk/aws-secretsmanager';
import * as elb from '@aws-cdk/aws-elasticloadbalancingv2';
import * as elbTargets from '@aws-cdk/aws-elasticloadbalancingv2-targets';
import * as acm from '@aws-cdk/aws-certificatemanager';
import * as r53 from '@aws-cdk/aws-route53';
import * as r53Targets from '@aws-cdk/aws-route53-targets';
import * as cr from '@aws-cdk/custom-resources';
import * as ssm from '@aws-cdk/aws-ssm';


//Paste Hosted zone ID from Route53 console 'Hosted zone details'
export const hostedZoneId = 'XXXXXXXXXXXXXXXXXXXXX';

// If zoneName = 'cdkexample.com' and subdomainName = 'iot', you can connect to the broker by 'iot.cdkexample.com'.
export const zoneName = 'cdkexample.com';
export const subdomainName = 'iot';

//You may use MQTT protocol as well by changing this value to 8883.
export const brokerPort = 61617;
export const mqConsolePort = 8162;
export const vpcCidr = '10.0.0.0/16';

export class TheBasicMQStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const zone = r53.HostedZone.fromHostedZoneAttributes(this, 'zone', {
      hostedZoneId: hostedZoneId,
      zoneName: zoneName
    });

    const cert = new acm.DnsValidatedCertificate(this, 'cert', {
      domainName: `${subdomainName}.${zoneName}`,
      hostedZone: zone,
    });

    // MQ needs to be setup in a VPC
    const vpc = new ec2.Vpc(this, 'vpc', {
      cidr: vpcCidr,
      maxAzs: 2, // Default is all AZs in the region
      subnetConfiguration: [
        {
          name: "vpc-public-subnet",
          cidrMask: 24,
          subnetType: ec2.SubnetType.PUBLIC
        },
        {
          name: "vpc-private-subnet",
          cidrMask: 24,
          subnetType: ec2.SubnetType.PRIVATE
        }
      ]
    });

    const mqGroup = new ec2.SecurityGroup(this, 'mqGroup', {
      vpc
    });

    const bastionToMQGroup = new ec2.SecurityGroup(this, 'bastionToMQGroup', {
      vpc
    });

    mqGroup.addIngressRule(ec2.Peer.ipv4(vpcCidr), ec2.Port.tcp(brokerPort), 'allow OpenWire communication within VPC');
    mqGroup.addIngressRule(ec2.Peer.ipv4(vpcCidr), ec2.Port.tcp(mqConsolePort), 'allow communication on ActiveMQ console port within VPC');
    mqGroup.addIngressRule(mqGroup, ec2.Port.allTcp(), 'allow communication from nlb and other brokers');

    //allow SSH to bastion from anywhere (for debugging)
    //bastionToMQGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22));

    new cdk.CfnOutput(this, "bastionToMQGroupSGID", {
      value: bastionToMQGroup.securityGroupId
    });

    const mqUsername = 'admin';
    const mqPassword = 'password1234';

    new ssm.StringParameter(this, 'stringParameter', {
      parameterName: 'MQBrokerUserPassword',
      stringValue: `${mqUsername},${mqPassword}`,
    });

    const mqMasterUser: mq.CfnBroker.UserProperty = {
      'consoleAccess': true,
      'username': mqUsername,
      'password': mqPassword,
    }

    const mqInstance = new mq.CfnBroker(this, 'mqInstance', {
      autoMinorVersionUpgrade: false,
      brokerName: 'myMQ',
      deploymentMode: 'ACTIVE_STANDBY_MULTI_AZ',
      engineType: 'ACTIVEMQ',
      engineVersion: '5.15.12',
      hostInstanceType: 'mq.t3.micro',
      publiclyAccessible: false,
      users: [mqMasterUser],
      subnetIds: vpc.selectSubnets({ subnetType: ec2.SubnetType.PRIVATE }).subnetIds,
      securityGroups: [mqGroup.securityGroupId],
    });

    const nlbTargetGroup = new elb.NetworkTargetGroup(this, 'nlbTarget', {
      vpc,
      port: brokerPort,
      targetType: elb.TargetType.IP,
      protocol: elb.Protocol.TLS,
      healthCheck: {
        enabled: true,
        port: mqConsolePort.toString(),
        protocol: elb.Protocol.TCP,
      },
    });

    // For now there is no way to retrieve private ip addresses of MQ broker instances from aws-amazonmq module.
    const mqDescribed = new cr.AwsCustomResource(this, 'function', {
      policy: cr.AwsCustomResourcePolicy.fromSdkCalls({
        resources: cr.AwsCustomResourcePolicy.ANY_RESOURCE
      }),
      onCreate: {
        physicalResourceId: {id: 'function'},
        service: 'MQ',
        action: 'describeBroker',
        parameters: {
          BrokerId: mqInstance.brokerName,
        }
      }
    });

    mqDescribed.node.addDependency(mqInstance);

    //Adding private ip addresses of broker instances to target group one by one
    for (let az = 0; az < vpc.availabilityZones.length; ++az) {
      const ip = mqDescribed.getResponseField(`BrokerInstances.${az}.IpAddress`);
      nlbTargetGroup.addTarget(new elbTargets.IpTarget(ip));
    }

    const mqNLB = new elb.NetworkLoadBalancer(this, 'mqNLB', {
      vpc,
      internetFacing: true,
    });

    mqNLB.addListener('listener', {
      port: brokerPort,
      protocol: elb.Protocol.TLS,
      certificates: [{certificateArn: cert.certificateArn}],
      defaultTargetGroups: [nlbTargetGroup],
    })

    new r53.ARecord(this, "aliasRecord", {
        zone: zone,
        recordName: subdomainName,
        target: r53.RecordTarget.fromAlias(new r53Targets.LoadBalancerTarget(mqNLB)),
    });

    const bastion = new ec2.BastionHostLinux(this, "bastion", {
      vpc: vpc,
      instanceName: "bastion",
      subnetSelection: {subnetType: ec2.SubnetType.PUBLIC},
      securityGroup: bastionToMQGroup,
    });

    //Allow port forwarding
    bastion.instance.addUserData(
      "sudo echo 'GatewayPorts yes' >> /etc/ssh/sshd_config",
      "sudo service sshd restart",
    );

    new cdk.CfnOutput(this, "bastionInstanceID", {
      value: bastion.instanceId
    });

    new cdk.CfnOutput(this, "bastionPublicDNS", {
      value: bastion.instancePublicDnsName
    });

  }
}

