#!/usr/bin/env python3

from aws_cdk import core

from s3_react_website.s3_react_website_stack import S3ReactWebsiteStack


app = core.App()
S3ReactWebsiteStack(app, "s3-react-website")

app.synth()
