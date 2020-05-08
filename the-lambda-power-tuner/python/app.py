#!/usr/bin/env python3

from aws_cdk import core

from the_lambda_power_tuner.the_lambda_power_tuner_stack import TheLambdaPowerTunerStack


app = core.App()
TheLambdaPowerTunerStack(app, "the-lambda-power-tuner")

app.synth()
