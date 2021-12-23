import aws_cdk as core
import aws_cdk.assertions as assertions

from s3_angular_website.s3_angular_website_stack import S3AngularWebsiteStack


def test_website_created():
    app = core.App()
    stack = S3AngularWebsiteStack(app, "s3-angular-website")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties('AWS::S3::Bucket',
                                     assertions.Match.object_like({
                                         "WebsiteConfiguration": {
                                             "IndexDocument": 'index.html',
                                         },
                                     }))

    template.has_resource('Custom::CDKBucketDeployment', {})

    template.has_resource_properties('AWS::S3::BucketPolicy',
                                     assertions.Match.object_like({
                                         "PolicyDocument": {
                                             "Statement": [
                                                 assertions.Match.object_like({
                                                     "Action": 's3:GetObject',
                                                     "Effect": 'Allow',
                                                     "Principal": {
                                                         "AWS": "*"
                                                     },
                                                 })],
                                         },
                                     }))
