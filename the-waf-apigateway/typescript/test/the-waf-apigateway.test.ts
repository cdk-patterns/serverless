import { expect as expectCDK, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as WAF from '../lib/the-waf-stack';

test('Rules Added To WebACL', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new WAF.TheWafStack(app, 'MyTestStack', {
      gatewayARN: '12345'
    });
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::WAFv2::WebACL", {
      "Scope": "REGIONAL",
      "Rules": [
        {
          "Name": "AWS-AWSManagedRulesCommonRuleSet"
        },
        {
          "Name": "awsAnonymousIP"
        },
        {
          "Name": "awsIPReputation"
        },
        {
          "Name": "geoblockRule"
        }
      ]
    }))
});

test('WebACL Associated', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new WAF.TheWafStack(app, 'MyTestStack', {
    gatewayARN: '12345'
  });
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::WAFv2::WebACLAssociation", {
    "ResourceArn": "12345"
  }))
});
