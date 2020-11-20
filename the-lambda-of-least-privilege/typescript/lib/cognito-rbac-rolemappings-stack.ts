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

// Helper Classes
import { RoleMapper } from "../util/role-mapper";

interface CognitoRbacRoleMappinglProps extends cdk.StackProps {
  cognitoIdentityPoolStack: CognitoIdentityPoolStack;
  webServiceStack: LeastPrivilegeWebserviceStack;
  providerName: string;
  mappingAttr: string;
}

export class CognitoRbacRoleMappingStack extends cdk.Stack {

  public readonly readOnlyRole: Role;
  public readonly creatorRole: Role;

  constructor(scope: cdk.Construct, id: string, props: CognitoRbacRoleMappinglProps) {
    super(scope, id, props);

    // ==================================================================================
    // Create our User Roles
    //
    // TODO are there any other managed policies that we should add to these?
    //
    // ==================================================================================

    // CREATE THE USER IAM ROLE
    /*this.readOnlyRole = new Role(this, id + 'ReadOnlyRole', {
      assumedBy: new ServicePrincipal('lambda.amazonaws.com')
    });*/

    this.readOnlyRole = new iam.Role(this, id + 'ReadOnlyRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": props.cognitoIdentityPoolStack.identityPool.ref },
        "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" },
      }, "sts:AssumeRoleWithWebIdentity"),
    });
    this.readOnlyRole.assumeRolePolicy?.addStatements(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        principals: [new iam.ServicePrincipal('lambda.amazonaws.com')],
        actions: ['sts:AssumeRole'],
      }),
    );
    // DynamoDB perms restricted to read operations
    this.readOnlyRole.addToPolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        resources: [props.webServiceStack.hitsTable.tableArn],
        actions: [
          'dynamodb:Scan',
          'dynamodb:Query',
          'dynamodb:Get',
          'logs:CreateLogStream',
          'logs:PutLogEvents'
        ]
      })
    );
    // Add permissions for calling the GET Operation
    this.readOnlyRole.addToPolicy(
      new PolicyStatement({
        actions: ['execute-api:Invoke'],
        effect: Effect.ALLOW,
        resources: [props.webServiceStack.getHitsMethod.methodArn]
      })
    )

    // CREATE THE ADMIN IAM ROLE.
    /*this.creatorRole = new Role(this, id + 'CreatorRole', {
      assumedBy: new ServicePrincipal('lambda.amazonaws.com')
    })*/
    this.creatorRole = new iam.Role(this, id + 'creatorRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": props.cognitoIdentityPoolStack.identityPool.ref },
        "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" },
      }, "sts:AssumeRoleWithWebIdentity"),
    });
    this.creatorRole.assumeRolePolicy?.addStatements(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        principals: [new iam.ServicePrincipal('lambda.amazonaws.com')],
        actions: ['sts:AssumeRole'],
      }),
    );
    // DynamoDB Perms - extended for UpdateItem
    this.creatorRole.addToPolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        resources: [props.webServiceStack.hitsTable.tableArn],
        actions: [
          'dynamodb:Scan',
          'dynamodb:Query',
          'dynamodb:Get',
          'dynamodb:UpdateItem',
          'logs:CreateLogStream',
          'logs:PutLogEvents'
        ]
      })
    );
    // Add permissions for calling the gateway
    this.readOnlyRole.addToPolicy(
      new PolicyStatement({
        actions: ['execute-api:Invoke'],
        effect: Effect.ALLOW,
        resources: [props.webServiceStack.putHitsMethod.methodArn]
      })
    )

    // ============================================================================================
    // Setup the LIST of MAPPING RULES:

    // Lets get a little prep work done before we create out Identity Pool
    // Create a mapping of roles from your provider JWT user claims to the IAM roles you created in your web service stack.
    // ============================================================================================
    let auth0RoleMapper = new RoleMapper();

    auth0RoleMapper.addMapping({
      claim: "custom:groups",
      matchType: 'Contains', // TODO We should try and find an enum for this element
      roleArn: this.creatorRole.roleArn,
      value: "admin" // user claim reference that should be on JWT
    });

    auth0RoleMapper.addMapping({
      claim: "custom:groups",
      matchType: 'Contains',
      roleArn: this.readOnlyRole.roleArn,
      value: "user" // user claim reference that should be on JWT.
    });

    // ============================================================================================
    // Each Identity Pool needs a default IAM role to assign to authenticated users / unauthenticated users
    //
    // Lets get rid of the unautheticated role post testing TODO MOR
    // ============================================================================================

    const unauthenticatedRole = new iam.Role(this, 'CognitoDefaultUnauthenticatedRole', {
      assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
        "StringEquals": { "cognito-identity.amazonaws.com:aud": props.cognitoIdentityPoolStack.identityPool.ref },
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
        "StringEquals": { "cognito-identity.amazonaws.com:aud": props.cognitoIdentityPoolStack.identityPool.ref },
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


    // Extend our Web Service Stack with Cognito Permissions

    // ========================================================================
    // Resource: Amazon Cognito Role Mapping
    // ========================================================================

    // Purpose: Map an external user claim to IAM Role ARN

    // See also:
    // - https://aws.amazon.com/cognito/
    // - vhttps://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html

    // Create a role-mapping attachment

    const roleAttachment = new CfnIdentityPoolRoleAttachment(this, "CustomRoleAttachmentFunction", {
      identityPoolId: props.cognitoIdentityPoolStack.identityPool.ref,
      roles: {
        'unauthenticated': unauthenticatedRole.roleArn,
        'authenticated': authenticatedRole.roleArn
      },
      roleMappings: {
        [props.providerName]: {
          identityProvider: 'cognito-idp.' + this.region + '.amazonaws.com/' + props.cognitoIdentityPoolStack.userPool.userPoolId + ':' + props.cognitoIdentityPoolStack.userPoolClient.ref,  //cognito-idp.${Stack.of(this).region}.amazonaws.com/${pool.userPoolId}:${client.userPoolClientId}
          ambiguousRoleResolution: 'Deny',
          type: 'Rules',
          rulesConfiguration: {
            rules: auth0RoleMapper.getRules()
          }
        }
      }

    })
  }
}