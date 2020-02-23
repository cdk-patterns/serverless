import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeCircuitBreaker = require('../lib/the-eventbridge-circuit-breaker-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheEventbridgeCircuitBreaker.TheEventbridgeCircuitBreakerStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
