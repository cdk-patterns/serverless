#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheLambdalithStack } from '../lib/the-lambda-lith-stack';
import { TheFatLambdaStack } from '../lib/the-fat-lambda-stack';
import { TheSinglePurposeFunctionStack } from '../lib/the-single-purpose-function-stack';

const app = new cdk.App();
new TheLambdalithStack(app, 'TheLambdaLithStack');
new TheFatLambdaStack(app, 'TheFatLambdaStack');
new TheSinglePurposeFunctionStack(app, 'TheSinglePurposeFunctionStack');
