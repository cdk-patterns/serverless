import * as cdk from '@aws-cdk/core';
import assets = require('@aws-cdk/aws-s3-assets');
const path = require('path');
import s3 = require('@aws-cdk/aws-s3');
const alexaAssets = '../../skill'
export class TheAssetStack extends cdk.Stack {
    public bucketARN: string;
    public bucketName: string;
    public objectKey: string;

  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const asset = new assets.Asset(this, 'SampleAsset', {
      path: path.join(__dirname, alexaAssets),
    })

    this.bucketARN = `arn:aws:s3:::${asset.s3BucketName}`;
    this.bucketName = asset.s3BucketName;
    this.objectKey = asset.s3ObjectKey;
  }
}
