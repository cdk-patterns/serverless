#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheEventbridgeEtlStack } from '../lib/the-eventbridge-etl-stack';

const app = new cdk.App();
new TheEventbridgeEtlStack(app, 'TheEventbridgeEtlStack');
