import * as cdk from '@aws-cdk/core';
import cognito = require("@aws-cdk/aws-cognito");
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import {CfnUserPool, CfnUserPoolIdentityProvider, SignInType, UserPool, UserPoolAttribute} from "@aws-cdk/aws-cognito";
import {BillingMode, StreamViewType} from "@aws-cdk/aws-dynamodb";

import {Utils} from "../cfg/utils";

export class TheLeastPrivilegeServiceStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ============================================================================
    // Environment variables and constants
    // ============================================================================
    
    const domain = Utils.getEnv("COGNITO_DOMAIN_NAME");
    const groupsAttributeName = Utils.getEnv("GROUPS_ATTRIBUTE_NAME", "groups");
    const identityProviderName = Utils.getEnv("IDENTITY_PROVIDER_NAME", "");
    const identityProviderMetadataURLOrFile = Utils.getEnv("IDENTITY_PROVIDER_METADATA", "");

    const groupsAttributeClaimName = "custom:" + groupsAttributeName;

    let appUrl = Utils.getEnv("APP_URL", "");

    // ========================================================================
    // Resource: Amazon Cognito User Pool
    // ========================================================================

    // Purpose: creates a user directory and allows federation from external IdPs

    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnUserPool.html
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html


    // high level construct
    const userPool: UserPool = new cognito.UserPool(this, id + "Pool", {});

    // any properties that are not part of the high level construct can be added using this method
    const userPoolCfn = userPool.node.defaultChild as CfnUserPool;
    userPoolCfn.userPoolAddOns = { advancedSecurityMode: "ENFORCED" }
    userPoolCfn.schema = [{
      name: groupsAttributeName,
      attributeDataType: "String",
      mutable: true,
      required: false,
      stringAttributeConstraints: {
        maxLength: "2048",
        minLength: "1"
      }
    }];
   
    // ========================================================================
    // Resource: Identity Provider Settings
    // ========================================================================

    // Purpose: Define the external Identity Provider details, field mappings etc.

    // See also:
    // - https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-saml-idp.html

    // mapping from IdP fields to Cognito attributes

    // We will allow Cognito in here for now however your organisation may not allow this. Worth a check.
   const supportedIdentityProviders = ["COGNITO"];
   let cognitoIdp: CfnUserPoolIdentityProvider | undefined = undefined;

   if (identityProviderMetadataURLOrFile && identityProviderName) {

     cognitoIdp = new cognito.CfnUserPoolIdentityProvider(this, "CognitoIdP", {
       providerName: identityProviderName,
       providerDetails: Utils.isURL(identityProviderMetadataURLOrFile) ? {
         MetadataURL: identityProviderMetadataURLOrFile
       } : {
         MetadataFile: identityProviderMetadataURLOrFile
       },
       providerType: "SAML",
       // Structure: { "<cognito attribute name>": "<IdP SAML attribute name>" }
       attributeMapping: {
         "email": "email",
         "family_name": "lastName",
         "given_name": "firstName",
         "name": "firstName", // alias to given_name
         [groupsAttributeClaimName]: "groups" //syntax for a dynamic key
       },
       userPoolId: userPool.userPoolId
     });

     supportedIdentityProviders.push(identityProviderName);
   }

    // ========================================================================
    // Resource: Cognito App Client
    // ========================================================================

    // Purpose: each app needs an app client defined, where app specific details are set, such as redirect URIs

    // See also:
    // - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html

    const cfnUserPoolClient = new cognito.CfnUserPoolClient(this, "CognitoAppClient", {
      supportedIdentityProviders: supportedIdentityProviders,
      clientName: "User-Pool-Client",
      allowedOAuthFlowsUserPoolClient: true,
      allowedOAuthFlows: ["code"],
      allowedOAuthScopes: ["openid", "profile", "aws.cognito.signin.user.admin"],
      explicitAuthFlows: ["ALLOW_REFRESH_TOKEN_AUTH"],
      preventUserExistenceErrors: "ENABLED",
      generateSecret: false,
      refreshTokenValidity: 1,
      callbackUrLs: [appUrl],
      logoutUrLs: [appUrl],
      userPoolId: userPool.userPoolId
    });

    // we want to make sure we do things in the right order
    if (cognitoIdp) {
      cfnUserPoolClient.node.addDependency(cognitoIdp);
    }

   // ========================================================================
    // Resource: Cognito Auth Domain
    // ========================================================================

    // Purpose: creates / updates the custom subdomain for cognito's hosted UI

    // See also:
    // https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html

    const cfnUserPoolDomain = new cognito.CfnUserPoolDomain(this, "CognitoDomain", {
      domain: domain,
      userPoolId: userPool.userPoolId
    });


    new cdk.CfnOutput(this, "UserPoolIdOutput", {
      description: "UserPool ID",
      value: userPool.userPoolId
    });

    new cdk.CfnOutput(this, "AppClientIdOutput", {
      description: "App Client ID",
      value: cfnUserPoolClient.ref
    });

    new cdk.CfnOutput(this, "RegionOutput", {
      description: "Region",
      value: this.region
    });

    new cdk.CfnOutput(this, "CognitoDomainOutput", {
      description: "Cognito Domain",
      value: cfnUserPoolDomain.domain
    });

    //DynamoDB Table
    const table = new dynamodb.Table(this, 'Hits', {
      billingMode: BillingMode.PAY_PER_REQUEST,
      serverSideEncryption: true,
      partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
    });

    // defines an AWS Lambda resource
    const dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
      handler: 'lambda.handler',                // file is "lambda", function is "handler"
      environment: {
        HITS_TABLE_NAME: table.tableName
      }
    });

    // grant the lambda role read/write permissions to our table
    table.grantReadWriteData(dynamoLambda);

    // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new apigw.LambdaProxyIntegration({
        handler: dynamoLambda
      })
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
}
