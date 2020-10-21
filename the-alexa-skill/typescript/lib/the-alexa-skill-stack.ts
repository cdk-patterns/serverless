import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import assets = require('@aws-cdk/aws-s3-assets');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import * as alexaAsk from '@aws-cdk/alexa-ask';
import { ServicePrincipal, Role, PolicyStatement, CompositePrincipal } from '@aws-cdk/aws-iam';
import { execSync } from 'child_process';
const path = require('path');
const alexaAssets = '../skill'

export class TheAlexaSkillStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const asset = new assets.Asset(this, 'SkillAsset', {
      path: path.join(__dirname, alexaAssets),
    })

    //role to access bucket
    const role = new Role(this, 'Role', {
      assumedBy:new CompositePrincipal(
        new ServicePrincipal('alexa-appkit.amazon.com'),
        new ServicePrincipal('cloudformation.amazonaws.com')
      )
    });


    // Allow the skill resource to access the zipped skill package
    role.addToPolicy(new PolicyStatement({
      actions: ['S3:GetObject'],
      resources: [`arn:aws:s3:::${asset.s3BucketName}/${asset.s3ObjectKey}`]
    }));

    // DynamoDB Table
     const usersTable = new dynamodb.Table(this, 'Users', {
      partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });

    // Install Dependencies and Compile Lambda Function
    execSync('cd lambda-fns && npm i && npm run build');

    // Lambda function for Alexa fulfillment
    const alexaLambda = new lambda.Function(this, 'AlexaLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambda-fns'),
      handler: 'lambda.handler',
      environment: {
        USERS_TABLE: usersTable.tableName
      }
    });

    // grant the lambda role read/write permissions to our table
    usersTable.grantReadWriteData(alexaLambda);

    // create the skill
    const skill = new alexaAsk.CfnSkill(this, 'the-alexa-skill', {
      vendorId: '',
      authenticationConfiguration: {
        clientId: '',
        clientSecret: '',
        refreshToken: ''
      },
      skillPackage:{
        s3Bucket: asset.s3BucketName,
        s3Key: asset.s3ObjectKey,
        s3BucketRole: role.roleArn,
        overrides : {
          manifest: {
            apis:{
              custom: {
                endpoint:{
                  uri: alexaLambda.functionArn
                }
              }
            }
          }
        }
      }
    })





  /*
    Allow the Alexa service to invoke the fulfillment Lambda.
    In order for the Skill to be created, the fulfillment Lambda
    must have a permission allowing Alexa to invoke it, this causes
    a circular dependency and requires the first deploy to allow all
    Alexa skills to invoke the lambda, subsequent deploys will work
    when specifying the eventSourceToken
  */
    alexaLambda.addPermission('AlexaPermission', {
      //eventSourceToken: skill.ref,
      principal: new ServicePrincipal('alexa-appkit.amazon.com'),
      action: 'lambda:InvokeFunction'
  });
  }
}
