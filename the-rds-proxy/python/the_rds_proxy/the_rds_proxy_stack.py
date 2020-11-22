from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secrets,
    aws_ssm as ssm,
    core
)


class TheRdsProxyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # RDS needs to be setup in a VPC
        vpc = ec2.Vpc(self, 'Vpc', max_azs=2)

        # We need this security group to add an ingress rule and allow our lambda to query the proxy
        lambda_to_proxy_group = ec2.SecurityGroup(self, 'Lambda to RDS Proxy Connection', vpc=vpc)

        # We need this security group to allow our proxy to query our MySQL Instance
        db_connection_group = ec2.SecurityGroup(self, 'Proxy to DB Connection', vpc=vpc)
        db_connection_group.add_ingress_rule(db_connection_group,ec2.Port.tcp(3306), 'allow db connection')
        db_connection_group.add_ingress_rule(lambda_to_proxy_group, ec2.Port.tcp(3306), 'allow lambda connection')

        db_credentials_secret = secrets.Secret(self, 'DBCredentialsSecret',
                                               secret_name=id+'-rds-credentials',
                                               generate_secret_string=secrets.SecretStringGenerator(
                                                   secret_string_template="{\"username\":\"syscdk\"}",
                                                   exclude_punctuation=True,
                                                   include_space=False,
                                                   generate_string_key="password"
                                               ))

        ssm.StringParameter(self, 'DBCredentialsArn',
                            parameter_name='rds-credentials-arn',
                            string_value=db_credentials_secret.secret_arn)

        # MySQL DB Instance (delete protection turned off because pattern is for learning.)
        # re-enable delete protection for a real implementation
        rds_instance = rds.DatabaseInstance(self,
                                            'DBInstance',
                                            engine=rds.DatabaseInstanceEngine.mysql(
                                                version=rds.MysqlEngineVersion.VER_5_7_30),
                                            credentials=rds.Credentials.from_secret(db_credentials_secret),
                                            instance_type=
                                            ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
                                            vpc=vpc,
                                            removal_policy=core.RemovalPolicy.DESTROY,
                                            deletion_protection=False,
                                            security_groups=[db_connection_group])

        # Create an RDS proxy
        proxy = rds_instance.add_proxy(id+'-proxy',
                                       secrets=[db_credentials_secret],
                                       debug_logging=True,
                                       vpc=vpc,
                                       security_groups=[db_connection_group])

        # Workaround for bug where TargetGroupName is not set but required
        target_group = proxy.node.find_child('ProxyTargetGroup')
        target_group.add_property_override('TargetGroupName', 'default')

        rds_lambda = _lambda.Function(self, 'rdsProxyHandler',
                                      runtime=_lambda.Runtime.NODEJS_12_X,
                                      code=_lambda.Code.asset('lambda_fns/rds'),
                                      handler='rdsLambda.handler',
                                      vpc=vpc,
                                      security_groups=[lambda_to_proxy_group],
                                      environment={
                                          "PROXY_ENDPOINT": proxy.endpoint,
                                          "RDS_SECRET_NAME": id+'-rds-credentials'
                                      })

        db_credentials_secret.grant_read(rds_lambda)

        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = api_gw.HttpApi(self, 'Endpoint',
                             default_integration=integrations.LambdaProxyIntegration(handler=rds_lambda));

        core.CfnOutput(self, 'HTTP API Url', value=api.url);
