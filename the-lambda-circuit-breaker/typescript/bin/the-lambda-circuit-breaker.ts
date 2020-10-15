#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheLambdaCircuitBreakerStack } from '../lib/the-lambda-circuit-breaker-stack';

const app = new cdk.App();
new TheLambdaCircuitBreakerStack(app, 'TheLambdaCircuitBreakerStack');
