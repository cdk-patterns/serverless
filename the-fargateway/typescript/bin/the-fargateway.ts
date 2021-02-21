#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheFargatewayStack } from '../lib/the-fargateway-stack';

const app = new cdk.App();
new TheFargatewayStack(app, 'TheFargatewayStack', {
    env: { region: "eu-west-1" }
});
