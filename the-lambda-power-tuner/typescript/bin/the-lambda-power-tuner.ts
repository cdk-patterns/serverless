#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheLambdaPowerTunerStack } from '../lib/the-lambda-power-tuner-stack';

const app = new cdk.App();
new TheLambdaPowerTunerStack(app, 'TheLambdaPowerTunerStack');
