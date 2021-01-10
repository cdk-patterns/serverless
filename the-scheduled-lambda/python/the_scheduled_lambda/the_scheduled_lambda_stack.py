from aws_cdk import (
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamo_db,
    core
)


class TheScheduledLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table = dynamo_db.Table(self, "RequestTable",
                                partition_key=dynamo_db.Attribute(name="requestid", type=dynamo_db.AttributeType.STRING),
                                removal_policy=core.RemovalPolicy.DESTROY
                                )

        # Create the Lambda function we want to run on a schedule
        scheduled_lambda = _lambda.Function(self, 'ScheduledLambda',
                                            runtime=_lambda.Runtime.NODEJS_12_X, # execution environment
                                            code=_lambda.Code.from_asset('lambda_fns'), # code loaded from the "lambda_fns" directory,
                                            handler='index.handler', # file is "index", function is "handler"
                                            environment={
                                                "TABLE_NAME": table.table_name
                                            })
        # Allow our lambda fn to write to the table
        table.grant_read_write_data(scheduled_lambda)

        # Create EventBridge rule that will execute our Lambda every 2 minutes
        schedule = events.Rule(self, 'scheduledLambda-schedule',
                               schedule=events.Schedule.expression('rate(2 minutes)'))
        #Set the target of our EventBridge rule to our Lambda function
        schedule.add_target(targets.LambdaFunction(scheduled_lambda))


