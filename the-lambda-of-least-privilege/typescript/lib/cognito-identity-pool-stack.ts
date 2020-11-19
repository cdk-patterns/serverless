import * as cdk from '@aws-cdk/core';
import cognito = require("@aws-cdk/aws-cognito");
import iam = require("@aws-cdk/aws-iam");
import { CfnUserPool, CfnUserPoolIdentityProvider, CfnIdentityPoolRoleAttachment, UserPool } from "@aws-cdk/aws-cognito";

interface CognitoIdentityPoolProps extends cdk.StackProps {
  configuration: {
    providerGroupsAttrName: string;
    providerClientId?: string;
    providerClientSecret?: string;
    providerIssuer?: string;
    providerType: string;
    metadataURL?: string;
    callbackUrls: string;
    logoutUrls: string;
  };
  providerName: string;
  cognitoDomainName: string
}

export class CognitoIdentityPoolStack extends cdk.Stack {
  public userPool: cognito.UserPool;
  public userPoolClient: cognito.CfnUserPoolClient;
  public identityPool: cognito.CfnIdentityPool;

  constructor(scope: cdk.Construct, id: string, props: CognitoIdentityPoolProps) {
    super(scope, id, props);

    // ============================================================================
    // Environment variables and constants
    // ============================================================================
    const cogAttrMappingNameRef = "custom:" + props.configuration.providerGroupsAttrName;

    // ========================================================================
    // Resource: Amazon Cognito User Pool
    // ========================================================================

    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html

    this.userPool = new cognito.UserPool(this, id + "UserPool", {});

    // any properties that are not part of the high level construct can be added using this method
    const userPoolCfn = this.userPool.node.defaultChild as CfnUserPool;
    userPoolCfn.userPoolAddOns = { advancedSecurityMode: "ENFORCED" } //TODO Mike why is this in here?
    userPoolCfn.schema = [{
      name: "groups",
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

    // Purpose: define the external Identity Provider details, field mappings etc.

    // See also:
    // - https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-saml-idp.html

    // mapping from IdP fields to Cognito attributes

    const supportedIdentityProviders = [];
    let cognitoManagedIdp: CfnUserPoolIdentityProvider | undefined = undefined;

    if (props.providerName) {
      //SAML CFG ==============================================================================
      if (props.configuration.providerType === "SAML") {
        //TODO extend to configure for SAML based configurations
        cognitoManagedIdp = new cognito.CfnUserPoolIdentityProvider(this, "CognitoIdP", {
          providerName: props.providerName,
          providerType: props.configuration.providerType,
          providerDetails: {
            MetadataURL: props.configuration.metadataURL
          },
          // Structure: { "<cognito attribute name>": "<IdP SAML attribute name>" }
          attributeMapping: {
            "custom:groups": props.configuration.providerGroupsAttrName //syntax for a dynamic key
          },
          userPoolId: this.userPool.userPoolId
        });
      } else {
        //OIDC CFG ==============================================================================
        cognitoManagedIdp = new cognito.CfnUserPoolIdentityProvider(this, "CognitoIdP", {
          providerName: props.providerName,
          providerType: props.configuration.providerType,
          providerDetails: {
            attributes_request_method: 'GET', // TODO Understand this better and move it to configuration
            authorize_scopes: 'openid profile',
            client_id: props.configuration.providerClientId,
            client_secret: props.configuration.providerClientSecret,
            oidc_issuer: props.configuration.providerIssuer,
          },
          // Structure: { "<cognito attribute name>": "<IdP SAML attribute name>" }
          attributeMapping: {
            "custom:groups": props.configuration.providerGroupsAttrName //syntax for a dynamic key
          },
          userPoolId: this.userPool.userPoolId
        });
      }
      supportedIdentityProviders.push(props.providerName);
    }

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
      allowedOAuthFlowsUserPoolClient: true,
      allowedOAuthFlows: ["code"],
      allowedOAuthScopes: ["openid", "profile", "aws.cognito.signin.user.admin"],
      refreshTokenValidity: 1,
      writeAttributes: ['picture','custom:groups'],
      callbackUrLs: [props.configuration.callbackUrls],
      logoutUrLs: [props.configuration.logoutUrls],
      clientName: id + 'UserPoolClient',
      userPoolId: this.userPool.userPoolId
    })

    // we want to make sure we do things in the right order
    if (cognitoManagedIdp) {
      this.userPoolClient.node.addDependency(cognitoManagedIdp);
    }

    // ========================================================================
    // Resource: Cognito Auth Domain
    // ========================================================================

    // Purpose: creates / updates the custom subdomain for cognito's hosted UI

    // See also:
    // https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html

    const cfnUserPoolDomain = new cognito.CfnUserPoolDomain(this, "CognitoDomain", {
      domain: props.cognitoDomainName,
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

    new cdk.CfnOutput(this, "AppClientIdOutput", {
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
