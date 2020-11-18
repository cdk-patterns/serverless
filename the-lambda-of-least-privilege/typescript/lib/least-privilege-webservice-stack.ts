import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigateway');
import {
    //ManagedPolicy,
    Role,
    ServicePrincipal,
    PolicyStatement,
    Effect
} from '@aws-cdk/aws-iam';
import { CfnApiGatewayManagedOverrides } from '@aws-cdk/aws-apigatewayv2';

export class LeastPrivilegeWebserviceStack extends cdk.Stack {

    public readonly readOnlyRole: Role;
    public readonly creatorRole: Role;

    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        //DynamoDB Table
        const table = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });

        //================================================================================================
        // Build out the Lambda Functions
        //
        // We are going to shout for a IAM based authoriser implementation on our routes.
        //================================================================================================
        const updateHitsLambda = new lambda.Function(this, 'getDynamoHitsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'updateHits.handler',                // file is "lambda", function is "handler"
            environment: {
                HITS_TABLE_NAME: table.tableName
            }
        });

        // Get HITs Function
        const getHitsLambda = new lambda.Function(this, 'updateDynamoHitsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'updateHits.handler',                // file is "lambda", function is "handler"
            environment: {
                HITS_TABLE_NAME: table.tableName
            }
        });

        //================================================================================================
        // Build out the API Gateways
        //
        // We are going to shout for a IAM based authoriser implementation on our routes.
        //================================================================================================

        const restGateway = new apigw.RestApi(this, 'hitsapi');

        const hitsResource = restGateway.root.addResource('hits');
        // We need to enable cors on this resource to enable us completing the exercise with our client application
        // You should remove or configure this securely for your end production app.
        hitsResource.addCorsPreflight({
            allowOrigins: ['*'],
            allowMethods: [ 'OPTIONS', 'GET', 'PUT' ]
          });

        // Lets create a GET method for the readOnly operation
        const getHitsMethod = hitsResource.addMethod('GET', new apigw.LambdaIntegration(getHitsLambda), {
            authorizationType: apigw.AuthorizationType.IAM
        });

        // Lets create a PUT method for the update/create operation
        const putHitsMethod = hitsResource.addMethod('PUT', new apigw.LambdaIntegration(updateHitsLambda), {
            authorizationType: apigw.AuthorizationType.IAM
        });


        // ==================================================================================
        // Create our User Roles
        //
        // TODO are there any other managed policies that we should add to these?
        //
        // ==================================================================================

        // IAM Role - Configured for a User to Read from a table from a specified endpoint.
        this.readOnlyRole = new Role(this, id + 'ReadOnlyRole', {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com')
        })

        // DynamoDB perms restricted to read operations
        this.readOnlyRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                resources: [table.tableArn],
                actions: [
                    'dynamodb:Scan',
                    'dynamodb:Query',
                    'dynamodb:Get',
                    'logs:CreateLogStream',
                    'logs:PutLogEvents'
                ]
            })
        );
        // Add permissions for calling the GET Operation
        this.readOnlyRole.addToPolicy(
            new PolicyStatement({
                actions: ['execute-api:Invoke'],
                effect: Effect.ALLOW,
                resources: [getHitsMethod.methodArn]
            })
        )

        // IAM Role - Configured for a User to Update the Database Table from a specified endpoint.
        this.creatorRole = new Role(this, id + 'CreatorRole', {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com')
        })

        // DynamoDB Perms - extended for UpdateItem
        this.creatorRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                resources: [table.tableArn],
                actions: [
                    'dynamodb:Scan',
                    'dynamodb:Query',
                    'dynamodb:Get',
                    'dynamodb:UpdateItem',
                    'logs:CreateLogStream',
                    'logs:PutLogEvents'
                ]
            })
        );

        // Add permissions for calling the gateway
        this.readOnlyRole.addToPolicy(
            new PolicyStatement({
                actions: ['execute-api:Invoke'],
                effect: Effect.ALLOW,
                resources: [putHitsMethod.methodArn]
            })
        )

        // Outputs
        new cdk.CfnOutput(this, 'HTTP API Url', {
            value: restGateway.url ?? 'Something went wrong with the deploy'
        });
    }
}