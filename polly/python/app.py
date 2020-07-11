#!/usr/bin/env python3

from aws_cdk import core

from polly.polly_stack import PollyStack


app = core.App()
PollyStack(app, "polly")

app.synth()
