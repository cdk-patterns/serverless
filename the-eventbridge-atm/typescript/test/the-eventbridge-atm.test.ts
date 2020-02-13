import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheEventbridgeAtm = require('../lib/the-eventbridge-atm-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheEventbridgeAtm.TheEventbridgeAtmStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
