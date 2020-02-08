#!/usr/bin/env python3

from aws_cdk import core

from the_scalable_webhook.the_scalable_webhook_stack import TheScalableWebhookStack


app = core.App()
TheScalableWebhookStack(app, "the-scalable-webhook")

app.synth()
