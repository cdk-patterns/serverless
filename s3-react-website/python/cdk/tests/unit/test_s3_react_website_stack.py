import aws_cdk as core
import aws_cdk.assertions as assertions

from s3_react_website.s3_react_website_stack import S3ReactWebsiteStack

# example tests. To run these tests, uncomment this file along with the example
# resource in s3_react_website/s3_react_website_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = S3ReactWebsiteStack(app, "s3-react-website")
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
