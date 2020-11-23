import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigateway');
import iam = require("@aws-cdk/aws-iam");
import {
    Role,
    PolicyStatement,
    Effect
  } from '@aws-cdk/aws-iam';

interface webServiceStackProps extends cdk.StackProps {
    identityPoolRef: string;
}

export class LeastPrivilegeWebserviceStack extends cdk.Stack {

    // table ref
    public readonly hitsTable: dynamodb.Table;
    // api's
    public readonly getHitsMethod: apigw.Method;
    public readonly putHitsMethod: apigw.Method;
    // roles
    public readonly userRole: iam.Role;
    public readonly adminRole: iam.Role;

    constructor(scope: cdk.Construct, id: string, props?: webServiceStackProps) {
        super(scope, id, props);

        // ========================================================================================================
        // Resource: AWS DynamoDB Table
        // ========================================================================================================
        this.hitsTable = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });

        // ========================================================================================================
        //  Resource: AWS Lambda
        // ========================================================================================================
        const updateHitsLambda = new lambda.Function(this, 'getDynamoHitsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'updateHits.handler',                // file is "lambda", function is "handler"
            environment: {
                HITS_TABLE_NAME: this.hitsTable.tableName
            }
        });

        this.hitsTable.grantReadWriteData(updateHitsLambda);

        // Get HITs Function
        const getHitsLambda = new lambda.Function(this, 'updateDynamoHitsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'updateHits.handler',                // file is "lambda", function is "handler"
            environment: {
                HITS_TABLE_NAME: this.hitsTable.tableName
            }
        });

        this.hitsTable.grantReadData(getHitsLambda);

        // ========================================================================================================
        //  Resource: AWS API Gateway - RestAPI
        // ========================================================================================================

        const restGateway = new apigw.RestApi(this, 'hitsapi');

        const hitsResource = restGateway.root.addResource('hits');
        // We need to enable cors on this resource to enable us completing the exercise with our client application
        // ** You should remove or re-configure this securely for your end production app.
        hitsResource.addCorsPreflight({
            allowOrigins: ['*'],
            allowMethods: ['OPTIONS', 'GET', 'PUT']
        });

        // Lets create a GET method for the readOnly operation
        this.getHitsMethod = hitsResource.addMethod('GET', new apigw.LambdaIntegration(getHitsLambda), {
            authorizationType: apigw.AuthorizationType.IAM
        });

        // Lets create a PUT method for the update/create operation
        this.putHitsMethod = hitsResource.addMethod('PUT', new apigw.LambdaIntegration(updateHitsLambda), {
            authorizationType: apigw.AuthorizationType.IAM
        });

        // ========================================================================================================
        //    Resource: AWS::IAM::Role 
        //        THE USER (READ-ONLY) IAM ROLE
        // ========================================================================================================
        this.userRole = new iam.Role(this, id + 'ReadOnlyRole', {
            assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
                "StringEquals": { "cognito-identity.amazonaws.com:aud": props?.identityPoolRef },
                "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" },
            }, "sts:AssumeRoleWithWebIdentity"),
        });
        this.userRole.assumeRolePolicy?.addStatements(
            new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                principals: [new iam.ServicePrincipal('lambda.amazonaws.com')],
                actions: ['sts:AssumeRole'],
            }),
        );
        this.userRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                resources: [this.hitsTable.tableArn],
                actions: [
                    'dynamodb:Scan',
                    'dynamodb:Query',
                    'dynamodb:Get',
                    'logs:CreateLogStream',
                    'logs:PutLogEvents',
                    "mobileanalytics:PutEvents",
                    "cognito-sync:*",
                    "cognito-identity:*"
                ]
            })
        );
        this.userRole.addToPolicy(
            new PolicyStatement({
                actions: ['execute-api:Invoke'],
                effect: Effect.ALLOW,
                resources: [this.getHitsMethod.methodArn]
            })
        )
        this.userRole.addToPolicy(
            new PolicyStatement({
                actions: ["mobileanalytics:PutEvents",
                    "cognito-sync:*",
                    "cognito-identity:*",],
                effect: Effect.ALLOW,
                resources: ['*']
            })
        )

        // ========================================================================================================
        //    Resource: AWS::IAM::Role 
        //        THE USER(ADMIN) IAM ROLE
        // ========================================================================================================

        this.adminRole = new iam.Role(this, id + 'creatorRole', {
            assumedBy: new iam.FederatedPrincipal('cognito-identity.amazonaws.com', {
                "StringEquals": { "cognito-identity.amazonaws.com:aud": props?.identityPoolRef },
                "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" },
            }, "sts:AssumeRoleWithWebIdentity"),
        });
        this.adminRole.assumeRolePolicy?.addStatements(
            new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                principals: [new iam.ServicePrincipal('lambda.amazonaws.com')],
                actions: ['sts:AssumeRole'],
            }),
        );
        this.adminRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                resources: [this.hitsTable.tableArn],
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
        this.adminRole.addToPolicy(
            new PolicyStatement({
                actions: ['execute-api:Invoke'],
                effect: Effect.ALLOW,
                resources: [this.putHitsMethod.methodArn,
                this.getHitsMethod.methodArn]
            })
        );
        this.adminRole.addToPolicy(
            new PolicyStatement({
                actions: ["mobileanalytics:PutEvents",
                    "cognito-sync:*",
                    "cognito-identity:*",],
                effect: Effect.ALLOW,
                resources: ['*']
            })
        )

        // Outputs
        new cdk.CfnOutput(this, 'HTTP API Url', {
            value: restGateway.url ?? 'Something went wrong with the deploy'
        });
    }
}