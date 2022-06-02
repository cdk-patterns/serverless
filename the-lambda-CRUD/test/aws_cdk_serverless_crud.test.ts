import {expect as expectCDK, haveResourceLike, matchTemplate, MatchStyle} from "@aws-cdk/assert"
import * as cdk from "@aws-cdk/core"
import * as AwsCdkServerlessCrud from "../lib/aws_cdk_serverless_crud-stack"

//dynamo db tests
test("DynamoDB table has 'itemId' key", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::DynamoDB::Table", {
      KeySchema: [
        {
          AttributeName: "itemId",
          KeyType: "HASH",
        },
      ],
    })
  )
})

test("DynamoDB table has table named 'items'", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::DynamoDB::Table", {
      TableName: "items",
    })
  )
})

//lambda tests
test("create item lambda created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::Lambda::Function", {
      Handler: "create.handler",
      Runtime: "nodejs10.x",
    })
  )
})

test("get one item lambda created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::Lambda::Function", {
      Handler: "get-one.handler",
      Runtime: "nodejs10.x",
    })
  )
})

test("get all items lambda created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::Lambda::Function", {
      Handler: "get-all.handler",
      Runtime: "nodejs10.x",
    })
  )
})

test("update one item lambda created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::Lambda::Function", {
      Handler: "update-one.handler",
      Runtime: "nodejs10.x",
    })
  )
})

test("delete one item lambda created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::Lambda::Function", {
      Handler: "delete-one.handler",
      Runtime: "nodejs10.x",
    })
  )
})

//API Gateway tests
test("Main items API path created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::ApiGateway::Resource", {
      PathPart: "items",
    })
  )
})

test("Single item API path created", () => {
  const app = new cdk.App()
  // WHEN
  const stack = new AwsCdkServerlessCrud.AwsCdkServerlessCrudStack(app, "MyTestStack")
  // THEN
  expectCDK(stack).to(
    haveResourceLike("AWS::ApiGateway::Resource", {
      PathPart: "{id}",
    })
  )
})
