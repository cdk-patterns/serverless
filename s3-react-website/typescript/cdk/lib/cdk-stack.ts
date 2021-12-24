import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { SPADeploy } from 'cdk-spa-deploy';

export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new SPADeploy(this, 'websiteDeploy')
        .createBasicSite({
          indexDoc: 'index.html',
          websiteFolder: '../website/build'
        })
  }
}