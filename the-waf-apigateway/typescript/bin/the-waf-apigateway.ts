#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheWafApigatewayStack } from '../lib/the-waf-apigateway-stack';

const app = new cdk.App();
new TheWafApigatewayStack(app, 'TheWafApigatewayStack');
