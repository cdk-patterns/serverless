from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_dynamodb as dynamo_db,
    core
)


class TheSimpleWebserviceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamo_db.Table(self, "Hits",
                                partition_key=dynamo_db.Attribute(name="path", type=dynamo_db.AttributeType.STRING)
                                )

        # defines an AWS  Lambda resource
        dynamo_lambda = _lambda.Function(self, "DynamoLambdaHandler",
                                            runtime=_lambda.Runtime.NODEJS_12_X,    # execution environment
                                            handler="lambda.handler",               # file is "lambda", function is "handler"
                                            code=_lambda.Code.from_asset("lambda_fns"), # Code loaded from the lambda_fns dir
                                            environment={
                                                'HITS_TABLE_NAME': table.table_name
                                            }
                                        )

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(dynamo_lambda)


        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = api_gw.HttpApi(self, 'Endpoint', default_integration=integrations.LambdaProxyIntegration(handler=dynamo_lambda));
    
        core.CfnOutput(self, 'HTTP API Url', value=api.url);