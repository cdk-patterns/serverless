#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';

// Helper Classes
import { RoleMapper } from "../util/role-mapper";

import { CognitoIdentityPoolStack } from '../lib/cognito-identity-pool-stack';
import { LeastPrivilegeWebserviceStack } from '../lib/least-privilege-webservice-stack';

import { StackConfiguration } from '../lib/configuration/stack-configuration';

const app = new cdk.App();

// ================================================================================
// Pre-requisites.
//
// Have created an Auth0 account and registered a client application by following x 
// instructions
// ================================================================================

// ================================================================================
// TODO What are the steps for having a local application up and running
//
// ================================================================================

// TODO Amplify Invocation library
// TODO Trigger Login
// TODO Use app-session created from login to call cognito-IDP
// TODO Invoke service for each user type
// TODO Handle errors

// ================================================================================
// Create a WebService implemented using ApiGateway and Lambda
// 
// Web API with a lambda writing into a gateway
// This stack should create a set of IAM roles that are required to invoke it.
// ================================================================================
const webServiceStack = new LeastPrivilegeWebserviceStack(app, 'swa-lp-ws')

// ================================================================================
// Create the Identity Pool Stack
// 
// Provide the details for your third party IDP (i.e. Auth0 or Ping)
// You will need to retrieve the client-id and secret from whatever vault solution that you use
//   !! Please dont commit client ids or secrets into your version control.
//
// =================================================================================

// Lets get a little prep work done before we create out Identity Pool
// Create a mapping of roles from your provider JWT user claims to the IAM roles you created in your web service stack.
let auth0RoleMapper = new RoleMapper();

auth0RoleMapper.addMapping({
    claim: 'custom:' + StackConfiguration.provider.claimsAttrRef,
    matchType: 'Contains', // TODO We should try and find an enum for this element
    roleArn: webServiceStack.creatorRole.roleArn,
    value: "creatorUser" // user claim reference that should be on JWT
});

auth0RoleMapper.addMapping({
    claim: 'custom:' + StackConfiguration.provider.claimsAttrRef,
    matchType: 'Contains',
    roleArn: webServiceStack.readOnlyRole.roleArn,
    value: "readOnlyUser" // user claim reference that should be on JWT.
});

const cognitoIdPool = new CognitoIdentityPoolStack(app, 'swa-lp-cog', {
    providerClientId: StackConfiguration.provider.clientId,
    providerClientSecret: StackConfiguration.provider.clientSecret,
    providerIssuer: StackConfiguration.provider.issuerEnpoint, 
    providerName: StackConfiguration.provider.name,
    providerType: StackConfiguration.provider.type,
    providerGroupsAttrName: StackConfiguration.provider.claimsAttrRef,
    callbackUrls: StackConfiguration.provider.callbackUrls,
    logoutUrls: StackConfiguration.provider.logoutUrls,
    roleMappingRules: auth0RoleMapper.getRules()
});