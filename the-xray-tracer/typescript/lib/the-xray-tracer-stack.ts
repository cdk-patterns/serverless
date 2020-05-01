import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

export interface XrayTraceStackProps extends cdk.StackProps{
  readonly dynamoFlowLambda: lambda.Function;
  readonly sqsFlowLambda: lambda.Function;
  readonly httpFlowLambda: lambda.Function;
}

export class TheXrayTracerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: XrayTraceStackProps) {
    super(scope, id, props);

     // defines an AWS Lambda resource that kicks off all the flows
     const orchLambda = new lambda.Function(this, 'OrchLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'orchestrator.handler',
      timeout: cdk.Duration.seconds(30),
      environment: {
        DYNAMO_FN_ARN: props.dynamoFlowLambda.functionArn,
        HTTP_FN_ARN: props.httpFlowLambda.functionArn,
        SQS_FN_ARN: props.sqsFlowLambda.functionArn
      },
      tracing: lambda.Tracing.ACTIVE
    });
    props.dynamoFlowLambda.grantInvoke(orchLambda);
    props.httpFlowLambda.grantInvoke(orchLambda);
    props.sqsFlowLambda.grantInvoke(orchLambda)

    // defines an API Gateway REST API resource backed by our "dynamoLambda" function.
    new apigw.LambdaRestApi(this, 'X-Ray_Endpoint', {
      handler: orchLambda,
      options: {
        deployOptions: {
          loggingLevel: apigw.MethodLoggingLevel.INFO,
          dataTraceEnabled: true,
          metricsEnabled: true,
          tracingEnabled: true
        }
      }
    });
  }
}
