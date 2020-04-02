#!/usr/bin/env python3

from aws_cdk import core

from the_lambda_trilogy.the_lambda_lith_stack import TheLambdalithStack
from the_lambda_trilogy.the_fat_lambda_stack import TheFatLambdaStack
from the_single_purpose_function_stack import TheSinglePurposeFunctionStack


app = core.App()
TheLambdalithStack(app, "the-lambda-lith-stack")
TheFatLambdaStack(app, "the-fat-lambda-stack")
TheSinglePurposeFunctionStack(app, "the-single-purpose-function-stack")

app.synth()
