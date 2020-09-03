import {
    expect as expectCDK,
    haveResourceLike
} from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import TheAlexaSkill = require('../lib/the-alexa-skill-stack');

//The Alexa Skill
test('IAM Role to Access S3 Assets', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::IAM::Role", {
        "AssumeRolePolicyDocument": {
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "alexa-appkit.amazon.com",
                        "cloudformation.amazonaws.com"
                    ]
                }
            }],
            "Version": "2012-10-17"
        }
    }));
});

test('IAM Policy to Access S3 Assets', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [{
                "Action": "S3:GetObject",
                "Effect": "Allow"
            }]
        }
    }));
});

test('DynamoDB Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::DynamoDB::Table", {
        "KeySchema": [{
            "AttributeName": "userId",
            "KeyType": "HASH"
        }],
    }));
});

test('Lambda Backend for Alexa', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Function", {
        "Runtime": "nodejs12.x",
        "Environment": {
            "Variables": {
                "USERS_TABLE": {
                }
            }
        }
    }));
});

test('DynamoDB Read/Write IAM Policy Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [{
                "Action": [
                    "dynamodb:BatchGetItem",
                    "dynamodb:GetRecords",
                    "dynamodb:GetShardIterator",
                    "dynamodb:Query",
                    "dynamodb:GetItem",
                    "dynamodb:Scan",
                    "dynamodb:BatchWriteItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem"
                ],
                "Effect": "Allow"
            }]
        }
    }));
});
test('Alexa Skill Created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("Alexa::ASK::Skill", {
        "SkillPackage": {
            "Overrides": {
                "Manifest": {
                    "apis": {
                        "custom": {
                            "endpoint": {
                                "uri": {}
                            }
                        }
                    }
                }
            }
        }
    }));
});

test('Lambda Permission for Alexa', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new TheAlexaSkill.TheAlexaSkillStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(haveResourceLike("AWS::Lambda::Permission", {
        "Action": "lambda:InvokeFunction",
        "Principal": "alexa-appkit.amazon.com"
    }));
});
