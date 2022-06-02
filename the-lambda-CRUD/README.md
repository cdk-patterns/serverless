# Api Gateway, Lambda and DynamoDB Serverless App

A serverless CRUD app built using aws-cdk.

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
