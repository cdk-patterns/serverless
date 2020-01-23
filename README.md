# AWS CDK Serverless Architecture Patterns

This is intended to be a repo containing all of the official AWS Serverless architecture patterns built with CDK for developers to use.

Follow [@CdkPatterns](https://twitter.com/cdkpatterns) for live discussion / new pattern announcements. I plan to add a new pattern weekly so check back regularly!

## New to AWS CDK?

* To learn more visit the [AWS getting started guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
* To do a workshop on CDK visit [cdkworkshop.com](https://cdkworkshop.com)

## Patterns
### Website Deploys
* [S3 Angular Deploy ](/s3-angular-website/README.md)
* [S3 React Deploy ](/s3-react-website/README.md)

### Jeremy Daly Patterns
These patterns are from https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/

#### [The Simple Webservice](/the-simple-webservice/README.md)
![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-simple-webservice/img/architecture.png)

#### [The Scalable Webhook](/the-scalable-webhook/README.md)
![Architecture](https://raw.githubusercontent.com/nideveloper/serverless/master/the-scalable-webhook/img/arch.png)

## Pattern Usage

All Patterns (unless otherwise stated in their readme) should support the same commands so you can just run:

* `git clone https://github.com/cdk-patterns/serverless.git`
* `cd {pattern-name}`
* `npm i` - install the dependencies
* `npm run build` - build the project
* `npm run test` - run the unit tests
* `npm run deploy` - deploy the pattern into your AWS account&#42;

&#42; Note this requires you to be using cloud9 or have ran aws configure to setup your local credentials

## Contributing
I hope for this to be something the whole cdk community contributes to so feel free to fork this repo and open up a pull request.
