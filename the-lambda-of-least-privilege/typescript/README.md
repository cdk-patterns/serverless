# The LAMBDA-OF-LEAST-PRIVILEGE

This is a pattern that aims to satisfy an application or standard needing to implement an service that implements Authentication and Authorisation checking based on an external IDP (such as Auth0). We will attempt to remain as well architected as possible.

Most of this code was inspired from working examples here 
https://github.com/aws-samples/amazon-cognito-example-for-external-idp/blob/master/cdk/src/cdk.ts

https://serverless-stack.com/chapters/configure-cognito-identity-pool-in-cdk.html 

https://stackoverflow.com/questions/55784746/how-to-create-cognito-identitypool-with-cognito-userpool-as-one-of-the-authentic

https://dev.to/martzcodes/token-authorizers-with-apigatewayv2-tricks-apigwv1-doesn-t-want-you-to-know-41jn

(Thank You)

## TODO The rest

Why are Identity Pool Implementations useful?

https://serverless-stack.com/chapters/cognito-user-pool-vs-identity-pool.html 

An overview of what we are trying to do. A pattern for Enterprise.


![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/the-simple-webservice/img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`  deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
