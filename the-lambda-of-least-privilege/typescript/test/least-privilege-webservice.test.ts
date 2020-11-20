import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import LeastPrivilegeWebserviceStack = require('../lib/least-privilege-webservice-stack');

test('DynamoDB Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
    // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "path",
        "KeyType": "HASH"
      }
    ]}
  ));
});


test('Update DynamoDB Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "updateHits.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Get DynamoDB Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "updateHits.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('API Gateway Rest API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::RestApi", {
    "Name": "hitsapi"
  }
  ));
});

test('API Gateway Rest Resource Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "hits"
  }
  ));
});

test('API Gateway GET Rest Method Created with IAM Auth', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Method", {
    "HttpMethod": "GET",
    "AuthorizationType": "AWS_IAM",
    "Integration": {
      "IntegrationHttpMethod": "POST"
    }
  }
  ));
});

test('API Gateway PUT Rest Method Created with IAM Auth', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Method", {
    "HttpMethod": "PUT",
    "AuthorizationType": "AWS_IAM",
    "Integration": {
      "IntegrationHttpMethod": "POST"
    }
  }
  ));
});
