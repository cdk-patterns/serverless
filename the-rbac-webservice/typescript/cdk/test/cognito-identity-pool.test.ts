import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import CognitoIdentityPoolStack = require('../lib/cognito-identity-pool-stack');
import { StackConfiguration } from '../lib/configuration/stack-configuration';
import '@aws-cdk/assert/jest';

function initTestStack(stackName: string, props?: {}) {

  let app = new cdk.App();

  StackConfiguration.cognitoDomain = "swa-hits";
  StackConfiguration.identityProviders.providerName = "Auth0";

  const cognitoIdPoolSaml = new CognitoIdentityPoolStack.CognitoIdentityPoolStack(app, stackName, {
    userPoolClientConfig: StackConfiguration.userPoolConfig,
    userPoolAttrSchema: StackConfiguration.userPoolAttrSchema,
    identityProviders: {
      providerName: StackConfiguration.identityProviders.providerName,
      samlProvider: StackConfiguration.identityProviders.samlProvider
    },
    cognitoDomain: StackConfiguration.cognitoDomain
  });

  return cognitoIdPoolSaml;
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
        "Name": "roles",
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
  expect(stack).toHaveResource("AWS::Cognito::UserPoolIdentityProvider", {
    "ProviderName": "Auth0",
    "ProviderType": "SAML",
    "UserPoolId": {
      "Ref": "MyTestUPIDPStackUserPoolE5D3352F"
    },
    "AttributeMapping": {
      "custom:roles": "http://schemas.auth0.com/roles",
      "Email": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
    },
    "ProviderDetails": {
      "MetadataURL": "http://saml-metadataurl.com/example/url"
    }
  }
  );
});

test('Verify that UserPoolClient has been Created', () => {
  // WHEN
  const stack = initTestStack('MyTestUPCStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Cognito::UserPoolClient", {
    "UserPoolId": {
      "Ref": "MyTestUPCStackUserPoolFC506A7B"
    },
    "AllowedOAuthFlows": [
      "code"
    ],
    "AllowedOAuthFlowsUserPoolClient": true,
    "AllowedOAuthScopes": [
      "openid",
      "profile",
      "aws.cognito.signin.user.admin"
    ],
    "CallbackURLs": [
      "http://localhost:8080/callback"
    ],
    "ClientName": "MyTestUPCStackUserPoolClient",
    "LogoutURLs": [
      "http://localhost:8080/logout"
    ],
    "RefreshTokenValidity": 1,
    "SupportedIdentityProviders": [
      "Auth0"
    ],
    "WriteAttributes": [
      "custom:roles"
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