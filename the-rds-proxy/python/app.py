#!/usr/bin/env python3
import subprocess
from aws_cdk import core

from the_rds_proxy.the_rds_proxy_stack import TheRdsProxyStack

# install node dependencies for lambdas
subprocess.check_call("npm i".split(), cwd="lambda_fns/rds", stdout=subprocess.DEVNULL)

app = core.App()
TheRdsProxyStack(app, "the-rds-proxy", env=core.Environment(region="us-east-1"))

app.synth()
