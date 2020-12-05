#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheScheduledLambdaStack } from '../lib/the-scheduled-lambda-stack';

const app = new cdk.App();
new TheScheduledLambdaStack(app, 'TheScheduledLambdaStack');