import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import LeastPrivilegeWebserviceStack = require('../lib/least-privilege-webservice-stack');
import CognitoIdentityPoolStack = require('../lib/cognito-identity-pool-stack');
import CognitoRbacRoleMappingStack = require('../lib/cognito-rbac-rolemappings-stack');
import { StackConfiguration } from '../lib/configuration/stack-configuration';

test('Test for accurate Role Mappings', () => {
    const app = new cdk.App();

    StackConfiguration.cognitoDomain = "swa-hits";
    StackConfiguration.identityProviders.providerName = "Auth0";

    const webServiceStack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'swa-lp-webservice-stack')

    const identityPoolStack = new CognitoIdentityPoolStack.CognitoIdentityPoolStack(app, 'swa-lp-identity-pool-stack', {
        userPoolClientConfig: StackConfiguration.userPoolConfig,
        userPoolAttrSchema: StackConfiguration.userPoolAttrSchema,
        identityProviders: {
            providerName: StackConfiguration.identityProviders.providerName,
            samlProvider: StackConfiguration.identityProviders.samlProvider
        },
        cognitoDomain: StackConfiguration.cognitoDomain

    });

    const stackUnderTest = new CognitoRbacRoleMappingStack.CognitoRbacRoleMappingStack(app, 'swa-lp-role-mappings', {
        cognitoIdentityPoolStack: identityPoolStack,
        webServiceStack: webServiceStack,
        mappingAttr: StackConfiguration.userPoolAttrSchema[0].name,
        cognitoAttr: StackConfiguration.cognitoDestAttr,
        providerName: StackConfiguration.identityProviders.providerName
    })

    expectCDK(stackUnderTest).to(haveResourceLike("AWS::Cognito::IdentityPoolRoleAttachment", {
        "RoleMappings": {
            "Auth0": {
              "AmbiguousRoleResolution": "Deny",
              "RulesConfiguration": {
                "Rules": [
                  {
                    "Claim": "custom:roles",
                    "MatchType": "Contains",
                    "Value": "admin"
                  },
                  {
                    "Claim": "custom:roles",
                    "MatchType": "Contains",
                    "Value": "user"
                  }
                ]
              },
              "Type": "Rules"
            }
          }
        }
    ));
});