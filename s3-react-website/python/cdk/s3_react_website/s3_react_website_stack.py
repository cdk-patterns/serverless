from aws_cdk import (
    Stack,
)
from constructs import Construct
from spa_deploy import SPADeploy

class S3ReactWebsiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SPADeploy(self, 'S3ReactDeploy').create_basic_site(index_doc='index.html',
                                                           website_folder='../website/build')
