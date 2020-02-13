#!/usr/bin/env python3

from aws_cdk import core

from the_eventbridge_atm.the_eventbridge_atm_stack import TheEventbridgeAtmStack


app = core.App()
TheEventbridgeAtmStack(app, "the-eventbridge-atm")

app.synth()
