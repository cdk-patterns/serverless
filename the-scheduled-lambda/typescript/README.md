# The Scheduled Lambda

This is an example CDK stack demonstrating how to use AWS EventBridge to invoke a Lambda function on a schedule or using a cron expression. The Lambda function will then write the request ID to a DynamoDB table.

![The Scheduled Lambda Architecture Diagram](../img/the-scheduled-lambda.png)

## Useful commands
- `npm run build` - compile TypeScript to JavaScript
- `npm run watch` - watch for changes and compile
- `npm run test` - perform the jest unit tests
- `npm run deploy` - deploy this stack to your default AWS account/region
- `cdk diff` - compare deployed stack with current state
- `cdk synth` - emits the synthesized CloudFormation template
- `cdk deploy` - deploy the synthesized CloudFormation template
- `cdk destroy TheScheduledLambdaStack` - remove this stack from your AWS account