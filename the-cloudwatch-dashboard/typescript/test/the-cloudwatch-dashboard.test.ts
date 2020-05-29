import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheCloudwatchDashboard from '../lib/the-cloudwatch-dashboard-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheCloudwatchDashboard.TheCloudwatchDashboardStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
