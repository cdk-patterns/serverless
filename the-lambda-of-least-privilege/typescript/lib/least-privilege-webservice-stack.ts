import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import dynamodb = require('@aws-cdk/aws-dynamodb');
import apigw = require('@aws-cdk/aws-apigateway');

export class LeastPrivilegeWebserviceStack extends cdk.Stack {

    public readonly hitsTable: dynamodb.Table;
    public readonly getHitsMethod: apigw.Method;
    public readonly putHitsMethod: apigw.Method;

    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        //DynamoDB Table
        this.hitsTable = new dynamodb.Table(this, 'Hits', {
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
                HITS_TABLE_NAME: this.hitsTable.tableName
            }
        });

        // Get HITs Function
        const getHitsLambda = new lambda.Function(this, 'updateDynamoHitsHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,      // execution environment
            code: lambda.Code.fromAsset('lambda-fns'),  // code loaded from the "lambda" directory
            handler: 'updateHits.handler',                // file is "lambda", function is "handler"
            environment: {
                HITS_TABLE_NAME: this.hitsTable.tableName
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
        this.getHitsMethod = hitsResource.addMethod('GET', new apigw.LambdaIntegration(getHitsLambda), {
            authorizationType: apigw.AuthorizationType.IAM
        });

        // Lets create a PUT method for the update/create operation
        this.putHitsMethod = hitsResource.addMethod('PUT', new apigw.LambdaIntegration(updateHitsLambda), {
            authorizationType: apigw.AuthorizationType.IAM
        });

        // Outputs
        new cdk.CfnOutput(this, 'HTTP API Url', {
            value: restGateway.url ?? 'Something went wrong with the deploy'
        });
    }
}