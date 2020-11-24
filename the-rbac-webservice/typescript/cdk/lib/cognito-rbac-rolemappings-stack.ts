import * as cdk from '@aws-cdk/core';
import iam = require("@aws-cdk/aws-iam");
import { CfnIdentityPoolRoleAttachment } from "@aws-cdk/aws-cognito";
import {
  Role,
  PolicyStatement,
  Effect
} from '@aws-cdk/aws-iam';
import { CognitoIdentityPoolStack } from './cognito-identity-pool-stack';
import { LeastPrivilegeWebserviceStack } from './least-privilege-webservice-stack';
import { eMatchTypes } from './enums/eMatchTypes';

// Helper Classes
import { RoleMapper } from "../util/role-mapper";

interface CognitoRbacRoleMappinglProps extends cdk.StackProps {
  cognitoIdentityPoolStack: CognitoIdentityPoolStack;
  cognitoAttr: string;
  webServiceStack: LeastPrivilegeWebserviceStack;
  providerName: string;
  mappingAttr: string;
}

export class CognitoRbacRoleMappingStack extends cdk.Stack {

  /**
   *  CognitoRbacRoleMappingStack (cdk.stack)
   * 
   *  This stack will create the roles for accessing our Web API Gateway Methods
   * 
   *  We will create two roles
   *    - Admin Role (Can put records into DynamoDB, Can call update & read endpoint)
   *    - Read Role (Can read a record from a DynamoDB, Can call read endpoint)
   * 
   *  We will allow both roles to be assumed-by the Cognito Identity Pool
   * 
   *  We will then setup the AWS-Cognito-Identity-Pool RoleMapping Attachments
   *    - Post Authentication this is how the Identity Pool will assign the role to the authenticated User
   * 
   */

  constructor(scope: cdk.Construct, id: string, props: CognitoRbacRoleMappinglProps) {
    super(scope, id, props);

    // ============================================================================================
    //    Resource: AWS::IAM::Role 
    //        The Deafult IAM Roles for the Identity Pool
    //        TODO Should be getting rid of these based on the refactorting of this stack.
    // ============================================================================================

    const unauthenticatedDefaultRole = new iam.Role(this, 'CognitoDefaultUnauthenticatedRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": props.cognitoIdentityPoolStack.identityPool.ref },
        "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "unauthenticated" },
      }, "sts:AssumeRoleWithWebIdentity"),
    });
    unauthenticatedDefaultRole.addToPolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        "mobileanalytics:PutEvents",
        "cognito-sync:*"
      ],
      resources: ["*"],
    }));

    const authenticatedDefaultRole = new iam.Role(this, 'CognitoDefaultAuthenticatedRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": props.cognitoIdentityPoolStack.identityPool.ref },
        "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" },
      }, "sts:AssumeRoleWithWebIdentity"),
    });

    authenticatedDefaultRole.addToPolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        "mobileanalytics:PutEvents",
        "cognito-sync:*",
        "cognito-identity:*"
      ],
      resources: ["*"],
    }));

    // ============================================================================================
    // Resource: RoleMapper
    //    Create a mapping of roles from your provider JWT user claims to the IAM roles you created 
    //    in your web service stack.
    //    Rule of Thumb: You should maybe have a mapping for each user role.
    // ============================================================================================
    let roleMap = new RoleMapper();

    roleMap.addMapping({
      claim: props.cognitoAttr,
      matchType: eMatchTypes.CONTAINS,
      roleArn: props.webServiceStack.adminRole.roleArn,
      value: "admin" // user claim reference that should be on JWT
    });

    roleMap.addMapping({
      claim: props.cognitoAttr,
      matchType: eMatchTypes.CONTAINS,
      roleArn: props.webServiceStack.userRole.roleArn,
      value: "user" // user claim reference that should be on JWT.
    });

    // ========================================================================
    // Resource: Amazon Cognito Identity Pool Role Attachment
    // ========================================================================
    // Purpose: Map an external user claim to IAM Role ARN
    // See also:
    // - https://aws.amazon.com/cognito/
    // - vhttps://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html

    const roleAttachment = new CfnIdentityPoolRoleAttachment(this, "CustomRoleAttachmentFunction", {
      identityPoolId: props.cognitoIdentityPoolStack.identityPool.ref,
      roles: {
        'unauthenticated': unauthenticatedDefaultRole.roleArn,
        'authenticated': authenticatedDefaultRole.roleArn
      },
      roleMappings: {
        [props.providerName]: {
          identityProvider: 'cognito-idp.' + this.region + '.amazonaws.com/' + props.cognitoIdentityPoolStack.userPool.userPoolId + ':' + props.cognitoIdentityPoolStack.userPoolClient.ref,  //cognito-idp.${Stack.of(this).region}.amazonaws.com/${pool.userPoolId}:${client.userPoolClientId}
          ambiguousRoleResolution: 'Deny',
          type: 'Rules',
          rulesConfiguration: {
            rules: roleMap.getRules()
          }
        }
      }

    })
  }
}