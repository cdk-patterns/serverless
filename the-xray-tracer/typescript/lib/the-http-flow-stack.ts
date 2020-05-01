import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');

export class TheHttpFlowStack extends cdk.Stack {

    httpLambda: lambda.Function;
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // defines an AWS Lambda resource
        this.httpLambda = new lambda.Function(this, 'httpLambdaHandler', {
            runtime: lambda.Runtime.NODEJS_12_X,
            code: lambda.Code.asset('lambdas'),
            handler: 'http.handler',
            tracing: lambda.Tracing.ACTIVE
        });
    }
}
