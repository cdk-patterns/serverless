import * as cdk from '@aws-cdk/core';
import cognito = require("@aws-cdk/aws-cognito");
import iam = require("@aws-cdk/aws-iam");
import { CfnUserPool, CfnUserPoolIdentityProvider, CfnIdentityPoolRoleAttachment, UserPool } from "@aws-cdk/aws-cognito";
import { PolicyStatement, Effect } from "@aws-cdk/aws-iam";

import { RoleMapping } from "../lib/interfaces/RoleMapping"; // This should be replaced by an actual CDK library class probably.

interface CognitoIdentityPoolProps extends cdk.StackProps {
  providerClientId: string;
  providerClientSecret: string;
  providerIssuer: string;
  providerName: string;
  providerGroupsAttrName: string;
  callbackUrls: string;
  logoutUrls: string;
  roleMappingRules: RoleMapping[];
}

export class CognitoIdentityPoolStack extends cdk.Stack {
  /**
   *  We need to set the objects that need externally referenced as class member variables
   * 
   *  public readonly ecsCluster: ecs.Cluster;
   *  public readonly ecsService: ecsPatterns.NetworkLoadBalancedFargateService;
   * 
   * @param scope 
   * 
   * @param id 
   * @param props 
   */

  constructor(scope: cdk.Construct, id: string, props: CognitoIdentityPoolProps) {
    super(scope, id, props);

    // ============================================================================
    // Environment variables and constants
    // ============================================================================
    const groupsAttributeClaimName = "custom:" + props.providerGroupsAttrName;

    // ========================================================================
    // Resource: Amazon Cognito User Pool
    // ========================================================================

    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html

    const userPool: UserPool = new cognito.UserPool(this, id + "UserPool", {});

    // any properties that are not part of the high level construct can be added using this method
    const userPoolCfn = userPool.node.defaultChild as CfnUserPool;
    userPoolCfn.userPoolAddOns = { advancedSecurityMode: "ENFORCED" }
    userPoolCfn.schema = [{
      name: props.providerGroupsAttrName,
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
    /**
     * ADIL CFT
     * const updateParams = {
        ProviderDetails: {
          attributes_request_method: 'GET',
          authorize_scopes: 'openid profile',
          client_id: IDPClientId,
          client_secret: IDPClientSecret,
          oidc_issuer: IDPIssuer,
        },
        ProviderName: 'lmidp',
        UserPoolId,
        AttributeMapping: {
          'custom:groups': 'groups',
          username: 'sub',
          name: 'displayName',
        },
      };
     */
    // mapping from IdP fields to Cognito attributes
    const supportedIdentityProviders = ["COGNITO"]; //TODO Remove Cognito as an option
    let cognitoIdp: CfnUserPoolIdentityProvider | undefined = undefined;

    if (props.providerName) {

      cognitoIdp = new cognito.CfnUserPoolIdentityProvider(this, "CognitoIdP", {
        providerName: props.providerName,
        providerDetails: {
          attributes_request_method: 'GET',
          authorize_scopes: 'openid profile',
          client_id: props.providerClientId,
          client_secret: props.providerClientSecret,
          oidc_issuer: props.providerIssuer,
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

    /**
     * ADIL CFT TODO REMOVE
     * 
     *  ClientName: UserPoolClientName,
        UserPoolId,
        CallbackURLs,
        LogoutURLs: [LogoutURL],
        AllowedOAuthFlows: ['code'],
        AllowedOAuthScopes: ['openid', 'profile', 'aws.cognito.signin.user.admin'],
        SupportedIdentityProviders: ['lmidp'],
        AllowedOAuthFlowsUserPoolClient: true,
        RefreshTokenValidity: 1,
        WriteAttributes: ['picture'], // All fields are writable by deafult. We need to set one field to writebale in order to disable all others.
     */
    const userPoolClient = new cognito.CfnUserPoolClient(this, id + 'UserPoolClient', {
      supportedIdentityProviders: supportedIdentityProviders,
      allowedOAuthFlowsUserPoolClient: true,
      allowedOAuthFlows: ["code"],
      allowedOAuthScopes: ["email", "openid", "profile", "aws.cognito.signin.user.admin"],
      refreshTokenValidity: 1,
      writeAttributes: ['picture'],
      callbackUrLs: [props.callbackUrls],
      logoutUrLs: [props.logoutUrls],
      clientName: id + 'UserPoolClient',
      userPoolId: userPool.userPoolId
    })

    // ========================================================================
    // Resource: Amazon Cognito Identity Pool
    // ========================================================================

    // Purpose: Create an pool that stores our 3p identities

    // See also:
    // - https://aws.amazon.com/cognito/
    // - https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html

    const identityPool = new cognito.CfnIdentityPool(this, id + 'IdentityPool', {
      allowUnauthenticatedIdentities: false,
      cognitoIdentityProviders: [{
        clientId: userPoolClient.ref,
        providerName: userPool.userPoolProviderName,
      }]
    });

    // ============================================================================================
    // Each Identity Pool needs a default IAM role to assign to authenticated users / unauthenticated users
    //
    // Lets get rid of the unautheticated role post testing TODO MOR
    // ============================================================================================

    const unauthenticatedRole = new iam.Role(this, 'CognitoDefaultUnauthenticatedRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": identityPool.ref },
        "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "unauthenticated" },
      }, "sts:AssumeRoleWithWebIdentity"),
    });
    unauthenticatedRole.addToPolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        "mobileanalytics:PutEvents",
        "cognito-sync:*"
      ],
      resources: ["*"],
    }));

    const authenticatedRole = new iam.Role(this, 'CognitoDefaultAuthenticatedRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": identityPool.ref },
        "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" },
      }, "sts:AssumeRoleWithWebIdentity"),
    });

    authenticatedRole.addToPolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        "mobileanalytics:PutEvents",
        "cognito-sync:*",
        "cognito-identity:*"
      ],
      resources: ["*"],
    }));

    const defaultPolicy = new cognito.CfnIdentityPoolRoleAttachment(this, 'DefaultValid', {
      identityPoolId: identityPool.ref,
      roles: {
        'unauthenticated': unauthenticatedRole.roleArn,
        'authenticated': authenticatedRole.roleArn
      }
    });

    /**
     * ADIL CFT
     *   # Identity Pool role mapping
      IdentityPoolRoleAttachmentMapping:
        Type: Custom::CognitoRoleMapping
        Properties:
          ServiceToken:
            Fn::ImportValue: !Sub adil-custom-resources-${AppEnv}-CognitoRoleMappingLambda
          AttributeName: RoleMappings
          Entries:
            - Key: !Sub ${UserPool.ProviderName}:${CustomUserPoolClient.UserPoolClientId}
              Value:
                Type: Rules
                AmbiguousRoleResolution: AuthenticatedRole
                RulesConfiguration:
                  Rules:
                    - Claim: custom:groups
                      MatchType: Contains
                      RoleARN: !GetAtt ADILCreateInspectionBRRole.Arn
                      Value: ADIL_Inspection_Create_BR
                    - Claim: custom:groups
                      MatchType: Contains
                      RoleARN: !GetAtt ADILReviewInspectionBRRole.Arn
                      Value: ADIL_Inspection_Review_BR
    * 
    */
    // ========================================================================
    // Resource: Amazon Cognito Role Mapping
    // ========================================================================

    // Purpose: Map an external user claim to IAM Role ARN

    // See also:
    // - https://aws.amazon.com/cognito/
    // - vhttps://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html

    // Create a role-mapping

    // TODO Is this mapping performed in the correct place??

    const roleAttachment = new CfnIdentityPoolRoleAttachment(this, "CustomRoleAttachmentFunction", {
      identityPoolId: identityPool.ref,
      roles: {
        'unauthenticated': unauthenticatedRole.roleArn,
        'authenticated': unauthenticatedRole.roleArn
      },
      roleMappings: {
        [props.providerName]: {
          identityProvider: props.providerName,
          ambiguousRoleResolution: 'Deny',
          type: 'Rules',
          rulesConfiguration: {
            rules: props.roleMappingRules
          }
        }
      }

    })

    //Outputs

    new cdk.CfnOutput(this, "UserPoolIdOutput", {
      description: "UserPool ID",
      value: userPool.userPoolId
    });

    new cdk.CfnOutput(this, "AppClientIdOutput", {
      description: "App Client ID",
      value: userPoolClient.ref
    });

    new cdk.CfnOutput(this, "RegionOutput", {
      description: "Region",
      value: this.region
    });
  }
}
