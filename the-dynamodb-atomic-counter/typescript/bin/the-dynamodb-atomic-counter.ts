#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheDynamodbAtomicCounterStack } from '../lib/the-dynamodb-atomic-counter-stack';

const app = new cdk.App();
new TheDynamodbAtomicCounterStack(app, 'TheDynamodbAtomicCounterStack');
