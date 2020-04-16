#!/usr/bin/env python3

from aws_cdk import core

from the_saga_stepfunction.the_saga_stepfunction_stack import TheSagaStepfunctionStack


app = core.App()
TheSagaStepfunctionStack(app, "the-saga-stepfunction")

app.synth()
