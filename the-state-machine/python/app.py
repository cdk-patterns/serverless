#!/usr/bin/env python3

from aws_cdk import core

from the_state_machine.the_state_machine_stack import TheStateMachineStack


app = core.App()
TheStateMachineStack(app, "the-state-machine")

app.synth()
