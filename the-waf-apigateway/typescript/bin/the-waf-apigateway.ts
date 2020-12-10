#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheWafStack } from '../lib/the-waf-stack';
import { ApigatewayStack } from '../lib/api-gateway-stack';

const app = new cdk.App();

const apiGatewayStack = new ApigatewayStack(app, 'APIGatewayStack')
const wafStack = new TheWafStack(app, 'TheWafStack', {
    gatewayARN: apiGatewayStack.apiGatewayARN
});

wafStack.addDependency(apiGatewayStack);