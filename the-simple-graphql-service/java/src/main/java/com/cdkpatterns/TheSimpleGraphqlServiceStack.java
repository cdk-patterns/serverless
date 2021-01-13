package com.cdkpatterns;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.appsync.GraphqlApi;
import software.amazon.awscdk.services.appsync.Schema;
import software.amazon.awscdk.services.appsync.DynamoDbDataSource;
import software.amazon.awscdk.services.appsync.LambdaDataSource;
import software.amazon.awscdk.services.appsync.CfnApiKey;
import software.amazon.awscdk.services.appsync.PrimaryKey;
import software.amazon.awscdk.services.appsync.Values;
import software.amazon.awscdk.services.appsync.MappingTemplate;
import software.amazon.awscdk.services.appsync.LogConfig;
import software.amazon.awscdk.services.appsync.FieldLogLevel;
import software.amazon.awscdk.services.appsync.BaseResolverProps;
import software.amazon.awscdk.services.dynamodb.Table;
import software.amazon.awscdk.services.dynamodb.BillingMode;
import software.amazon.awscdk.services.dynamodb.Attribute;
import software.amazon.awscdk.services.dynamodb.AttributeType;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Runtime;

public class TheSimpleGraphqlServiceStack extends Stack {
    public TheSimpleGraphqlServiceStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public TheSimpleGraphqlServiceStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        /*
         * Create a new AppSync GraphQL API
         */
        GraphqlApi grapqlApi = GraphqlApi.Builder.create(this, "Api")
        		.name("demoapi")
        		.logConfig(new LogConfig
        				.Builder()
        				.fieldLogLevel(FieldLogLevel.ALL)
        				.build())
        		.schema(Schema.fromAsset("./schema/schema.graphql"))
        		.build();
        
        /*
         * Create Appsync Api Key
         */
        CfnApiKey graphqlKey = CfnApiKey.Builder.create(this, "the-simple-graphql-service-api-key")
        		.apiId(grapqlApi.getApiId())
        		.build();
        
        /*
         * Create new DynamoDB Table for Customer
         */
        Table customerTable = Table.Builder.create(this, "CustomerTable")
        		.billingMode(BillingMode.PAY_PER_REQUEST)
        		.partitionKey(new Attribute
        				.Builder()
        				.name("id")
        				.type(AttributeType.STRING)
        				.build())
        		.build();
        		
        /*
         * Add Customer DynamoDB as a Datasource for the Graphql API.
         */
        DynamoDbDataSource customerDS = grapqlApi.addDynamoDbDataSource("Customer", customerTable);
        
        // Query Resolver to get all Customers
        customerDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Query")
        		.fieldName("getCustomers")
        		.requestMappingTemplate(MappingTemplate.dynamoDbScanTable())
        		.responseMappingTemplate(MappingTemplate.dynamoDbResultList())
        		.build());

        // Query Resolver to get an individual Customer by their id
        customerDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Query")
        		.fieldName("getCustomer")
        		.requestMappingTemplate(MappingTemplate.dynamoDbGetItem("id", "id"))
        		.responseMappingTemplate(MappingTemplate.dynamoDbResultItem())
        		.build());

        // Mutation Resolver for adding a new Customer
        customerDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Mutation")
        		.fieldName("addCustomer")
        		.requestMappingTemplate(MappingTemplate.dynamoDbPutItem(
        				PrimaryKey.partition("id").auto(), 
        				Values.projecting("customer")))
        		.responseMappingTemplate(MappingTemplate.dynamoDbResultItem())
        		.build());
        
        // Mutation Resolver for updating an exisiting Customer
        customerDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Mutation")
        		.fieldName("saveCustomer")
        		.requestMappingTemplate(MappingTemplate.dynamoDbPutItem(
        				PrimaryKey.partition("id").is("id"), 
        				Values.projecting("customer")))
        		.responseMappingTemplate(MappingTemplate.dynamoDbResultItem())
        		.build());

        // Mutation resolver for creating a new customer along with their first order 
        customerDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Mutation")
        		.fieldName("saveCustomerWithFirstOrder")
        		.requestMappingTemplate(MappingTemplate.dynamoDbPutItem(
        				PrimaryKey.partition("order").auto().sort("customer").is("customer.id"), 
        				Values.projecting("order").attribute("referral").is("referral")))
        		.responseMappingTemplate(MappingTemplate.dynamoDbResultItem())
        		.build());

        // Mutation Resolver for deleting an exisiting Customer
        customerDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Mutation")
        		.fieldName("removeCustomer")
        		.requestMappingTemplate(MappingTemplate.dynamoDbDeleteItem("id", "id"))
        		.responseMappingTemplate(MappingTemplate.dynamoDbResultItem())
        		.build());
        
        // defines an AWS Lambda resource
        Function loyaltyLambda = Function.Builder.create(this, "LoyaltyLambdaHandler")
        		.runtime(Runtime.NODEJS_12_X) // execution environment
        		.code(Code.fromAsset("lambda_fns")) // code loaded from the "lambda_fns" directory
        		.handler("loyalty.handler") // code loaded from the "lambda_fns" directory
        		.build();
        
        /*
         * Add Loyalty Lambda as a Datasource for the Graphql API.
         */
        LambdaDataSource loyaltyDS = grapqlApi.addLambdaDataSource("Loyalty", loyaltyLambda);
        
        // Query Resolver to get all Customers
        loyaltyDS.createResolver(new BaseResolverProps
        		.Builder()
        		.typeName("Query")
        		.fieldName("getLoyaltyLevel")
        		.requestMappingTemplate(MappingTemplate.lambdaRequest())
        		.responseMappingTemplate(MappingTemplate.lambdaResult())
        		.build());

        // GraphQL API Endpoint
        CfnOutput.Builder.create(this, "Endpoint")
        	.value(grapqlApi.getGraphqlUrl())
        	.build();
        
        // API Key
        CfnOutput.Builder.create(this, "API_Key")
        	.value(graphqlKey.getAttrApiKey())
        	.build();
        
    }
}
