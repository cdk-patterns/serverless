import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');

export class TheDynamoFlowStack extends cdk.Stack {
    dynamoLambda: lambda.Function;
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        //DynamoDB Table
        const table = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });

        // defines an AWS Lambda resource
        this.dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.asset('lambdas'),
            handler: 'dynamo.handler',
            environment: {
                HITS_TABLE_NAME: table.tableName
            },
            tracing: lambda.Tracing.ACTIVE
        });

        // grant the lambda role read/write permissions to our table
        table.grantReadWriteData(this.dynamoLambda);
    }
}
