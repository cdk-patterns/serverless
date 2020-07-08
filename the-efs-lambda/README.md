# The EFS Lambda Pattern

This is a pattern that attaches an EFS file system to your lambda function to give it expandable, persistent storage. Having this level of storage in a Lambda Function opens the door to many new possibilities. Multiple functions can even use the same file system.

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| AWS Docs | [Using Amazon EFS with Lambda](https://docs.aws.amazon.com/lambda/latest/dg/services-efs.html) |
| AWS Docs | [Configuring file system access for Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem.html)
| James Beswick | [Using Amazon EFS for AWS Lambda in your serverless applications](https://aws.amazon.com/blogs/compute/using-amazon-efs-for-aws-lambda-in-your-serverless-applications/) |
| Danilo Poccia | [A Shared File System for Your Lambda Functions](https://aws.amazon.com/blogs/aws/new-a-shared-file-system-for-your-lambda-functions/) |
| Yan Cui | [Unlocking New Serverless Use Caes With EFS and Lambda](https://lumigo.io/blog/unlocking-more-serverless-use-cases-with-efs-and-lambda/) |


## What's Included In This Pattern?
This pattern covers the first half of Danilo Poccia's awesome [blog post](https://aws.amazon.com/blogs/aws/new-a-shared-file-system-for-your-lambda-functions/). After deployment you will have an API Gateway HTTP API where any url you hit gets directed to a Lambda Function.

This Lambda Function is acting as a shared message broker. It allows you to send messages to it which it stores in EFS, then you can retrieve all messages to read them or delete all messages after you have finished reading.

The Lambda Function will behave differently based on the RESTful verb you use:

- GET - Retrieve messages
- POST - Send a message
- DELETE - Deletes all stored messages
