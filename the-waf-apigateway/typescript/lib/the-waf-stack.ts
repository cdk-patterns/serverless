import * as cdk from '@aws-cdk/core';
import waf = require('@aws-cdk/aws-wafv2');

export interface WafStackProps extends cdk.StackProps{
  gatewayARN: string
}

export class TheWafStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: WafStackProps) {
    super(scope, id, props);

    /**
     * Setup WAF Rules
     */

    let wafRules:Array<waf.CfnWebACL.RuleProperty>  = [];

    // 1 AWS Managed Rules
    let awsManagedRules:waf.CfnWebACL.RuleProperty  = {
      name: 'AWS-AWSManagedRulesCommonRuleSet',
      priority: 1,
      overrideAction: {none: {}},
      statement: {
        managedRuleGroupStatement: {
          name: 'AWSManagedRulesCommonRuleSet',
          vendorName: 'AWS',
          excludedRules: [{name: 'SizeRestrictions_BODY'}]
        }
      },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'awsCommonRules',
        sampledRequestsEnabled: true
      }
    };

    wafRules.push(awsManagedRules);

    // 2 AWS AnonIPAddress
    let awsAnonIPList:waf.CfnWebACL.RuleProperty  = {
      name: 'awsAnonymousIP',
      priority: 2,
      overrideAction: {none: {}},
      statement: {
        managedRuleGroupStatement: {
          name: 'AWSManagedRulesAnonymousIpList',
          vendorName: 'AWS',
          excludedRules: []
        }
      },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'awsAnonymous',
        sampledRequestsEnabled: true
      }
    };

    wafRules.push(awsAnonIPList);

    // 3 AWS ip reputation List
    let awsIPRepList:waf.CfnWebACL.RuleProperty  = {
      name: 'awsIPReputation',
      priority: 3,
      overrideAction: {none: {}},
      statement: {
        managedRuleGroupStatement: {
          name: 'AWSManagedRulesAmazonIpReputationList',
          vendorName: 'AWS',
          excludedRules: []
        }
      },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'awsReputation',
        sampledRequestsEnabled: true
      }
    };

    wafRules.push(awsIPRepList);

    // 4 GeoBlock NZ from accessing gateway
    let geoBlockRule:waf.CfnWebACL.RuleProperty  = {
      name: 'geoblockRule',
      priority: 4,
      action: {block: {}},
      statement: {
        geoMatchStatement: {
          countryCodes: ['NZ']
        }
      },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'geoBlock',
        sampledRequestsEnabled: true
      }
    };

    wafRules.push(geoBlockRule);

    /**
     * Create and Associate ACL with Gateway
     */

    // Create our Web ACL
    let webACL = new waf.CfnWebACL(this, 'WebACL', {
      defaultAction: {
        allow: {}
      },
      scope: 'REGIONAL',
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'webACL',
        sampledRequestsEnabled: true
      },
      rules: wafRules
    });

    // Associate with our gateway
    new waf.CfnWebACLAssociation(this, 'WebACLAssociation', {
      webAclArn: webACL.attrArn,
      resourceArn: props.gatewayARN
    })
  }
}
