#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheXrayTracerStack } from '../lib/the-xray-tracer-stack';

const app = new cdk.App();
new TheXrayTracerStack(app, 'TheXrayTracerStack');
