# The Dynamo Streamer 

The Dynamo Streamer pattern was taken from from this [Tweet](https://twitter.com/edjgeek/status/1220227872511496192?s=20) by [Eric Johnson](https://twitter.com/edjgeek). He later went on to use this pattern to build a lambdaless, serverless url shortener. 

- [Github Repo](https://github.com/aws-samples/amazon-api-gateway-url-shortener)
- [Blog Post](https://aws.amazon.com/blogs/compute/building-a-serverless-url-shortener-app-without-lambda-part-1/)

This is a variation on [The Simple Webservice](../the-simple-webservice/README.md) pattern from Jeremy Daly only instead of a lambda being connected to the apigateway, the dynamodb is connected directly and the api gateway uses templates to transform the incoming message to insert the data. A lambda then listens for events coming from dynamodb streams and can be used to do data transforms after insertion meaning if an error occurs you lose no data.

"When thinking about #Serverless architectures, consider how much of your processing can happen AFTER the data is saved. Thinking asynchronously can lead to greater resiliency and often, less code."

![Architecture](https://raw.githubusercontent.com/nideveloper/serverless/master/the-dynamo-streamer/img/arch.jpg)

## How To Test Pattern

After deployment you will have an API Gateway with one endpint (/InsertItem) that takes an application/json payload via POST. It will insert the contents of the message field into DynamoDB where that new event will be streamed to a Lambda that will print the contents to the console. To see the full flow you need to look in the AWS Console and look in DynamoDB and the Lambda Cloudwatch logs

### JSON Payload Format
`{ "message": "hello" }`

### Example Request
![Postman](https://raw.githubusercontent.com/nideveloper/serverless/master/the-dynamo-streamer/img/request.png)

# CDK Useful Commands

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
