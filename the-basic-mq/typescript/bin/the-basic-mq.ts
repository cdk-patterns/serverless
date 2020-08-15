#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheBasicMQStack } from '../lib/the-basic-mq-stack';

const app = new cdk.App();
new TheBasicMQStack(app, 'TheBasicMQStack');