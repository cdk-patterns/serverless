# The Simple Webservice

This is an example CDK stack to deploy The Simple Webservice stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#simplewebservice

Most of this code was borrowed from https://www.cdkworkshop.com

This is the most basic of implementations and would have to be hardened before production use. e.g. cognito added to the API Gateway

![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-simple-webservice/img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

## Available Versions

 * [TypeScript](typescript/README.md)
 * [Python](python/README.md)

