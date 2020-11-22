from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_ec2 as ec2,
    aws_efs as efs,
    core
)


class TheEfsLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # EFS needs to be setup in a VPC
        vpc = ec2.Vpc(self, 'Vpc', max_azs=2)

        # Create a file system in EFS to store information
        fs = efs.FileSystem(self, 'FileSystem',
                            vpc=vpc,
                            removal_policy=core.RemovalPolicy.DESTROY)

        access_point = fs.add_access_point('AccessPoint',
                                           create_acl=efs.Acl(owner_gid='1001', owner_uid='1001', permissions='750'),
                                           path="/export/lambda",
                                           posix_user=efs.PosixUser(gid="1001", uid="1001"))

        efs_lambda = _lambda.Function(self, 'rdsProxyHandler',
                                      runtime=_lambda.Runtime.PYTHON_3_8,
                                      code=_lambda.Code.asset('lambda_fns'),
                                      handler='message_wall.lambda_handler',
                                      vpc=vpc,
                                      filesystem=_lambda.FileSystem.from_efs_access_point(access_point, '/mnt/msg'))

        # defines an API Gateway Http API resource backed by our "efs_lambda" function.
        api = api_gw.HttpApi(self, 'EFS Lambda',
                             default_integration=integrations.LambdaProxyIntegration(handler=efs_lambda));

        core.CfnOutput(self, 'HTTP API Url', value=api.url);