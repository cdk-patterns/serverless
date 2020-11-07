from aws_cdk import (
    aws_cloudformation as cfn,
    aws_logs as cwlogs,
    aws_lambda_python as py_lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    core
)


class Apigateway(cfn.NestedStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        api_log_group = cwlogs.LogGroup(self, "HelloWorldAPILogs")

        # Create the api gateway for this lambda set
        self.target_api = apigw.RestApi(self, 'HelloWorldAPI',
            rest_api_name='HelloWorld',
            endpoint_types= [apigw.EndpointType.REGIONAL],
            deploy_options={
                "access_log_destination": apigw.LogGroupLogDestination(api_log_group),
                "access_log_format": apigw.AccessLogFormat.clf(),
                "method_options": {
                    "/*/*": {# This special path applies to all resource paths and all HTTP methods
                        "throttling_rate_limit": 100,
                        "throttling_burst_limit": 200
                    }
                }
            }
        )

        hello_world =  py_lambda.PythonFunction(self, "HelloWorld",
            entry= 'thewafapigateway/lambda_fns',                           
            index = 'helloworld.py',                          
            handler = 'lambda_handler',                 
            description = 'Helloworld',
            timeout = core.Duration.seconds(60)
        )
        
        entity = self.target_api.root.add_resource('helloworld')  
        this_lambda_integration = apigw.LambdaIntegration(hello_world,proxy=False, integration_responses=
                [
                    {
                        'statusCode': '200',
                        'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        }
                    }
                ]
            )
        method = entity.add_method('GET', this_lambda_integration, 
                method_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                        }
                    }
                ]
            )

        self.resource_arn= f"arn:aws:apigateway:ap-southeast-2::/restapis/{self.target_api.rest_api_id}/stages/{self.target_api.deployment_stage.stage_name}"