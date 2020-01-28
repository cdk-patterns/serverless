# The Dynamo Streamer

This pattern was taken from from this [Tweet](https://twitter.com/edjgeek/status/1220227872511496192?s=20)

This is a variation on [The Simple Webservice](../the-simple-webservice/README.md) pattern only instead of a lambda being connected to the apigateway, the dynamodb is connected directly and the api gateway uses templates to transform the incoming message to insert the data. The lambda that listens for events coming from dynamo can be used to do data transforms after insertion meaning if an error occurs you lose no data.

"When thinking about #Serverless architectures, consider how much of your processing can happen AFTER the data is saved. Thinking asynchronously can lead to greater resiliency and often, less code."

![Architecture](https://raw.githubusercontent.com/nideveloper/serverless/master/the-dynamo-streamer/img/arch.jpg)

## How To Test Pattern

After deployment you will have an API Gateway with one endpint (/InsertItem) that takes an application/json payload via POST. It will insert the contents of the message field into DynamoDB where that new event will be streamed to a Lambda that will print the contents to the console. To see the full flow you need to look in the AWS Console and look in DynamoDB and the Lambda Cloudwatch logs

### JSON Payload Format
`{ "message": "hello" }`

### Example Request
![Postman](https://raw.githubusercontent.com/nideveloper/serverless/master/the-dynamo-streamer/img/request.png)

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
