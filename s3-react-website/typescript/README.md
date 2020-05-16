# AWS S3 / React Website Pattern
This is a starter with AWS CDK and React packaged together in a way that you can deploy the starter React application to s3 with no changes

### Possible Architecture:
![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/s3-react-website/img/architecture.PNG)

### Packaged Architecture:
This pattern out of the box deploys the React website to Amazon S3 but does not setup CloudFront, Route53 or Aws Certificate Manager. You can learn how to do that by looking at the [cdk-spa-deploy docs](https://github.com/nideveloper/CDK-SPA-Deploy)

## Deconstructing the S3 React Deploy Pattern
If you want a walkthrough of the theory, the code and finally a demo of the deployed implementation check out:

[![Alt text](https://img.youtube.com/vi/tUUNiF0q7rk/0.jpg)](https://www.youtube.com/watch?v=tUUNiF0q7rk)

## How To Use
If you have aws configured locally or you are in cloud9 this is as simple as running two commands (assuming your terminal starts at the README.md level):
- cd website && npm i && npm run build
- cd ../cdk && npm i && npm run build && npm run deploy 

## Project Structure

### React website (/website)
This can be found in the website folder. This is just the initial site that is created on npx create-react-app.

#### Some Commands
- npm install
- npm run build
- npm run start

### CDK S3 Deploy Infrastructure (/cdk)
This can be found in the cdk folder, it sets up an S3 bucket as a website deploy and uploads your react website in the website folder. This uses the JSII Construct - https://www.npmjs.com/package/cdk-spa-deploy

The initial setup here doesn't use cloudfront but the cdk-spa-deploy module details how easy it is to add it and a custom domain

#### Useful Commands

- npm run build
- cpm run cdk synth - outputs a cloudformation in the console
- npm run deploy - after running build on website folder then you deploy to s3

### buildspec.yml
I included this incase you want to setup a codebuild resource on aws to build/deploy your project automatically
