# The Role Based Access Control (RBAC) Web Service Pattern

Do you manage your users and their access controls/definitions in an external Identity Providers (IDPs) such as Ping, Auth0 or Azure? Do you want to extend this role based access into your cloud workloads? Then this pattern might work for you and your team.  This is a Pattern where we can federate the users from your external IDP using AWS Cognito Identity Pools. Cognito Identity Pool will map your external user claims to defined IAM roles for your workload. After login you can exchange your identity token for a secure set of AWS Credentials for invoking your API.

[An Overview of RBAC with Auth0](https://auth0.com/docs/authorization/rbac)

##  So what does this Pattern give us?

![Architecture](./img/RoleBasedAccess.png)

## What is Role-Based-Access-Control (RBAC)

Role-based access control (RBAC) is an idea of assigning permissions to users based on their role within an orgnaisation. It offers a simple, manageable approach to access management that is less prone to error than assigning permissions to users individually.

When using RBAC, you analyze the system needs of your users and group them into roles based on common responsibilities and needs. You then assign one or more roles to each user and one or more permissions to each role. The user-role and role-permissions relationships make it simple to perform user assignments since users no longer need to be managed individually, but instead have privileges that conform to the permissions assigned to their role(s).

When planning your access control strategy, it's best practice to assign users the fewest number of permissions that allow them to get their work done. Adopting a **security principle of Least Privilege access.**

## Accelerated Setup Instructions

The accelerated setup is federating users coming from an Auth0 SAML based Identity Provider.  
If just getting started with this I would reccomend reading this [blog post](https://auth0.com/blog/how-saml-authentication-works/) it will give you an idea into how this is setup.

### 1 - Get your IDP Integration Configuration OR set one up

* Open the `cdk/lib/configuration/stack-configuration.ts` set the values for the 
    - `EXTERNAL_IDENTITY_PROVIDER_NAME` and 
    - `SAML_METADATA_URL` configuration items.

* If you havent got an IDP and you want to follow along then something like Auth0 might work for you getting up and running 
    - [Auth0 Quick Start](https://auth0.com/docs/quickstart/webapp)

If interested in the underlying configuration see
    - [Cognito User Pools with SAML IDP](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-saml-idp.html)

* _This pattern can be easily extended to support OIDC exposed IDPs._


### 2 - Configure your Cognito Identity Pool and Attribute Mapping

As users from your External IDP are federated VIA Cognito they will be stored in a Cognito User Pool. Any attributes such as groups or roles from your External IDP that you will need for later in terms of mapping to IAM roles should be configured within your User Pool. In our example I am mapping the 'roles' SAML claim into the UserPool as a UserPool Attribute.  (Note: The need for this is made clear in the roles mapping section below.)

* Open the `cdk/lib/configuration/stack-configuration.ts` and scroll down to the 'USER POOL ATTRIBUTE DEFINITION CONFIGURATION'
* You can see an example of this Attribute Mapping within the configuration for
    - Email
    - Role
* This is where you would configure the attributes to mapped from your IDP. 
    - In the exported config within `stack-configuration.ts` make sure these are writeable attributes.


### 3 - Configure a User Pool App Client for our Sample Front End Application

This pattern comes with a sample UI Client for the purposes of demonstrating the auth flow of the pattern (_I used VUE to annoy the React folks :)_).  This Vue UI Client application will need a **'Cognito App Client'** to integrate with and will simulate a User Login and API Gateway call. 
More Information on the purpose of this App Client can be found [here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html). It is worth reading in terms of understanding your Client Applications ideal OIDC Flow.

* Give Cognito a unique domain name setting the `COGNITO_DOMAIN` Configuration item. (i.e. if Auth0 use 'Auth0')
* Set the standard Call Back and Log-out URLs information for your UI-Application setting the `CLIENT_CALLBACKURLS` and `CLIENT_LOGOUTURLS`.
* Have a think about the scopes your client needs in terms of its OIDC Flow. Configure the remaining settings as required.

### 4 - Understand the Role Based Mapping for Access to the Sample Web Services in this Stack.

* Navigate to `cdk/lib/least-privilege-webservice-stack.ts`

In this example we are deploying two APIs, a GET and a PUT operation. Each operation is exposed via API-Gateway, with Lambda compute and both interacting with DynamoDB for some persistance.

**Important** This stack also defines and creates Two IAM Roles. 
1. The 'Admin role' has access to all this is required for both the GET and PUT Api operations.  
2. The 'Read role' has only access to the GET operation.  

You will also notice that both roles have a Policy that dictates that Cognito can only assume this role for authenticated users.

**So how does Cognito assign these roles to Authenticated Users**? Great question...

* Navigate to `cdk/lib/cognito-rbac-rolemappings.ts`
* Scroll down to the RoleMapper Resource code around line 84
* Here you can see the following 
    * Using the attribute that we mapped from the external IDP in step 2 `roles` (defined here as `props.cognitoAttr`) we can create rules that dictate the IAM role that is used.
    * In this example we have two rules. One for mapping the admin user and the other for a user.

This role mapping is used to create a custom `IdentityPoolRoleAttachment` of type `Rules` for the external IDP you have configured above. 
This will be used to setup the Cognito Identity Pool with the rules it needs to map users with external claims to the IAM roles that you have defined.

---
***Consider***
---
In a real world example you may have many roles / overlapping roles and this is likely the area that you are going to spend a lot of time getting correct. 

However sticking true to the principles of RBAC ensure that each role is consistent with the **Rules of Least Privilege**.
- A role contains the minimum amount of permissions necessary.
- A user is assigned to a role that allows him or her to perform only what’s required for that role.
- No single role is given more permission than the same role for another user.

---
This role mapping approach is described here [Rule Based Role Mapping](https://docs.aws.amazon.com/cognito/latest/developerguide/role-based-access-control.html)

### 5 - Deploy the CDK Stack.

Once you have made the configuration changes above run the CDK Deployment. 
* `npm run build` (Otherwise your lambda package wont get found unfortunately)
* `npm run deploy`
* Keep track of the outputs in your console, you will need these for the next step..
    - CognitoDomain
    - WebClientIDOutput
    - IdentityPoolID
    - UserPoolId
    - Region
    - httpURI

### 6 - Update your Vue UI Client with Cognito Identity Pool Integration Configuration

If you have made it this far Kudos, keep going. If the CDK Stack deployed successfully you will now have output described in Step 5 to plug into your Client Configuration.

* Assumption: This Vue application is using a manually configured AWS Amplify JS library for actioning the requests for authentication and authorisation. It is the basic of basic so please never deploy anything here to production.

* Open the `/sample-client/src/dev-cfg.ts`
* Complete the Auth Configuration properties
    - `CognitoDomain`
    - `WebClientIDOutput`
    - `IdentityPoolID`
    - `UserPoolId`
    - `Region`
* Setup an endpoint configuration within the API block of cfg
    - URI for apigateway endpoint

* Open the `/sample-client/src/main.js`
    - This is where we have configured the routes for the app supporting the callback and logout urls specified in Step 3

* Open the `/sample-client/src/components/HelloWorld.vue`
    - This is where I have rigged up a button to lauch the login process using the `Amplify.FederatedSignin` library.
    - Update the `provider` value within the props of the `Auth.federatedSignin` call to the name of your External Provider (i.e. Auth0)

* Start up the Application `npm run serve`

* Open browser and navigate to the local url for the app (i.e. http://localhost:8000/)

* Inspect your traffic and observe the exhange

* Click the login button. Hopefull you are directed to your IDP login page.

* In my Auth0 Application I had two users setup. One user with an 'Admin' role and one user with a 'User' role.
    - To get this setup I had to configure Auth0 with the Authorisation Extension
    - [Auth0 Authorisation Extension](https://auth0.com/docs/extensions/authorization-extension)
    - The user with the 'User' role will not be able to create a blog suggestion. You should see a 400 error in the console.

Bada-Bing. Hopefully that was worthwhile and helped you in someway.

Thanks to [CalumMcElhone](https://twitter.com/calummcelhone) and [Mark McKim](https://twitter.com/markmckim) as I extracted this pattern from work they have been doing in their domains.

_Apologies, this is a fairly complex pattern that probably requires an actual workshop. If there is enough interest I will produce that sort of asset. (A promise from Michael.)_  

## Additional Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`  deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template


## Additional Reading/Resource

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
