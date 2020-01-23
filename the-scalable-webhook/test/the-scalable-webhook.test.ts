import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheScalableWebhook = require('../lib/the-scalable-webhook-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheScalableWebhook.TheScalableWebhookStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
