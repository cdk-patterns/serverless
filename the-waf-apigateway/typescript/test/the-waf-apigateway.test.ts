import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as WAF from '../lib/the-waf-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new WAF.TheWafStack(app, 'MyTestStack', {
      gatewayARN: '12345'
    });
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
