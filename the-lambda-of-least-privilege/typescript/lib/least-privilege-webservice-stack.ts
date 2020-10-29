import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigatewayv2');
import {
    ManagedPolicy,
    Role,
    ServicePrincipal,
    PolicyStatement,
    Effect
} from '@aws-cdk/aws-iam';

export class LeastPrivilegeWebserviceStack extends cdk.Stack {

    public readonly readOnlyRole: Role;
    public readonly creatorRole: Role;

    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        //DynamoDB Table
        const table = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });

        // Define a lambda with the !!basic execution role.
        // The lambda handler will inherit the role based on the User that is logged in.
        const dynamoLambda = new lambda.Function(this, 'DynamoLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'lambda.handler',                // file is "lambda", function is "handler"
            environment: {
                HITS_TABLE_NAME: table.tableName
            }
        });

        // defines an API Gateway Http API resource backed by our "dynamoLambda" function.
        let api = new apigw.HttpApi(this, 'Endpoint', {
            defaultIntegration: new apigw.LambdaProxyIntegration({
                handler: dynamoLambda
            })
        });

        // ==================================================================================
        // Create our User Roles
        //
        // TODO are there any other managed policies that we should add to these?
        //
        // ==================================================================================

        // Create a Read Only Role to be mapped to our external user
        this.readOnlyRole = new Role(this, id + 'ReadOnlyRole', {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com')
        })

        // Add permissions for scanning and reading the DynamoDB
        this.readOnlyRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                resources: [table.tableArn], //lock down the policy to this table only
                actions: [
                    'dynamodb:Scan',
                    'dynamodb:Query',
                    'logs:CreateLogStream',
                    'logs:PutLogEvents'
                ]
            })
        );

        // Create a Write Role
        this.creatorRole = new Role(this, id + 'CreatorRole', {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com')
        })

        // Add permissions for updating the DynamoDB
        this.creatorRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                resources: [table.tableArn], //lock down the policy to this table only
                actions: [
                    'dynamodb:Scan',
                    'dynamodb:Query',
                    'dynamodb:UpdateItem',
                    'logs:CreateLogStream',
                    'logs:PutLogEvents'
                ]
            })
        );


        // Outputs

        new cdk.CfnOutput(this, 'HTTP API Url', {
            value: api.url ?? 'Something went wrong with the deploy'
        });
    }
}