import { Stack, Construct, StackProps, RemovalPolicy } from '@aws-cdk/core';
import { Function, Code, Runtime } from '@aws-cdk/aws-lambda';
import { Table, AttributeType } from "@aws-cdk/aws-dynamodb";
import { Schedule, Rule } from '@aws-cdk/aws-events'
import { LambdaFunction } from '@aws-cdk/aws-events-targets'

export class TheScheduledLambdaStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

    // Create a DynamoDB table with a single attribute
    const table = new Table(this, 'RequestTable', {
        partitionKey: {
            name: 'requestid',
            type: AttributeType.STRING
        },
        removalPolicy: RemovalPolicy.DESTROY
    });

    // Create the Lambda function we want to run on a schedule
    const scheduledLambda = new Function(this, 'scheduledLambda', {
        runtime: Runtime.NODEJS_12_X, // execution environment
        code: Code.fromAsset('lambda-fns'), // code loaded from the "lambda-fns" directory,
        handler: 'index.handler', // file is "index", function is "handler"
        environment: {
            TABLE_NAME: table.tableName
        },
    });

    // Allow our lambda fn to write to the table
    table.grantWriteData(scheduledLambda);

    // Create EventBridge rule that will execute our Lambda every 2 minutes
    const schedule = new Rule(this, 'scheduledLambda-schedule', {
        schedule: Schedule.expression('rate(2 minutes)'),
    });

    // Set the target of our EventBridge rule to our Lambda function
    schedule.addTarget(new LambdaFunction(scheduledLambda));

    }
}