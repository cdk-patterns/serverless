# The Simple Webservice

This is an example CDK stack to deploy The Simple Webservice stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#simplewebservice

This is the most basic of implementations and would have to be hardened before production use. e.g. cognito added to the API Gateway

![Architecture](img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

#### Requirements
- Java JDK 11
- node.js

As a packaging and dependency management tool Maven is used for Lambda and CDK.
Maven doesn't have to be installed since you can use the [Maven Wrapper](https://github.com/takari/maven-wrapper).
The Maven Wrapper can be run by using the `./mvnw` (Unix based) or `./mvnw.cmd` (Windows based). 

**Example:** 
```
./mvnw clean package
```
You can compile & package from this folder, to deploy go to the **cdk** subfolder.

## Useful commands

 * `./mvnw package`     compiles and packages the source code for both Lambda and CDK modules
 * `./mvnw test`        perform the unit tests for both Lambda and CDK modules
 * `cdk diff`           compare deployed stack with current state
 * `cdk synth`          emits the synthesized CloudFormation template
