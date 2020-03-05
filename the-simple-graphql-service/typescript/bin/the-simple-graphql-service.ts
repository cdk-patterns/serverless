#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheSimpleGraphQLServiceStack } from '../lib/the-simple-graphql-service-stack';

const app = new cdk.App();
new TheSimpleGraphQLServiceStack(app, 'TheSimpleGraphqlServiceStack');
