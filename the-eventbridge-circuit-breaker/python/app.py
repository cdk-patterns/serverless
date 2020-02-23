#!/usr/bin/env python3

from aws_cdk import core

from the_eventbridge_circuit_breaker.the_eventbridge_circuit_breaker_stack import TheEventbridgeCircuitBreakerStack


app = core.App()
TheEventbridgeCircuitBreakerStack(app, "the-eventbridge-circuit-breaker")

app.synth()
