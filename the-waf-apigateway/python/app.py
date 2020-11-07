#!/usr/bin/env python3

from aws_cdk import core

from thewafapigateway.top import Top
from thewafapigateway.apigateway import Apigateway          
from thewafapigateway.waf import Waf

app = core.App()

top_stack = Top(app, "thewafapigateway")
api_stack = Apigateway(top_stack, 'apigateway')
waf_stack = Waf(top_stack, 'wafstack', target_arn = api_stack.resource_arn)
    

app.synth()


