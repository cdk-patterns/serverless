#!/usr/bin/env python3

from aws_cdk import core

from the_eventbridge_etl.the_eventbridge_etl_stack import TheEventbridgeEtlStack


app = core.App()
TheEventbridgeEtlStack(app, "the-eventbridge-etl")

app.synth()
