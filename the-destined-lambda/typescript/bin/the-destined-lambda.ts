#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheDestinedLambdaStack } from '../lib/the-destined-lambda-stack';

const app = new cdk.App();
new TheDestinedLambdaStack(app, 'TheDestinedLambdaStack');
