# The RBAC Web Service Pattern

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`  deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template

 ### Cognito Resources
- [Lots of my code was inspired/borrowed from here](https://github.com/aws-samples/amazon-cognito-example-for-external-idp/blob/master/cdk/src/cdk.ts)
- [Identity Pools versus User Pools](https://serverless-stack.com/chapters/cognito-user-pool-vs-identity-pool.html)
- [Cognito Identity Pool Workshop](https://serverless-stack.com/chapters/configure-cognito-identity-pool-in-cdk.html) 
- [Cognito Userpool Auth](https://stackoverflow.com/questions/55784746/how-to-create-cognito-identitypool-with-cognito-userpool-as-one-of-the-authentic)
- [Cognito Identity Pool Tutorial for Google](https://medium.com/faun/cognito-idp-google-tutorial-379fa08464) 
- [Understanding Userpool Grants](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/)

### RBAC Resources
- [CSRC RBAC](https://csrc.nist.gov/CSRC/media/Presentations/Role-based-Access-Control/images-media/Role-based%20Access%20Control2.pdf) 
- [RBAC Introduction](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)
- [RBAC Wiki](https://en.wikipedia.org/wiki/Role-based_access_control)
- [RBAC at AWS](https://docs.amazonaws.cn/en_us/cognito/latest/developerguide/role-based-access-control.html)
- [RBAC v ABAC](https://www.dnsstuff.com/rbac-vs-abac-access-control)
