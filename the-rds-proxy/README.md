# The RDS Proxy

This is a project that has been configured with a MySQL RDS DB, an RDS Proxy, a Lambda Function to run queries and an API Gateway HTTP API to trigger the lambda function.

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| AWS RDS Proxy | [RDS Proxy Site](https://aws.amazon.com/rds/proxy/) |
| AWS User Guide | [Managing Connections with Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
| Ben Smith   | [Introducing the serverless LAMP stack - part 2](https://aws.amazon.com/blogs/compute/introducing-the-serverless-lamp-stack-part-2-relational-databases/)  |
| George Mao | [Using Amazon RDS Proxy with AWS Lambda](https://aws.amazon.com/blogs/compute/using-amazon-rds-proxy-with-aws-lambda/)
| SSL Cert for RDS MySQL | [AmazonRootCA1.pem](https://www.amazontrust.com/repository/AmazonRootCA1.pem) |
| AWS User Guide | [Manual Steps for RDS Creation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html) |
| AWS User Guide | [MySQL in Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html) |
| Node MySQL Lib | [MySQL](https://github.com/mysqljs/mysql) |
| AWS Docs | [Secrets Manager JS SDK Docs](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SecretsManager.html) |
| AWS User Guide | [Creating and Retrieving a Secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/tutorials_basic.html) |



This is a blank project for TypeScript development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
