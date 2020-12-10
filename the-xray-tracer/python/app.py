#!/usr/bin/env python3
import subprocess
from aws_cdk import core

from the_xray_tracer.the_xray_tracer_stack import TheXrayTracerStack
from the_xray_tracer.the_http_flow_stack import TheHttpFlowStack
from the_xray_tracer.the_dynamo_flow_stack import TheDynamoFlowStack
from the_xray_tracer.the_sns_flow_stack import TheSnsFlowStack
from the_xray_tracer.the_sqs_flow_stack import TheSqsFlowStack

# install node dependencies for lambdas
subprocess.check_call("npm i".split(), cwd="lambda_fns", stdout=subprocess.DEVNULL)

app = core.App()
xray_tracer = TheXrayTracerStack(app, "the-xray-tracer")
http_flow = TheHttpFlowStack(app, 'the-http-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)
dynamo_flow = TheDynamoFlowStack(app, 'the-dynamo-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)
sns_flow = TheSnsFlowStack(app, 'the-sns-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)
sqs_flow = TheSqsFlowStack(app, 'the-sqs-flow-stack', sns_topic_arn=xray_tracer.sns_topic_arn)

http_flow.add_dependency(xray_tracer)
dynamo_flow.add_dependency(xray_tracer)
sns_flow.add_dependency(xray_tracer)
sqs_flow.add_dependency(xray_tracer)

app.synth()
