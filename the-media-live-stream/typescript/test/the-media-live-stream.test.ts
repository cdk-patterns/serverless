import { expect as expectCDK, matchTemplate, MatchStyle, haveResourceLike } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheMediaLiveStream from '../lib/the-media-live-stream-stack';

test('MediaPackage Channel exists', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheMediaLiveStream.TheMediaLiveStreamStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::MediaPackage::Channel"));
});

test('MediaPackage Endpoint exists', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheMediaLiveStream.TheMediaLiveStreamStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::MediaPackage::OriginEndpoint"));
});

test('MediaLive SecurityGroup exists', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheMediaLiveStream.TheMediaLiveStreamStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::MediaLive::InputSecurityGroup"));
});

test('MediaLive Input exists', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheMediaLiveStream.TheMediaLiveStreamStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::MediaLive::Input"));
});

test('MediaLive Channel exists', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheMediaLiveStream.TheMediaLiveStreamStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::MediaLive::Channel"));
});

test('MediaLive Role exists', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheMediaLiveStream.TheMediaLiveStreamStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::IAM::Role", {
    "RoleName": "medialive_role"
  }));
});