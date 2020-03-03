#!/usr/bin/env python3

from aws_cdk import core

from the_big_fan.the_big_fan_stack import TheBigFanStack


app = core.App()
TheBigFanStack(app, "the-big-fan")

app.synth()
