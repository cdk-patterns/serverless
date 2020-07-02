import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import * as secrets from '@aws-cdk/aws-secretsmanager';
import * as lambda from '@aws-cdk/aws-lambda';

export class TheRdsProxyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2, // Default is all AZs in the region
    });

    new ec2.SecurityGroup(this, 'securityGroup', {
      vpc
    })
    const secret = new secrets.Secret(this, 'secret');

    // Create a MySQL DB
    const rdsInstance = new rds.DatabaseInstance(this, 'Instance', {
      engine: rds.DatabaseInstanceEngine.MYSQL,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
      masterUsername: 'syscdk',
      vpc
    });

    // Create an RDS Proxy
    const proxy = rdsInstance.addProxy('proxy', {
        borrowTimeout: cdk.Duration.seconds(30),
        maxConnectionsPercent: 50,
        secret,
        vpc,
    });

    // Lambda to Interact with RDS Proxy
    const rdsLambda = new lambda.Function(this, 'extractLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas/rds'), 
      handler: 'rdsLambda.handler',
      vpc: vpc,
      environment: {
        PROXY_ENDPOINT: proxy.endpoint,
        PROXY_SECRET: secret.secretValue.toString()
      }
    });

    // Allow our lambda function to connect to our proxy
    proxy.connections.allowFrom(rdsLambda, ec2.Port.allTraffic())
  }
}
