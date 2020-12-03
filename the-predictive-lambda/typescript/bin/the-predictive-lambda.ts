#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { ThePredictiveLambdaStack } from '../lib/the-predictive-lambda-stack';

const app = new cdk.App();
new ThePredictiveLambdaStack(app, 'ThePredictiveLambdaStack');
