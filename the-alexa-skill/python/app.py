#!/usr/bin/env python3

from aws_cdk import core

from the_alexa_skill.the_alexa_skill_stack import TheAlexaSkillStack


app = core.App()
TheAlexaSkillStack(app, "the-alexa-skill")

app.synth()
