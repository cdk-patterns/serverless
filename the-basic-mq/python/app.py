#!/usr/bin/env python3

from aws_cdk import core

from the_basic_mq.the_basic_mq_stack import TheBasicMQStack


app = core.App()
TheBasicMQStack(app, "TheBasicMQStack", env=core.Environment(region="us-east-1"))

app.synth()
