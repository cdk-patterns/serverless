from aws_cdk import (
    aws_apigateway as api_gw,
    aws_iam as iam,
    aws_sns as sns,
    core
)
import json


class TheXrayTracerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # SNS Topic Creation
        # Our API Gateway posts messages directly to this
        ###
        topic = sns.Topic(self, 'TheXRayTracerSnsFanOutTopic', display_name='The XRay Tracer Fan Out Topic')
        self.sns_topic_arn = topic.topic_arn

        ###
        # API Gateway Creation
        # This is complicated because it is a direct SNS integration through VTL not a proxy integration
        # Tracing is enabled for X-Ray
        ###

        gateway = api_gw.RestApi(self, 'xrayTracerAPI',
                                 deploy_options=api_gw.StageOptions(
                                     metrics_enabled=True,
                                     logging_level=api_gw.MethodLoggingLevel.INFO,
                                     data_trace_enabled=True,
                                     tracing_enabled=True,
                                     stage_name='prod'
                                 ))

        # Give our gateway permissions to interact with SNS
        api_gw_sns_role = iam.Role(self, 'ApiGatewaySNSRole',
                                   assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))
        topic.grant_publish(api_gw_sns_role)

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

        request_template = "Action=Publish&" + \
                           "TargetArn=$util.urlEncode('" + topic.topic_arn + "')&" + \
                           "Message=$util.urlEncode($context.path)&" + \
                           "Version=2010-03-31"

        # This is the VTL to transform the error response
        error_template = {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }
        error_template_string = json.dumps(error_template, separators=(',', ':'))

        # This is how our gateway chooses what response to send based on selection_pattern
        integration_options = api_gw.IntegrationOptions(
            credentials_role=api_gw_sns_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates={
                "application/json": request_template
            },
            passthrough_behavior=api_gw.PassthroughBehavior.NEVER,
            integration_responses=[
                api_gw.IntegrationResponse(
                    status_code='200',
                    response_templates={
                        "application/json": json.dumps(
                            {"message": 'message added to topic'})
                    }),
                api_gw.IntegrationResponse(
                    selection_pattern="^\[Error\].*",
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

        method_responses = [
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

        # Add a / endpoint onto the gateway
        gateway.root \
            .add_method('GET', api_gw.Integration(type=api_gw.IntegrationType.AWS,
                                                  integration_http_method='POST',
                                                  uri='arn:aws:apigateway:us-east-1:sns:path//',
                                                  options=integration_options
                                                  ),
                        method_responses=method_responses
                        )

        # Add a {proxy+} endpoint onto the gateway
        gateway.root.add_resource('{proxy+}') \
            .add_method('GET', api_gw.Integration(type=api_gw.IntegrationType.AWS,
                                                  integration_http_method='POST',
                                                  uri='arn:aws:apigateway:us-east-1:sns:path//',
                                                  options=integration_options
                                                  ),
                        method_responses=method_responses
                        )
