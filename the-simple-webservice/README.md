# The Simple Webservice

This is an example CDK stack to deploy The Simple Webservice stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#simplewebservice

An advanced version of this pattern was talked about by [Heitor Lessa](https://twitter.com/heitor_lessa) at re:Invent 2019 as The comfortable “REST”

* [Youtube Recording](https://www.youtube.com/watch?v=9IYpGTS7Jy0)
* [Static Slides](https://d1.awsstatic.com/events/reinvent/2019/REPEAT_3_Serverless_architectural_patterns_and_best_practices_ARC307-R3.pdf)

Most of this code was borrowed from https://cdkworkshop.com/.

This is the most basic of implementations and would have to be hardened before production use. e.g. cognito added to the API Gateway

![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-simple-webservice/img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

## Available Versions

 * [TypeScript](typescript/)
 * [Python](python/)
 * [C#](csharp/)
 * [Java](java/)