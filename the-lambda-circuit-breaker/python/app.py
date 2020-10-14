#!/usr/bin/env python3

from aws_cdk import core

from the_lambda_circuit_breaker.the_lambda_circuit_breaker_stack import TheLambdaCircuitBreakerStack


app = core.App()
TheLambdaCircuitBreakerStack(app, "the-lambda-circuit-breaker")

app.synth()
