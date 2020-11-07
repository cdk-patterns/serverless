from aws_cdk import (
    core, aws_iam as iam, aws_s3 as s3
)

from aws_cdk.custom_resources import (
    AwsCustomResource, AwsCustomResourcePolicy, AwsSdkCall, PhysicalResourceId
)

class TheMediaPackageConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, id_channel: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.id_channel = id_channel
        self.scope = scope

    def create_package(self):
        """
        First step: 
        - Define lambda role to ger ResourceToken
        - Define policy. In this step policy might be overpermissive, but we don't know the ARN resource \
        So we will use ANY_RESOURCE tricl
        """
        lambda_role_mediapackage = self.get_provisioning_lambda_role(role_name=f'stack-the-media-live')
        custom_policy = AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)

        """
        Second step:
        - Define create/update/delete method for both: MediaPackageChannel and MediaPackageOriginEndpoint
        """
        on_create_mediapackage = self.on_create_mediapackage()
        on_update_mediapackage = self.on_update_mediapackage()
        on_delete_mediapackage = self.on_delete_mediapackage()

        on_create_mediapackage_endpoint = self.on_create_mediapackage_endpoint()
        on_update_mediapackage_endpoint = self.on_update_mediapackage_endpoint()
        on_delete_mediapackage_endpoint = self.on_delete_mediapackage_endpoint()

        """
        Third step:
        - Create MediaPackageChannel
        """
        channel = AwsCustomResource(scope=self.scope,
                            id=f'{self.id_channel}-MediaPackage-AWSCustomResource',
                            policy=custom_policy,
                            log_retention=None, # We don't need log at this moment
                            on_create=on_create_mediapackage, 
                            on_update=on_update_mediapackage, 
                            on_delete=on_delete_mediapackage,
                            resource_type='Custom::MediaPackageChannel',
                            role=lambda_role_mediapackage,
                            timeout=None)  # Timeout of the Lambda implementing this custom resource. Default: Duration.minutes(2)

        """
        Fourth step:
        - Create MediaPackageOriginEndpoint
        By default HLS endpoint is the most common endpoint used, so we will create it
        You can choose your own endpoint here: 
        https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/MediaPackage.html#createOriginEndpoint-property
        """
        hls_endpoint = AwsCustomResource(scope=self.scope,
                                        id=f'{self.id_channel}-MediaPackageEndpoint-AWSCustomResource',
                                        policy=custom_policy,
                                        log_retention=None, # We don't need log at this moment
                                        on_create=on_create_mediapackage_endpoint, 
                                        on_update=on_update_mediapackage_endpoint, 
                                        on_delete=on_delete_mediapackage_endpoint,
                                        resource_type='Custom::MediaPackageHlsEndpoint',
                                        role=lambda_role_mediapackage,
                                        timeout=None)  # Timeout of the Lambda implementing this custom resource. Default: Duration.minutes(2)

        """ Must fix the dependency among custom resources """
        mediadep = core.ConcreteDependable()
        mediadep.add(channel)
        hls_endpoint.node.add_dependency(mediadep)

        core.CfnOutput(scope=self, id="media-package-url-strem", value=hls_endpoint.get_response_field("Url"))
        
        return hls_endpoint.get_response_field("Url")
    """
    General functions
    """
    def get_provisioning_lambda_role(self, role_name: str):
        return iam.Role(
            scope=self,
            id=f'{role_name}-LambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSElementalMediaPackageFullAccess")],
        )

    """
    MediaPackageChannel functions
    """
    def on_create_mediapackage(self):
        create_params = {
            "Id": self.id_channel,
            "Description": f"Channel - {self.id_channel}"
        }

        on_create = AwsSdkCall(
            action='createChannel',
            service='MediaPackage',
            api_version=None, # Uses the latest api
            parameters=create_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of("media-live-stack"),
        )
        return on_create
    
    def on_update_mediapackage(self):
        update_params = {
            "Id": self.id_channel,
            "Description": f"Channel - {self.id_channel}"
        }
 
        on_update = AwsSdkCall(
            action='updateChannel',
            service='MediaPackage',
            api_version=None, # Uses the latest api
            parameters=update_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of("media-live-stack"),
        )
        return on_update

    def on_delete_mediapackage(self):
        delete_params = {
            "Id": self.id_channel
        }
 
        on_delete = AwsSdkCall(
            action='deleteChannel',
            service='MediaPackage',
            api_version=None, # Uses the latest api
            parameters=delete_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of("media-live-stack"),
        )
        return on_delete

    """
    MediaPackageEndpoint functions
    """
    def on_create_mediapackage_endpoint(self):
        create_params = {
            "ChannelId": self.id_channel,
            "Id": f"endpoint-{self.id_channel}",
            "Description": f"Endpoint - {self.id_channel}",
            "HlsPackage": {"SegmentDurationSeconds": 6, "PlaylistWindowSeconds": 60,
                           "StreamSelection": { "MaxVideoBitsPerSecond": 2147483647, "MinVideoBitsPerSecond": 0,
                           "StreamOrder": "ORIGINAL"}}

        }

        on_create_endpoint = AwsSdkCall(
            action='createOriginEndpoint',
            service='MediaPackage',
            api_version=None, # Uses the latest api
            parameters=create_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of("media-live-stack-endpoint"),
        )
        return on_create_endpoint
    
    def on_update_mediapackage_endpoint(self):
        update_params = {
            "ChannelId": self.id_channel,
            "Id": f"endpoint-{self.id_channel}",
            "Description": f"Endpoint - {self.id_channel}",
            "HlsPackage": {"SegmentDurationSeconds": 5, "PlaylistWindowSeconds": 59,
                           "StreamSelection": { "MaxVideoBitsPerSecond": 2147483647, "MinVideoBitsPerSecond": 0,
                           "StreamOrder": "ORIGINAL"}}
        }
 
        on_update = AwsSdkCall(
            action='updateOriginEndpoint',
            service='MediaPackage',
            api_version=None, # Uses the latest api
            parameters=update_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of("media-live-stack-endpoint"),
        )
        return on_update

    def on_delete_mediapackage_endpoint(self):
        delete_params = {
            "Id": f"endpoint-{self.id_channel}"
        }
 
        on_delete = AwsSdkCall(
            action='deleteOriginEndpoint',
            service='MediaPackage',
            api_version=None, # Uses the latest api
            parameters=delete_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CloudFormation
            physical_resource_id=PhysicalResourceId.of("media-live-stack-endpoint"),
        )
        return on_delete