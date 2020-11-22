from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as dynamo_db,
    aws_s3_assets as assets,
    core,
    alexa_ask
)
from aws_cdk.aws_iam import (
    ServicePrincipal,
    Role,
    PolicyStatement,
    CompositePrincipal
)
import subprocess
import os


class TheAlexaSkillStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        alexa_assets = os.path.dirname(os.path.realpath(__file__)) + "/../skill"
        asset = assets.Asset(self, 'SkillAsset',
                             path=alexa_assets
                             )

        # role to access bucket
        role = Role(self, 'Role',
                    assumed_by=CompositePrincipal(
                        ServicePrincipal('alexa-appkit.amazon.com'),
                        ServicePrincipal('cloudformation.amazonaws.com')
                    )
                    )

        # Allow the skill resource to access the zipped skill package
        role.add_to_policy(PolicyStatement(
                           actions=['S3:GetObject'],
                           resources=[f'arn:aws:s3:::{asset.s3_bucket_name}/{asset.s3_object_key}']
                           )
                           )

        # DynamoDB Table
        users_table = dynamo_db.Table(self, 'Users',
                                      partition_key=dynamo_db.Attribute(name='userId', type=dynamo_db.AttributeType.STRING),
                                      billing_mode=dynamo_db.BillingMode.PAY_PER_REQUEST,
                                      removal_policy=core.RemovalPolicy.DESTROY
                                      )

        # install node dependencies for lambdas
        lambda_folder = os.path.dirname(os.path.realpath(__file__)) + "/../lambda_fns"
        subprocess.check_call("npm i".split(), cwd=lambda_folder, stdout=subprocess.DEVNULL)
        subprocess.check_call("npm run build".split(), cwd=lambda_folder, stdout=subprocess.DEVNULL)

        alexa_lambda = _lambda.Function(self, "AlexaLambdaHandler",
                                        runtime=_lambda.Runtime.NODEJS_12_X,
                                        code=_lambda.Code.from_asset("lambda_fns"),
                                        handler="lambda.handler",
                                        environment={
                                            "USERS_TABLE": users_table.table_name
                                        }
                                        )

        # grant the lambda role read/write permissions to our table
        users_table.grant_read_write_data(alexa_lambda)

        # create the skill
        skill = alexa_ask.CfnSkill(self, 'the-alexa-skill',
                                   vendor_id='',
                                   authentication_configuration={
                                       'clientId': '',
                                       'clientSecret': '',
                                       'refreshToken': ''
                                   },
                                   skill_package={
                                       's3Bucket': asset.s3_bucket_name,
                                       's3Key': asset.s3_object_key,
                                       's3BucketRole': role.role_arn,
                                       'overrides': {
                                           'manifest': {
                                               'apis': {
                                                   'custom': {
                                                       'endpoint': {
                                                           'uri': alexa_lambda.function_arn
                                                       }
                                                   }
                                               }
                                           }
                                       }
                                   }
                                   )

        ###
        # Allow the Alexa service to invoke the fulfillment Lambda.
        # In order for the Skill to be created, the fulfillment Lambda
        # must have a permission allowing Alexa to invoke it, this causes
        # a circular dependency and requires the first deploy to allow all
        # Alexa skills to invoke the lambda, subsequent deploys will work
        # when specifying the eventSourceToken
        ###
        alexa_lambda.add_permission('AlexaPermission',
                                    # eventSourceToken: skill.ref,
                                    principal=ServicePrincipal('alexa-appkit.amazon.com'),
                                    action='lambda:InvokeFunction'
                                    )
