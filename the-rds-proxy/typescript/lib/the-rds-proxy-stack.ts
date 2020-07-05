import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import * as secrets from '@aws-cdk/aws-secretsmanager';
const ssm = require('@aws-cdk/aws-ssm');
import * as lambda from '@aws-cdk/aws-lambda';
import apigw = require('@aws-cdk/aws-apigatewayv2');
import iam = require('@aws-cdk/aws-iam');

export class TheRdsProxyStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2, // Default is all AZs in the region
    });
    
    let lambdaToDBGroup = new ec2.SecurityGroup(this, 'Lambda to DB Connection', {
      vpc
    });
    let dbConnectionGroup = new ec2.SecurityGroup(this, 'Proxy to DB Connection', {
      vpc
    });
    dbConnectionGroup.addIngressRule(dbConnectionGroup, ec2.Port.tcp(3306), 'allow db connection');
    dbConnectionGroup.addIngressRule(lambdaToDBGroup, ec2.Port.tcp(3306), 'allow lambda connection');

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

    const rdsInstance = new rds.DatabaseInstance(this, 'DBInstance', {
      engine: rds.DatabaseInstanceEngine.MYSQL,
      masterUsername: databaseCredentialsSecret.secretValueFromJson('username').toString(),
      masterUserPassword: databaseCredentialsSecret.secretValueFromJson('password'),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
      vpc,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      deletionProtection: false,
      securityGroups: [dbConnectionGroup]
    });

    // Create an RDS Proxy
    const proxy = rdsInstance.addProxy('proxy', {
        secret: databaseCredentialsSecret,
        debugLogging: true,
        vpc,
        securityGroups: [dbConnectionGroup]
    });
    
    // Workaround for bug where TargetGroupName is not set but required
    let targetGroup = proxy.node.children.find((child:any) => {
      return child instanceof rds.CfnDBProxyTargetGroup
    }) as rds.CfnDBProxyTargetGroup

    targetGroup.addPropertyOverride('TargetGroupName', 'default');
    
    // Lambda to Interact with RDS Proxy
    const rdsLambda = new lambda.Function(this, 'extractLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas/rds'), 
      handler: 'rdsLambda.handler',
      vpc: vpc,
      securityGroups: [lambdaToDBGroup],
      environment: {
        PROXY_ENDPOINT: proxy.endpoint,
        RDS_SECRET_NAME: 'rds-credentials'
      }
    });

    databaseCredentialsSecret.grantRead(rdsLambda);

    // defines an API Gateway Http API resource backed by our "rdsLambda" function.
    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new apigw.LambdaProxyIntegration({
        handler: rdsLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
