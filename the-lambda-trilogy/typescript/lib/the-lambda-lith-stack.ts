import * as cdk from '@aws-cdk/core';
import lambda = require('@aws-cdk/aws-lambda');
import apigw = require('@aws-cdk/aws-apigateway');

export class TheLambdalithStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /**
     * Only one lambda, the lambdalith
     */

    const lambdalith = new lambda.Function(this, 'lambdalithHandler', {
      runtime: lambda.Runtime.NODEJS_12_X,
      code: lambda.Code.fromAsset('lambda-fns/the-lambda-lith'),
      handler: 'lambdalith.main',                
    });


    /**
     * All routes go to lambdalith which handles routes internally
     */
    
    new apigw.LambdaRestApi(this, 'LambdalithAPI', {
      handler: lambdalith
    });
  }
}
