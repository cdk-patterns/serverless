import { expect as expectCDK, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as WAF from '../lib/the-waf-stack';
import * as Gateway from '../lib/api-gateway-stack';

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
          "Name": "AWS-AWSManagedRulesCommonRuleSet",
          "Priority": 1,
          "Statement": {
            "ManagedRuleGroupStatement": {
              "Name": "AWSManagedRulesCommonRuleSet"
            }
          }
        },
        {
          "Name": "awsAnonymousIP",
          "Priority": 2,
          "Statement": {
            "ManagedRuleGroupStatement": {
              "Name": "AWSManagedRulesAnonymousIpList"
            }
          }
        },
        {
          "Name": "awsIPReputation",
          "Priority": 3,
          "Statement": {
            "ManagedRuleGroupStatement": {
              "Name": "AWSManagedRulesAmazonIpReputationList"
            }
          }
        },
        {
          "Name": "geoblockRule",
          "Priority": 4,
          "Statement": {
            "GeoMatchStatement": {
              "CountryCodes": ["NZ"]
            }
          }
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

test('API Gateway Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Gateway.ApigatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::RestApi", {
  }))
});

test('Lambda Function Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new Gateway.ApigatewayStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "helloworld.handler",
    "Runtime": "nodejs12.x"
  }))
});
