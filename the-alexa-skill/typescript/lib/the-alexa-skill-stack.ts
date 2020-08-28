import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import * as alexaAsk from '@aws-cdk/alexa-ask';
import { ServicePrincipal, Role, PolicyStatement, CompositePrincipal } from '@aws-cdk/aws-iam';


export interface AssetProps extends cdk.StackProps {
  readonly assetBucketARN: string;
  readonly assetBucketName: string;
  readonly assetObjectKey: string;
}

export class TheAlexaSkillStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: AssetProps) {
    super(scope, id, props);

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
      resources: [props.assetBucketARN+'/'+props.assetObjectKey]
    }));

    // DynamoDB Table
     const usersTable = new dynamodb.Table(this, 'Users', {
      partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
    });

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

    // create the skill /* TODO identify something unique that can trigger this to look for new contents at the S3 Key */
    const skill = new alexaAsk.CfnSkill(this, 'the-alexa-skill', {
      vendorId: 'foo',
      authenticationConfiguration: {
        clientId: 'foo',
        clientSecret: 'bar',
        refreshToken: 'foobar'
      },
      skillPackage:{
        s3Bucket: props.assetBucketName,
        s3Key: props.assetObjectKey,
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
