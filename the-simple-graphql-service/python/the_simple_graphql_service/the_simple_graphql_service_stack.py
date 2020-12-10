from aws_cdk import (
    aws_lambda as _lambda,
    aws_appsync as appsync,
    aws_dynamodb as dynamo_db,
    core
)
import os


class TheSimpleGraphqlServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        schema_location = os.path.dirname(os.path.realpath(__file__)) + "/../schema/schema.graphql"

        # Create a new AppSync GraphQL API
        api = appsync.GraphqlApi(self, 'Api',
                                 name="demoapi",
                                 log_config=appsync.LogConfig(field_log_level=appsync.FieldLogLevel.ALL),
                                 schema=appsync.Schema.from_asset(schema_location)
                                 )

        api_key = appsync.CfnApiKey(self, 'the-simple-graphql-service-api-key',
                                    api_id=api.api_id
                                    )

        # Create new DynamoDB Table for Customer
        customer_table = dynamo_db.Table(self, "CustomerTable",
                                         partition_key=dynamo_db.Attribute(name="id",
                                                                           type=dynamo_db.AttributeType.STRING)
                                         )

        # Add Customer DynamoDB as a Datasource for the Graphql API.
        customer_ds = api.add_dynamo_db_data_source('Customer', customer_table)

        # Query Resolver to get all Customers
        customer_ds.create_resolver(
            type_name='Query',
            field_name='getCustomers',
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list(),
        )

        # Query Resolver to get an individual Customer by their id
        customer_ds.create_resolver(
            type_name='Query',
            field_name='getCustomer',
            request_mapping_template=appsync.MappingTemplate.dynamo_db_get_item('id', 'id'),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item(),
        )

        # Mutation Resolver for adding a new Customer
        customer_ds.create_resolver(
            type_name='Mutation',
            field_name='addCustomer',
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                key=appsync.PrimaryKey.partition('id').auto(),
                values=appsync.Values.projecting('customer')
            ),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )

        # Mutation Resolver for updating an existing Customer
        customer_ds.create_resolver(
            type_name='Mutation',
            field_name='saveCustomer',
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                key=appsync.PrimaryKey.partition('id').is_('id'),
                values=appsync.Values.projecting('customer')
            ),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )

        #  Mutation resolver for creating a new customer along with their first order 
        customer_ds.create_resolver(
            type_name='Mutation',
            field_name='saveCustomerWithFirstOrder',
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                key=appsync.PrimaryKey.partition('order').auto().sort('customer').is_('customer.id'),
                values=appsync.Values.projecting('order').attribute('referral').is_('referral')
            ),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )

        # Mutation Resolver for deleting an existing Customer
        customer_ds.create_resolver(
            type_name='Mutation',
            field_name='removeCustomer',
            request_mapping_template=appsync.MappingTemplate.dynamo_db_delete_item('id', 'id'),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item(),
        )

        # defines an AWS  Lambda resource
        loyalty_lambda = _lambda.Function(self, "LoyaltyLambdaHandler",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="loyalty.handler",
                                          code=_lambda.Code.from_asset("lambda_fns"),
                                          )

        # Add Loyalty Lambda as a Datasource for the Graphql API.
        loyalty_ds = api.add_lambda_data_source('Loyalty', loyalty_lambda)

        # Query Resolver to get all Customers
        loyalty_ds.create_resolver(
            type_name='Query',
            field_name='getLoyaltyLevel',
            request_mapping_template=appsync.MappingTemplate.lambda_request(),
            response_mapping_template=appsync.MappingTemplate.lambda_result(),
        )

        # GraphQL API Endpoint
        core.CfnOutput(self, 'Endpoint',
                       value=api.graphql_url
                       )

        # API Key
        core.CfnOutput(self, 'API_Key',
                       value=api_key.attr_api_key
                       )
