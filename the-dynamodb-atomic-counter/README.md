# The DynamoDB Atomic Counter

![the dynamodb atomic counter](img/stack.png)

This is a pattern that implements an Atomic counter using only ApiGateway and DynamoDB. In many cases, we can use UUID to identify the key, but there are situations where we need an incremental and unique number due to design. In this case, we must ensure that the number will be unique and won't be repeated, so this stack can solve this. 

A special thanks to Vikas Solegaonkar for sharing this link [Simple Atomic Counter with DynamoDB and API Gateway](https://itnext.io/simple-atomic-counter-with-dynamodb-and-api-gateway-e72115c209ff)

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| AWS Docs | [Increment an Atomic Counter](https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/GettingStarted.NodeJs.03.html#GettingStarted.NodeJs.03.04) |
| A Cloud Guru | [DynamoDB Atomic Counters](https://acloudguru.com/blog/engineering/dynamodb-atomic-counters) |



# Available Versions

* [TypeScript](typescript)
* [Python](python)
* [Csharp](csharp)

## What's Included In This Pattern?
This pattern covers the first half of Danilo Poccia's awesome [blog post](https://aws.amazon.com/blogs/aws/new-a-shared-file-system-for-your-lambda-functions/). After deployment you will have an API Gateway HTTP API where any url you hit gets directed to a Lambda Function that is integrated with EFS.

### VPC
A VPC is bundled in this pattern because EFS requires it, this is using the default settings from CDK so if you want to put this in production you will have to review / refine this

### EFS FileSystem
A FileSystem is included in the above VPC with a removal policy of destroy. In a production system you probably would want to retain your storage on stack deletion.

POSIX permissions are also setup for this File System

### Lambda Function
A simple Python lambda function that interacts with the file system - storing, retrieving and deleting messages

### API Gateway HTTP API
This is configured with the Lambda Function as the default handler for any url you hit.

## How Do I Test This Pattern?

Our deployed Lambda Function is acting as a shared message broker. It allows you to send messages to it which it stores in EFS, then you can retrieve all messages to read them or delete all messages after you have finished reading.

The Lambda Function will behave differently based on the RESTful verb you use:

- GET - Retrieve messages
- POST - Send a message (whatever you send in the body is the message)
- DELETE - Deletes all stored messages

The URL for the HTTP API to use these commands will be printed in the CloudFormation stack output after you deploy.

Note - After deployment you may need to wait 60-90 seconds before the implementation works as expected. There are a lot of network configurations happening so you need to wait on propagation