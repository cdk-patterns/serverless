import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheXrayTracer from '../lib/the-xray-tracer-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheXrayTracer.TheXrayTracerStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
