import { Match, Template } from "aws-cdk-lib/assertions";
import cdk = require('aws-cdk-lib');
import { CdkStack } from '../lib/cdk-stack';


test('Basic Site Setup', () => {
  //GIVEN
  const app = new cdk.App();

  //WHEN
  let stack = new CdkStack(app, 'CdkArticleStack');
  
  const template = Template.fromStack(stack);
  
  // THEN
  template.hasResourceProperties('AWS::S3::Bucket', 
    Match.objectLike({
      WebsiteConfiguration: {
        IndexDocument: 'index.html',
      },
    }));
  
  template.hasResource('Custom::CDKBucketDeployment', {});
  
  template.hasResourceProperties('AWS::S3::BucketPolicy', 
    Match.objectLike({
      PolicyDocument: {
        Statement: [
          Match.objectLike({
            Action: 's3:GetObject',
            Effect: 'Allow',
            Principal: {
              "AWS": "*"
            },
          })],
      },
    }));
});