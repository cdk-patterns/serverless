#!/usr/bin/env python3

from aws_cdk import core

from the_rds_proxy.the_rds_proxy_stack import TheRdsProxyStack


app = core.App()
TheRdsProxyStack(app, "the-rds-proxy")

app.synth()
