#!/usr/bin/env python3

from aws_cdk import core

from the_scheduled_lambda.the_scheduled_lambda_stack import TheScheduledLambdaStack


app = core.App()
TheScheduledLambdaStack(app, "the-scheduled-lambda")

app.synth()
