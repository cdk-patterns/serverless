import aws_cdk as core
import aws_cdk.assertions as assertions

from s3_angular_website.s3_angular_website_stack import S3AngularWebsiteStack

# example tests. To run these tests, uncomment this file along with the example
# resource in s3_angular_website/s3_angular_website_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = S3AngularWebsiteStack(app, "s3-angular-website")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
