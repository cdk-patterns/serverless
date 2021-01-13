using Amazon.CDK;
using Lambda = Amazon.CDK.AWS.Lambda;
using DynamoDB = Amazon.CDK.AWS.DynamoDB;
using AppSync = Amazon.CDK.AWS.AppSync;

namespace TheSimpleGraphqlService
{
    public class TheSimpleGraphqlServiceStack : Stack
    {

        private readonly AppSync.GraphqlApi _graphqlApi;
        private readonly AppSync.CfnApiKey _graphqlKey;
        private readonly DynamoDB.Table _customerTable;
        private readonly Lambda.Function _loyaltyLambda;

        internal TheSimpleGraphqlServiceStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            /**
            * Create a new AppSync GraphQL API
            */
            _graphqlApi = new AppSync.GraphqlApi(this, "Api", new AppSync.GraphqlApiProps
            {
                Name = "demoapi",
                LogConfig = new AppSync.LogConfig
                {
                    FieldLogLevel = AppSync.FieldLogLevel.ALL
                },
                Schema = AppSync.Schema.FromAsset("./schema/schema.graphql")
            });

            /**
             * Create Appsync Api Key
             */
            _graphqlKey = new AppSync.CfnApiKey(this, "the-simple-graphql-service-api-key", new AppSync.CfnApiKeyProps
            {
                ApiId = _graphqlApi.ApiId
            });


            /**
             * Create new DynamoDB Table for Customer
             */
            _customerTable = new DynamoDB.Table(this, "CustomerTable", new DynamoDB.TableProps
            {
                BillingMode = DynamoDB.BillingMode.PAY_PER_REQUEST,
                PartitionKey = new DynamoDB.Attribute
                {
                    Name = "id",
                    Type = DynamoDB.AttributeType.STRING
                }
            });

            /**
             * Add Customer DynamoDB as a Datasource for the Graphql API.
             */
            var customerDS = _graphqlApi.AddDynamoDbDataSource("Customer", _customerTable);

            // Query Resolver to get all Customers
            customerDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Query",
                FieldName = "getCustomers",
                RequestMappingTemplate = AppSync.MappingTemplate.DynamoDbScanTable(),
                ResponseMappingTemplate = AppSync.MappingTemplate.DynamoDbResultList()
            });

            // Query Resolver to get an individual Customer by their id
            customerDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Query",
                FieldName = "getCustomer",
                RequestMappingTemplate = AppSync.MappingTemplate.DynamoDbGetItem("id", "id"),
                ResponseMappingTemplate = AppSync.MappingTemplate.DynamoDbResultItem()
            });

            // Mutation Resolver for adding a new Customer
            customerDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Mutation",
                FieldName = "addCustomer",
                RequestMappingTemplate = AppSync.MappingTemplate.DynamoDbPutItem(
                    AppSync.PrimaryKey.Partition("id").Auto(),
                    AppSync.Values.Projecting("customer")
                ),
                ResponseMappingTemplate = AppSync.MappingTemplate.DynamoDbResultItem()
            });


            // Mutation Resolver for updating an exisiting Customer
            customerDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Mutation",
                FieldName = "saveCustomer",
                RequestMappingTemplate = AppSync.MappingTemplate.DynamoDbPutItem(
                    AppSync.PrimaryKey.Partition("id").Is("id"),
                    AppSync.Values.Projecting("customer")
                ),
                ResponseMappingTemplate = AppSync.MappingTemplate.DynamoDbResultItem()
            });


            // Mutation resolver for creating a new customer along with their first order 
            customerDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Mutation",
                FieldName = "saveCustomerWithFirstOrder",
                RequestMappingTemplate = AppSync.MappingTemplate.DynamoDbPutItem(
                    AppSync.PrimaryKey.Partition("order").Auto().Sort("customer").Is("customer.id"),
                    AppSync.Values.Projecting("order").Attribute("referral").Is("referral")
                ),
                ResponseMappingTemplate = AppSync.MappingTemplate.DynamoDbResultItem()
            });

            // Mutation Resolver for deleting an exisiting Customer
            customerDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Mutation",
                FieldName = "removeCustomer",
                RequestMappingTemplate = AppSync.MappingTemplate.DynamoDbDeleteItem("id", "id"),
                ResponseMappingTemplate = AppSync.MappingTemplate.DynamoDbResultItem()
            });

            // defines an AWS Lambda resource
            _loyaltyLambda = new Lambda.Function(this, "LoyaltyLambdaHandler", new Lambda.FunctionProps
            {
                Runtime = Lambda.Runtime.NODEJS_12_X, // execution environment
                Code = Lambda.Code.FromAsset("lambda_fns"), // code loaded from the "lambda_fns" directory
                Handler = "loyalty.handler" // file is "loyalty", function is "handler"
            });
            
            /**
             * Add Loyalty Lambda as a Datasource for the Graphql API.
             */
            var loyaltyDS = _graphqlApi.AddLambdaDataSource("Loyalty", _loyaltyLambda);

            // Query Resolver to get all Customers
            loyaltyDS.CreateResolver(new AppSync.BaseResolverProps
            {
                TypeName = "Query",
                FieldName = "getLoyaltyLevel",
                RequestMappingTemplate = AppSync.MappingTemplate.LambdaRequest(),
                ResponseMappingTemplate = AppSync.MappingTemplate.LambdaResult()
            });

            // GraphQL API Endpoint
            new CfnOutput(this, "Endpoint", new CfnOutputProps
            {
                Value = _graphqlApi.GraphqlUrl
            });

            // API Key
            new CfnOutput(this, "API_Key", new CfnOutputProps
            {
                Value = _graphqlApi.ApiKey
            });

        }
    }
}
