#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { AwsCdkServerlessCrudStack } from '../lib/aws_cdk_serverless_crud-stack';

const app = new cdk.App();
new AwsCdkServerlessCrudStack(app, 'AwsCdkServerlessCrudStack');
