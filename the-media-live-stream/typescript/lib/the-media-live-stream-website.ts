import * as cdk from '@aws-cdk/core';
import * as spadeploy from 'cdk-spa-deploy';
import { SPADeploy } from 'cdk-spa-deploy';
import * as fs from 'fs';


export class TheMediaLiveStreamWebsiteStack extends cdk.Stack {
  
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    let url = "";

    // Getting URL from mediapackage
    fs.exists('./urlwebsite.json', (exists) => {
      if (exists) {
        var jsonFile = require('../urlwebsite.json');
        let jsondata = JSON.parse(JSON.stringify(jsonFile));
        url = jsondata["TheMediaLiveStreamStack"]["mediapackageurlstream"];

        // Writing new file
        let data = fs.readFileSync('website/index_original.html').toString('utf-8'); {
          let dataWithUrl = data.replace("##URLMEDIA##", url);
          fs.writeFile('website/index.html', dataWithUrl, function(err) {
            if (err) {
                return console.error(err);
            }
          });
        };

        new SPADeploy(scope=this, id="S3MediaLiveExample").createBasicSite({indexDoc: 'index.html',
                                                                          websiteFolder: 'website/'});
      }
    });
  }
}
