from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    core
)


class TheEventbridgeCircuitBreakerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        # This will store our error records
        # TTL Docs - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/time-to-live-ttl-how-to.html
        table = dynamo_db.Table(self, "CircuitBreaker",
                                partition_key=dynamo_db.Attribute(name="RequestID",
                                                                  type=dynamo_db.AttributeType.STRING),
                                sort_key=dynamo_db.Attribute(name="ExpirationTime",
                                                             type=dynamo_db.AttributeType.NUMBER),
                                time_to_live_attribute='ExpirationTime'
                                )

        # Add an index that lets us query on site url and Expiration Time
        table.add_global_secondary_index(
            index_name='UrlIndex',
            partition_key=dynamo_db.Attribute(name="SiteUrl", type=dynamo_db.AttributeType.STRING),
            sort_key=dynamo_db.Attribute(name="ExpirationTime", type=dynamo_db.AttributeType.NUMBER))

        # defines an Integration Lambda to call our failing web service
        integration_lambda = _lambda.Function(self, "WebserviceIntegrationLambdaHandler",
                                              runtime=_lambda.Runtime.NODEJS_12_X,
                                              handler="lambda.handler",
                                              code=_lambda.Code.from_asset("lambda_fns/webservice"),
                                              timeout=core.Duration.seconds(20),
                                              environment=dict(TABLE_NAME=table.table_name)
                                              )

        # grant the lambda role read/write permissions to our table
        table.grant_read_data(integration_lambda)

        # We need to give your lambda permission to put events on our EventBridge
        event_policy = iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=['*'], actions=['events:PutEvents'])
        integration_lambda.add_to_role_policy(event_policy)

        # defines a lambda to insert errors into dynamoDB
        error_lambda = _lambda.Function(self, "ErrorLambdaHandler",
                                        runtime=_lambda.Runtime.NODEJS_12_X,
                                        handler="lambda.handler",
                                        code=_lambda.Code.from_asset("lambda_fns/error"),
                                        timeout=core.Duration.seconds(3),
                                        environment=dict(TABLE_NAME=table.table_name)
                                        )

        table.grant_write_data(error_lambda)

        # Create EventBridge rule to route failures
        error_rule = events.Rule(self, 'webserviceErrorRule',
                                 description='Failed Webservice Call',
                                 event_pattern=events.EventPattern(source=['cdkpatterns.eventbridge.circuitbreaker'],
                                                                   detail_type=['httpcall'],
                                                                   detail={
                                                                       "status": ["fail"]
                                                                   }))

        error_rule.add_target(targets.LambdaFunction(handler=error_lambda))

        # defines an API Gateway REST API resource backed by our "integration_lambda" function
        api_gw.LambdaRestApi(self, 'CircuitBreakerGateway',
                             handler=integration_lambda
                             )
