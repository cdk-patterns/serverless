import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import { PrimaryKey, Values, GraphQLApi, MappingTemplate, UserPoolDefaultAction, FieldLogLevel} from '@aws-cdk/aws-appsync';
import { UserPool, SignInType } from "@aws-cdk/aws-cognito";
import { AttributeType, BillingMode, Table } from '@aws-cdk/aws-dynamodb';
import { join } from 'path';

export class TheSimpleGraphQLServiceStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Create a new Cognito User Pool
     */
    const userPool = new UserPool(this, 'UserPool', {
      signInType: SignInType.USERNAME
    });

    /**
     * Create a new AppSync GraphQL API
     */
    const api = new GraphQLApi(this, 'Api', {
      name: `demoapi`,
      logConfig: {
        fieldLogLevel: FieldLogLevel.ALL,
      },
      // User pool authorizer configuration
      // userPoolConfig: {
      //   userPool,
      //   defaultAction: UserPoolDefaultAction.ALLOW,
      // },
      schemaDefinitionFile: join('__dirname', '/../', 'schema/schema.graphql'),
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
    const customerDS = api.addDynamoDbDataSource('Customer', 'The customer data source', customerTable);

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
      code: lambda.Code.asset('lambda'),  // code loaded from the "lambda" directory
      handler: 'loyalty.handler',                // file is "loyalty", function is "handler"
    });

    /**
     * Add Loyalty Lambda as a Datasource for the Graphql API.
     */
    const loyaltyDS = api.addLambdaDataSource('Loyalty', 'The loyalty data source', loyaltyLambda);

    // Query Resolver to get all Customers
    loyaltyDS.createResolver({
      typeName: 'Query',
      fieldName: 'getLoyaltyLevel',
      requestMappingTemplate: MappingTemplate.lambdaRequest(),
      responseMappingTemplate: MappingTemplate.lambdaResult(),
    });
  }
}

