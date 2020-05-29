import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import cloudwatch = require('@aws-cdk/aws-cloudwatch');
import { GraphWidget, IMetric } from "@aws-cdk/aws-cloudwatch";
import { SnsAction } from '@aws-cdk/aws-cloudwatch-actions';
import sns = require('@aws-cdk/aws-sns');

export class TheCloudwatchDashboardStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    /**
     * The Simple Webservice Logic
     * 
     * API GW HTTP API, Lambda Fn and DynamoDB
     */

    //DynamoDB Table
    const table = new dynamodb.Table(this, 'Hits', {
      partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
    });

    // defines an AWS Lambda resource
    const dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambda'),
      handler: 'lambda.handler',
      environment: {
        HITS_TABLE_NAME: table.tableName
      }
    });

    // grant the lambda role read/write permissions to our table
    table.grantReadWriteData(dynamoLambda);

    // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
    let api = new apigw.HttpApi(this, 'HttpAPI', {
      defaultIntegration: new apigw.LambdaProxyIntegration({
        handler: dynamoLambda
      })
    });

    /**
     * Monitoring Logic
     * 
     * This is everything we need to understand the state of our system:
     * - custom metrics
     * - cloudwatch alarms
     * - custom cloudwatch dashboard
     */

    //SNS Topic so we can hook things into our alerts e.g. email
    const errorTopic = new sns.Topic(this, 'errorTopic');

    /**
     * Custom Metrics
     */

    // Gather the % of lambda invocations that error in past 30 mins
    let dynamoLambdaErrorPercentage = new cloudwatch.MathExpression({
      expression: 'e / i * 100',
      usingMetrics: {
        i: dynamoLambda.metric("Invocations", {statistic: 'sum'}),
        e: dynamoLambda.metric("Errors", {statistic: 'sum'}),
      },
      period: cdk.Duration.minutes(30)
    });

    // note: throttled requests are not counted in total num of invocations
    let dynamoLambdaThrottledPercentage = new cloudwatch.MathExpression({
      expression: 't / (i + t) * 100',
      usingMetrics: {
        i: dynamoLambda.metric("Invocations", {statistic: 'sum'}),
        t: dynamoLambda.metric("Throttles", {statistic: 'sum'}),
      },
      period: cdk.Duration.minutes(30)
    });
    
    /**
     * Alarms
     */

    // Lambda

    // Add an alarm for when over 2%
    dynamoLambdaErrorPercentage.createAlarm(this, 'Dynamo Lambda 2% Error Alarm', {
      threshold: 2,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));

    // Add alarm for Lambda invocations taking longer than 1 second
    new cloudwatch.Alarm(this, 'Dynamo Lambda Long Duration Alarm', {
      metric: dynamoLambda.metricDuration(),
      threshold: 1000,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));

    // Add alarm for if 2% of our calls are throttled
    new cloudwatch.Alarm(this, 'Dynamo Lambda 2% Throttled Alarm', {
      metric: dynamoLambdaThrottledPercentage,
      threshold: 2,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));

    // DynamoDB

    // Add alarm for throttled reads to dynamo
    new cloudwatch.Alarm(this, 'DynamoDB Table Reads Throttled Alarm', {
      metric: table.metric('ReadThrottleEvents', {statistic: 'sum'}),
      threshold: 1,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));

    // Add alarm for throttled writes to dynamo
    new cloudwatch.Alarm(this, 'DynamoDB Table Writes Throttled Alarm', {
      metric: table.metric('WriteThrottleEvents', {statistic: 'sum'}),
      threshold: 1,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));
    
    // Add alarm for if a user executes a bad query against our table
    new cloudwatch.Alarm(this, 'DynamoDB Table User Error Alarm', {
      metric: table.metric('UserErrors', {statistic: 'sum'}),
      threshold: 1,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));

    // Add alarm for if something is wrong with our table
    new cloudwatch.Alarm(this, 'DynamoDB Table System Error Alarm', {
      metric: table.metric('SystemErrors', {statistic: 'sum'}),
      threshold: 1,
      evaluationPeriods: 3,
      datapointsToAlarm: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING
    }).addAlarmAction(new SnsAction(errorTopic));

    /**
     * Custom Cloudwatch Dashboard 
     */  
    
    new cloudwatch.Dashboard(this, 'CloudWatchDashBoard').addWidgets(
      this.buildGraphWidget('API GW Count', [
        this.metricForApiGw(api.httpApiId, 'Count', '# Requests', 'sum')
      ]),
      this.buildGraphWidget('API GW Latency', [
        this.metricForApiGw(api.httpApiId, 'Latency', 'API Latency p95', 'p95')
      ]),
      this.buildGraphWidget('API GW Errors', [
        this.metricForApiGw(api.httpApiId, '4XXError', '4XX Errors', 'sum'),
        this.metricForApiGw(api.httpApiId, '5XXError', '5XX Errors', 'sum')
      ], true),
      this.buildGraphWidget('Dynamo Lambda Error %', [dynamoLambdaErrorPercentage]),
      this.buildGraphWidget('Dynamo Lambda Average Duration', [dynamoLambda.metricDuration()]),
      this.buildGraphWidget('Dynamo Lambda Throttle %', [dynamoLambdaThrottledPercentage]),
      this.buildGraphWidget('DynamoDB System Errors', [table.metric('SystemErrors')]),
      this.buildGraphWidget('DynamoDB User Errors', [table.metric('UserErrors')]),
      this.buildGraphWidget('DynamoDB Throttled Read', [table.metric('ReadThrottleEvents')]),
      this.buildGraphWidget('DynamoDB Throttled Write', [table.metric('WriteThrottleEvents')])
    )

    new cdk.CfnOutput(this, 'HTTP API Url', {
      value: api.url ?? 'Something went wrong with the deploy'
    });
  }

  private buildGraphWidget(widgetName: string, metrics: IMetric[], stacked = false): GraphWidget {
    return new GraphWidget({
      title: widgetName,
      left: metrics,
      stacked: stacked,
      width: 8
    });
  }

  private metricForApiGw(apiId: string, metricName: string, label: string, stat = 'avg'): cloudwatch.Metric {
    let dimensions = {
      ApiId: apiId
    };
    return this.buildMetric(metricName, 'AWS/ApiGateway', dimensions, cloudwatch.Unit.COUNT, label, stat);
  }

  private buildMetric(metricName: string, namespace: string, dimensions: any, unit: cloudwatch.Unit, label: string, stat = 'avg', period = 900): cloudwatch.Metric {
    return new cloudwatch.Metric({
      metricName,
      namespace: namespace,
      dimensions: dimensions,
      unit: unit,
      label: label,
      statistic: stat,
      period: cdk.Duration.seconds(period)
    });
  }
}
