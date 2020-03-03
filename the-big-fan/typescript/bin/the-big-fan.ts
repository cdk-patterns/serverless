#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheBigFanStack } from '../lib/the-big-fan-stack';

const app = new cdk.App();
new TheBigFanStack(app, 'TheBigFanStack');
