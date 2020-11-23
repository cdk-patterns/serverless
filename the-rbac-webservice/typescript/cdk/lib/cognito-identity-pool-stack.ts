import * as cdk from '@aws-cdk/core';
import cognito = require("@aws-cdk/aws-cognito");
import { CfnUserPool, CfnUserPoolIdentityProvider, CfnIdentityPoolRoleAttachment, UserPool } from "@aws-cdk/aws-cognito";

import { iSAMLProviderConfig } from "./interfaces/ISAMLProviderConfig";
import { iOIDCProviderConfig } from "./interfaces/iOIDCProviderConfig";
import { iAttrSchema } from "./interfaces/iAttrSchema";
import { iUserPoolConfig } from "./interfaces/iUserPoolConfig";

interface CognitoIdentityPoolProps extends cdk.StackProps {
  userPoolClientConfig: iUserPoolConfig;
  userPoolAttrSchema: Array<iAttrSchema>;
  identityProviders: {
    providerName: string;
    oidcProvider?: iOIDCProviderConfig;
    samlProvider?: iSAMLProviderConfig;
  }
  cognitoDomain: string;
}

export class CognitoIdentityPoolStack extends cdk.Stack {
  
  public userPool: cognito.UserPool;
  public userPoolClient: cognito.CfnUserPoolClient;
  public identityPool: cognito.CfnIdentityPool;

  constructor(scope: cdk.Construct, id: string, props: CognitoIdentityPoolProps) {
    super(scope, id, props);

    // ========================================================================
    // Resource: Amazon Cognito User Pool
    // ========================================================================

    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html

    this.userPool = new cognito.UserPool(this, id + "UserPool", {});

    // any properties that are not part of the high level construct can be added using this method
    const userPoolCfn = this.userPool.node.defaultChild as CfnUserPool;
    userPoolCfn.userPoolAddOns = { advancedSecurityMode: "ENFORCED" }
    userPoolCfn.schema = props.userPoolAttrSchema;

    // ========================================================================
    // Resource: Identity Provider Settings
    // ========================================================================
    // Purpose: define the external Identity Provider details, field mappings etc.
    // See also:
    // - https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-saml-idp.html

    const supportedIdentityProviders = [];
    let cognitoManagedIdp: CfnUserPoolIdentityProvider | undefined = undefined;

    if (props.identityProviders.samlProvider) {
      cognitoManagedIdp = new cognito.CfnUserPoolIdentityProvider(this, "CognitoIdP", {
        providerName: props.identityProviders.providerName,
        providerType: props.identityProviders.samlProvider.type,
        providerDetails: {
          MetadataURL: props.identityProviders.samlProvider.details.MetaDataURL
        },
        // Structure: { "<cognito attribute name>": "<IdP SAML attribute name>" }
        attributeMapping: props.identityProviders.samlProvider.attributeMapping,
        userPoolId: this.userPool.userPoolId
      });
    } // TODO Extend this for OIDC
    supportedIdentityProviders.push(props.identityProviders.providerName);


    // ========================================================================
    // Resource: Amazon Cognito User Pool Client
    // ========================================================================

    // A User Pool Client resource represents an Amazon Cognito User Pool Client that provides a way to 
    // generate authentication tokens used to authorize a user for an application. Configuring a User Pool Client 
    // then connecting it to a User Pool will generate to a User Pool client ID. An application will need this 
    // client ID in order for it to access the User Pool, in addition to the necessary User Pool's identifiers.

    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html

    this.userPoolClient = new cognito.CfnUserPoolClient(this, id + 'UserPoolClient', {
      supportedIdentityProviders: supportedIdentityProviders,
      allowedOAuthFlowsUserPoolClient: props.userPoolClientConfig.allowedOAuthFlowsUserPoolClient,
      allowedOAuthFlows: props.userPoolClientConfig.allowedOAuthFlows,
      allowedOAuthScopes: props.userPoolClientConfig.allowedOAuthScopes,
      refreshTokenValidity: props.userPoolClientConfig.refreshTokenValidity,
      writeAttributes: props.userPoolClientConfig.writeAttributes,
      callbackUrLs: props.userPoolClientConfig.callbackUrLs,
      logoutUrLs: props.userPoolClientConfig.logoutUrLs,
      clientName: id + 'UserPoolClient',
      userPoolId: this.userPool.userPoolId
    })

    // we want to make sure we do things in the right order
    if (cognitoManagedIdp) {
      this.userPoolClient.node.addDependency(cognitoManagedIdp);
    }

    // ========================================================================
    // Resource: CognitoUserPoolDomain
    // ========================================================================

    // Purpose: creates / updates the custom subdomain for cognito's hosted UI

    // See also:
    // https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html

    const cfnUserPoolDomain = new cognito.CfnUserPoolDomain(this, "CognitoDomain", {
      domain: props.cognitoDomain,
      userPoolId: this.userPool.userPoolId
    });

    // ========================================================================
    // Resource: Amazon Cognito Identity Pool
    // ========================================================================
    //
    // Purpose: Create an pool that stores our 3p identities
    //
    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html

    this.identityPool = new cognito.CfnIdentityPool(this, id + 'IdentityPool', {
      allowUnauthenticatedIdentities: false,
      cognitoIdentityProviders: [{
        clientId: this.userPoolClient.ref,
        providerName: this.userPool.userPoolProviderName,
      }]
    });

    //Outputs
    new cdk.CfnOutput(this, "UserPoolIdOutput", {
      description: "UserPool ID",
      value: this.userPool.userPoolId
    });

    new cdk.CfnOutput(this, "WebClientIdOutput", {
      description: "App Client ID",
      value: this.userPoolClient.ref
    });

    new cdk.CfnOutput(this, "IdentityPoolId", {
      description: "Identity Pool ID",
      value: this.identityPool.ref
    });

    new cdk.CfnOutput(this, "CognitoDomainOutput", {
      description: "Cognito Domain",
      value: cfnUserPoolDomain.domain
    });

    new cdk.CfnOutput(this, "RegionOutput", {
      description: "Region",
      value: this.region
    });
  }
}
