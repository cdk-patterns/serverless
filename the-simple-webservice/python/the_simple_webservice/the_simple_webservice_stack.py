from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    core
)


class TheSimpleWebserviceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(self, "Hits",
                               partition_key=dynamodb.Attribute(name="path", type=dynamodb.AttributeType.STRING)
                               )

        # defines an AWS  Lambda resource
        dynamoLambda = _lambda.Function(self, "DynamoLambdaHandler",
                                        runtime=_lambda.Runtime.NODEJS_12_X,
                                        handler="lambda.handler",
                                        code=_lambda.Code.from_asset("lambda"),
                                        environment={
                                            'HITS_TABLE_NAME': table.table_name
                                        }
                                        )

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(dynamoLambda)

        # defines an API Gateway REST API resource backed by our "dynamoLambda" function.
        apigw.LambdaRestApi(self, 'Endpoint',
                            handler=dynamoLambda
                            )
