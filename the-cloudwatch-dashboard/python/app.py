#!/usr/bin/env python3

from aws_cdk import core

from the_cloudwatch_dashboard.the_cloudwatch_dashboard_stack import TheCloudwatchDashboardStack


app = core.App()
TheCloudwatchDashboardStack(app, "the-cloudwatch-dashboard")

app.synth()
