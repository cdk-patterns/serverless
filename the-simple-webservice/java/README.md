# The Simple Webservice

This is an example CDK stack to deploy The Simple Webservice stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#simplewebservice

This is the most basic of implementations and would have to be hardened before production use. e.g. cognito added to the API Gateway

![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-simple-webservice/img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

The only requirement is to have a JDK 11 (Java Development Kit) and AWS CDK installed.
You can compile & package from this folder, to deploy go to the **cdk** subfolder.

## Useful commands

From the root folder:
 * `./mvnw package`   compiles and packages the source code
 * `./mvnw test`      perform the unit tests
 
From the cdk subfolder folder: 
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
