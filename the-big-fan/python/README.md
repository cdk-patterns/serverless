
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

## Useful CDK Commands

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
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
