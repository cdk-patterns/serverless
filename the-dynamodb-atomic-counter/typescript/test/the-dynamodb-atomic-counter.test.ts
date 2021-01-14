import { expect as expectCDK, haveResourceLike, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as TheDynamodbAtomicCounter from '../lib/the-dynamodb-atomic-counter-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheDynamodbAtomicCounter.TheDynamodbAtomicCounterStack(app, 'MyTestStack');

    console.log(stack);
    // THEN
    //expectCDK(stack).
    expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table"));
    //expectCDK(stack).to(haveResourceLike("AWS::IAM::Role"));
});
