from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as _event,
    aws_apigateway as api_gw,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_sqs as sqs,
    core
)
import json


class TheBigFanStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # SNS Topic Creation
        # Our API Gateway posts messages directly to this
        ###
        topic = sns.Topic(self, 'theBigFanTopic', display_name='The Big Fan CDK Pattern Topic')

        ###
        # SQS Subscribers creation for our SNS Topic
        # 2 subscribers, one for messages with a status of created one for any other message
        ###

        # Status:created SNS Subscriber Queue
        created_status_queue = sqs.Queue(self, 'BigFanTopicStatusCreatedSubscriberQueue',
                                         visibility_timeout=core.Duration.seconds(300),
                                         queue_name='BigFanTopicStatusCreatedSubscriberQueue')

        # Only send messages to our created_status_queue with a status of created
        created_filter = sns.SubscriptionFilter.string_filter(whitelist=['created'])
        topic.add_subscription(subscriptions.SqsSubscription(created_status_queue,
                                                             raw_message_delivery=True,
                                                             filter_policy={'status': created_filter}))

        # Any other status SNS Subscriber Queue
        other_status_queue = sqs.Queue(self, 'BigFanTopicAnyOtherStatusSubscriberQueue',
                                       visibility_timeout=core.Duration.seconds(300),
                                       queue_name='BigFanTopicAnyOtherStatusSubscriberQueue')

        # Only send messages to our other_status_queue that do not have a status of created
        other_filter = sns.SubscriptionFilter.string_filter(blacklist=['created'])
        topic.add_subscription(subscriptions.SqsSubscription(other_status_queue,
                                                             raw_message_delivery=True,
                                                             filter_policy={'status': other_filter}))

        ###
        # Creation of Lambdas that subscribe to above SQS queues
        ###

        # Created status queue lambda
        sqs_created_status_subscriber = _lambda.Function(self, "SQSCreatedStatusSubscribeLambdaHandler",
                                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                                         handler="createdStatus.handler",
                                                         code=_lambda.Code.from_asset("lambda_fns/subscribe")
                                                         )
        created_status_queue.grant_consume_messages(sqs_created_status_subscriber)
        sqs_created_status_subscriber.add_event_source(_event.SqsEventSource(created_status_queue))

        # Any other status queue lambda
        sqs_other_status_subscriber = _lambda.Function(self, "SQSAnyOtherStatusSubscribeLambdaHandler",
                                                       runtime=_lambda.Runtime.PYTHON_3_8,
                                                       handler="anyOtherStatus.handler",
                                                       code=_lambda.Code.from_asset("lambda_fns/subscribe")
                                                       )
        other_status_queue.grant_consume_messages(sqs_other_status_subscriber)
        sqs_other_status_subscriber.add_event_source(_event.SqsEventSource(other_status_queue))

        ###
        # API Gateway Creation
        # This is complicated because it transforms the incoming json payload into a query string url
        # this url is used to post the payload to sns without a lambda inbetween
        ###

        gateway = api_gw.RestApi(self, 'theBigFanAPI',
                                 deploy_options=api_gw.StageOptions(metrics_enabled=True,
                                                                    logging_level=api_gw.MethodLoggingLevel.INFO,
                                                                    data_trace_enabled=True,
                                                                    stage_name='prod'
                                                                    ))

        # Give our gateway permissions to interact with SNS
        api_gw_sns_role = iam.Role(self, 'DefaultLambdaHanderRole',
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
                           "Message=$util.urlEncode($input.path('$.message'))&" + \
                           "Version=2010-03-31&" + \
                           "MessageAttributes.entry.1.Name=status&" + \
                           "MessageAttributes.entry.1.Value.DataType=String&" + \
                           "MessageAttributes.entry.1.Value.StringValue=$util.urlEncode($input.path('$.status'))"

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

        # Add an SendEvent endpoint onto the gateway
        gateway.root.add_resource('SendEvent') \
            .add_method('POST', api_gw.Integration(type=api_gw.IntegrationType.AWS,
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
