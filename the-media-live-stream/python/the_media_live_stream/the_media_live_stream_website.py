import json
import os

from aws_cdk import (
    core
)

from spa_deploy import SPADeploy

class TheMediaLiveStreamWebsiteStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        url = ""
        # Getting URL export from CfnOutput
        if os.path.isfile('urlwebsite.json') and os.access('urlwebsite.json', os.R_OK):
            with open('urlwebsite.json') as json_file:
                data = json.load(json_file)
                if "the-media-live-stream" in data:
                    url = data["the-media-live-stream"]["mediapackageurlstream"]

        with open("../python/website/index_original.html", "rt") as index_o:
            with open("../python/website/index.html", "wt") as index_f:
                for line in index_o:
                    index_f.write(line.replace('##URLMEDIA##', url))
        
        SPADeploy(scope=self, id='S3MediaLiveExample').create_basic_site(index_doc="index.html",
                                                                         website_folder="../python/website")
