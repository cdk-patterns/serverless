# The Alexa Skill

This deploys two CDK stacks that produce an Alexa Skill backed by a Lambda Function.

## Architecture

![arch](img/arch.png)

## Prerequisites:
1. An Amazon Developer account from: https://developer.amazon.com/
1. A developer account security profile: https://developer.amazon.com/loginwithamazon/console/site/lwa/create-security-profile.html
1. An AWS Account with CLI Access

## Before You Deploy
You need to add your ClientID, ClientSecret and VendorID to the skill resource which can be found in `the-alexa-skill-stack.ts`
```
 authenticationConfiguration: {
        clientId: 'foo',
        clientSecret: 'bar',
        refreshToken: 'foobar'
      }
```

## Components
### Asset Stack
Deploys a S3 bucket and uploads zipped Alexa manifest to the bucket. Must be deployed before Alexa Skill Stack
### Alexa Skill Stack
Deploys an Alexa skill, Lambda Function, and Dynamo DB table. The Alexa skill is fulfilled by the Lambda function. The Lambda function writes basic user details to the Dynamo Table.


## Available Versions

 * [TypeScript](typescript/)