# The RDS Proxy

This is a project that has been configured with a MySQL RDS DB, an RDS Proxy, a Lambda Function to run queries and an API Gateway HTTP API to trigger the lambda function.

A VPC is included in this project that has the RDS Subnets configured and custom security groups for allowing communication between Lambda -> Proxy -> MySQL.

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

# Available Versions

* [TypeScript](typescript)
* [Python](python)

![AWS Well Architected](img/well_architected.png)

The [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) Framework helps you understand the pros and cons of
decisions you make while building systems on AWS. By using the Framework, you will learn architectural best practices for designing and operating reliable, secure, efficient, and cost-effective systems in the cloud. It provides a way for you to consistently measure your architectures against best practices and identify areas for improvement.

We believe that having well-architected systems greatly increases the likelihood of business success.

[Serverless Lens Whitepaper](https://d1.awsstatic.com/whitepapers/architecture/AWS-Serverless-Applications-Lens.pdf) <br />
[Well Architected Whitepaper](http://d0.awsstatic.com/whitepapers/architecture/AWS_Well-Architected_Framework.pdf)