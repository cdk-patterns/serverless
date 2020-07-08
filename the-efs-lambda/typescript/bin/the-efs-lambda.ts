#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheEfsLambdaStack } from '../lib/the-efs-lambda-stack';

const app = new cdk.App();
new TheEfsLambdaStack(app, 'TheEfsLambdaStack');
