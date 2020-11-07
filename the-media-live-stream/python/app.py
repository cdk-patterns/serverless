#!/usr/bin/env python3

from aws_cdk import core

from the_media_live_stream.the_media_live_stream_stack import TheMediaLiveStreamStack


app = core.App()
TheMediaLiveStreamStack(app, "the-media-live-stream")

app.synth()
