/**
 * Sample Structure..
 * rules: [{
              claim: 'custom:groups',
              matchType: 'Contains',
              roleArn: 'TODO Should be mapping a secure external user to a IAM group',
              value: "BASIC_USER_RULE"
            }]
 */

export interface RoleMapping {
    claim: string;
    matchType: string;
    roleArn: string;
    value: string;
  }