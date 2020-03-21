# The Destined Lambda

![arch](img/arch.png)

This project combines [Lambda Destinations](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-destinations/) with [Amazon EventBridge](https://aws.amazon.com/eventbridge/) to show how not only can you decouple your components in an event driven architecture but you can strip out EventBridge specific code from your lambda functions themselves and decouple further.

At time of writing there are 4 available destinations targets but I have chosen EventBridge as to be honest this is the most complicated and powerful of the 4:

![destinations](img/destinations.png)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
