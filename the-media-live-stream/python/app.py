#!/usr/bin/env python3

from aws_cdk import core

from the_media_live_stream.the_media_live_stream_stack import TheMediaLiveStreamStack
from the_media_live_stream.the_media_live_stream_website import TheMediaLiveStreamWebsiteStack


app = core.App()
medialivestream = TheMediaLiveStreamStack(app, "the-media-live-stream")
medialivewebsite = TheMediaLiveStreamWebsiteStack(app, "the-media-live-stream-website").add_dependency(medialivestream)

app.synth()
