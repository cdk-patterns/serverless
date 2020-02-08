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

This module includes core classes for to CDK assets, used for copying asset
files to a staging area. Most CDK users should not need to use the classes in
this package directly.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.core
import aws_cdk.cx_api

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/assets", "1.23.0", __name__, "assets@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/assets.CopyOptions", jsii_struct_bases=[], name_mapping={'exclude': 'exclude', 'follow': 'follow'})
class CopyOptions():
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None):
        """Obtains applied when copying directories into the staging location.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow

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
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CopyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/assets.FingerprintOptions", jsii_struct_bases=[CopyOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'extra_hash': 'extraHash'})
class FingerprintOptions(CopyOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None, extra_hash: typing.Optional[str]=None):
        """Options related to calculating source hash.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content

        stability
        :stability: experimental
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if extra_hash is not None: self._values["extra_hash"] = extra_hash

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
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @builtins.property
    def extra_hash(self) -> typing.Optional[str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: experimental
        """
        return self._values.get('extra_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FingerprintOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/assets.FollowMode")
class FollowMode(enum.Enum):
    """
    stability
    :stability: experimental
    """
    NEVER = "NEVER"
    """Never follow symlinks.

    stability
    :stability: experimental
    """
    ALWAYS = "ALWAYS"
    """Materialize all symlinks, whether they are internal or external to the source directory.

    stability
    :stability: experimental
    """
    EXTERNAL = "EXTERNAL"
    """Only follows symlinks that are external to the source directory.

    stability
    :stability: experimental
    """
    BLOCK_EXTERNAL = "BLOCK_EXTERNAL"
    """Forbids source from having any symlinks pointing outside of the source tree.

    This is the safest mode of operation as it ensures that copy operations
    won't materialize files from the user's file system. Internal symlinks are
    not followed.

    If the copy operation runs into an external symlink, it will fail.

    stability
    :stability: experimental
    """

@jsii.interface(jsii_type="@aws-cdk/assets.IAsset")
class IAsset(jsii.compat.Protocol):
    """Common interface for all assets.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAssetProxy

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
        ...


class _IAssetProxy():
    """Common interface for all assets.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/assets.IAsset"
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


class Staging(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.Staging"):
    """Stages a file or directory from a location on the file system into a staging directory.

    This is controlled by the context key 'aws:cdk:asset-staging' and enabled
    by the CLI by default in order to ensure that when the CDK app exists, all
    assets are available for deployment. Otherwise, if an app references assets
    in temporary locations, those will not be available when it exists (see
    https://github.com/aws/aws-cdk/issues/1716).

    The ``stagedPath`` property is a stringified token that represents the location
    of the file or directory after staging. It will be resolved only during the
    "prepare" stage and may be either the original path or the staged path
    depending on the context setting.

    The file/directory are staged based on their content hash (fingerprint). This
    means that only if content was changed, copy will happen.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, source_path: str, extra_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param source_path: 
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = StagingProps(source_path=source_path, extra_hash=extra_hash, exclude=exclude, follow=follow)

        jsii.create(Staging, self, [scope, id, props])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: aws_cdk.core.ISynthesisSession) -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesize", [session])

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A cryptographic hash of the source document(s).

        stability
        :stability: experimental
        """
        return jsii.get(self, "sourceHash")

    @builtins.property
    @jsii.member(jsii_name="sourcePath")
    def source_path(self) -> str:
        """The path of the asset as it was referenced by the user.

        stability
        :stability: experimental
        """
        return jsii.get(self, "sourcePath")

    @builtins.property
    @jsii.member(jsii_name="stagedPath")
    def staged_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stagedPath")


@jsii.data_type(jsii_type="@aws-cdk/assets.StagingProps", jsii_struct_bases=[FingerprintOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'extra_hash': 'extraHash', 'source_path': 'sourcePath'})
class StagingProps(FingerprintOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None, extra_hash: typing.Optional[str]=None, source_path: str):
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param source_path: 

        stability
        :stability: experimental
        """
        self._values = {
            'source_path': source_path,
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if extra_hash is not None: self._values["extra_hash"] = extra_hash

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
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @builtins.property
    def extra_hash(self) -> typing.Optional[str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: experimental
        """
        return self._values.get('extra_hash')

    @builtins.property
    def source_path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StagingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CopyOptions", "FingerprintOptions", "FollowMode", "IAsset", "Staging", "StagingProps", "__jsii_assembly__"]

publication.publish()
