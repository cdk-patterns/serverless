#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { TheAlexaSkillStack } from '../lib/the-alexa-skill-stack';

const app = new cdk.App();

const alexaStack = new TheAlexaSkillStack(app, 'TheAlexaSkillStack');

