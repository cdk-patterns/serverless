from aws_cdk import core
from spa_deploy import SPADeploy

class S3AngularWebsiteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        SPADeploy(self, 'S3AngularDeploy').create_basic_site(index_doc='index.html',
                                                             website_folder='../website/dist/website')
