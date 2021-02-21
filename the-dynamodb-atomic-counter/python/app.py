#!/usr/bin/env python3

from aws_cdk import core

from the_dynamodb_atomic_counter.the_dynamodb_atomic_counter_stack import TheDynamodbAtomicCounterStack


app = core.App()
TheDynamodbAtomicCounterStack(app, "the-dynamodb-atomic-counter")

app.synth()
