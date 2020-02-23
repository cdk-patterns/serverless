#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheEventbridgeCircuitBreakerStack } from '../lib/the-eventbridge-circuit-breaker-stack';

const app = new cdk.App();
new TheEventbridgeCircuitBreakerStack(app, 'TheEventbridgeCircuitBreakerStack');
