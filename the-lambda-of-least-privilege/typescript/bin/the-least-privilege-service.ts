#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheLeastPrivilegeServiceStack } from '../lib/the-least-privilege-service-stack';

const app = new cdk.App();
new TheLeastPrivilegeServiceStack(app, 'TheSimpleWebserviceStack');
