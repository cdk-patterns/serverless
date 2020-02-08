#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheScalableWebhookStack } from '../lib/the-scalable-webhook-stack';

const app = new cdk.App();
new TheScalableWebhookStack(app, 'TheScalableWebhookStack');
