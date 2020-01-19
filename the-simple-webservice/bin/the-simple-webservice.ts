#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheSimpleWebserviceStack } from '../lib/the-simple-webservice-stack';

const app = new cdk.App();
new TheSimpleWebserviceStack(app, 'TheSimpleWebserviceStack');
