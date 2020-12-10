from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_dynamodb as dynamo_db,
    core
)
import subprocess
import os


class TheLambdaCircuitBreakerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamo_db.Table(self, "CircuitBreakerTable",
                                partition_key=dynamo_db.Attribute(name="id", type=dynamo_db.AttributeType.STRING),
                                removal_policy=core.RemovalPolicy.DESTROY
                                )

        # install node dependencies for lambdas
        lambda_folder = os.path.dirname(os.path.realpath(__file__)) + "/../lambda_fns"
        subprocess.check_call("npm i".split(), cwd=lambda_folder, stdout=subprocess.DEVNULL)
        subprocess.check_call("npm run build".split(), cwd=lambda_folder, stdout=subprocess.DEVNULL)

        # defines an AWS Lambda resource with unreliable code
        unreliable_lambda = _lambda.Function(self, "UnreliableLambdaHandler",
                                             runtime=_lambda.Runtime.NODEJS_12_X,
                                             handler="unreliable.handler",
                                             code=_lambda.Code.from_asset("lambda_fns"),
                                             # Code loaded from the lambda_fns dir
                                             environment={
                                                 'CIRCUITBREAKER_TABLE': table.table_name
                                             }
                                             )

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(unreliable_lambda)

        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = api_gw.HttpApi(self, 'CircuitBreakerGateway',
                             default_integration=integrations.LambdaProxyIntegration(handler=unreliable_lambda));

        core.CfnOutput(self, 'HTTP API Url', value=api.url);
