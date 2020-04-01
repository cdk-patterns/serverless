# The Lambda Trilogy

The three states of AWS Lambda are something that has been discussed by many serverless heroes since their invention.

Some examples from [Paul Swail](https://twitter.com/paulswail), [Yan Cui](https://twitter.com/theburningmonk) and [Jeremy Daly](https://twitter.com/jeremy_daly):
- [Serverless Chats](https://www.serverlesschats.com/41)
- [Off By None](https://www.jeremydaly.com/newsletter-issue-63/)
- [Yan Cui Presentation (slide 41 on)](https://www.slideshare.net/theburningmonk/beware-the-potholes-on-the-road-to-serverless-224107000)

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

## What's Actually In This Pattern?
I have bundled fully TypeScript and fully Python versions (including the lambdas) for this pattern because most of the logic takes place outside the AWS CDK infrastructure code.

The logic that I have used to demonstrate these patterns is a partially functional calculator.

This calculator can only perform three functions (It was on sale):
- Add
- Subtract
- Multiply

When you deploy this project you should have 3 API Gateways in your deployment logs, one for each of the patterns.

You can hit the same URLs on all 3 to see the same responses. You pass in two query params for the numbers you want to use in the operation (firstNum and secondNum). If you don't provide a valid a default of 0 is used.

```
Addition - https://{api gateway url}/add?firstNum=3&secondNum=4
Subtraction - https://{api gateway url}/subtract?firstNum=4&secondNum=3
Multiply - https://{api gateway url}/multiply?firstNum=3&secondNum=4
```

## There's A Lot Of Code Here, What Should I Actually Look At?

There are 3 distinct CDK stacks in this project which are all instantiated in the [bin file](bin/the-lambda-trilogy.ts). When CDK deploys this application you should see 3 different cloudformation stacks and if you update the code in one but not the other 2 you should see CDK only deploy the one you changed. This is a pretty cool, advanced feature of AWS CDK.

![bin file](img/bin.png)

### TheSinglePurposeFunctionStack

You can see inside our [stack definition](lib/the-single-purpose-function-stack.ts) that this project has 3 endpoints defined on the api gateway and 3 [lambdas](lambdas/single-purpose-function) defined. 

If you look carefully inside each lambda you will see a [duplicated function](lambdas/single-purpose-function/add.ts#L16) sendRes that formats the response from the Lambda for API Gateway. You could use layers or create a package that you install via npm for these kinds of things but in the purest representation of this pattern for the purpose of autonomy you see small levels of code duplication. This is a positive when you want to move a different direction with one function and a negative if you need to update them all.

### TheFatLambdaStack

### TheLambdalithStack

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
