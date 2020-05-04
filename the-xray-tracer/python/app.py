#!/usr/bin/env python3

from aws_cdk import core

from the_xray_tracer.the_xray_tracer_stack import TheXrayTracerStack


app = core.App()
TheXrayTracerStack(app, "the-xray-tracer")

app.synth()
