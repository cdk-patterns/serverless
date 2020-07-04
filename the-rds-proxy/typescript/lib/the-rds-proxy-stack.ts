import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import * as secrets from '@aws-cdk/aws-secretsmanager';
const ssm = require('@aws-cdk/aws-ssm');

export class TheRdsProxyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2, // Default is all AZs in the region
    });
    
    let group = new ec2.SecurityGroup(this, 'DB Connection', {
      vpc
    })
    group.addIngressRule(group, ec2.Port.tcp(3306), 'allow db connection');

    const databaseUsername = 'syscdk';

    const databaseCredentialsSecret = new secrets.Secret(this, 'DBCredentialsSecret', {
      secretName: 'rds-credentials',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          username: databaseUsername,
        }),
        excludePunctuation: true,
        includeSpace: false,
        generateStringKey: 'password'
      }
    });

    new ssm.StringParameter(this, 'DBCredentialsArn', {
      parameterName: 'rds-credentials-arn',
      stringValue: databaseCredentialsSecret.secretArn,
    });

    //let parameterGroup = rds.ClusterParameterGroup.fromParameterGroupName(this, 'ParameterGroup', "default.aurora-mysql5.7")

    const rdsInstance = new rds.DatabaseInstance(this, 'DBInstance', {
      engine: rds.DatabaseInstanceEngine.MYSQL,
      masterUsername: databaseCredentialsSecret.secretValueFromJson('username').toString(),
      masterUserPassword: databaseCredentialsSecret.secretValueFromJson('password'),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
      vpc,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      deletionProtection: false
    });
    
    rdsInstance.connections.addSecurityGroup(group)

    // Create an RDS Proxy
    const proxy = rdsInstance.addProxy('proxy', {
        secret: databaseCredentialsSecret,
        iamAuth: true,
        debugLogging: true,
        vpc,
        securityGroups: [group]
    });
    
    rdsInstance.connections.allowFrom(proxy, ec2.Port.allTraffic())
    
    // Workaround for bug where TargetGroupName is not set but required
    let targetGroup = proxy.node.children.find((child:any) => {
      return child instanceof rds.CfnDBProxyTargetGroup
    }) as rds.CfnDBProxyTargetGroup

    targetGroup.addPropertyOverride('TargetGroupName', 'default')

  }
}
