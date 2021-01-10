from aws_cdk import (
    aws_lambda as _lambda,
    aws_sam as sam,
    core
)


class TheLambdaPowerTunerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        power_values = '128,256,512,1024,1536,3008'
        lambda_resource = '*'

        # An example lambda that can be used to test the powertuner
        example_lambda = _lambda.Function(self, "exampleLambda",
                                          runtime=_lambda.Runtime.NODEJS_12_X,
                                          handler="index.handler",
                                          code=_lambda.Code.from_inline("exports.handler = function(event, ctx, cb) { return cb(null, 'hi'); }"),
                                          )

        # uncomment to only allow this power tuner to manipulate this defined function
        # lambda_resource = example_lambda.function_arn

        # Output the Lambda function ARN in the deploy logs to ease testing
        core.CfnOutput(self, 'LambdaARN', value=example_lambda.function_arn)

        # Deploy the aws-lambda-powertuning application from the Serverless Application Repository
        # https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning
        sam.CfnApplication(self, 'powerTuner', location={
            "applicationId": "arn:aws:serverlessrepo:us-east-1:451282441545:applications/aws-lambda-power-tuning",
            "semanticVersion": "3.4.0"
        }, parameters={
            "lambdaResource": lambda_resource,
            "PowerValues": power_values
        })


