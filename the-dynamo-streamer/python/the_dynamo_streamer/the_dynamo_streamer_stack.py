from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as _event,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    aws_iam as iam,
    core
)
import json


class TheDynamoStreamerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        # Streaming is enabled to send the whole new object down the pipe
        table = dynamo_db.Table(self, "TheDynamoStreamer",
                                partition_key=dynamo_db.Attribute(name="message",
                                                                  type=dynamo_db.AttributeType.STRING),
                                stream=dynamo_db.StreamViewType.NEW_IMAGE
                                )

        # defines an AWS  Lambda resource
        subscriber_lambda = _lambda.Function(self, "DynamoLambdaHandler",
                                             runtime=_lambda.Runtime.PYTHON_3_8,
                                             handler="lambda.handler",
                                             code=_lambda.Code.from_asset("lambda_fns/subscribe")
                                             )

        subscriber_lambda.add_event_source(_event.DynamoEventSource(table=table,
                                                                    starting_position=_lambda.StartingPosition.LATEST))

        # API Gateway Creation
        gateway = api_gw.RestApi(self, 'DynamoStreamerAPI',
                                 deploy_options=api_gw.StageOptions(metrics_enabled=True,
                                                                    logging_level=api_gw.MethodLoggingLevel.INFO,
                                                                    data_trace_enabled=True,
                                                                    stage_name='prod'
                                                                    ))

        # Give our gateway permissions to interact with dynamodb
        api_gw_dynamo_role = iam.Role(self, 'DefaultLambdaHanderRole',
                                      assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))
        table.grant_read_write_data(api_gw_dynamo_role)

        # shortening the lines of later code
        schema = api_gw.JsonSchema
        schema_type = api_gw.JsonSchemaType

        # Because this isn't a proxy integration, we need to define our response model
        response_model = gateway.add_model('ResponseModel',
                                           content_type='application/json',
                                           model_name='ResponseModel',
                                           schema=schema(schema=api_gw.JsonSchemaVersion.DRAFT4,
                                                         title='pollResponse',
                                                         type=schema_type.OBJECT,
                                                         properties={
                                                             'message': schema(type=schema_type.STRING)
                                                         }))

        error_response_model = gateway.add_model('ErrorResponseModel',
                                                 content_type='application/json',
                                                 model_name='ErrorResponseModel',
                                                 schema=schema(schema=api_gw.JsonSchemaVersion.DRAFT4,
                                                               title='errorResponse',
                                                               type=schema_type.OBJECT,
                                                               properties={
                                                                   'state': schema(type=schema_type.STRING),
                                                                   'message': schema(type=schema_type.STRING)
                                                               }))

        # This is the VTL to transform our incoming JSON to a Dynamo Insert Query
        request_template = {
            "TableName": table.table_name,
            "Item": {
                "message": {"S": "$input.path('$.message')"}
            }
        }
        request_template_string = json.dumps(request_template, separators=(',', ':'))

        # This is the VTL to transform the error response
        error_template = {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }
        error_template_string = json.dumps(error_template, separators=(',', ':'))

        # This is how our gateway chooses what response to send based on selection_pattern
        integration_options = api_gw.IntegrationOptions(
            credentials_role=api_gw_dynamo_role,
            request_templates={
                "application/json": request_template_string
            },
            passthrough_behavior=api_gw.PassthroughBehavior.NEVER,
            integration_responses=[
                api_gw.IntegrationResponse(
                    status_code='200',
                    response_templates={
                        "application/json": json.dumps(
                            {"message": 'item added to db'})
                    }),
                api_gw.IntegrationResponse(
                    selection_pattern="^\[BadRequest\].*",
                    status_code='400',
                    response_templates={
                        "application/json": error_template_string
                    },
                    response_parameters={
                        'method.response.header.Content-Type': "'application/json'",
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        'method.response.header.Access-Control-Allow-Credentials': "'true'"
                    }
                )
            ]
        )

        # Add an InsertItem endpoint onto the gateway
        gateway.root.add_resource('InsertItem') \
            .add_method('POST', api_gw.Integration(type=api_gw.IntegrationType.AWS,
                                                   integration_http_method='POST',
                                                   uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
                                                   options=integration_options
                                                   ),
                        method_responses=[
                            api_gw.MethodResponse(status_code='200',
                                                  response_parameters={
                                                      'method.response.header.Content-Type': True,
                                                      'method.response.header.Access-Control-Allow-Origin': True,
                                                      'method.response.header.Access-Control-Allow-Credentials': True
                                                  },
                                                  response_models={
                                                      'application/json': response_model
                                                  }),
                            api_gw.MethodResponse(status_code='400',
                                                  response_parameters={
                                                      'method.response.header.Content-Type': True,
                                                      'method.response.header.Access-Control-Allow-Origin': True,
                                                      'method.response.header.Access-Control-Allow-Credentials': True
                                                  },
                                                  response_models={
                                                      'application/json': error_response_model
                                                  }),
                        ]
                        )
