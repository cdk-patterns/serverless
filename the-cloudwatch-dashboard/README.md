# The CloudWatch Dashboard

![Example Dashboard](img/dashboard.png)

This is a project that has been configured with a well architected dashboard for the simple webservice stack. It includes multiple alerts which are all sending messages to an SNS Topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
