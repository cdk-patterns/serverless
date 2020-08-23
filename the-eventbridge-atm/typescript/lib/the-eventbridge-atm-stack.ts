import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import iam = require('@aws-cdk/aws-iam');
import events = require('@aws-cdk/aws-events');
import events_targets = require('@aws-cdk/aws-events-targets');
import apigw = require('@aws-cdk/aws-apigateway');

export class TheEventbridgeAtmStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Producer Lambda
     */
    const atmProducerLambda = new lambda.Function(this, 'atmProducerLambda', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/atmProducer'),
      handler: 'handler.lambdaHandler'
    });

    let eventPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ['events:PutEvents']
    })

    atmProducerLambda.addToRolePolicy(eventPolicy);

    /**
     * Approved Transaction Consumer
     */
    const atmConsumer1Lambda = new lambda.Function(this, 'atmConsumer1Lambda', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/atmConsumer'),
      handler: 'handler.case1Handler'
    });

    const atmConsumer1LambdaRule = new events.Rule(this, 'atmConsumer1LambdaRule', {
      description: 'Approved transactions',
      eventPattern: {
        source: ['custom.myATMapp'],
        detailType: ['transaction'],
        detail: {
          result: ["approved"]
        }
      }
    });

    atmConsumer1LambdaRule.addTarget(new events_targets.LambdaFunction(atmConsumer1Lambda));

    /**
     * NY Prefix Consumer
     */
    const atmConsumer2Lambda = new lambda.Function(this, 'atmConsumer2Lambda', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/atmConsumer'),
      handler: 'handler.case2Handler'
    });

    const atmConsumer2LambdaRule = new events.Rule(this, 'atmConsumer2LambdaRule', {
      eventPattern: {
        source: ['custom.myATMapp'],
        detailType: ['transaction'],
        detail: {
          location: [{
            "prefix": "NY-"
          }]
        }
      }
    })

    atmConsumer2LambdaRule.addTarget(new events_targets.LambdaFunction(atmConsumer2Lambda));

    /**
     * Not Approved Consumer
     */
    const atmConsumer3Lambda = new lambda.Function(this, 'atmConsumer3Lambda', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/atmConsumer'),
      handler: 'handler.case3Handler'
    });

    const atmConsumer3LambdaRule = new events.Rule(this, 'atmConsumer3LambdaRule', {
      eventPattern: {
        source: ['custom.myATMapp'],
        detailType: ['transaction'],
        detail: {
          result: [{
            "anything-but": "approved"
          }]
        }
      }
    })

    atmConsumer3LambdaRule.addTarget(new events_targets.LambdaFunction(atmConsumer3Lambda));

    /**
     * API Gateway proxy integration
     */
    // defines an API Gateway REST API resource backed by our "atmProducerLambda" function.
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: atmProducerLambda
    });
  
  }
}
