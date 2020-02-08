#!/usr/bin/env python3

from aws_cdk import core

from the_simple_webservice.the_simple_webservice_stack import TheSimpleWebserviceStack


app = core.App()
TheSimpleWebserviceStack(app, "the-simple-webservice")

app.synth()
