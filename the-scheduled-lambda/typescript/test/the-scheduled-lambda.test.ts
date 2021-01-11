import { expect, haveResourceLike } from '@aws-cdk/assert';
import { App } from '@aws-cdk/core';
import  { TheScheduledLambdaStack } from '../lib/the-scheduled-lambda-stack';

test('DynamoDB Created', () => {
    const app = new App();
    // WHEN
    const stack = new TheScheduledLambdaStack(app, 'MyTestStack');
    // THEN
    expect(stack).to(haveResourceLike('AWS::DynamoDB::Table', {
        KeySchema: [
            {
                AttributeName: 'requestid',
                KeyType: 'HASH'
            }
        ]}
    ));
});

test('DynamoDB write IAM Policy Created', () => {
    const app = new App();
    // WHEN
    const stack = new TheScheduledLambdaStack(app, 'MyTestStack');
    // THEN
    expect(stack).to(haveResourceLike('AWS::IAM::Policy', {
            PolicyDocument: {
                Statement: [
                    {
                        Action: [
                            'dynamodb:BatchWriteItem',
                            'dynamodb:PutItem',
                            'dynamodb:UpdateItem',
                            'dynamodb:DeleteItem'
                        ],
                        Effect: 'Allow'
                    }]
            }
        }
    ));
});

test('Scheduled Lambda Created', () => {
    const app = new App();
    // WHEN
    const stack = new TheScheduledLambdaStack(app, 'MyTestStack');
    // THEN
    expect(stack).to(haveResourceLike('AWS::Lambda::Function', {
            Handler: 'index.handler',
            Runtime: 'nodejs12.x'
        }
    ));
});

test('EventBridge rule created', () => {
    const app = new App();
    // WHEN
    const stack = new TheScheduledLambdaStack(app, 'MyTestStack');
    // THEN
    expect(stack).to(haveResourceLike('AWS::Events::Rule', {}));
});
