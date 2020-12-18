import * as cdk from '@aws-cdk/core';
import { SPADeploy } from 'cdk-spa-deploy';
const fs = require('fs')

export class TheMediaLiveStreamWebsiteStack extends cdk.Stack {
  
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    let url = "";
    let that = this;

    // Getting URL from mediapackage
    fs.exists('./urlwebsite.json', (exists:any) => {
      if (exists) {
        var jsonFile = require('../urlwebsite.json');
        let jsondata = JSON.parse(JSON.stringify(jsonFile));
        if(jsondata.hasOwnProperty('TheMediaLiveStreamStack')){
          url = jsondata["TheMediaLiveStreamStack"]["mediapackageurlstream"];
        }

        // Writing new file
        let data = fs.readFileSync('website/index_original.html').toString('utf-8'); {
          let dataWithUrl = data.replace("##URLMEDIA##", url);
          fs.writeFile('website/index.html', dataWithUrl, function(err:any) {
            if (err) {
                return console.error(err);
            }else {
              new SPADeploy(that, "S3MediaLiveExample").createBasicSite({indexDoc: 'index.html',
                                                                          websiteFolder: 'website/'});
            }
          });
        };

      }
    });

  }
}
