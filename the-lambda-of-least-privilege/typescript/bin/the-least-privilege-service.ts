#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';

// Helper Classes
import { RoleMapper } from "../cfg/role-mapper";

import { CognitoIdentityPoolStack } from '../lib/cognito-identity-pool-stack';
import { LeastPrivilegeWebserviceStack } from '../lib/least-privilege-webservice-stack';

const app = new cdk.App();

// ================================================================================
// TODO Mike We should probably have a basic UI/UX To demonstrate the setup.
//
// ================================================================================

// TODO maybe leverage Auth0 sample UI with CDKSPA pattern to produce a FE for calling 
// the service

// ================================================================================
// Create a WebService implemented using ApiGateway and Lambda
// 
// Web API with a lambda writing into a gateway
// This stack should create a set of IAM roles that are required to invoke it.
// ================================================================================
const webServiceStack = new LeastPrivilegeWebserviceStack(app, 'swa-lp-ws')

// ================================================================================
// Extend the Cognito Identity Pool with User Role Mapping
// 
// So can we map the user to the 
// ================================================================================
// TODO Mike - Clean up the role mapping.

let roleMapper = new RoleMapper();

roleMapper.addMapping({
    claim: 'custom:groups',
    matchType: 'Contains',
    roleArn: webServiceStack.creatorRole.roleArn,
    value: "idp:creatorUser"
});

roleMapper.addMapping({
    claim: 'custom:groups',
    matchType: 'Contains',
    roleArn: webServiceStack.readOnlyRole.roleArn,
    value: "idp:readOnlyUser"
});

// ================================================================================
// Create the Identity Pool Stack
// 
// Provide the details for your third party IDP (i.e. Auth0 or Ping)
// You will need to retrieve the client-id and secret from whatever vault solution that you use
//   !! Please dont commit client ids or secrets into your version control.
//
// =================================================================================

const cognitoIdPool = new CognitoIdentityPoolStack(app, 'swa-lp-cog', {
    providerClientId: 'client-id-placeholder',
    providerClientSecret: 'client-id-secret',
    providerIssuer: 'provider-endpoint',
    providerName: 'provider-name',
    providerGroupsAttrName: 'groups',
    callbackUrls: 'callback-urls-placeholder',
    logoutUrls: 'logout-urls-placeholder',
    roleMappingRules: roleMapper.getRules()
});