#!/usr/bin/env python3

from aws_cdk import core

from the_efs_lambda.the_efs_lambda_stack import TheEfsLambdaStack


app = core.App()
TheEfsLambdaStack(app, "the-efs-lambda")

app.synth()
