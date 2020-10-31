#!/usr/bin/env python3

from aws_cdk import core

from helloworld.top import Top
from helloworld.apigateway import Apigateway          
from helloworld.waf import Waf

app = core.App()

top_stack = Top(app, "thewafapigateway")
api_stack = Apigateway(top_stack, 'apigateway')
waf_stack = Waf(top_stack, 'wafstack', target_arn = api_stack.resource_arn)
    

app.synth()


