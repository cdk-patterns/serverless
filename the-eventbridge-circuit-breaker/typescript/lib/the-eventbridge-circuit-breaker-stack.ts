import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import iam = require('@aws-cdk/aws-iam');
import events = require('@aws-cdk/aws-events');
import events_targets = require('@aws-cdk/aws-events-targets');
import { GlobalSecondaryIndexProps } from '@aws-cdk/aws-dynamodb';
import { Duration } from '@aws-cdk/core';

export class TheEventbridgeCircuitBreakerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Table
    // This will store our error records
    // TTL Docs - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/time-to-live-ttl-how-to.html
    const table = new dynamodb.Table(this, 'CircuitBreaker', {
      partitionKey: { name: 'RequestID', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'ExpirationTime', type: dynamodb.AttributeType.NUMBER },
      timeToLiveAttribute: 'ExpirationTime'
    });
    
    // Add index to let us query on siteUrl
    let secondaryIndex:GlobalSecondaryIndexProps = {
      indexName: 'UrlIndex',
      partitionKey: { name: 'SiteUrl', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'ExpirationTime', type: dynamodb.AttributeType.NUMBER }
    }
    
    table.addGlobalSecondaryIndex(secondaryIndex);

    // defines an Integration Lambda to call our failing web service
    const webserviceIntegrationLambda = new lambda.Function(this, 'WebserviceIntegrationLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/webservice'),
      handler: 'lambda.handler',
      timeout: Duration.seconds(20),
      environment: {
        TABLE_NAME: table.tableName
      }
    });

    // grant the lambda role read permissions for our table
    table.grantReadData(webserviceIntegrationLambda);

    // We need to give your lambda permission to put events on our EventBridge
    let eventPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ['events:PutEvents']
    })

    webserviceIntegrationLambda.addToRolePolicy(eventPolicy);

    // Error Lambda
    // defines a lambda to insert errors into dynamo
    const errorLambda = new lambda.Function(this, 'ErrorLambdaHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/error'),
      handler: 'lambda.handler',
      timeout: Duration.seconds(3),
      environment: {
        TABLE_NAME: table.tableName
      }
    });

    table.grantWriteData(errorLambda);

    // Create EventBridge rule to route failures
    const webserviceErrorRule = new events.Rule(this, 'webserviceErrorRule', {
      description: 'Failed Webservice Call',
      eventPattern: {
        source: ['cdkpatterns.eventbridge.circuitbreaker'],
        detailType: ['httpcall'],
        detail: {
          status: ["fail"]
        }
      }
    });

    webserviceErrorRule.addTarget(new events_targets.LambdaFunction(errorLambda));

    // defines an API Gateway REST API resource backed by our "webserviceIntegrationLambda" function.
    new apigw.LambdaRestApi(this, 'CircuitBreakerGateway', {
      handler: webserviceIntegrationLambda
    });
  }
}
