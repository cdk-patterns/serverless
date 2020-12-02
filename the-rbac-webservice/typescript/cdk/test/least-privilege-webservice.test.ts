import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import LeastPrivilegeWebserviceStack = require('../lib/least-privilege-webservice-stack');

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
    "KeySchema": [
      {
        "AttributeName": "title",
        "KeyType": "HASH"
      },
    ],
    "AttributeDefinitions": [
      {
        "AttributeName": "title",
        "AttributeType": "S"
      }
    ],
    "ProvisionedThroughput": {
      "ReadCapacityUnits": 5,
      "WriteCapacityUnits": 5
    },
    "TableName": "blogs"
  }
  ));
});


test('Update DynamoDB Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "createBlog.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('Get DynamoDB Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "readBlogs.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('API Gateway Rest API Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::RestApi", {
    "Name": "blogsapi"
  }
  ));
});

test('API Gateway Rest Resource Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Resource", {
    "PathPart": "blogs"
  }
  ));
});

test('API Gateway GET Rest Method Created with IAM Auth', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
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
  const stack = new LeastPrivilegeWebserviceStack.LeastPrivilegeWebserviceStack(app, 'MyTestStack', {
    identityPoolRef: "identityPoolStack.identityPool.ref"
  });
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
