# Api Gateway, Lambda and DynamoDB Serverless App

A serverless CRUD app built using aws-cdk.

<br>
<br>

## Building Lambda

AWS CDK is an innovative and useful tool, but it surprisingly does not build the lambda functions for you. You will have to zip the files on your own before deploying. I use 7-zip running on Windows 10.

The NodeJsFunction construct on the aws-lambda-nodejs module attempts to solve this and build the lambda functions for you, but its still in the experimental phase and I found it to not even work on a simple function. I left the code in commented, try and maybe it may work for you.

Use any zipping tool, but you will need to add the zipped files to the LambdaBuilt directory before deploying or testing. Be sure to zip the individual files and not just the parent directory.

Note: functions without 3rd party libraries dont need to be zipped.

<br>
<br>

## Installing 3rd Party Libraries to a Lambda Function

You will need to install the required node modules inside the directory on each function and zip the modules and function together to deploy.

<br>
<br>

## Local Testing Lambda

note: you will need the sam cli installed to test lambda locally.

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

1. Output a template.yaml file with the command
`cdk synth > template.yaml`

2. Move the `template.yaml` file from root to `cdk.out` folder

3. Test the lambda
`sam local invoke funtionName123`

4. You can also start a local api server and test with a tool like Postman
`sam local start-api`

<br>
<br>

## Useful commands

- `npm run build` compile typescript to js
- `npm run watch` watch for changes and compile
- `npm run test` perform the jest unit tests
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk synth` emits the synthesized CloudFormation template
