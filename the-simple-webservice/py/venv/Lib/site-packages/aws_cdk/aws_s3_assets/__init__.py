"""
## AWS CDK Assets

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

Assets are local files or directories which are needed by a CDK app. A common
example is a directory which contains the handler code for a Lambda function,
but assets can represent any artifact that is needed for the app's operation.

When deploying a CDK app that includes constructs with assets, the CDK toolkit
will first upload all the assets to S3, and only then deploy the stacks. The S3
locations of the uploaded assets will be passed in as CloudFormation Parameters
to the relevant stacks.

The following JavaScript example defines an directory asset which is archived as
a .zip file and uploaded to S3 during deployment.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
asset = assets.Asset(self, "SampleAsset",
    path=path.join(__dirname, "sample-asset-directory")
)
```

The following JavaScript example defines a file asset, which is uploaded as-is
to an S3 bucket during deployment.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
asset = assets.Asset(self, "SampleAsset",
    path=path.join(__dirname, "file-asset.txt")
)
```

## Attributes

`Asset` constructs expose the following deploy-time attributes:

* `s3BucketName` - the name of the assets S3 bucket.
* `s3ObjectKey` - the S3 object key of the asset file (whether it's a file or a zip archive)
* `s3Url` - the S3 URL of the asset (i.e. https://s3.us-east-1.amazonaws.com/mybucket/mykey.zip)

In the following example, the various asset attributes are exported as stack outputs:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
asset = assets.Asset(self, "SampleAsset",
    path=path.join(__dirname, "sample-asset-directory")
)

cdk.CfnOutput(self, "S3BucketName", value=asset.s3_bucket_name)
cdk.CfnOutput(self, "S3ObjectKey", value=asset.s3_object_key)
cdk.CfnOutput(self, "S3URL", value=asset.s3_url)
```

## Permissions

IAM roles, users or groups which need to be able to read assets in runtime will should be
granted IAM permissions. To do that use the `asset.grantRead(principal)` method:

The following examples grants an IAM group read permissions on an asset:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
group = iam.Group(self, "MyUserGroup")
asset.grant_read(group)
```

## How does it work?

When an asset is defined in a construct, a construct metadata entry
`aws:cdk:asset` is emitted with instructions on where to find the asset and what
type of packaging to perform (`zip` or `file`). Furthermore, the synthesized
CloudFormation template will also include two CloudFormation parameters: one for
the asset's bucket and one for the asset S3 key. Those parameters are used to
reference the deploy-time values of the asset (using `{ Ref: "Param" }`).

Then, when the stack is deployed, the toolkit will package the asset (i.e. zip
the directory), calculate an MD5 hash of the contents and will render an S3 key
for this asset within the toolkit's asset store. If the file doesn't exist in
the asset store, it is uploaded during deployment.

> The toolkit's asset store is an S3 bucket created by the toolkit for each
> environment the toolkit operates in (environment = account + region).

Now, when the toolkit deploys the stack, it will set the relevant CloudFormation
Parameters to point to the actual bucket and key for each asset.

## CloudFormation Resource Metadata

> NOTE: This section is relevant for authors of AWS Resource Constructs.

In certain situations, it is desirable for tools to be able to know that a certain CloudFormation
resource is using a local asset. For example, SAM CLI can be used to invoke AWS Lambda functions
locally for debugging purposes.

To enable such use cases, external tools will consult a set of metadata entries on AWS CloudFormation
resources:

* `aws:asset:path` points to the local path of the asset.
* `aws:asset:property` is the name of the resource property where the asset is used

Using these two metadata entries, tools will be able to identify that assets are used
by a certain resource, and enable advanced local experiences.

To add these metadata entries to a resource, use the
`asset.addResourceMetadata(resource, property)` method.

See https://github.com/aws/aws-cdk/issues/1432 for more details
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.assets
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.core
import aws_cdk.cx_api

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3-assets", "1.23.0", __name__, "aws-s3-assets@1.23.0.jsii.tgz")


@jsii.implements(aws_cdk.assets.IAsset)
class Asset(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-assets.Asset"):
    """An asset represents a local file or directory, which is automatically uploaded to S3 and then can be referenced within a CDK application.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None, source_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom source hash to use when identifying the specific version of the asset. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = AssetProps(path=path, readers=readers, source_hash=source_hash, exclude=exclude, follow=follow)

        jsii.create(Asset, self, [scope, id, props])

    @jsii.member(jsii_name="addResourceMetadata")
    def add_resource_metadata(self, resource: aws_cdk.core.CfnResource, resource_property: str) -> None:
        """Adds CloudFormation template metadata to the specified resource with information that indicates which resource property is mapped to this local asset.

        This can be used by tools such as SAM CLI to provide local
        experience such as local invocation and debugging of Lambda functions.

        Asset metadata will only be included if the stack is synthesized with the
        "aws:cdk:enable-asset-metadata" context key defined, which is the default
        behavior when synthesizing via the CDK Toolkit.

        :param resource: The CloudFormation resource which is using this asset [disable-awslint:ref-via-interface].
        :param resource_property: The property name where this asset is referenced (e.g. "Code" for AWS::Lambda::Function).

        see
        :see: https://github.com/aws/aws-cdk/issues/1432
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addResourceMetadata", [resource, resource_property])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        """Grants read permissions to the principal on the assets bucket.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property
    @jsii.member(jsii_name="assetPath")
    def asset_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assetPath")

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 bucket in which this asset resides.

        stability
        :stability: experimental
        """
        return jsii.get(self, "bucket")

    @builtins.property
    @jsii.member(jsii_name="isZipArchive")
    def is_zip_archive(self) -> bool:
        """Indicates if this asset is a zip archive.

        Allows constructs to ensure that the
        correct file type was used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isZipArchive")

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> str:
        """Attribute that represents the name of the bucket this asset exists in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3BucketName")

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> str:
        """Attribute which represents the S3 object key of this asset.

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3ObjectKey")

    @builtins.property
    @jsii.member(jsii_name="s3Url")
    def s3_url(self) -> str:
        """Attribute which represents the S3 URL of this asset.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.get(self, "s3Url")

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "sourceHash")


@jsii.data_type(jsii_type="@aws-cdk/aws-s3-assets.AssetOptions", jsii_struct_bases=[aws_cdk.assets.CopyOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'readers': 'readers', 'source_hash': 'sourceHash'})
class AssetOptions(aws_cdk.assets.CopyOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None, source_hash: typing.Optional[str]=None):
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom source hash to use when identifying the specific version of the asset. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if readers is not None: self._values["readers"] = readers
        if source_hash is not None: self._values["source_hash"] = source_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: experimental
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional[aws_cdk.assets.FollowMode]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @builtins.property
    def readers(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]:
        """A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        default
        :default: - No principals that can read file asset.

        stability
        :stability: experimental
        """
        return self._values.get('readers')

    @builtins.property
    def source_hash(self) -> typing.Optional[str]:
        """Custom source hash to use when identifying the specific version of the asset.

        NOTE: the source hash is used in order to identify a specific revision of the asset,
        and used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the source hash,
        you will need to make sure it is updated every time the source changes, or otherwise
        it is possible that some deployments will not be invalidated.

        default
        :default:

        - automatically calculate source hash based on the contents
          of the source file or directory.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3-assets.AssetProps", jsii_struct_bases=[AssetOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'readers': 'readers', 'source_hash': 'sourceHash', 'path': 'path'})
class AssetProps(AssetOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None, source_hash: typing.Optional[str]=None, path: str):
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom source hash to use when identifying the specific version of the asset. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.

        stability
        :stability: experimental
        """
        self._values = {
            'path': path,
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if readers is not None: self._values["readers"] = readers
        if source_hash is not None: self._values["source_hash"] = source_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: experimental
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional[aws_cdk.assets.FollowMode]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @builtins.property
    def readers(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]:
        """A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        default
        :default: - No principals that can read file asset.

        stability
        :stability: experimental
        """
        return self._values.get('readers')

    @builtins.property
    def source_hash(self) -> typing.Optional[str]:
        """Custom source hash to use when identifying the specific version of the asset.

        NOTE: the source hash is used in order to identify a specific revision of the asset,
        and used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the source hash,
        you will need to make sure it is updated every time the source changes, or otherwise
        it is possible that some deployments will not be invalidated.

        default
        :default:

        - automatically calculate source hash based on the contents
          of the source file or directory.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    @builtins.property
    def path(self) -> str:
        """The disk location of the asset.

        The path should refer to one of the following:

        - A regular file or a .zip file, in which case the file will be uploaded as-is to S3.
        - A directory, in which case it will be archived into a .zip file and uploaded to S3.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["Asset", "AssetOptions", "AssetProps", "__jsii_assembly__"]

publication.publish()
