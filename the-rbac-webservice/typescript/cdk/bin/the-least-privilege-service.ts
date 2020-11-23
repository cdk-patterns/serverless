#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';

import { CognitoIdentityPoolStack } from '../lib/cognito-identity-pool-stack';
import { LeastPrivilegeWebserviceStack } from '../lib/least-privilege-webservice-stack';
import { CognitoRbacRoleMappingStack } from '../lib/cognito-rbac-rolemappings-stack';

import { StackConfiguration } from '../lib/configuration/stack-configuration';

const app = new cdk.App();

// ================================================================================
// Create the Identity Pool Stack
// 
// Creates an AWS Cognito Identity pool for identities federated from the external identity provider
// Creates an AWS Cognito User Pool Client for your front end application to integrate with using OIDC
// =================================================================================

const identityPoolStack = new CognitoIdentityPoolStack(app, 'swa-lp-identity-pool-stack', {
    userPoolClientConfig: StackConfiguration.userPoolConfig,
    userPoolAttrSchema: StackConfiguration.userPoolAttrSchema,
    identityProviders: {
      providerName: StackConfiguration.identityProviders.providerName,
      samlProvider: StackConfiguration.identityProviders.samlProvider
    },
    cognitoDomain: StackConfiguration.cognitoDomain
  });

// ================================================================================
// Create a WebService implemented using ApiGateway and Lambda
// 
// Web API with a lambda writing into a gateway
// We will define the Roles for this in the RBAC Role Mappings later in the stack
// ================================================================================
const webServiceStack = new LeastPrivilegeWebserviceStack(app, 'swa-lp-webservice-stack', {
  identityPoolRef: identityPoolStack.identityPool.ref
})

// ================================================================================
// Map our Roles
// 
// Sets up the Roles needed for using our service (Admin Role and User Role)
// Using User Claims from the federated identity we map the user to a defined IAM Role
// =================================================================================

new CognitoRbacRoleMappingStack(app, 'swa-lp-role-mappings', {
    cognitoIdentityPoolStack: identityPoolStack,
    webServiceStack: webServiceStack,
    mappingAttr: StackConfiguration.userPoolAttrSchema[0].name,
    cognitoAttr: StackConfiguration.cognitoDestAttr,
    providerName: StackConfiguration.identityProviders.providerName
})
