#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheCloudwatchDashboardStack } from '../lib/the-cloudwatch-dashboard-stack';

const app = new cdk.App();
new TheCloudwatchDashboardStack(app, 'TheCloudwatchDashboardStack');
