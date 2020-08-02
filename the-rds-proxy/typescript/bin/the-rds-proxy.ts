#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheRdsProxyStack } from '../lib/the-rds-proxy-stack';

const app = new cdk.App();
new TheRdsProxyStack(app, 'TheRdsProxyStack', {
    env: {region: "us-east-1"}
});
