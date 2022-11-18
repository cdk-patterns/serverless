#!/usr/bin/env python3

from aws_cdk import App

from the_lambda_power_tuner.the_lambda_power_tuner_stack import TheLambdaPowerTunerStack


app = App()
TheLambdaPowerTunerStack(app, "the-lambda-power-tuner")

app.synth()
