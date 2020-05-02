import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

export interface XrayTraceStackProps extends cdk.StackProps{
  readonly lambdasToInvoke: lambda.Function[];
}

export class TheXrayTracerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: XrayTraceStackProps) {
    super(scope, id, props);

    const lambdaARNs:string[] = Array.from(props.lambdasToInvoke, (lambda) => lambda.functionArn);

     // defines an AWS Lambda resource that kicks off all the flows
     const orchLambda = new lambda.Function(this, 'OrchLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'orchestrator.handler',
      timeout: cdk.Duration.seconds(30),
      environment: {
        LAMBDA_ARNS_TO_INVOKE: JSON.stringify(lambdaARNs)
      },
      tracing: lambda.Tracing.ACTIVE
    });

    props.lambdasToInvoke.forEach((lambda)=>{
      lambda.grantInvoke(orchLambda);
    });

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
