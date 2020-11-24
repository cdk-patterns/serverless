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
    public readonly blogTable: dynamodb.Table;
    // api's
    public readonly getBlogsMethod: apigw.Method;
    public readonly putBlogsMethod: apigw.Method;
    // roles
    public readonly userRole: iam.Role;
    public readonly adminRole: iam.Role;

    constructor(scope: cdk.Construct, id: string, props?: webServiceStackProps) {
        super(scope, id, props);

        // ========================================================================================================
        // Resource: AWS DynamoDB Table
        // ========================================================================================================
        this.blogTable = new dynamodb.Table(this, 'Blogs', {
            partitionKey: { name: 'title', type: dynamodb.AttributeType.STRING },
            tableName: 'blogs',
            // The default removal policy is RETAIN, which means that cdk destroy will not attempt to delete
            // the new table, and it will remain in your account until manually deleted. By setting the policy to 
            // DESTROY, cdk destroy will delete the table (even if it has data in it)
            removalPolicy: cdk.RemovalPolicy.DESTROY, // NOT recommended for production code
        });

        // ========================================================================================================
        //  Resource: AWS Lambda
        // ========================================================================================================
        const createBlogLda = new lambda.Function(this, 'createBlogsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'createBlog.handler',                // file is "lambda", function is "handler"
            environment: {
                BLOGS_TABLE_NAME: this.blogTable.tableName,
                PRIMARY_KEY: 'itemId'
            }
        });

        this.blogTable.grantReadWriteData(createBlogLda); // Give this lambda read/write privileges

        // Get HITs Function
        const getBlogslda = new lambda.Function(this, 'getBlogsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'readBlogs.handler',                // file is "lambda", function is "handler"
            environment: {
                BLOGS_TABLE_NAME: this.blogTable.tableName,
                PRIMARY_KEY: 'itemId'
            }
        });

        this.blogTable.grantReadData(getBlogslda); // Give this lambda readonly privileges

        // ========================================================================================================
        //  Resource: AWS API Gateway - RestAPI
        // ========================================================================================================

        const restGateway = new apigw.RestApi(this, 'blogsapi');

        const blogsResource = restGateway.root.addResource('blogs');
        // We need to enable cors on this resource to enable us completing the exercise with our client application
        // ** You should remove or re-configure this securely for your end production app.
        blogsResource.addCorsPreflight({
            allowOrigins: ['*'],
            allowMethods: ['OPTIONS', 'GET', 'PUT']
        });

        // Lets create a GET method for the readOnly operation
        this.getBlogsMethod = blogsResource.addMethod('GET', new apigw.LambdaIntegration(getBlogslda), {
            authorizationType: apigw.AuthorizationType.IAM
        });

        // Lets create a PUT method for the update/create operation
        this.putBlogsMethod = blogsResource.addMethod('PUT', new apigw.LambdaIntegration(createBlogLda), {
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
                resources: [this.blogTable.tableArn],
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
                resources: [this.getBlogsMethod.methodArn]
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
                resources: [this.blogTable.tableArn],
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
                resources: [this.putBlogsMethod.methodArn,
                this.getBlogsMethod.methodArn]
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