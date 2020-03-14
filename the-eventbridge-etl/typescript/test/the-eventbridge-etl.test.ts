import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeEtl = require('../lib/the-eventbridge-etl-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheEventbridgeEtl.TheEventbridgeEtlStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
