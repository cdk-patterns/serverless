# AWS S3 / React Website Pattern
This is a starter with AWS CDK and React packaged together in a way that you can deploy the starter React application to s3 with no changes

Possible Architecture:
![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/s3-react-website/img/architecture.PNG)

Packaged Architecture:
![Architecture](https://raw.githubusercontent.com/cdk-patterns/serverless/master/s3-react-website/img/spa-deploy-arch.png)

## How To Use
If you have aws configured locally or you are in cloud9 this is as simple as running two commands (assuming your terminal starts at the README.md level):
- cd website && npm i && npm run build
- cd ../cdk && follow readme.md instructions

## Project Structure

### React website (/website)
This can be found in the website folder. This is just the initial site that is created on npx create-react-app.

#### Some Commands
- npm install
- npm run build
- npm run start

### CDK S3 Deploy Infrastructure (/cdk)
This can be found in the cdk folder, it sets up an S3 bucket as a website deploy and uploads your react website in the website folder. This uses the JSII Construct - https://pypi.org/project/cdk-spa-deploy/

The inital setup here doesn't use cloudfront but the cdk-spa-deploy module details how easy it is to add it and a custom domain

#### Useful Commands

- cdk synth - outputs a cloudformation template into the console
- cdk deploy - deploys to your aws account
