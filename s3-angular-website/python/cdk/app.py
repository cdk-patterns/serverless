#!/usr/bin/env python3

from aws_cdk import core

from s3_angular_website.s3_angular_website_stack import S3AngularWebsiteStack


app = core.App()
S3AngularWebsiteStack(app, "s3-angular-website")

app.synth()
