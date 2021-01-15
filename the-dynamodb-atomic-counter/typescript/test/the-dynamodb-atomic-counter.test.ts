import { expect as expectCDK, haveResourceLike, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheDynamodbAtomicCounter from '../lib/the-dynamodb-atomic-counter-stack';

test('Atomic DynamoDB Table', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheDynamodbAtomicCounter.TheDynamodbAtomicCounterStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
      "KeySchema": [
        {
          "AttributeName": "atomicCounter",
          "KeyType": "HASH"
        }
      ]
    }));
});

test('Atomic Count API', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamodbAtomicCounter.TheDynamodbAtomicCounterStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::RestApi", {
    "Name": "Atomic Count API"
  }));
});

test('Atomic Count API Method', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new TheDynamodbAtomicCounter.TheDynamodbAtomicCounterStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(haveResourceLike("AWS::ApiGateway::Method", {
    "HttpMethod": "GET",
    "Integration": {
      "IntegrationHttpMethod": "POST",
          "IntegrationResponses": [
            {
              "ResponseTemplates": {
                "application/json": "#set($value = $input.json('Attributes.counterValue.N'))\r\n#set($l = $value.length())\r\n#set($l = $l - 1)\r\n$value.substring(1,$l)"
              },
              "StatusCode": "200"
            }
          ],
      "PassthroughBehavior": "NEVER"
     }
  }));
});
