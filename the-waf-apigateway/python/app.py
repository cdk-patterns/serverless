#!/usr/bin/env python3

from aws_cdk import core

from the_waf_apigateway.top import Top
from the_waf_apigateway.apigateway import Apigateway
from the_waf_apigateway.waf import Waf

app = core.App()

top_stack = Top(app, "the-waf-apigateway")
api_stack = Apigateway(top_stack, 'apigateway')
waf_stack = Waf(top_stack, 'wafstack', target_arn = api_stack.resource_arn)
    

app.synth()


