import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import CognitoIdentityPoolStack = require('../lib/cognito-identity-pool-stack');
import { RoleMapper } from '../util/role-mapper';


function initTestStack(stackName: string, props?: {}) {

  let app = new cdk.App();

  let auth0toIAMroleMapper = new RoleMapper();

  // Mock those settings, sure why not.
  auth0toIAMroleMapper.addMapping({
    claim: 'custom:groups',
    matchType: 'Contains',
    roleArn: 'updateRoleARN',
    value: "idp:creatorUser"
  });

  auth0toIAMroleMapper.addMapping({
    claim: 'custom:groups',
    matchType: 'Contains',
    roleArn: 'readRoleARN',
    value: "idp:readOnlyUser"
  });

  let cognitoIdPool = new CognitoIdentityPoolStack.CognitoIdentityPoolStack(app, stackName, {
    providerClientId: 'client-id-placeholder',
    providerClientSecret: 'client-id-secret',
    providerIssuer: 'provider-endpoint',
    providerName: 'provider-name',
    providerType: 'OIDC',
    providerGroupsAttrName: 'groups',
    callbackUrls: 'callback-urls-placeholder',
    logoutUrls: 'logout-urls-placeholder',
    roleMappingRules: auth0toIAMroleMapper.getRules(),
    cognitoDomainName: 'swa-hits'
  });

  return cognitoIdPool;
}

test('Verify that UserPool Resource has been Created', () => {
  // WHEN
  const stack = initTestStack('MyTestUPStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::UserPool", {
    "Schema": [
      {
        "AttributeDataType": "String",
        "Mutable": true,
        "Name": "groups",
        "Required": false,
        "StringAttributeConstraints": {
          "MaxLength": "2048",
          "MinLength": "1"
        }
      }
    ]
  }
  ));
});

test('Verify that UserPoolIdentityProvider Resource has been Created', () => {
  // WHEN
  const stack = initTestStack('MyTestUPIDPStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::UserPoolIdentityProvider", {
    "AttributeMapping": {
      "email": "email",
      "family_name": "lastName",
      "given_name": "firstName",
      "name": "firstName",
      "custom:groups": "groups"
    },
    "ProviderDetails": {
      "attributes_request_method": "GET",
      "authorize_scopes": "openid profile",
      "client_id": "client-id-placeholder",
      "client_secret": "client-id-secret",
      "oidc_issuer": "provider-endpoint"
    }
  }
  ));
});

test('Verify that UserPoolClient has been Created', () => {
  // WHEN
  const stack = initTestStack('MyTestUPCStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::UserPoolClient", {
    "AllowedOAuthScopes": [
      "email",
      "openid",
      "profile",
      "aws.cognito.signin.user.admin"
    ],
    "CallbackURLs": [
      "callback-urls-placeholder"
    ],
    "ClientName": "MyTestUPCStackUserPoolClient",
    "LogoutURLs": [
      "logout-urls-placeholder"
    ],
    "RefreshTokenValidity": 1,
    "SupportedIdentityProviders": [
      "provider-name"
    ],
    "WriteAttributes": [
      "picture"
    ]
  }
  ));
});

test('Verify that UserPoolClient has been Created', () => {
  // WHEN
  const stack = initTestStack('MyTestUPCStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::IdentityPool", {
    "AllowUnauthenticatedIdentities": false
  }
  ));
});

test('Verify that UserPoolDomain has been Created', () => {
  // WHEN
  const stack = initTestStack('Mycodomainstack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::UserPoolDomain", {
    "Domain": "swa-hits"
  }
  ));
});

test('Verify that IdentityPoolRoleAttachment has been Created with RoleMappings', () => {
  // WHEN
  const stack = initTestStack('MyTestIdPRAStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::IdentityPoolRoleAttachment", {
    "IdentityPoolId": {
      "Ref": "MyTestIdPRAStackIdentityPool"
    },
    "RoleMappings": {
      "provider-name": {
        "AmbiguousRoleResolution": "Deny",
        "IdentityProvider": {
          "Fn::Join": [
            "",
            [
              "cognito-idp.",
              {
                "Ref": "AWS::Region"
              },
              ".amazonaws.com/",
              {
                "Ref": "MyTestIdPRAStackUserPoolED618D1F"
              },
              ":",
              {
                "Ref": "MyTestIdPRAStackUserPoolClient"
              }
            ]
          ]
        },
        "RulesConfiguration": {
          "Rules": [
            {
              "Claim": "custom:groups",
              "MatchType": "Contains",
              "RoleARN": "updateRoleARN",
              "Value": "idp:creatorUser"
            },
            {
              "Claim": "custom:groups",
              "MatchType": "Contains",
              "RoleARN": "readRoleARN",
              "Value": "idp:readOnlyUser"
            }
          ]
        },
        "Type": "Rules"
      }
    }
  }
  ));
});