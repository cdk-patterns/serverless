import * as cdk from "@aws-cdk/core"
import apigateway = require("@aws-cdk/aws-apigateway")
import dynamodb = require("@aws-cdk/aws-dynamodb")
import lambda = require("@aws-cdk/aws-lambda")
import lambdaNode = require("@aws-cdk/aws-lambda-nodejs")

export class AwsCdkServerlessCrudStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props)

    // The code that defines your stack goes here
    const dynamoTable = new dynamodb.Table(this, "items", {
      partitionKey: {
        name: "itemId",
        type: dynamodb.AttributeType.STRING,
      },
      tableName: "items",
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    })

    //const createOne = new lambdaNode.NodejsFunction(this, "createItemFunction", {
    //  entry: "Lambda/create2/create.js",
    //  handler: "handler",
    //  externalModules: ["aws-sdk", "uuidv4"],
    //})

    const createOne = new lambda.Function(this, "createItemFunction", {
      code: lambda.Code.fromAsset("LambdaBuilt/create.zip"),
      handler: "create.handler",
      runtime: lambda.Runtime.NODEJS_10_X,
      environment: {
        TABLE_NAME: dynamoTable.tableName,
      },
    })

    const getOneLambda = new lambda.Function(this, "getOneItemFunction", {
      code: lambda.Code.fromAsset("LambdaBuilt/get-one.zip"),
      handler: "get-one.handler",
      runtime: lambda.Runtime.NODEJS_10_X,
      environment: {
        TABLE_NAME: dynamoTable.tableName,
      },
    })

    const getAllLambda = new lambda.Function(this, "getAllItemsFunction", {
      code: lambda.Code.fromAsset("LambdaBuilt/get-all.zip"),
      handler: "get-all.handler",
      runtime: lambda.Runtime.NODEJS_10_X,
      environment: {
        TABLE_NAME: dynamoTable.tableName,
      },
    })

    const updateOne = new lambda.Function(this, "updateItemFunction", {
      code: lambda.Code.fromAsset("LambdaBuilt/update-one.zip"),
      handler: "update-one.handler",
      runtime: lambda.Runtime.NODEJS_10_X,
      environment: {
        TABLE_NAME: dynamoTable.tableName,
      },
    })

    const deleteOne = new lambda.Function(this, "deleteItemFunction", {
      code: lambda.Code.fromAsset("LambdaBuilt/delete-one.zip"),
      handler: "delete-one.handler",
      runtime: lambda.Runtime.NODEJS_10_X,
      environment: {
        TABLE_NAME: dynamoTable.tableName,
      },
    })

    dynamoTable.grantReadWriteData(getAllLambda)
    dynamoTable.grantReadWriteData(getOneLambda)
    dynamoTable.grantReadWriteData(createOne)
    dynamoTable.grantReadWriteData(updateOne)
    dynamoTable.grantReadWriteData(deleteOne)

    const api = new apigateway.RestApi(this, "itemsApi", {
      restApiName: "Items Service",
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS, // this is also the default
      },
    })

    const items = api.root.addResource("items")
    const getAllIntegration = new apigateway.LambdaIntegration(getAllLambda)
    items.addMethod("GET", getAllIntegration)

    const createOneIntegration = new apigateway.LambdaIntegration(createOne)
    items.addMethod("POST", createOneIntegration)

    const singleItem = items.addResource("{id}")
    const getOneIntegration = new apigateway.LambdaIntegration(getOneLambda)
    singleItem.addMethod("GET", getOneIntegration)

    const updateOneIntegration = new apigateway.LambdaIntegration(updateOne)
    singleItem.addMethod("PATCH", updateOneIntegration)

    const deleteOneIntegration = new apigateway.LambdaIntegration(deleteOne)
    singleItem.addMethod("DELETE", deleteOneIntegration)
  }
}
