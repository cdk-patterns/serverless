# The Destined Lambda

This project combines [Lambda Destinations](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-destinations/) 
with [Amazon EventBridge](https://aws.amazon.com/eventbridge/) to show you that with EventBridge rules you can decouple 
your components in an event driven architecture and by combining it with lambda destinations you can strip out EventBridge 
specific code from your lambda functions themselves and decouple further.

An important point about Lambda Destinations is that they have to be executed asyncronously which is why the lambda is 
invoked via SNS in this pattern. To reduce custom code, I have integrated the SNS directly with API Gateway using 
[Apache VTL](https://velocity.apache.org/engine/1.7/vtl-reference.html).

## Architecture

![arch](img/arch.png)

### Architecture Notes

At time of writing there are 4 available destinations targets but I have chosen EventBridge as to be honest this is the 
most complicated and powerful of the 4:

![destinations](img/destinations.png)

The destined lambda sends some extra parameters in its response json. This is because we don't manually create the 
EventBridge envelope like normal so we need the ability to control how our events are processed:

```typescript
{
    source: 'cdkpatterns.the-destined-lambda',
    action: 'message',
    message: 'hello world'
}
```

by adding in the source and action fields this means that I could have multiple rules in eventbridge going to 
different targets based on the successful result of this function rather than the simple success/failure split you see today. 

```typescript
const successRule = new events.Rule(this, 'successRule', {
      eventBus: bus,
      description: 'all success events are caught here and logged centrally',
      eventPattern:
      {
        "detail": {
          "requestContext": {
            "condition": ["Success"]
          },
          "responsePayload": {
            "source": ["cdkpatterns.the-destined-lambda"],
            "action": ["message"]
          }
        }
      }
    });
```


For a complete version of routing flow based on the json payload see 
[The EventBridge ETL Pattern](https://github.com/cdk-patterns/serverless/tree/master/the-eventbridge-etl)


## When You Would Use This Pattern
If you are building an asynchronous, event driven flow but step functions seem too heavy weight for your current needs. 

Alternatively As illustrated in this implementation, you can use it to strip custom logic for sending events to EventBridge from your Lambdas

## Desconstructing The Destined Lambda
If you want a walkthrough of the theory, the code and finally a demo of the deployed implementation check out:
[![Alt text](https://img.youtube.com/vi/DQgq_p6Q03M/0.jpg)](https://www.youtube.com/watch?v=DQgq_p6Q03M)

## How To Test Pattern
After you deploy this pattern you will have an API Gateway with one endpoint "SendEvent" that accepts GET requests.

You will get the base url for your deployed api from the deploy logs.

To send a message that triggers the onSuccess flow just open the endpoint in a browser.

```https://{{API ID}}.execute-api.us-east-1.amazonaws.com/prod/SendEvent```

To send a message that triggers the onFailure flow add ?mode=fail onto the url.

```https://{{API ID}}.execute-api.us-east-1.amazonaws.com/prod/SendEvent?mode=fail```

What you are looking for in both flows is inside the cloudwatch logs for the Success and Failure Lambda functions. 
You will see that in the logs for failure, not only do you get the actual error that was thrown but it also includes 
the event details that came into the function to cause the error. This means you have everything you need to replay it 
at your leisure.


## Python Setup
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
