#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheEventbridgeAtmStack } from '../lib/the-eventbridge-atm-stack';

const app = new cdk.App();
new TheEventbridgeAtmStack(app, 'TheEventbridgeAtmStack');
