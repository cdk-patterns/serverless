import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import destinations = require('@aws-cdk/aws-lambda-destinations');
import events = require('@aws-cdk/aws-events');
import events_targets = require('@aws-cdk/aws-events-targets');
import apigw = require('@aws-cdk/aws-apigateway');

export class TheDestinedLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Lambda configured with destinations
     */
    const destinedLambda = new lambda.Function(this, 'destinedLambda', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'destinedLambda.handler',
      onSuccess: new destinations.EventBridgeDestination()
    });

    /**
     * Generic API Gateway where all endpoints hit our destined lambda
     */
    new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: destinedLambda
    });

    /**
     * This Lambda catches all EventBridge events from 'cdkpatterns.the-destined-lambda' source
     */
    const observeLambda = new lambda.Function(this, 'ObserveLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.asset('lambdas'),
      handler: 'observe.handler',
      timeout: cdk.Duration.seconds(3)
    });

    // Create EventBridge rule to route events
    const observeRule = new events.Rule(this, 'observeRule', {
      description: 'all events are caught here and logged centrally',
      eventPattern: {
        source: ['cdkpatterns.the-destined-lambda']
      }
    });

    observeRule.addTarget(new events_targets.LambdaFunction(observeLambda));
  }
}
