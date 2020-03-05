from aws_cdk import (
    aws_lambda as _lambda,
    aws_appsync as appsync,
    aws_cognito as cognito,
    aws_dynamodb as dynamo_db,
    core
)

class TheSimpleGraphqlServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a new Cognito User Pool
        userPool = cognito.UserPool(self, 'UserPool',
            sign_in_aliases=cognito.SignInAliases(username=True)
        )

        # Create a new AppSync GraphQL API
        api = appsync.GraphQLApi(self, 'Api',
            name= "demoapi",
            log_config={
                appsync.LogConfig(field_log_level=appsync.FieldLogLevel.ALL)
            },
            #  User pool authorizer configuration
            #  userPoolConfig={
            #    userPool,
            #    defaultAction: UserPoolDefaultAction.ALLOW,
            #  },
            schema_definition_file=join('__dirname', '/../', 'schema/schema.graphql'),
        )

        # Create new DynamoDB Table for Customer
        customerTable = dynamo_db.Table(self, "CustomerTable",
                                partition_key=dynamo_db.Attribute(name="id", type=dynamo_db.AttributeType.STRING)
                                )
                                
        # Add Customer DynamoDB as a Datasource for the Graphql API.
        customerDS = api.add_dynamo_db_data_source('Customer', 'The customer data source', customerTable)

        # Query Resolver to get all Customers
        customerDS.createResolver(
            type_name = 'Query',
            field_ame = 'getCustomers',
            request_mapping_template = appsync.MappingTemplate.dynamoDbScanTable(),
            responseMappingTemplate = appsync.MappingTemplate.dynamoDbResultList(),
        )

        # Query Resolver to get an individual Customer by their id
        customerDS.createResolver(
        type_name = 'Query',
        field_ame = 'getCustomer',
        request_mapping_template = appsync.MappingTemplate.dynamoDbGetItem('id', 'id'),
        responseMappingTemplate = appsync.MappingTemplate.dynamo_db_result_item(),
        )

        # Mutation Resolver for adding a new Customer
        customerDS.createResolver(
        type_name = 'Mutation',
        field_ame = 'addCustomer',
        request_mapping_template = appsync.MappingTemplate.dynamo_db_put_item(
            key=appsync.PrimaryKey.partition('id').auto(),
            values=appsync.AttributeValues.projecting('customer')),
        responseMappingTemplate = appsync.MappingTemplate.dynamo_db_result_item(),
        )

        # Mutation Resolver for updating an exisiting Customer
        customerDS.createResolver(
        type_name = 'Mutation',
        field_ame = 'saveCustomerWithFirstOrder',
        request_mapping_template = appsync.MappingTemplate.dynamo_db_put_item(
            key=appsync.PrimaryKey
                .partition('order').auto()
                .sort('customer').is_('customer.id'),
            Values=
                appsync.projecting('order')
                .attribute('referral').is_('referral')),
        responseMappingTemplate = appsync.MappingTemplate.dynamo_db_result_item(),
        )

        # Mutation Resolver for deleting an exisiting Customer
        customerDS.createResolver(
        type_name = 'Mutation',
        field_ame = 'removeCustomer',
        request_mapping_template = appsync.MappingTemplate.dynamoDbDeleteItem('id', 'id'),
        responseMappingTemplate = appsync.MappingTemplate.dynamo_db_result_item(),
        )

        # defines an AWS  Lambda resource
        loyalty_lambda = _lambda.Function(self, "LoyaltyLambdaHandler",
                                            runtime=_lambda.Runtime.NODEJS_12_X,    # execution environment
                                            handler="loyalty.handler",              # file is "loyalty", function is "handler"
                                            code=_lambda.Code.from_asset("lambda"), # Code loaded from the lambda dir
                                        )

        # Add Loyalty Lambda as a Datasource for the Graphql API.
        loyaltyDS = api.addLambdaDataSource('Loyalty', 'The loyalty data source', loyalty_lambda)

        # Query Resolver to get all Customers
        loyaltyDS.createResolver(
        type_name = 'Query',
        field_ame = 'getLoyaltyLevel',
        request_mapping_template = appsync.MappingTemplate.lambdaRequest(),
        responseMappingTemplate = appsync.MappingTemplate.lambdaResult(),
        )