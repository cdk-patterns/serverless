# The Simple Webservice

This is an example CDK stack to deploy The Simple Webservice stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#simplewebservice

Most of this code was borrowed from https://www.cdkworkshop.com

This is the most basic of implementations and would have to be hardened before production use. e.g. cognito added to the API Gateway

![Architecture](img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`  deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
