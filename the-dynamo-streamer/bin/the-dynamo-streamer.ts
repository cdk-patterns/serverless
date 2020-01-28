#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheDynamoStreamerStack } from '../lib/the-dynamo-streamer-stack';

const app = new cdk.App();
new TheDynamoStreamerStack(app, 'TheDynamoStreamerStack');
