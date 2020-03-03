# The Big Fan

![architecture](../img/the-big-fan-arch.png)

This is an example cdk stack to deploy "The Big Fan" from Heitor Lessa as seen in these [re:Invent slides](https://d1.awsstatic.com/events/reinvent/2019/REPEAT_3_Serverless_architectural_patterns_and_best_practices_ARC307-R3.pdf) or this [Youtube Recording](https://www.youtube.com/watch?v=9IYpGTS7Jy0) from [Heitor Lessa](https://twitter.com/heitor_lessa).

In this example we have an API Gateway with a "/SendEvent" endpoint that takes a POST request with a JSON payload. The payload formats are beneath.

When API Gateway receives the json it automatically through VTL routes it to an SNS Topic, this Topic then has two subscribers which are SQS Queues. The difference between the two subscribers is that one looks for a property of "status":"created" in the json and the other subscriber looks for any message that doesn't have that property. Each queue has a lambda that subscribes to it and prints whatever message it recieves to cloudwatch.

### JSON Payload Format

To send to the first lambda
`{ "message": "hello", "status": "created" }`

To send to the second lambda
`{ "message": "hello", "status": "not created" }`

### Postman Example
![postman](../img/postman.png)

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`  deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
