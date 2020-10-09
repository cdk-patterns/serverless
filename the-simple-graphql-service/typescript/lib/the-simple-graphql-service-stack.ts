import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import { CfnApiKey, MappingTemplate, PrimaryKey, Values, GraphqlApi, Schema, FieldLogLevel } from '@aws-cdk/aws-appsync';
import { AttributeType, BillingMode, Table } from '@aws-cdk/aws-dynamodb';
import { join } from 'path';

export class TheSimpleGraphQLServiceStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Create a new AppSync GraphQL API
     */
    const api = new GraphqlApi(this, 'Api', {
      name: `demoapi`,
      logConfig: {
        fieldLogLevel: FieldLogLevel.ALL,
      },
      schema: new Schema({ filePath: join('__dirname', '/../', 'schema/schema.graphql') }),
    });
    
    const apiKey = new CfnApiKey(this, 'the-simple-graphql-service-api-key', {
      apiId: api.apiId
    });

    /**
     * Create new DynamoDB Table for Customer
     */
    const customerTable = new Table(this, 'CustomerTable', {
      billingMode: BillingMode.PAY_PER_REQUEST,
      partitionKey: {
        name: 'id',
        type: AttributeType.STRING,
      },
    });

    /**
     * Add Customer DynamoDB as a Datasource for the Graphql API.
     */
    const customerDS = api.addDynamoDbDataSource('Customer', customerTable);

    // Query Resolver to get all Customers
    customerDS.createResolver({
      typeName: 'Query',
      fieldName: 'getCustomers',
      requestMappingTemplate: MappingTemplate.dynamoDbScanTable(),
      responseMappingTemplate: MappingTemplate.dynamoDbResultList(),
    });

    // Query Resolver to get an individual Customer by their id
    customerDS.createResolver({
      typeName: 'Query',
      fieldName: 'getCustomer',
      requestMappingTemplate: MappingTemplate.dynamoDbGetItem('id', 'id'),
      responseMappingTemplate: MappingTemplate.dynamoDbResultItem(),
    });

    // Mutation Resolver for adding a new Customer
    customerDS.createResolver({
      typeName: 'Mutation',
      fieldName: 'addCustomer',
      requestMappingTemplate: MappingTemplate.dynamoDbPutItem(
        PrimaryKey.partition('id').auto(),
        Values.projecting('customer')),
      responseMappingTemplate: MappingTemplate.dynamoDbResultItem(),
    });

    // Mutation Resolver for updating an exisiting Customer
    customerDS.createResolver({
      typeName: 'Mutation',
      fieldName: 'saveCustomer',
      requestMappingTemplate: MappingTemplate.dynamoDbPutItem(
          PrimaryKey.partition('id').is('id'),
          Values.projecting('customer')),
      responseMappingTemplate: MappingTemplate.dynamoDbResultItem(),
    });

    // Mutation resolver for creating a new customer along with their first order 
    customerDS.createResolver({
      typeName: 'Mutation',
      fieldName: 'saveCustomerWithFirstOrder',
      requestMappingTemplate: MappingTemplate.dynamoDbPutItem(
        PrimaryKey
          .partition('order').auto()
          .sort('customer').is('customer.id'),
        Values
          .projecting('order')
          .attribute('referral').is('referral')),
      responseMappingTemplate: MappingTemplate.dynamoDbResultItem(),
    });

    // Mutation Resolver for deleting an exisiting Customer
    customerDS.createResolver({
      typeName: 'Mutation',
      fieldName: 'removeCustomer',
      requestMappingTemplate: MappingTemplate.dynamoDbDeleteItem('id', 'id'),
      responseMappingTemplate: MappingTemplate.dynamoDbResultItem(),
    });

    // defines an AWS Lambda resource
    const loyaltyLambda = new lambda.Function(this, 'LoyaltyLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
      code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
      handler: 'loyalty.handler',                // file is "loyalty", function is "handler"
    });

    /**
     * Add Loyalty Lambda as a Datasource for the Graphql API.
     */
    const loyaltyDS = api.addLambdaDataSource('Loyalty', loyaltyLambda);

    // Query Resolver to get all Customers
    loyaltyDS.createResolver({
      typeName: 'Query',
      fieldName: 'getLoyaltyLevel',
      requestMappingTemplate: MappingTemplate.lambdaRequest(),
      responseMappingTemplate: MappingTemplate.lambdaResult(),
    });
    
    // GraphQL API Endpoint
    new cdk.CfnOutput(this, 'Endpoint', {
      value: api.graphqlUrl
    });

    // API Key
    new cdk.CfnOutput(this, 'API_Key', {
      value: apiKey.attrApiKey
    });
  }
}

