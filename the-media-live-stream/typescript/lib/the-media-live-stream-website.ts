import * as cdk from '@aws-cdk/core';
import { SPADeploy } from 'cdk-spa-deploy';
const fs = require('fs')

export interface WebsiteStackProps extends cdk.StackProps{
  readonly urlStream: string;
}


export class TheMediaLiveStreamWebsiteStack extends cdk.Stack {
  
  constructor(scope: cdk.Construct, id: string, props: WebsiteStackProps) {
    super(scope, id, props);

    let url = props.urlStream;

    // Writing new file
    let data = fs.readFileSync('website/index_original.html').toString('utf-8'); {
      let dataWithUrl = data.replace("##URLMEDIA##", url);
      fs.writeFile('website/index.html', dataWithUrl, function(err:any) {
        if (err) {
            return console.error(err);
        }
      });
    };

    new SPADeploy(scope=this, id="S3MediaLiveExample").createBasicSite({indexDoc: 'index.html',
                                                                      websiteFolder: 'website/'});

  }
}
