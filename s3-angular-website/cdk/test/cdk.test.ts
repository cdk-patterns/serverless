import { expect as expectCDK, haveResource, haveResourceLike } from '@aws-cdk/assert';
import cdk = require('@aws-cdk/core');
import { CdkStack } from '../lib/cdk-stack';


test('Basic Site Setup', () => {
  //GIVEN
  const app = new cdk.App();

  //WHEN
  let stack = new CdkStack(app, 'CdkArticleStack');
  
  // THEN
  expectCDK(stack).to(haveResource('AWS::S3::Bucket', {
    WebsiteConfiguration: {
      IndexDocument: 'index.html'
    }
  }));
  
  expectCDK(stack).to(haveResource('Custom::CDKBucketDeployment'));
  
  expectCDK(stack).to(haveResourceLike('AWS::S3::BucketPolicy',  {
          PolicyDocument: {
              Statement: [
                  {
                      "Action": "s3:GetObject",
                      "Effect": "Allow",
                      "Principal": "*"
                  }]
          }
  }));
});