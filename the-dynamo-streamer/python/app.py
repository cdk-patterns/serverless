#!/usr/bin/env python3

from aws_cdk import core

from the_dynamo_streamer.the_dynamo_streamer_stack import TheDynamoStreamerStack


app = core.App()
TheDynamoStreamerStack(app, "the-dynamo-streamer")

app.synth()
