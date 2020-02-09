# AWS CDK Serverless Architecture Patterns

This is intended to be a repo containing all of the official AWS Serverless architecture patterns built with CDK for developers to use.

Follow [@CdkPatterns](https://twitter.com/cdkpatterns) for live discussion / new pattern announcements. I plan to add a new pattern weekly so check back regularly!

Note, this is maintained by [@nideveloper](https://twitter.com/nideveloper) not AWS. For my motivation, please read this [blog post](https://www.mattcoulter.com/blog/post/2)

## New to AWS CDK?

* To learn more visit the [AWS getting started guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
* To do a workshop on CDK visit [cdkworkshop.com](https://cdkworkshop.com)
* Visit the [Hey CDK &quot;How To&quot; series](https://garbe.io/blog/2019/09/11/hey-cdk-how-to-migrate/) for some detailed answers
* Check out [Awesome CDK](https://github.com/eladb/awesome-cdk) for a curated list of awesome projects related to CDK

## Pattern Usage

### TypeScript
All Patterns (unless otherwise stated in their readme) should support the same commands so you can just run:

* `git clone https://github.com/cdk-patterns/serverless.git`
* `cd {pattern-name}/typescript`
* `npm i` - install the dependencies
* `npm run build` - build the project
* `npm run test` - run the unit tests
* `npm run deploy` - deploy the pattern into your AWS account&#42;

&#42; Note this requires you to be using cloud9 or have ran aws configure to setup your local credentials

### Python

* `npm install -g aws-cdk`
* `git clone https://github.com/cdk-patterns/serverless.git`
* `cd {pattern-name}/python`
* `python -m venv .env` - Create a virtual env
* `source .env/bin/activate` - Activate the virtual env
* `pip install -r requirements.txt` - Install the dependencies
* `cdk synth` - generate a cft from the stack to validate your setup
* `cdk deploy` - deploy the pattern into your AWS account&#42;

&#42; Note this requires you to be using cloud9 or have ran aws configure to setup your local credentials

## Patterns
### Matt Coulter Patterns ([@nideveloper](https://twitter.com/nideveloper))

#### Single Page Application S3 Website Deploy
These are built using https://www.npmjs.com/package/cdk-spa-deploy

* [S3 Angular Deploy ](/s3-angular-website/README.md)
* [S3 React Deploy ](/s3-react-website/README.md)

![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/s3-angular-website/img/architecture.PNG)

<br /><hr /><br />

### Jeremy Daly Patterns ([@jeremy_daly](https://twitter.com/jeremy_daly))
These patterns are from https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/

#### [The Simple Webservice](/the-simple-webservice/README.md)
![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-simple-webservice/img/architecture.png)

#### [The Scalable Webhook](/the-scalable-webhook/README.md)
![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-scalable-webhook/img/architecture.png)

#### [The State Machine](/the-state-machine/README.md)
![Architecture](/the-state-machine/img/the-state-machine-arch.png)

<br /><hr /><br />

### Eric Johnson Patterns ([@edjgeek](https://twitter.com/edjgeek))

#### [The Dynamo Streamer](/the-dynamo-streamer/README.md)
This was taken from this [Tweet](https://twitter.com/edjgeek/status/1220227872511496192?s=20)

![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-dynamo-streamer/img/arch.jpg)

<br /><hr /><br />

## External Patterns

### AWS Examples

#### [Building enterprise applications using Amazon DynamoDB, AWS Lambda, and Go](https://github.com/aws-samples/aws-dynamodb-enterprise-application/blob/master/README.md) by Geoffroy Rollat


Found via this [tweet](https://twitter.com/danilop/status/1222856997751656449)
* [Tutorial](https://aws.amazon.com/blogs/database/building-enterprise-applications-using-amazon-dynamodb-aws-lambda-and-golang/)
* [GitHub Repo](https://github.com/aws-samples/aws-dynamodb-enterprise-application)

![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/img/building-enterprise-architecture.jpg)

### Sebastian Müller ([@sbstjn](https://twitter.com/sbstjn), [@superluminario](https://twitter.com/superluminario))

> Full-featured example project based on [create-react-app](https://create-react-app.dev/) with server-side rendering and continuous deployment.

#### [React SPA with server-side rendering on AWS Lambda](https://github.com/sbstjn/cra-serverless/blob/master/README.md)

Found via this [tweet](https://twitter.com/sbstjn/status/1225811582061621250?s=20) and [this](https://twitter.com/superluminario/status/1225779586161684480).

* [Tutorial (English)](https://sbstjn.com/serverless-create-react-app-server-side-rendering-ssr-lamda.html)
* [Tutorial (German)](https://superluminar.io/2020/02/07/react-spa-und-server-side-rendering-ssr-mit-aws-lambda-cloudfront-und-dem-cdk/)
* [GitHub Repo](https://github.com/sbstjn/cra-serverless/blob/master/README.md)

#### Architecture (English)

![Architecture](/img/serverless-ssr-react-lambda-en.png)

#### Architecture (German)

![Architecture](/img/serverless-ssr-react-lambda-de.png)

## Contributing
I hope for this to be something the whole cdk community contributes to so feel free to fork this repo and open up a pull request. For full details see our [Contributing Guidelines](CONTRIBUTING.md)
