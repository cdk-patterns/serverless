import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import sns_sub = require('@aws-cdk/aws-sns-subscriptions');
import sns = require('@aws-cdk/aws-sns');

export interface DynamoFlowStackProps extends cdk.StackProps{
    readonly snsTopicARN: string;
}

export class TheDynamoFlowStack extends cdk.Stack {
    dynamoLambda: lambda.Function;
    constructor(scope: cdk.Construct, id: string, props: DynamoFlowStackProps) {
        super(scope, id, props);

        //DynamoDB Table
        const table = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });

        // defines an AWS Lambda resource
        this.dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.fromAsset('lambda-fns'),
            handler: 'dynamo.handler',
            environment: {
                HITS_TABLE_NAME: table.tableName
            },
            tracing: lambda.Tracing.ACTIVE
        });

        // grant the lambda role read/write permissions to our table
        table.grantReadWriteData(this.dynamoLambda);

        let topic = sns.Topic.fromTopicArn(this, 'SNSTopic', props.snsTopicARN);
        topic.addSubscription(new sns_sub.LambdaSubscription(this.dynamoLambda));
    }
}
