# The Lambda Trilogy

> Note, deployment instructions are at the bottom of this readme.

The three states of AWS Lambda are something that has been discussed by many serverless heroes since their invention. This is probably the most controversial subject in all of serverless so I am not going to tell you which of the three is the best because like everything you need to adapt the right implementation to fit your context!

Some examples from [Paul Swail](https://twitter.com/paulswail), [Yan Cui](https://twitter.com/theburningmonk), [Jeremy Daly](https://twitter.com/jeremy_daly) and others:
- [Jeremy Daly & Paul Swail Serverless Chats #41](https://www.serverlesschats.com/41)
- [Jeremy Daly Off By None](https://www.jeremydaly.com/newsletter-issue-63/)
- [Yan Cui Presentation (slide 41 on)](https://www.slideshare.net/theburningmonk/beware-the-potholes-on-the-road-to-serverless-224107000)
- [Yan Cui re:Invent 2019](https://d1.awsstatic.com/events/reinvent/2019/REPEAT_1_How_to_refactor_a_monolith_to_serverless_in_8_steps_API310-R1.pdf)
- [Yan Cui Hackernoon - monolithic or single purpose functions?](https://hackernoon.com/aws-lambda-should-you-have-few-monolithic-functions-or-many-single-purposed-functions-8c3872d4338f)
- [Yan Cui monoliths vs cold starts](https://theburningmonk.com/2018/02/aws-lambda-monolithic-functions-wont-help-you-with-cold-starts/)
- [J D Hollis medium.com](https://medium.com/statics-and-dynamics/should-i-use-a-single-monolithic-lambda-function-or-multiple-lambda-functions-with-api-gateway-d99b0230f1e7)
- [Ryanne Dolan medium.com](https://medium.com/@ryannedolan/aws-lambda-and-the-monolith-a0eb2d1516ef)

The three states are:

![arch](img/the-single-purpose-function.png)

### Description
This is the purest of all the serverless patterns. Each lambda does one unique function and the code is in its own file.

### Pros
- Maximum code reusability
- Forces you to write more testable code
- Introduces lowest cognitive burden for developers making changes to that individual function
- Easier to optimize your lambda execution times and by extension costs

### Cons
- Only works for fully event driven architectures
- Seeing the bigger picture, congnitive burden increases as system wide changes are talked about
- Maintenance as it grows (how do you make sure 7000 lambdas have no code vulnerabilities?)

![arch](img/the-fat-lambda.png)

### Description
This is a compromise option where we can still have individual lambdas but we group the actual code together in one (or more) files. You would decide what goes into a file based on low coupling, high cohesion arguments like in traditional development.

### Pros
- Related logic is grouped together making your code easier to see the bigger picture
- Code can easily be shared between lambda functions without needing things like layers
- Security footprint reduced as updating one file can update many lambda functions

### Cons
- How big is too big? Every extra byte of code added slows your lambda cold start times.
- Increased blast radius of changes. Now one line of code being changed could bring down a section of your infrastructure instead of one lambda.

![arch](img/the-lambda-lith.png)

### Description
This is using the lambda runtime container like a docker container. You use a web framework like Flask or Express and put them inside the lambda, then have your api gateway pass all requests through to the lambda and have that framework process the request.

### Pros
- You can have an identical local development experience to deployed since you are using no AWS specific features
- The code could be moved to Fargate later if it got too big for lambda with minimal changes (or another cloud)
- Developers already know these frameworks

### Cons
- Is this really what Lambda excels at? The larger project sizes will increase cold start times and there will be restrictions on incoming/outgoing payload sizes
- Higher exposure to cold starts as the lambda will spend longer processing events
- Lower levels of code reuse as probably still building the traditional ball of mud
- Adapters required to make existing frameworks work with lambda. These are in various states of maturity and are another potential vulnerability in your app.

## Deconstructing The Lambda Trilogy
If you want a walkthrough of the theory, the code and finally a demo of the deployed implementation check out:

[![Alt text](https://img.youtube.com/vi/tHD3i06Z6gU/0.jpg)](https://www.youtube.com/watch?v=tHD3i06Z6gU)

## What's In This CDK Pattern?
I have bundled fully TypeScript and fully Python versions (including the lambdas) for all 3 lambda states inside this pattern because most of the logic takes place outside the AWS CDK infrastructure code.

The logic that I have used to demonstrate these patterns is a partially functional calculator.

This calculator can only perform three functions (It was on sale):
- Add
- Subtract
- Multiply

When you deploy this project you should have 3 API Gateways in your deployment logs, one for each of the states.

You can hit the same URLs on all 3 to see the same responses. You pass in two query params for the numbers you want to use in the operation (firstNum and secondNum). If you don't provide a valid a default of 0 is used.

```
Addition - https://{api gateway url}/add?firstNum=3&secondNum=4
Subtraction - https://{api gateway url}/subtract?firstNum=4&secondNum=3
Multiply - https://{api gateway url}/multiply?firstNum=3&secondNum=4
```

## There's A Lot Of Code Here, What Should I Actually Look At?

There are 3 distinct CDK stacks in this project which are all instantiated in the [bin file](bin/the-lambda-trilogy.ts). When CDK deploys this application you should see 3 different cloudformation stacks in the AWS Console and if you update the code in one but not the other 2 you should see CDK only deploy the one you changed. This is a pretty cool, advanced feature of AWS CDK.

![bin file](img/bin.png)

### TheSinglePurposeFunctionStack

You can see inside our [stack definition](lib/the-single-purpose-function-stack.ts) that this project has 3 endpoints defined on the api gateway and 3 [lambdas](lambdas/single-purpose-function) defined. 

![api gateway](img/spf_apigw.png)

If you look carefully inside each lambda you will notice that they only perform a single operation (add, subtract or multiply) but you will also see a [duplicated function](lambdas/single-purpose-function/add.ts#L16) sendRes that formats the response from the Lambda for API Gateway. 

![lambda](img/spf_add_lambda.png)

You could use layers or create a package that you install via npm for these kinds of things but in the purest representation of this pattern for the purpose of autonomy you see small levels of code duplication. This is a positive when you want to move a different direction with one function and a negative if you need to update them all.

### TheFatLambdaStack

The big difference between this implementation and the one above is that all 3 functions (add, subtract and multiply) are inside the same [TS file](lambdas/fat-lambda/fat-lambda.ts).

This means that we can still define 3 lambdas inside our cdk logic but we point to a different method in the same file all 3 times:

![lambda definition](img/fl_cdk.png)

You should also notice that the [sendRes method](lambdas/fat-lambda/fat-lambda.ts#L49) is no longer duplicated with this pattern as all 3 lambdas can just call the same one.

### TheLambdalithStack

OK, this state is very different from the other two. The cdk for this is bare bones, just one lambda function and a proxy api gateway:

![lambdalith cdk](img/lambdalith_cdk2.png)

All of the action takes place inside [the lambda-lith](lambdas/the-lambda-lith) itself.

#### [package.json](lambdas/the-lambda-lith/package.json)
Now that we are building an application using express.js inside our lambda we need to pull it in as a dependency. We also need to pull in aws-serverless-express to make express compatible with lambda and api gateway.

You will be responsible for keeping these versions up to date unlike using API Gateway for the routing.

I did include a start command for starting up the express server locally to show the advantage of this pattern

![package json](img/lambdalith_package.png)

#### Routing

Inside the [lambdalith lambda](lambdas/the-lambda-lith/lambdalith.ts) we use express for routing to logic in this file rather than using API Gateway in the previous states:

![express routing](img/lambdalith_routes.png)

#### Local vs Deployed

We also need to define logic for how to start up the server locally vs in a lambda container since locally we don't need the aws-serverless-express adapter

![lambdalith startup](img/lambdalith_startup.png)

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
