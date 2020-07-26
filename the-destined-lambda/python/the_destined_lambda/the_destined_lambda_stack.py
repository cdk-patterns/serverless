from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_destinations as destinations,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_apigateway as api_gw,
    core
)
import json


class TheDestinedLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # Let's create our own Event Bus for this rather than using default
        ###
        bus = events.EventBus(self, 'DestinedEventBus', event_bus_name='the-destined-lambda')

        ###
        # Destinations need invoked Asynchronously so let's use SNS
        ###
        topic = sns.Topic(self, 'theDestinedLambdaTopic', display_name='The Destined Lambda CDK Pattern Topic')

        ###
        # Lambda configured with success and failure destinations
        # Note the actual lambda has no EventBridge code inside it
        ###
        destined_lambda = _lambda.Function(self, "destinedLambda",
                                           runtime=_lambda.Runtime.NODEJS_12_X,
                                           handler="destinedLambda.handler",
                                           code=_lambda.Code.from_asset("lambda_fns"),
                                           retry_attempts=0,
                                           on_success=destinations.EventBridgeDestination(event_bus=bus),
                                           on_failure=destinations.EventBridgeDestination(event_bus=bus)
                                           )
        topic.add_subscription(subscriptions.LambdaSubscription(destined_lambda))

        ###
        # This is a lambda that will be called by onSuccess for destinedLambda
        # It simply prints the event it receives to the cloudwatch logs
        ###
        success_lambda = _lambda.Function(self, "successLambda",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="success.handler",
                                          code=_lambda.Code.from_asset("lambda_fns"),
                                          timeout=core.Duration.seconds(3)
                                          )
        ###
        # EventBridge Rule to send events to our success lambda
        # Notice how we can still do event filtering based on the json payload returned by the destined lambda
        ###
        success_rule = events.Rule(self, 'successRule',
                                   event_bus=bus,
                                   description='all success events are caught here and logged centrally',
                                   event_pattern=events.EventPattern(
                                       detail={
                                           "requestContext": {
                                               "condition": ["Success"]
                                           },
                                           "responsePayload": {
                                               "source": ["cdkpatterns.the-destined-lambda"],
                                               "action": ["message"]
                                           }
                                       }))
        success_rule.add_target(targets.LambdaFunction(success_lambda))

        ###
        # This is a lambda that will be called by onFailure for destinedLambda
        # It simply prints the event it receives to the cloudwatch logs.
        # Notice how it includes the message that came into destined lambda to make it fail so you have
        # everything you need to do retries or manually investigate
        ###
        failure_lambda = _lambda.Function(self, "failureLambda",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="failure.handler",
                                          code=_lambda.Code.from_asset("lambda_fns"),
                                          timeout=core.Duration.seconds(3)
                                          )

        ###
        # EventBridge Rule to send events to our failure lambda
        ###
        failure_rule = events.Rule(self, 'failureRule',
                                   event_bus=bus,
                                   description='all failure events are caught here and logged centrally',
                                   event_pattern=events.EventPattern(
                                       detail={
                                           "responsePayload": {
                                               "errorType": ["Error"]
                                           }
                                       }))
        failure_rule.add_target(targets.LambdaFunction(failure_lambda))

        ###
        # API Gateway Creation
        # This is complicated because it transforms the incoming json payload into a query string url
        # this url is used to post the payload to sns without a lambda inbetween
        ###

        gateway = api_gw.RestApi(self, 'theDestinedLambdaAPI',
                                 deploy_options=api_gw.StageOptions(metrics_enabled=True,
                                                                    logging_level=api_gw.MethodLoggingLevel.INFO,
                                                                    data_trace_enabled=True,
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
                           "Message=please $input.params().querystring.get('mode')&" + \
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
                            {"message": 'Message added to SNS topic'})
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

        # Add an SendEvent endpoint onto the gateway
        gateway.root.add_resource('SendEvent') \
            .add_method('GET', api_gw.Integration(type=api_gw.IntegrationType.AWS,
                                                  integration_http_method='POST',
                                                  uri='arn:aws:apigateway:us-east-1:sns:path//',
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
