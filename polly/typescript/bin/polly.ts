#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { PollyStack } from '../lib/polly-stack';

const app = new cdk.App();
new PollyStack(app, 'PollyStack');
