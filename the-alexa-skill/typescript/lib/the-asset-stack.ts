import * as cdk from '@aws-cdk/core';

import s3 = require('@aws-cdk/aws-s3');
const alexaAssets = '../skill'
import * as S3Deployment from '@aws-cdk/aws-s3-deployment'

export class TheAssetStack extends cdk.Stack {
    public bucketARN: string;
    public bucketName: string;

  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //Assets Bucket
    const bucket = new s3.Bucket(this, 'alexaAssets',{
    });
    //Upload files to S3
    const fileUpload = new S3Deployment.BucketDeployment(this, 'Deployment', {
      sources: [S3Deployment.Source.asset(alexaAssets)],
      destinationBucket: bucket
    })
    this.bucketARN = bucket.bucketArn;
    this.bucketName = bucket.bucketName;
  }
}
