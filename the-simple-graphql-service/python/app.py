#!/usr/bin/env python3

from aws_cdk import core

from the_simple_graphql_service.the_simple_graphql_service_stack import TheSimpleGraphqlServiceStack


app = core.App()
TheSimpleGraphqlServiceStack(app, "the-simple-graphql-service")

app.synth()
