import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as lambda from '@aws-cdk/aws-lambda';
import * as efs from '@aws-cdk/aws-efs';
import apigw = require('@aws-cdk/aws-apigatewayv2');
import integrations = require('@aws-cdk/aws-apigatewayv2-integrations');

export class TheEfsLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2, // Default is all AZs in the region
    });

    // Create a file system in EFS to store information
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

    // This lambda function is given access to our EFS File System
    const efsLambda = new lambda.Function(this, 'efsLambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lambda-fns'), 
      handler: 'message_wall.lambda_handler',
      vpc: vpc,
      filesystem: lambda.FileSystem.fromEfsAccessPoint(accessPoint, '/mnt/msg')
    });

    // defines an API Gateway Http API resource backed by our "efsLambda" function.
    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new integrations.LambdaProxyIntegration({
        handler: efsLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
