import * as cdk from '@aws-cdk/core';

export interface WafStackProps extends cdk.StackProps{
  gatewayARN: string
}

export class TheWafStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: WafStackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
  }
}
