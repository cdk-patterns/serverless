#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheSagaStepfunctionStack } from '../lib/the-saga-stepfunction-stack';
import { TheSagaStepfunctionSingleTableStack } from '../lib/the-saga-stepfunction-single-table-stack';

const app = new cdk.App();
new TheSagaStepfunctionStack(app, 'TheSagaStepfunctionStack');
new TheSagaStepfunctionSingleTableStack(app, 'TheSagaStepfunctionSingleTableStack');
