#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheMediaLiveStreamStack } from '../lib/the-media-live-stream-stack';
import { TheMediaLiveStreamWebsiteStack } from '../lib/the-media-live-stream-website';

const app = new cdk.App();
var mediaChannel = new TheMediaLiveStreamStack(app, 'TheMediaLiveStreamStack');
new TheMediaLiveStreamWebsiteStack(app, 'TheMediaLiveStreamWebsiteStack').addDependency(mediaChannel);
