import { expect as expectCDK, matchTemplate, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheSimpleGraphQLService = require('../lib/the-simple-graphql-service-stack');
const assert_1 = require("@aws-cdk/assert");

test('DynamoDB Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
      "KeySchema": [
        {
          "AttributeName": "id",
          "KeyType": "HASH"
        }
      ],
      "BillingMode": "PAY_PER_REQUEST"
    },
  ));
});

test('AppSync Endpoint Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::GraphQLApi", {
    "Name": "demoapi"
  }
  ));
});

test('API Key Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::ApiKey"));
});

test('DynamoDB Read/Write IAM Policy Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  assert_1.expect(stack).to(assert_1.haveResourceLike("AWS::IAM::Policy", {
      "PolicyDocument": {
          "Statement": [
              {
                  "Action": [
                      "dynamodb:BatchGetItem",
                      "dynamodb:GetRecords",
                      "dynamodb:GetShardIterator",
                      "dynamodb:Query",
                      "dynamodb:GetItem",
                      "dynamodb:Scan",
                      "dynamodb:BatchWriteItem",
                      "dynamodb:PutItem",
                      "dynamodb:UpdateItem",
                      "dynamodb:DeleteItem"
                  ],
                  "Effect": "Allow"
              }
          ]
      }
  }));
});

test('AppSync DynamoDB DataSource connected', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::DataSource", {
    "Type": "AMAZON_DYNAMODB"
  }
  ));
});

test('AppSync Query Resolver for getCustomer', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::Resolver", {
    "FieldName": "getCustomer",
    "TypeName": "Query"
  }
  ));
});

test('AppSync Query Resolver for getCustomers', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::Resolver", {
    "FieldName": "getCustomers",
    "TypeName": "Query"
  }
  ));
});

test('AppSync Mutation Resolver for addCustomer', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::Resolver", {
    "FieldName": "addCustomer",
    "TypeName": "Mutation"
  }
  ));
});

test('AppSync Mutation Resolver for saveCustomer', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::Resolver", {
    "FieldName": "saveCustomerWithFirstOrder",
    "TypeName": "Mutation"
  }
  ));
});

test('AppSync Mutation Resolver for removeCustomers', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::Resolver", {
    "FieldName": "removeCustomer",
    "TypeName": "Mutation"
  }
  ));
});

test('Loyalty Lambda Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
    "Handler": "loyalty.handler",
    "Runtime": "nodejs12.x"
  }
  ));
});

test('AppSync Lambda DataSource connected', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::DataSource", {
    "Type": "AWS_LAMBDA"
  }
  ));
});

test('AppSync Query Resolver for getLoyalty', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheSimpleGraphQLService.TheSimpleGraphQLServiceStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::AppSync::Resolver", {
    "FieldName": "getLoyaltyLevel",
    "TypeName": "Query"
  }
  ));
});
