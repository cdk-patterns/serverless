import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheLambdaPowerTuner from '../lib/the-lambda-power-tuner-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheLambdaPowerTuner.TheLambdaPowerTunerStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
