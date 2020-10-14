from aws_cdk import (
    aws_lambda_nodejs as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_dynamodb as dynamo_db,
    core
)
import os


class TheLambdaCircuitBreakerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table to hold Circuitbreaker State
        table = dynamo_db.Table(self, "CircuitBreakerTable",
                                partition_key=dynamo_db.Attribute(name="id", type=dynamo_db.AttributeType.STRING),
                                removal_policy=core.RemovalPolicy.DESTROY
                                )

        # Get the path to directory containing this file
        dir_path = os.path.dirname(os.path.realpath(__file__))+"/"

        # defines an AWS Lambda resource with unreliable code
        unreliable_lambda = _lambda.NodejsFunction(self, "UnreliableLambdaHandler",
                                                   entry=dir_path+"../lambda-fns/unreliable.ts",
                                                   handler="handler",
                                                   environment={
                                                       "CIRCUITBREAKER_TABLE": table.table_name
                                                   })

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(unreliable_lambda)

        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = api_gw.HttpApi(self, 'CircuitBreakerGateway',
                             default_integration=api_gw.LambdaProxyIntegration(handler=unreliable_lambda));

        core.CfnOutput(self, 'HTTP API Url', value=api.url);
