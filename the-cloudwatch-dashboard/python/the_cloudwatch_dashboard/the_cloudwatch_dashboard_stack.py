from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_dynamodb as dynamo_db,
    aws_sns as sns,
    aws_cloudwatch as cloud_watch,
    aws_cloudwatch_actions as actions,
    core
)
import jsii


class TheCloudwatchDashboardStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # -----------------------------------------------------------------------------------------------------------
        # The Simple Webservice Logic - This is what we will be monitoring
        #
        # API GW HTTP API, Lambda Fn and DynamoDB
        # https://github.com/cdk-patterns/serverless/tree/master/the-simple-webservice
        # -----------------------------------------------------------------------------------------------------------

        # DynamoDB Table
        table = dynamo_db.Table(self, "Hits",
                                partition_key=dynamo_db.Attribute(name="path", type=dynamo_db.AttributeType.STRING),
                                billing_mode=dynamo_db.BillingMode.PAY_PER_REQUEST
                                )

        # defines an AWS  Lambda resource
        dynamo_lambda = _lambda.Function(self, "DynamoLambdaHandler",
                                         runtime=_lambda.Runtime.NODEJS_12_X,  # execution environment
                                         handler="lambda.handler",  # file is "lambda", function is "handler"
                                         code=_lambda.Code.from_asset("lambda_fns"),  # Code loaded from the lambda dir
                                         environment={
                                             'HITS_TABLE_NAME': table.table_name
                                         }
                                         )

        # grant the lambda role read/write permissions to our table'
        table.grant_read_write_data(dynamo_lambda)

        # defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        api = api_gw.HttpApi(self, 'HttpAPI',
                             default_integration=integrations.LambdaProxyIntegration(handler=dynamo_lambda));

        core.CfnOutput(self, 'HTTP API Url', value=api.url);

        # -----------------------------------------------------------------------------------------------------------
        # Monitoring Logic Starts Here
        #
        # This is everything we need to understand the state of our system:
        # - custom metrics
        # - cloudwatch alarms
        # - custom cloudwatch dashboard
        # -----------------------------------------------------------------------------------------------------------

        # SNS Topic so we can hook things into our alerts e.g. email
        error_topic = sns.Topic(self, 'theBigFanTopic')

        ###
        # Custom Metrics
        ###

        api_gw_4xx_error_percentage = cloud_watch.MathExpression(expression="m1/m2*100",
                                                                 label="% API Gateway 4xx Errors",
                                                                 using_metrics={
                                                                     "m1": self.metric_for_api_gw(
                                                                         api.http_api_id,
                                                                         '4XXError',
                                                                         '4XX Errors',
                                                                         'sum'),
                                                                     "m2": self.metric_for_api_gw(
                                                                         api.http_api_id,
                                                                         'Count',
                                                                         '# Requests',
                                                                         'sum'),
                                                                 },
                                                                 period=core.Duration.minutes(5))

        # Gather the % of lambda invocations that error in past 5 mins
        lambda_error_perc = cloud_watch.MathExpression(expression="e / i * 100",
                                                       label="% of invocations that errored, last 5 mins",
                                                       using_metrics={
                                                           "i": dynamo_lambda.metric(metric_name="Invocations",
                                                                                     statistic="sum"),
                                                           "e": dynamo_lambda.metric(metric_name="Errors",
                                                                                     statistic="sum"),
                                                       },
                                                       period=core.Duration.minutes(5))

        # note: throttled requests are not counted in total num of invocations
        lambda_throttled_perc = cloud_watch.MathExpression(expression="t / (i + t) * 100",
                                                           label="% of throttled requests, last 30 mins",
                                                           using_metrics={
                                                               "i": dynamo_lambda.metric(metric_name="Invocations",
                                                                                         statistic="sum"),
                                                               "t": dynamo_lambda.metric(metric_name="Throttles",
                                                                                         statistic="sum"),
                                                           },
                                                           period=core.Duration.minutes(5))

        # I think usererrors are at an account level rather than a table level so merging
        # these two metrics until I can get a definitive answer. I think usererrors
        # will always show as 0 when scoped to a table so this is still effectively
        # a system errors count
        dynamo_db_total_errors = cloud_watch.MathExpression(expression="m1 + m2",
                                                            label="DynamoDB Errors",
                                                            using_metrics={
                                                                "m1": table.metric_user_errors(),
                                                                "m2": table.metric_system_errors_for_operations(),
                                                            },
                                                            period=core.Duration.minutes(5))

        # Rather than have 2 alerts, let's create one aggregate metric
        dynamo_db_throttles = cloud_watch.MathExpression(expression="m1 + m2",
                                                         label="DynamoDB Throttles",
                                                         using_metrics={
                                                             "m1": table.metric(metric_name="ReadThrottleEvents",
                                                                                statistic="sum"),
                                                             "m2": table.metric(metric_name="WriteThrottleEvents",
                                                                                statistic="sum"),
                                                         },
                                                         period=core.Duration.minutes(5))
        ###
        # Alarms
        ###

        # Api Gateway

        # 4xx are user errors so a large volume indicates a problem
        cloud_watch.Alarm(self,
                          id="API Gateway 4XX Errors > 1%",
                          metric=api_gw_4xx_error_percentage,
                          threshold=1,
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        # 5xx are internal server errors so we want 0 of these
        cloud_watch.Alarm(self,
                          id="API Gateway 5XX Errors > 0",
                          metric=self.metric_for_api_gw(api_id=api.http_api_id,
                                                        metric_name="5XXError",
                                                        label="5XX Errors",
                                                        stat="p99"),
                          threshold=0,
                          period=core.Duration.minutes(5),
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        cloud_watch.Alarm(self,
                          id="API p99 latency alarm >= 1s",
                          metric=self.metric_for_api_gw(api_id=api.http_api_id,
                                                        metric_name="Latency",
                                                        label="API GW Latency",
                                                        stat="p99"),
                          threshold=1000,
                          period=core.Duration.minutes(5),
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        # Lambda

        # 2% of Dynamo Lambda invocations erroring
        cloud_watch.Alarm(self,
                          id="Dynamo Lambda 2% Error",
                          metric=lambda_error_perc,
                          threshold=2,
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        # 1% of Lambda invocations taking longer than 1 second
        cloud_watch.Alarm(self,
                          id="Dynamo Lambda p99 Long Duration (>1s)",
                          metric=dynamo_lambda.metric_duration(),
                          period=core.Duration.minutes(5),
                          threshold=1000,
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          statistic="p99",
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        # 2% of our lambda invocations are throttled
        cloud_watch.Alarm(self,
                          id="Dynamo Lambda 2% Throttled",
                          metric=lambda_throttled_perc,
                          threshold=2,
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        # DynamoDB

        # DynamoDB Interactions are throttled - indicated poorly provisioned
        cloud_watch.Alarm(self,
                          id="DynamoDB Table Reads/Writes Throttled",
                          metric=dynamo_db_throttles,
                          threshold=1,
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        # There should be 0 DynamoDB errors
        cloud_watch.Alarm(self,
                          id="DynamoDB Errors > 0",
                          metric=dynamo_db_total_errors,
                          threshold=0,
                          evaluation_periods=6,
                          datapoints_to_alarm=1,
                          treat_missing_data=cloud_watch.TreatMissingData.NOT_BREACHING) \
            .add_alarm_action(actions.SnsAction(error_topic))

        dashboard = cloud_watch.Dashboard(self, id="CloudWatchDashBoard")
        dashboard.add_widgets(cloud_watch.GraphWidget(title="Requests",
                                                      width=8,
                                                      left=[self.metric_for_api_gw(api_id=api.http_api_id,
                                                                                   metric_name="Count",
                                                                                   label="# Requests",
                                                                                   stat="sum")]),
                              cloud_watch.GraphWidget(title="API GW Latency",
                                                      width=8,
                                                      stacked=True,
                                                      left=[self.metric_for_api_gw(api_id=api.http_api_id,
                                                                                   metric_name="Latency",
                                                                                   label="API Latency p50",
                                                                                   stat="p50"),
                                                            self.metric_for_api_gw(api_id=api.http_api_id,
                                                                                   metric_name="Latency",
                                                                                   label="API Latency p90",
                                                                                   stat="p90"),
                                                            self.metric_for_api_gw(api_id=api.http_api_id,
                                                                                   metric_name="Latency",
                                                                                   label="API Latency p99",
                                                                                   stat="p99")
                                                            ]),
                              cloud_watch.GraphWidget(title="API GW Errors",
                                                      width=8,
                                                      stacked=True,
                                                      left=[self.metric_for_api_gw(api_id=api.http_api_id,
                                                                                   metric_name="4XXError",
                                                                                   label="4XX Errors",
                                                                                   stat="sum"),
                                                            self.metric_for_api_gw(api_id=api.http_api_id,
                                                                                   metric_name="5XXError",
                                                                                   label="5XX Errors",
                                                                                   stat="sum")
                                                            ]),
                              cloud_watch.GraphWidget(title="Dynamo Lambda Error %",
                                                      width=8,
                                                      left=[lambda_error_perc]),
                              cloud_watch.GraphWidget(title="Dynamo Lambda Duration",
                                                      width=8,
                                                      stacked=True,
                                                      left=[dynamo_lambda.metric_duration(statistic="p50"),
                                                            dynamo_lambda.metric_duration(statistic="p90"),
                                                            dynamo_lambda.metric_duration(statistic="p99")]),
                              cloud_watch.GraphWidget(title="Dynamo Lambda Throttle %",
                                                      width=8,
                                                      left=[lambda_throttled_perc]),
                              cloud_watch.GraphWidget(title="DynamoDB Latency",
                                                      width=8,
                                                      stacked=True,
                                                      left=[table.metric_successful_request_latency(
                                                              dimensions={"TableName": table.table_name,
                                                                          "Operation": "GetItem"}),
                                                            table.metric_successful_request_latency(
                                                              dimensions={"TableName": table.table_name,
                                                                          "Operation": "UpdateItem"}),
                                                            table.metric_successful_request_latency(
                                                              dimensions={"TableName": table.table_name,
                                                                          "Operation": "PutItem"}),
                                                            table.metric_successful_request_latency(
                                                              dimensions={"TableName": table.table_name,
                                                                          "Operation": "DeleteItem"}),
                                                            table.metric_successful_request_latency(
                                                              dimensions={"TableName": table.table_name,
                                                                          "Operation": "Query"}),
                                                            ]),
                              cloud_watch.GraphWidget(title="DynamoDB Consumed Read/Write Units",
                                                      width=8,
                                                      stacked=False,
                                                      left=[table.metric(metric_name="ConsumedReadCapacityUnits"),
                                                            table.metric(metric_name="ConsumedWriteCapacityUnits")]),
                              cloud_watch.GraphWidget(title="DynamoDB Throttles",
                                                      width=8,
                                                      stacked=True,
                                                      left=[table.metric(metric_name="ReadThrottleEvents",
                                                                         statistic="sum"),
                                                            table.metric(metric_name="WriteThrottleEvents",
                                                                         statistic="sum")]),
                              )

    @jsii.implements(cloud_watch.IMetric)
    def metric_for_api_gw(self, api_id: str, metric_name: str, label: str, stat: str = 'avg'):
        return self.build_metric(metric_name, "AWS/ApiGateway", {"ApiId": api_id}, cloud_watch.Unit.COUNT, label, stat)

    @staticmethod
    def build_metric(metric_name: str, name_space: str, dimensions, unit: cloud_watch.Unit, label: str,
                     stat: str = 'avg', period: int = 900):
        return cloud_watch.Metric(metric_name=metric_name,
                                  namespace=name_space,
                                  dimensions=dimensions,
                                  unit=unit,
                                  label=label,
                                  statistic=stat,
                                  period=core.Duration.seconds(period))
