#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { TheAlexaSkillStack } from '../lib/the-alexa-skill-stack';
import { TheAssetStack } from '../lib/the-asset-stack';

const app = new cdk.App();
const assetStack = new TheAssetStack(app, 'TheAssetStack');

const alexaStack = new TheAlexaSkillStack(app, 'TheAlexaSkillStack', {
    assetBucketARN: assetStack.bucketARN,
    assetBucketName: assetStack.bucketName,
    assetObjectKey: assetStack.objectKey
});

alexaStack.addDependency(assetStack, 'Assets must be uploaded');
