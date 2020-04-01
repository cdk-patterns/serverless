#!/usr/bin/env python3

from aws_cdk import core

from the_lambda_trilogy.the_lambda_lith_stack import TheLambdalithStack


app = core.App()
TheLambdalithStack(app, "the-lambda-lith-stack")

app.synth()
