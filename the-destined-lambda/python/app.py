#!/usr/bin/env python3

from aws_cdk import core

from the_destined_lambda.the_destined_lambda_stack import TheDestinedLambdaStack


app = core.App()
TheDestinedLambdaStack(app, "the-destined-lambda")

app.synth()
