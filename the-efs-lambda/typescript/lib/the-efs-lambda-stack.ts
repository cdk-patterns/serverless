import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as lambda from '@aws-cdk/aws-lambda';
import * as efs from '@aws-cdk/aws-efs';
import apigw = require('@aws-cdk/aws-apigatewayv2');

export class TheEfsLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2, // Default is all AZs in the region
    });

    const fs = new efs.FileSystem(this, 'FileSystem', {
      vpc,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });

    const accessPoint = fs.addAccessPoint('AccessPoint',{
      createAcl: {
        ownerGid: '1001',
        ownerUid: '1001',
        permissions: '750'
      },
      path:'/export/lambda',
      posixUser: {
        gid: '1001',
        uid: '1001'
      }
    });

    const efsLambda = new lambda.Function(this, 'efsLambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.asset('lambdas'), 
      handler: 'MessageWall.lambda_handler',
      vpc: vpc,
      filesystem: lambda.FileSystem.fromEfsAccessPoint(accessPoint, '/mnt/msg')
    });

    // defines an API Gateway Http API resource backed by our "rdsLambda" function.
    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new apigw.LambdaProxyIntegration({
        handler: efsLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
