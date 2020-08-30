from aws_cdk import (
    core,
    aws_route53 as r53,
    aws_route53_targets as r53_targets,
    aws_certificatemanager as acm,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_amazonmq as mq,
    aws_elasticloadbalancingv2 as elb,
    aws_elasticloadbalancingv2_targets as elb_targets,
    custom_resources as cr,
)

# Paste Hosted zone ID from Route53 console 'Hosted zone details'
hosted_zone_id = '1234'

# If zone_name = 'cdkexample.com' and subdomain_name = 'iot', you can connect to the broker by 'iot.cdkexample.com'.
zone_name = 'cdkexample.com'
subdomain_name = 'iot'

# Request and issue a certificate for the subdomain (iot.cdkexample.com in this example) beforehand, and paste ARN.
cert_arn = 'arn:aws:acm:us-east-1:228575038959:certificate/e1f36358-f619-4b73-ab08-f8a700cb0f69'
cidr = '10.0.0.0/16'

# You may use MQTT protocol as well by changing this value to 8883.
broker_port = 61617
mq_console_port = 8162


class TheBasicMQStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        zone = r53.HostedZone.from_hosted_zone_attributes(self, 'zone',
                                                          hosted_zone_id=hosted_zone_id,
                                                          zone_name=zone_name)

        # You may use acm.DnsValidatedCertificate to automate certificate provision.
        # However, be careful of ACM yearly certificate limit.
        # You will bump into the error after you destroy/deploy the stack over and over again.
        # See https://github.com/aws/aws-cdk/issues/5889 for the details.
        cert = acm.Certificate.from_certificate_arn(self, 'cert', certificate_arn=cert_arn)

        # MQ needs to be setup in a VPC
        vpc = ec2.Vpc(self, 'vpc',
                      cidr=cidr,
                      max_azs=2, # Default is all AZs in the region
                      subnet_configuration=[
                          ec2.SubnetConfiguration(name='vpc-public-subnet',
                                                  cidr_mask=24,
                                                  subnet_type=ec2.SubnetType.PUBLIC),
                          ec2.SubnetConfiguration(name='vpc-private-subnet',
                                                  cidr_mask=24,
                                                  subnet_type=ec2.SubnetType.PRIVATE)
                      ])

        mq_group = ec2.SecurityGroup(self, 'mq_group', vpc=vpc)
        bastion_to_mq_group = ec2.SecurityGroup(self, 'bastion_to_mq_group', vpc=vpc)

        mq_group.add_ingress_rule(peer=ec2.Peer.ipv4(cidr),
                                  connection=ec2.Port.tcp(broker_port),
                                  description='allow OpenWire communication within VPC')
        mq_group.add_ingress_rule(peer=ec2.Peer.ipv4(cidr),
                                  connection=ec2.Port.tcp(mq_console_port),
                                  description='allow communication on ActiveMQ console port within VPC')
        mq_group.add_ingress_rule(peer=mq_group,
                                  connection=ec2.Port.all_tcp(),
                                  description='allow communication from nlb and other brokers')

        # allow SSH to bastion from anywhere (for debugging)
        # bastion_to_mq_group.add_ingress_rule(connection=ec2.Port.all_tcp())

        core.CfnOutput(self, 'bastionToMQGroupSGID', value=bastion_to_mq_group.security_group_id)

        mq_username = 'admin'
        mq_password = 'password1234'

        ssm.StringParameter(self, 'string_parameter',
                            parameter_name='MQBrokerUserPassword',
                            string_value='{username},{password}'.format(username=mq_username, password=mq_password))

        mq_master = mq.CfnBroker.UserProperty(console_access=True,
                                              username=mq_username,
                                              password=mq_password)

        mq_instance = mq.CfnBroker(self, 'mq_instance',
                                   auto_minor_version_upgrade=False,
                                   broker_name='myMQ',
                                   deployment_mode='ACTIVE_STANDBY_MULTI_AZ',
                                   engine_type='ACTIVEMQ',
                                   engine_version='5.15.12',
                                   host_instance_type='mq.t3.micro',
                                   publicly_accessible=False,
                                   users=[mq_master],
                                   subnet_ids=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE).subnet_ids,
                                   security_groups=[mq_group.security_group_id])

        nlb_target_group = elb.NetworkTargetGroup(self, 'nlb_target',
                                                  vpc=vpc,
                                                  port=broker_port,
                                                  target_type=elb.TargetType.IP,
                                                  protocol=elb.Protocol.TLS,
                                                  health_check=elb.HealthCheck(enabled=True,
                                                                               port=str(mq_console_port),
                                                                               protocol=elb.Protocol.TCP))

        # For now there is no way to retrieve private ip addresses of MQ broker instances from aws-amazonmq module.
        mq_described = cr.AwsCustomResource(self, 'function',
                                            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                                                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE),
                                            on_create=cr.AwsSdkCall(
                                                physical_resource_id=cr.PhysicalResourceId.of('function'),
                                                service='MQ',
                                                action='describeBroker',
                                                parameters={'BrokerId': mq_instance.broker_name}))

        mq_described.node.add_dependency(mq_instance)

        # Adding private ip addresses of broker instances to target group one by one
        for az in range(len(vpc.availability_zones)):
            ip = mq_described.get_response_field('BrokerInstances.{az}.IpAddress'.format(az=az))
            nlb_target_group.add_target(elb_targets.IpTarget(ip_address=ip))

        mq_nlb = elb.NetworkLoadBalancer(self, 'mq_nlb',
                                         vpc=vpc,
                                         internet_facing=True)

        mq_nlb.add_listener('listener',
                            port=broker_port,
                            protocol=elb.Protocol.TLS,
                            certificates=[elb.ListenerCertificate(certificate_arn=cert.certificate_arn)],
                            default_target_groups=[nlb_target_group])

        r53.ARecord(self, 'alias_record',
                    zone=zone,
                    record_name=subdomain_name,
                    target=r53.RecordTarget.from_alias(r53_targets.LoadBalancerTarget(mq_nlb)))

        bastion = ec2.BastionHostLinux(self, 'bastion',
                                       vpc=vpc,
                                       instance_name='bastion',
                                       subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                       security_group=bastion_to_mq_group)

        # Allow port forwarding
        bastion.instance.add_user_data(
            "sudo echo 'GatewayPorts yes' >> /etc/ssh/sshd_config",
            "sudo service sshd restart",
        )

        core.CfnOutput(self, 'bastionInstanceID', value=bastion.instance_id)

        core.CfnOutput(self, 'bastionPublicDNS', value=bastion.instance_public_dns_name)


