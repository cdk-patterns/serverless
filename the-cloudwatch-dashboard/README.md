# The CloudWatch Dashboard

![Example Dashboard](img/dashboard.png)

This is a project that has been configured with a well architected CloudWatch dashboard for the simple webservice stack (API Gateway HTTP API, Lambda Function and DynamoDB). It also includes multiple alerts which send messages to an SNS Topic.

Some useful References:


| Author        | Link           |
| ------------- | ------------- |
| Julian Wood     | [Understanding application health – part 1](https://aws.amazon.com/blogs/compute/building-well-architected-serverless-applications-understanding-application-health-part-1/)  |
| AWS Docs    | [CloudWatch NameSpaces](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html)  |
| AWS Docs    | [Metric Math](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html)  |
| AWS Docs    | [Lambda Metrics](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html)  |
| AWS Docs    | [DynamoDB Metrics](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html)  |
| AWS Docs    | [HTTP API Metrics](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-metrics.html)  |
| AWS Docs    | [REST API Metrics](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html)  |
| Yan Cui    | [Lambda Alerts](https://lumigo.io/blog/how-to-monitor-lambda-with-cloudwatch-metrics/) and [Logging Timeouts](https://theburningmonk.com/2019/05/how-to-log-timed-out-lambda-invocations/) |
| Yan Cui    | [Doing Better Than Percentiles](https://theburningmonk.com/2018/10/we-can-do-better-than-percentile-latencies/) |
| Blue Matador   | [Monitoring DynamoDB](https://www.bluematador.com/blog/how-to-monitor-amazon-dynamodb-with-cloudwatch) |
| DataDog   | [Top DynamoDB Performance Metrics](https://www.datadoghq.com/blog/top-dynamodb-performance-metrics/) |
| Abhaya Chauhan   | [DynamoDB: Monitoring Capacity and Throttling](https://www.abhayachauhan.com/2018/01/dynamodb-monitoring-capacity/) |

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
