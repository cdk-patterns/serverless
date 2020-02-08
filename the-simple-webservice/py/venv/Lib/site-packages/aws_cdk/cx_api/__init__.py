"""
## Cloud Executable protocol

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

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/cx-api", "1.23.0", __name__, "cx-api@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/cx-api.AmiContextQuery", jsii_struct_bases=[], name_mapping={'filters': 'filters', 'owners': 'owners'})
class AmiContextQuery():
    def __init__(self, *, filters: typing.Mapping[str,typing.List[str]], owners: typing.Optional[typing.List[str]]=None):
        """Query to AMI context provider.

        :param filters: Filters to DescribeImages call.
        :param owners: Owners to DescribeImages call. Default: - All owners

        stability
        :stability: experimental
        """
        self._values = {
            'filters': filters,
        }
        if owners is not None: self._values["owners"] = owners

    @builtins.property
    def filters(self) -> typing.Mapping[str,typing.List[str]]:
        """Filters to DescribeImages call.

        stability
        :stability: experimental
        """
        return self._values.get('filters')

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[str]]:
        """Owners to DescribeImages call.

        default
        :default: - All owners

        stability
        :stability: experimental
        """
        return self._values.get('owners')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AmiContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.ArtifactManifest", jsii_struct_bases=[], name_mapping={'type': 'type', 'dependencies': 'dependencies', 'environment': 'environment', 'metadata': 'metadata', 'properties': 'properties'})
class ArtifactManifest():
    def __init__(self, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None):
        """A manifest for a single artifact within the cloud assembly.

        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact.
        :param environment: The environment into which this artifact is deployed.
        :param metadata: Associated metadata.
        :param properties: The set of properties for this artifact (depends on type).

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
        }
        if dependencies is not None: self._values["dependencies"] = dependencies
        if environment is not None: self._values["environment"] = environment
        if metadata is not None: self._values["metadata"] = metadata
        if properties is not None: self._values["properties"] = properties

    @builtins.property
    def type(self) -> "ArtifactType":
        """The type of artifact.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[str]]:
        """IDs of artifacts that must be deployed before this artifact.

        stability
        :stability: experimental
        """
        return self._values.get('dependencies')

    @builtins.property
    def environment(self) -> typing.Optional[str]:
        """The environment into which this artifact is deployed.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]:
        """Associated metadata.

        stability
        :stability: experimental
        """
        return self._values.get('metadata')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """The set of properties for this artifact (depends on type).

        stability
        :stability: experimental
        """
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArtifactManifest(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/cx-api.ArtifactType")
class ArtifactType(enum.Enum):
    """Type of cloud artifact.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """
    stability
    :stability: experimental
    """
    AWS_CLOUDFORMATION_STACK = "AWS_CLOUDFORMATION_STACK"
    """The artifact is an AWS CloudFormation stack.

    stability
    :stability: experimental
    """
    CDK_TREE = "CDK_TREE"
    """The artifact contains metadata generated out of the CDK application.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AssemblyBuildOptions", jsii_struct_bases=[], name_mapping={'runtime_info': 'runtimeInfo'})
class AssemblyBuildOptions():
    def __init__(self, *, runtime_info: typing.Optional["RuntimeInfo"]=None):
        """
        :param runtime_info: Include the specified runtime information (module versions) in manifest. Default: - if this option is not specified, runtime info will not be included

        stability
        :stability: experimental
        """
        if isinstance(runtime_info, dict): runtime_info = RuntimeInfo(**runtime_info)
        self._values = {
        }
        if runtime_info is not None: self._values["runtime_info"] = runtime_info

    @builtins.property
    def runtime_info(self) -> typing.Optional["RuntimeInfo"]:
        """Include the specified runtime information (module versions) in manifest.

        default
        :default: - if this option is not specified, runtime info will not be included

        stability
        :stability: experimental
        """
        return self._values.get('runtime_info')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssemblyBuildOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.AssemblyManifest", jsii_struct_bases=[], name_mapping={'version': 'version', 'artifacts': 'artifacts', 'missing': 'missing', 'runtime': 'runtime'})
class AssemblyManifest():
    def __init__(self, *, version: str, artifacts: typing.Optional[typing.Mapping[str,"ArtifactManifest"]]=None, missing: typing.Optional[typing.List["MissingContext"]]=None, runtime: typing.Optional["RuntimeInfo"]=None):
        """A manifest which describes the cloud assembly.

        :param version: Protocol version.
        :param artifacts: The set of artifacts in this assembly.
        :param missing: Missing context information. If this field has values, it means that the cloud assembly is not complete and should not be deployed.
        :param runtime: Runtime information.

        stability
        :stability: experimental
        """
        if isinstance(runtime, dict): runtime = RuntimeInfo(**runtime)
        self._values = {
            'version': version,
        }
        if artifacts is not None: self._values["artifacts"] = artifacts
        if missing is not None: self._values["missing"] = missing
        if runtime is not None: self._values["runtime"] = runtime

    @builtins.property
    def version(self) -> str:
        """Protocol version.

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def artifacts(self) -> typing.Optional[typing.Mapping[str,"ArtifactManifest"]]:
        """The set of artifacts in this assembly.

        stability
        :stability: experimental
        """
        return self._values.get('artifacts')

    @builtins.property
    def missing(self) -> typing.Optional[typing.List["MissingContext"]]:
        """Missing context information.

        If this field has values, it means that the
        cloud assembly is not complete and should not be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('missing')

    @builtins.property
    def runtime(self) -> typing.Optional["RuntimeInfo"]:
        """Runtime information.

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssemblyManifest(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.AvailabilityZonesContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'region': 'region'})
class AvailabilityZonesContextQuery():
    def __init__(self, *, account: typing.Optional[str]=None, region: typing.Optional[str]=None):
        """Query to hosted zone context provider.

        :param account: Query account.
        :param region: Query region.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if region is not None: self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AvailabilityZonesContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.AwsCloudFormationStackProperties", jsii_struct_bases=[], name_mapping={'template_file': 'templateFile', 'parameters': 'parameters', 'stack_name': 'stackName'})
class AwsCloudFormationStackProperties():
    def __init__(self, *, template_file: str, parameters: typing.Optional[typing.Mapping[str,str]]=None, stack_name: typing.Optional[str]=None):
        """Artifact properties for CloudFormation stacks.

        :param template_file: A file relative to the assembly root which contains the CloudFormation template for this stack.
        :param parameters: Values for CloudFormation stack parameters that should be passed when the stack is deployed.
        :param stack_name: The name to use for the CloudFormation stack. Default: - name derived from artifact ID

        stability
        :stability: experimental
        """
        self._values = {
            'template_file': template_file,
        }
        if parameters is not None: self._values["parameters"] = parameters
        if stack_name is not None: self._values["stack_name"] = stack_name

    @builtins.property
    def template_file(self) -> str:
        """A file relative to the assembly root which contains the CloudFormation template for this stack.

        stability
        :stability: experimental
        """
        return self._values.get('template_file')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Values for CloudFormation stack parameters that should be passed when the stack is deployed.

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """The name to use for the CloudFormation stack.

        default
        :default: - name derived from artifact ID

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsCloudFormationStackProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudArtifact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudArtifact"):
    """Represents an artifact within a cloud assembly.

    stability
    :stability: experimental
    """
    def __init__(self, assembly: "CloudAssembly", id: str, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        :param assembly: -
        :param id: -
        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact.
        :param environment: The environment into which this artifact is deployed.
        :param metadata: Associated metadata.
        :param properties: The set of properties for this artifact (depends on type).

        stability
        :stability: experimental
        """
        manifest = ArtifactManifest(type=type, dependencies=dependencies, environment=environment, metadata=metadata, properties=properties)

        jsii.create(CloudArtifact, self, [assembly, id, manifest])

    @jsii.member(jsii_name="fromManifest")
    @builtins.classmethod
    def from_manifest(cls, assembly: "CloudAssembly", id: str, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> typing.Optional["CloudArtifact"]:
        """Returns a subclass of ``CloudArtifact`` based on the artifact type defined in the artifact manifest.

        :param assembly: The cloud assembly from which to load the artifact.
        :param id: The artifact ID.
        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact.
        :param environment: The environment into which this artifact is deployed.
        :param metadata: Associated metadata.
        :param properties: The set of properties for this artifact (depends on type).

        return
        :return: the ``CloudArtifact`` that matches the artifact type or ``undefined`` if it's an artifact type that is unrecognized by this module.

        stability
        :stability: experimental
        """
        artifact = ArtifactManifest(type=type, dependencies=dependencies, environment=environment, metadata=metadata, properties=properties)

        return jsii.sinvoke(cls, "fromManifest", [assembly, id, artifact])

    @jsii.member(jsii_name="findMetadataByType")
    def find_metadata_by_type(self, type: str) -> typing.List["MetadataEntryResult"]:
        """
        :param type: -

        return
        :return: all the metadata entries of a specific type in this artifact.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findMetadataByType", [type])

    @builtins.property
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> "CloudAssembly":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "assembly")

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["CloudArtifact"]:
        """Returns all the artifacts that this artifact depends on.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dependencies")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "ArtifactManifest":
        """The artifact's manifest.

        stability
        :stability: experimental
        """
        return jsii.get(self, "manifest")

    @builtins.property
    @jsii.member(jsii_name="messages")
    def messages(self) -> typing.List["SynthesisMessage"]:
        """The set of messages extracted from the artifact's metadata.

        stability
        :stability: experimental
        """
        return jsii.get(self, "messages")


class CloudAssembly(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudAssembly"):
    """Represents a deployable cloud application.

    stability
    :stability: experimental
    """
    def __init__(self, directory: str) -> None:
        """Reads a cloud assembly from the specified directory.

        :param directory: The root directory of the assembly.

        stability
        :stability: experimental
        """
        jsii.create(CloudAssembly, self, [directory])

    @jsii.member(jsii_name="getStack")
    def get_stack(self, stack_name: str) -> "CloudFormationStackArtifact":
        """Returns a CloudFormation stack artifact by name from this assembly.

        :param stack_name: -

        deprecated
        :deprecated: renamed to ``getStackByName`` (or ``getStackArtifact(id)``)

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "getStack", [stack_name])

    @jsii.member(jsii_name="getStackArtifact")
    def get_stack_artifact(self, artifact_id: str) -> "CloudFormationStackArtifact":
        """Returns a CloudFormation stack artifact from this assembly.

        :param artifact_id: the artifact id of the stack (can be obtained through ``stack.artifactId``).

        return
        :return: a ``CloudFormationStackArtifact`` object.

        stability
        :stability: experimental
        throws:
        :throws:: if there is no stack artifact with that id
        """
        return jsii.invoke(self, "getStackArtifact", [artifact_id])

    @jsii.member(jsii_name="getStackByName")
    def get_stack_by_name(self, stack_name: str) -> "CloudFormationStackArtifact":
        """Returns a CloudFormation stack artifact from this assembly.

        :param stack_name: the name of the CloudFormation stack.

        return
        :return: a ``CloudFormationStackArtifact`` object.

        stability
        :stability: experimental
        throws:
        :throws::

        if there is more than one stack with the same stack name. You can
        use ``getStackArtifact(stack.artifactId)`` instead.
        """
        return jsii.invoke(self, "getStackByName", [stack_name])

    @jsii.member(jsii_name="tree")
    def tree(self) -> typing.Optional["TreeCloudArtifact"]:
        """Returns the tree metadata artifact from this assembly.

        return
        :return: a ``TreeCloudArtifact`` object if there is one defined in the manifest, ``undefined`` otherwise.

        stability
        :stability: experimental
        throws:
        :throws:: if there is no metadata artifact by that name
        """
        return jsii.invoke(self, "tree", [])

    @jsii.member(jsii_name="tryGetArtifact")
    def try_get_artifact(self, id: str) -> typing.Optional["CloudArtifact"]:
        """Attempts to find an artifact with a specific identity.

        :param id: The artifact ID.

        return
        :return: A ``CloudArtifact`` object or ``undefined`` if the artifact does not exist in this assembly.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "tryGetArtifact", [id])

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.List["CloudArtifact"]:
        """All artifacts included in this assembly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "artifacts")

    @builtins.property
    @jsii.member(jsii_name="directory")
    def directory(self) -> str:
        """The root directory of the cloud assembly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "directory")

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "AssemblyManifest":
        """The raw assembly manifest.

        stability
        :stability: experimental
        """
        return jsii.get(self, "manifest")

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "RuntimeInfo":
        """Runtime information such as module versions used to synthesize this assembly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "runtime")

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List["CloudFormationStackArtifact"]:
        """
        return
        :return: all the CloudFormation stack artifacts that are included in this assembly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stacks")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """The schema version of the assembly manifest.

        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class CloudAssemblyBuilder(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudAssemblyBuilder"):
    """Can be used to build a cloud assembly.

    stability
    :stability: experimental
    """
    def __init__(self, outdir: typing.Optional[str]=None) -> None:
        """Initializes a cloud assembly builder.

        :param outdir: The output directory, uses temporary directory if undefined.

        stability
        :stability: experimental
        """
        jsii.create(CloudAssemblyBuilder, self, [outdir])

    @jsii.member(jsii_name="addArtifact")
    def add_artifact(self, id: str, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """Adds an artifact into the cloud assembly.

        :param id: The ID of the artifact.
        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact.
        :param environment: The environment into which this artifact is deployed.
        :param metadata: Associated metadata.
        :param properties: The set of properties for this artifact (depends on type).

        stability
        :stability: experimental
        """
        manifest = ArtifactManifest(type=type, dependencies=dependencies, environment=environment, metadata=metadata, properties=properties)

        return jsii.invoke(self, "addArtifact", [id, manifest])

    @jsii.member(jsii_name="addMissing")
    def add_missing(self, *, key: str, props: typing.Mapping[str,typing.Any], provider: str) -> None:
        """Reports that some context is missing in order for this cloud assembly to be fully synthesized.

        :param key: The missing context key.
        :param props: A set of provider-specific options.
        :param provider: The provider from which we expect this context key to be obtained.

        stability
        :stability: experimental
        """
        missing = MissingContext(key=key, props=props, provider=provider)

        return jsii.invoke(self, "addMissing", [missing])

    @jsii.member(jsii_name="buildAssembly")
    def build_assembly(self, *, runtime_info: typing.Optional["RuntimeInfo"]=None) -> "CloudAssembly":
        """Finalizes the cloud assembly into the output directory returns a ``CloudAssembly`` object that can be used to inspect the assembly.

        :param runtime_info: Include the specified runtime information (module versions) in manifest. Default: - if this option is not specified, runtime info will not be included

        stability
        :stability: experimental
        """
        options = AssemblyBuildOptions(runtime_info=runtime_info)

        return jsii.invoke(self, "buildAssembly", [options])

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        """The root directory of the resulting cloud assembly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "outdir")


class CloudFormationStackArtifact(CloudArtifact, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.CloudFormationStackArtifact"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, assembly: "CloudAssembly", artifact_id: str, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        :param assembly: -
        :param artifact_id: -
        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact.
        :param environment: The environment into which this artifact is deployed.
        :param metadata: Associated metadata.
        :param properties: The set of properties for this artifact (depends on type).

        stability
        :stability: experimental
        """
        artifact = ArtifactManifest(type=type, dependencies=dependencies, environment=environment, metadata=metadata, properties=properties)

        jsii.create(CloudFormationStackArtifact, self, [assembly, artifact_id, artifact])

    @builtins.property
    @jsii.member(jsii_name="assets")
    def assets(self) -> typing.List[typing.Union["FileAssetMetadataEntry", "ContainerImageAssetMetadataEntry"]]:
        """Any assets associated with this stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assets")

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> str:
        """A string that represents this stack.

        Should only be used in user interfaces.
        If the stackName and artifactId are the same, it will just return that. Otherwise,
        it will return something like " ()"

        stability
        :stability: experimental
        """
        return jsii.get(self, "displayName")

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> "Environment":
        """The environment into which to deploy this artifact.

        stability
        :stability: experimental
        """
        return jsii.get(self, "environment")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The physical name of this stack.

        deprecated
        :deprecated: renamed to ``stackName``

        stability
        :stability: deprecated
        """
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="originalName")
    def original_name(self) -> str:
        """The original name as defined in the CDK app.

        stability
        :stability: experimental
        """
        return jsii.get(self, "originalName")

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[str,str]:
        """CloudFormation parameters to pass to the stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "parameters")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        """The physical name of this stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Any:
        """The CloudFormation template for this stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "template")

    @builtins.property
    @jsii.member(jsii_name="templateFile")
    def template_file(self) -> str:
        """The file name of the template.

        stability
        :stability: experimental
        """
        return jsii.get(self, "templateFile")


@jsii.data_type(jsii_type="@aws-cdk/cx-api.ContainerImageAssetMetadataEntry", jsii_struct_bases=[], name_mapping={'id': 'id', 'packaging': 'packaging', 'path': 'path', 'source_hash': 'sourceHash', 'build_args': 'buildArgs', 'file': 'file', 'image_name_parameter': 'imageNameParameter', 'image_tag': 'imageTag', 'repository_name': 'repositoryName', 'target': 'target'})
class ContainerImageAssetMetadataEntry():
    def __init__(self, *, id: str, packaging: str, path: str, source_hash: str, build_args: typing.Optional[typing.Mapping[str,str]]=None, file: typing.Optional[str]=None, image_name_parameter: typing.Optional[str]=None, image_tag: typing.Optional[str]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None):
        """
        :param id: Logical identifier for the asset.
        :param packaging: Type of asset.
        :param path: Path on disk to the asset.
        :param source_hash: The hash of the source directory used to build the asset.
        :param build_args: Build args to pass to the ``docker build`` command. Default: no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: - no file is passed
        :param image_name_parameter: ECR Repository name and repo digest (separated by "@sha256:") where this image is stored. Default: undefined If not specified, ``repositoryName`` and ``imageTag`` are required because otherwise how will the stack know where to find the asset, ha?
        :param image_tag: The docker image tag to use for tagging pushed images. This field is required if ``imageParameterName`` is ommited (otherwise, the app won't be able to find the image). Default: - this parameter is REQUIRED after 1.21.0
        :param repository_name: ECR repository name, if omitted a default name based on the asset's ID is used instead. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - this parameter is REQUIRED after 1.21.0
        :param target: Docker target to build to. Default: no build target

        stability
        :stability: experimental
        """
        self._values = {
            'id': id,
            'packaging': packaging,
            'path': path,
            'source_hash': source_hash,
        }
        if build_args is not None: self._values["build_args"] = build_args
        if file is not None: self._values["file"] = file
        if image_name_parameter is not None: self._values["image_name_parameter"] = image_name_parameter
        if image_tag is not None: self._values["image_tag"] = image_tag
        if repository_name is not None: self._values["repository_name"] = repository_name
        if target is not None: self._values["target"] = target

    @builtins.property
    def id(self) -> str:
        """Logical identifier for the asset.

        stability
        :stability: experimental
        """
        return self._values.get('id')

    @builtins.property
    def packaging(self) -> str:
        """Type of asset.

        stability
        :stability: experimental
        """
        return self._values.get('packaging')

    @builtins.property
    def path(self) -> str:
        """Path on disk to the asset.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def source_hash(self) -> str:
        """The hash of the source directory used to build the asset.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Build args to pass to the ``docker build`` command.

        default
        :default: no build args are passed

        stability
        :stability: experimental
        """
        return self._values.get('build_args')

    @builtins.property
    def file(self) -> typing.Optional[str]:
        """Path to the Dockerfile (relative to the directory).

        default
        :default: - no file is passed

        stability
        :stability: experimental
        """
        return self._values.get('file')

    @builtins.property
    def image_name_parameter(self) -> typing.Optional[str]:
        """ECR Repository name and repo digest (separated by "@sha256:") where this image is stored.

        default
        :default:

        undefined If not specified, ``repositoryName`` and ``imageTag`` are
        required because otherwise how will the stack know where to find the asset,
        ha?

        deprecated
        :deprecated:

        specify ``repositoryName`` and ``imageTag`` instead, and then you
        know where the image will go.

        stability
        :stability: deprecated
        """
        return self._values.get('image_name_parameter')

    @builtins.property
    def image_tag(self) -> typing.Optional[str]:
        """The docker image tag to use for tagging pushed images.

        This field is
        required if ``imageParameterName`` is ommited (otherwise, the app won't be
        able to find the image).

        default
        :default: - this parameter is REQUIRED after 1.21.0

        stability
        :stability: experimental
        """
        return self._values.get('image_tag')

    @builtins.property
    def repository_name(self) -> typing.Optional[str]:
        """ECR repository name, if omitted a default name based on the asset's ID is used instead.

        Specify this property if you need to statically address the
        image, e.g. from a Kubernetes Pod. Note, this is only the repository name,
        without the registry and the tag parts.

        default
        :default: - this parameter is REQUIRED after 1.21.0

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: no build target

        stability
        :stability: experimental
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerImageAssetMetadataEntry(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.Environment", jsii_struct_bases=[], name_mapping={'account': 'account', 'name': 'name', 'region': 'region'})
class Environment():
    def __init__(self, *, account: str, name: str, region: str):
        """Models an AWS execution environment, for use within the CDK toolkit.

        :param account: The AWS account this environment deploys into.
        :param name: The arbitrary name of this environment (user-set, or at least user-meaningful).
        :param region: The AWS region name where this environment deploys into.

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'name': name,
            'region': region,
        }

    @builtins.property
    def account(self) -> str:
        """The AWS account this environment deploys into.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def name(self) -> str:
        """The arbitrary name of this environment (user-set, or at least user-meaningful).

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def region(self) -> str:
        """The AWS region name where this environment deploys into.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Environment(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EnvironmentUtils(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.EnvironmentUtils"):
    """
    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(EnvironmentUtils, self, [])

    @jsii.member(jsii_name="format")
    @builtins.classmethod
    def format(cls, account: str, region: str) -> str:
        """
        :param account: -
        :param region: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "format", [account, region])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, environment: str) -> "Environment":
        """
        :param environment: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "parse", [environment])


@jsii.data_type(jsii_type="@aws-cdk/cx-api.FileAssetMetadataEntry", jsii_struct_bases=[], name_mapping={'artifact_hash_parameter': 'artifactHashParameter', 'id': 'id', 'packaging': 'packaging', 'path': 'path', 's3_bucket_parameter': 's3BucketParameter', 's3_key_parameter': 's3KeyParameter', 'source_hash': 'sourceHash'})
class FileAssetMetadataEntry():
    def __init__(self, *, artifact_hash_parameter: str, id: str, packaging: str, path: str, s3_bucket_parameter: str, s3_key_parameter: str, source_hash: str):
        """
        :param artifact_hash_parameter: The name of the parameter where the hash of the bundled asset should be passed in.
        :param id: Logical identifier for the asset.
        :param packaging: Requested packaging style.
        :param path: Path on disk to the asset.
        :param s3_bucket_parameter: Name of parameter where S3 bucket should be passed in.
        :param s3_key_parameter: Name of parameter where S3 key should be passed in.
        :param source_hash: The hash of the source directory used to build the asset.

        stability
        :stability: experimental
        """
        self._values = {
            'artifact_hash_parameter': artifact_hash_parameter,
            'id': id,
            'packaging': packaging,
            'path': path,
            's3_bucket_parameter': s3_bucket_parameter,
            's3_key_parameter': s3_key_parameter,
            'source_hash': source_hash,
        }

    @builtins.property
    def artifact_hash_parameter(self) -> str:
        """The name of the parameter where the hash of the bundled asset should be passed in.

        stability
        :stability: experimental
        """
        return self._values.get('artifact_hash_parameter')

    @builtins.property
    def id(self) -> str:
        """Logical identifier for the asset.

        stability
        :stability: experimental
        """
        return self._values.get('id')

    @builtins.property
    def packaging(self) -> str:
        """Requested packaging style.

        stability
        :stability: experimental
        """
        return self._values.get('packaging')

    @builtins.property
    def path(self) -> str:
        """Path on disk to the asset.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def s3_bucket_parameter(self) -> str:
        """Name of parameter where S3 bucket should be passed in.

        stability
        :stability: experimental
        """
        return self._values.get('s3_bucket_parameter')

    @builtins.property
    def s3_key_parameter(self) -> str:
        """Name of parameter where S3 key should be passed in.

        stability
        :stability: experimental
        """
        return self._values.get('s3_key_parameter')

    @builtins.property
    def source_hash(self) -> str:
        """The hash of the source directory used to build the asset.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAssetMetadataEntry(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.HostedZoneContextQuery", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'account': 'account', 'private_zone': 'privateZone', 'region': 'region', 'vpc_id': 'vpcId'})
class HostedZoneContextQuery():
    def __init__(self, *, domain_name: str, account: typing.Optional[str]=None, private_zone: typing.Optional[bool]=None, region: typing.Optional[str]=None, vpc_id: typing.Optional[str]=None):
        """Query to hosted zone context provider.

        :param domain_name: The domain name e.g. example.com to lookup.
        :param account: Query account.
        :param private_zone: True if the zone you want to find is a private hosted zone.
        :param region: Query region.
        :param vpc_id: The VPC ID to that the private zone must be associated with. If you provide VPC ID and privateZone is false, this will return no results and raise an error.

        stability
        :stability: experimental
        """
        self._values = {
            'domain_name': domain_name,
        }
        if account is not None: self._values["account"] = account
        if private_zone is not None: self._values["private_zone"] = private_zone
        if region is not None: self._values["region"] = region
        if vpc_id is not None: self._values["vpc_id"] = vpc_id

    @builtins.property
    def domain_name(self) -> str:
        """The domain name e.g. example.com to lookup.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def private_zone(self) -> typing.Optional[bool]:
        """True if the zone you want to find is a private hosted zone.

        stability
        :stability: experimental
        """
        return self._values.get('private_zone')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def vpc_id(self) -> typing.Optional[str]:
        """The VPC ID to that the private zone must be associated with.

        If you provide VPC ID and privateZone is false, this will return no results
        and raise an error.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HostedZoneContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.MetadataEntry", jsii_struct_bases=[], name_mapping={'type': 'type', 'data': 'data', 'trace': 'trace'})
class MetadataEntry():
    def __init__(self, *, type: str, data: typing.Any=None, trace: typing.Optional[typing.List[str]]=None):
        """An metadata entry in the construct.

        :param type: The type of the metadata entry.
        :param data: The data.
        :param trace: A stack trace for when the entry was created.

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
        }
        if data is not None: self._values["data"] = data
        if trace is not None: self._values["trace"] = trace

    @builtins.property
    def type(self) -> str:
        """The type of the metadata entry.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def data(self) -> typing.Any:
        """The data.

        stability
        :stability: experimental
        """
        return self._values.get('data')

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[str]]:
        """A stack trace for when the entry was created.

        stability
        :stability: experimental
        """
        return self._values.get('trace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetadataEntry(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.MetadataEntryResult", jsii_struct_bases=[MetadataEntry], name_mapping={'type': 'type', 'data': 'data', 'trace': 'trace', 'path': 'path'})
class MetadataEntryResult(MetadataEntry):
    def __init__(self, *, type: str, data: typing.Any=None, trace: typing.Optional[typing.List[str]]=None, path: str):
        """
        :param type: The type of the metadata entry.
        :param data: The data.
        :param trace: A stack trace for when the entry was created.
        :param path: The path in which this entry was defined.

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
            'path': path,
        }
        if data is not None: self._values["data"] = data
        if trace is not None: self._values["trace"] = trace

    @builtins.property
    def type(self) -> str:
        """The type of the metadata entry.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def data(self) -> typing.Any:
        """The data.

        stability
        :stability: experimental
        """
        return self._values.get('data')

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[str]]:
        """A stack trace for when the entry was created.

        stability
        :stability: experimental
        """
        return self._values.get('trace')

    @builtins.property
    def path(self) -> str:
        """The path in which this entry was defined.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetadataEntryResult(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.MissingContext", jsii_struct_bases=[], name_mapping={'key': 'key', 'props': 'props', 'provider': 'provider'})
class MissingContext():
    def __init__(self, *, key: str, props: typing.Mapping[str,typing.Any], provider: str):
        """Represents a missing piece of context.

        :param key: The missing context key.
        :param props: A set of provider-specific options.
        :param provider: The provider from which we expect this context key to be obtained.

        stability
        :stability: experimental
        """
        self._values = {
            'key': key,
            'props': props,
            'provider': provider,
        }

    @builtins.property
    def key(self) -> str:
        """The missing context key.

        stability
        :stability: experimental
        """
        return self._values.get('key')

    @builtins.property
    def props(self) -> typing.Mapping[str,typing.Any]:
        """A set of provider-specific options.

        stability
        :stability: experimental
        """
        return self._values.get('props')

    @builtins.property
    def provider(self) -> str:
        """The provider from which we expect this context key to be obtained.

        stability
        :stability: experimental
        """
        return self._values.get('provider')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MissingContext(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.RuntimeInfo", jsii_struct_bases=[], name_mapping={'libraries': 'libraries'})
class RuntimeInfo():
    def __init__(self, *, libraries: typing.Mapping[str,str]):
        """Information about the application's runtime components.

        :param libraries: The list of libraries loaded in the application, associated with their versions.

        stability
        :stability: experimental
        """
        self._values = {
            'libraries': libraries,
        }

    @builtins.property
    def libraries(self) -> typing.Mapping[str,str]:
        """The list of libraries loaded in the application, associated with their versions.

        stability
        :stability: experimental
        """
        return self._values.get('libraries')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RuntimeInfo(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.SSMParameterContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'parameter_name': 'parameterName', 'region': 'region'})
class SSMParameterContextQuery():
    def __init__(self, *, account: typing.Optional[str]=None, parameter_name: typing.Optional[str]=None, region: typing.Optional[str]=None):
        """Query to hosted zone context provider.

        :param account: Query account.
        :param parameter_name: Parameter name to query.
        :param region: Query region.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if parameter_name is not None: self._values["parameter_name"] = parameter_name
        if region is not None: self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def parameter_name(self) -> typing.Optional[str]:
        """Parameter name to query.

        stability
        :stability: experimental
        """
        return self._values.get('parameter_name')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SSMParameterContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.SynthesisMessage", jsii_struct_bases=[], name_mapping={'entry': 'entry', 'id': 'id', 'level': 'level'})
class SynthesisMessage():
    def __init__(self, *, entry: "MetadataEntry", id: str, level: "SynthesisMessageLevel"):
        """
        :param entry: 
        :param id: 
        :param level: 

        stability
        :stability: experimental
        """
        if isinstance(entry, dict): entry = MetadataEntry(**entry)
        self._values = {
            'entry': entry,
            'id': id,
            'level': level,
        }

    @builtins.property
    def entry(self) -> "MetadataEntry":
        """
        stability
        :stability: experimental
        """
        return self._values.get('entry')

    @builtins.property
    def id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('id')

    @builtins.property
    def level(self) -> "SynthesisMessageLevel":
        """
        stability
        :stability: experimental
        """
        return self._values.get('level')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SynthesisMessage(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/cx-api.SynthesisMessageLevel")
class SynthesisMessageLevel(enum.Enum):
    """
    stability
    :stability: experimental
    """
    INFO = "INFO"
    """
    stability
    :stability: experimental
    """
    WARNING = "WARNING"
    """
    stability
    :stability: experimental
    """
    ERROR = "ERROR"
    """
    stability
    :stability: experimental
    """

class TreeCloudArtifact(CloudArtifact, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cx-api.TreeCloudArtifact"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, assembly: "CloudAssembly", name: str, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str,typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        :param assembly: -
        :param name: -
        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact.
        :param environment: The environment into which this artifact is deployed.
        :param metadata: Associated metadata.
        :param properties: The set of properties for this artifact (depends on type).

        stability
        :stability: experimental
        """
        artifact = ArtifactManifest(type=type, dependencies=dependencies, environment=environment, metadata=metadata, properties=properties)

        jsii.create(TreeCloudArtifact, self, [assembly, name, artifact])

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "file")


@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextQuery", jsii_struct_bases=[], name_mapping={'filter': 'filter', 'account': 'account', 'region': 'region', 'return_asymmetric_subnets': 'returnAsymmetricSubnets', 'subnet_group_name_tag': 'subnetGroupNameTag'})
class VpcContextQuery():
    def __init__(self, *, filter: typing.Mapping[str,str], account: typing.Optional[str]=None, region: typing.Optional[str]=None, return_asymmetric_subnets: typing.Optional[bool]=None, subnet_group_name_tag: typing.Optional[str]=None):
        """Query input for looking up a VPC.

        :param filter: Filters to apply to the VPC. Filter parameters are the same as passed to DescribeVpcs.
        :param account: Query account.
        :param region: Query region.
        :param return_asymmetric_subnets: Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups. Default: false
        :param subnet_group_name_tag: Optional tag for subnet group name. If not provided, we'll look at the aws-cdk:subnet-name tag. If the subnet does not have the specified tag, we'll use its type as the name. Default: 'aws-cdk:subnet-name'

        stability
        :stability: experimental
        """
        self._values = {
            'filter': filter,
        }
        if account is not None: self._values["account"] = account
        if region is not None: self._values["region"] = region
        if return_asymmetric_subnets is not None: self._values["return_asymmetric_subnets"] = return_asymmetric_subnets
        if subnet_group_name_tag is not None: self._values["subnet_group_name_tag"] = subnet_group_name_tag

    @builtins.property
    def filter(self) -> typing.Mapping[str,str]:
        """Filters to apply to the VPC.

        Filter parameters are the same as passed to DescribeVpcs.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html
        stability
        :stability: experimental
        """
        return self._values.get('filter')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def return_asymmetric_subnets(self) -> typing.Optional[bool]:
        """Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('return_asymmetric_subnets')

    @builtins.property
    def subnet_group_name_tag(self) -> typing.Optional[str]:
        """Optional tag for subnet group name.

        If not provided, we'll look at the aws-cdk:subnet-name tag.
        If the subnet does not have the specified tag,
        we'll use its type as the name.

        default
        :default: 'aws-cdk:subnet-name'

        stability
        :stability: experimental
        """
        return self._values.get('subnet_group_name_tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextResponse", jsii_struct_bases=[], name_mapping={'availability_zones': 'availabilityZones', 'vpc_id': 'vpcId', 'isolated_subnet_ids': 'isolatedSubnetIds', 'isolated_subnet_names': 'isolatedSubnetNames', 'isolated_subnet_route_table_ids': 'isolatedSubnetRouteTableIds', 'private_subnet_ids': 'privateSubnetIds', 'private_subnet_names': 'privateSubnetNames', 'private_subnet_route_table_ids': 'privateSubnetRouteTableIds', 'public_subnet_ids': 'publicSubnetIds', 'public_subnet_names': 'publicSubnetNames', 'public_subnet_route_table_ids': 'publicSubnetRouteTableIds', 'subnet_groups': 'subnetGroups', 'vpc_cidr_block': 'vpcCidrBlock', 'vpn_gateway_id': 'vpnGatewayId'})
class VpcContextResponse():
    def __init__(self, *, availability_zones: typing.List[str], vpc_id: str, isolated_subnet_ids: typing.Optional[typing.List[str]]=None, isolated_subnet_names: typing.Optional[typing.List[str]]=None, isolated_subnet_route_table_ids: typing.Optional[typing.List[str]]=None, private_subnet_ids: typing.Optional[typing.List[str]]=None, private_subnet_names: typing.Optional[typing.List[str]]=None, private_subnet_route_table_ids: typing.Optional[typing.List[str]]=None, public_subnet_ids: typing.Optional[typing.List[str]]=None, public_subnet_names: typing.Optional[typing.List[str]]=None, public_subnet_route_table_ids: typing.Optional[typing.List[str]]=None, subnet_groups: typing.Optional[typing.List["VpcSubnetGroup"]]=None, vpc_cidr_block: typing.Optional[str]=None, vpn_gateway_id: typing.Optional[str]=None):
        """Properties of a discovered VPC.

        :param availability_zones: AZs.
        :param vpc_id: VPC id.
        :param isolated_subnet_ids: IDs of all isolated subnets. Element count: #(availabilityZones) · #(isolatedGroups)
        :param isolated_subnet_names: Name of isolated subnet groups. Element count: #(isolatedGroups)
        :param isolated_subnet_route_table_ids: Route Table IDs of isolated subnet groups. Element count: #(availabilityZones) · #(isolatedGroups)
        :param private_subnet_ids: IDs of all private subnets. Element count: #(availabilityZones) · #(privateGroups)
        :param private_subnet_names: Name of private subnet groups. Element count: #(privateGroups)
        :param private_subnet_route_table_ids: Route Table IDs of private subnet groups. Element count: #(availabilityZones) · #(privateGroups)
        :param public_subnet_ids: IDs of all public subnets. Element count: #(availabilityZones) · #(publicGroups)
        :param public_subnet_names: Name of public subnet groups. Element count: #(publicGroups)
        :param public_subnet_route_table_ids: Route Table IDs of public subnet groups. Element count: #(availabilityZones) · #(publicGroups)
        :param subnet_groups: The subnet groups discovered for the given VPC. Unlike the above properties, this will include asymmetric subnets, if the VPC has any. This property will only be populated if {@link VpcContextQuery.returnAsymmetricSubnets} is true. Default: - no subnet groups will be returned unless {@link VpcContextQuery.returnAsymmetricSubnets} is true
        :param vpc_cidr_block: VPC cidr. Default: - CIDR information not available
        :param vpn_gateway_id: The VPN gateway ID.

        stability
        :stability: experimental
        """
        self._values = {
            'availability_zones': availability_zones,
            'vpc_id': vpc_id,
        }
        if isolated_subnet_ids is not None: self._values["isolated_subnet_ids"] = isolated_subnet_ids
        if isolated_subnet_names is not None: self._values["isolated_subnet_names"] = isolated_subnet_names
        if isolated_subnet_route_table_ids is not None: self._values["isolated_subnet_route_table_ids"] = isolated_subnet_route_table_ids
        if private_subnet_ids is not None: self._values["private_subnet_ids"] = private_subnet_ids
        if private_subnet_names is not None: self._values["private_subnet_names"] = private_subnet_names
        if private_subnet_route_table_ids is not None: self._values["private_subnet_route_table_ids"] = private_subnet_route_table_ids
        if public_subnet_ids is not None: self._values["public_subnet_ids"] = public_subnet_ids
        if public_subnet_names is not None: self._values["public_subnet_names"] = public_subnet_names
        if public_subnet_route_table_ids is not None: self._values["public_subnet_route_table_ids"] = public_subnet_route_table_ids
        if subnet_groups is not None: self._values["subnet_groups"] = subnet_groups
        if vpc_cidr_block is not None: self._values["vpc_cidr_block"] = vpc_cidr_block
        if vpn_gateway_id is not None: self._values["vpn_gateway_id"] = vpn_gateway_id

    @builtins.property
    def availability_zones(self) -> typing.List[str]:
        """AZs.

        stability
        :stability: experimental
        """
        return self._values.get('availability_zones')

    @builtins.property
    def vpc_id(self) -> str:
        """VPC id.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_id')

    @builtins.property
    def isolated_subnet_ids(self) -> typing.Optional[typing.List[str]]:
        """IDs of all isolated subnets.

        Element count: #(availabilityZones) · #(isolatedGroups)

        stability
        :stability: experimental
        """
        return self._values.get('isolated_subnet_ids')

    @builtins.property
    def isolated_subnet_names(self) -> typing.Optional[typing.List[str]]:
        """Name of isolated subnet groups.

        Element count: #(isolatedGroups)

        stability
        :stability: experimental
        """
        return self._values.get('isolated_subnet_names')

    @builtins.property
    def isolated_subnet_route_table_ids(self) -> typing.Optional[typing.List[str]]:
        """Route Table IDs of isolated subnet groups.

        Element count: #(availabilityZones) · #(isolatedGroups)

        stability
        :stability: experimental
        """
        return self._values.get('isolated_subnet_route_table_ids')

    @builtins.property
    def private_subnet_ids(self) -> typing.Optional[typing.List[str]]:
        """IDs of all private subnets.

        Element count: #(availabilityZones) · #(privateGroups)

        stability
        :stability: experimental
        """
        return self._values.get('private_subnet_ids')

    @builtins.property
    def private_subnet_names(self) -> typing.Optional[typing.List[str]]:
        """Name of private subnet groups.

        Element count: #(privateGroups)

        stability
        :stability: experimental
        """
        return self._values.get('private_subnet_names')

    @builtins.property
    def private_subnet_route_table_ids(self) -> typing.Optional[typing.List[str]]:
        """Route Table IDs of private subnet groups.

        Element count: #(availabilityZones) · #(privateGroups)

        stability
        :stability: experimental
        """
        return self._values.get('private_subnet_route_table_ids')

    @builtins.property
    def public_subnet_ids(self) -> typing.Optional[typing.List[str]]:
        """IDs of all public subnets.

        Element count: #(availabilityZones) · #(publicGroups)

        stability
        :stability: experimental
        """
        return self._values.get('public_subnet_ids')

    @builtins.property
    def public_subnet_names(self) -> typing.Optional[typing.List[str]]:
        """Name of public subnet groups.

        Element count: #(publicGroups)

        stability
        :stability: experimental
        """
        return self._values.get('public_subnet_names')

    @builtins.property
    def public_subnet_route_table_ids(self) -> typing.Optional[typing.List[str]]:
        """Route Table IDs of public subnet groups.

        Element count: #(availabilityZones) · #(publicGroups)

        stability
        :stability: experimental
        """
        return self._values.get('public_subnet_route_table_ids')

    @builtins.property
    def subnet_groups(self) -> typing.Optional[typing.List["VpcSubnetGroup"]]:
        """The subnet groups discovered for the given VPC.

        Unlike the above properties, this will include asymmetric subnets,
        if the VPC has any.
        This property will only be populated if {@link VpcContextQuery.returnAsymmetricSubnets}
        is true.

        default
        :default: - no subnet groups will be returned unless {@link VpcContextQuery.returnAsymmetricSubnets} is true

        stability
        :stability: experimental
        """
        return self._values.get('subnet_groups')

    @builtins.property
    def vpc_cidr_block(self) -> typing.Optional[str]:
        """VPC cidr.

        default
        :default: - CIDR information not available

        stability
        :stability: experimental
        """
        return self._values.get('vpc_cidr_block')

    @builtins.property
    def vpn_gateway_id(self) -> typing.Optional[str]:
        """The VPN gateway ID.

        stability
        :stability: experimental
        """
        return self._values.get('vpn_gateway_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcContextResponse(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcSubnet", jsii_struct_bases=[], name_mapping={'availability_zone': 'availabilityZone', 'route_table_id': 'routeTableId', 'subnet_id': 'subnetId', 'cidr': 'cidr'})
class VpcSubnet():
    def __init__(self, *, availability_zone: str, route_table_id: str, subnet_id: str, cidr: typing.Optional[str]=None):
        """A subnet representation that the VPC provider uses.

        :param availability_zone: The code of the availability zone this subnet is in (for example, 'us-west-2a').
        :param route_table_id: The identifier of the route table for this subnet.
        :param subnet_id: The identifier of the subnet.
        :param cidr: CIDR range of the subnet. Default: - CIDR information not available

        stability
        :stability: experimental
        """
        self._values = {
            'availability_zone': availability_zone,
            'route_table_id': route_table_id,
            'subnet_id': subnet_id,
        }
        if cidr is not None: self._values["cidr"] = cidr

    @builtins.property
    def availability_zone(self) -> str:
        """The code of the availability zone this subnet is in (for example, 'us-west-2a').

        stability
        :stability: experimental
        """
        return self._values.get('availability_zone')

    @builtins.property
    def route_table_id(self) -> str:
        """The identifier of the route table for this subnet.

        stability
        :stability: experimental
        """
        return self._values.get('route_table_id')

    @builtins.property
    def subnet_id(self) -> str:
        """The identifier of the subnet.

        stability
        :stability: experimental
        """
        return self._values.get('subnet_id')

    @builtins.property
    def cidr(self) -> typing.Optional[str]:
        """CIDR range of the subnet.

        default
        :default: - CIDR information not available

        stability
        :stability: experimental
        """
        return self._values.get('cidr')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcSubnet(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcSubnetGroup", jsii_struct_bases=[], name_mapping={'name': 'name', 'subnets': 'subnets', 'type': 'type'})
class VpcSubnetGroup():
    def __init__(self, *, name: str, subnets: typing.List["VpcSubnet"], type: "VpcSubnetGroupType"):
        """A group of subnets returned by the VPC provider.

        The included subnets do NOT have to be symmetric!

        :param name: The name of the subnet group, determined by looking at the tags of of the subnets that belong to it.
        :param subnets: The subnets that are part of this group. There is no condition that the subnets have to be symmetric in the group.
        :param type: The type of the subnet group.

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
            'subnets': subnets,
            'type': type,
        }

    @builtins.property
    def name(self) -> str:
        """The name of the subnet group, determined by looking at the tags of of the subnets that belong to it.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def subnets(self) -> typing.List["VpcSubnet"]:
        """The subnets that are part of this group.

        There is no condition that the subnets have to be symmetric
        in the group.

        stability
        :stability: experimental
        """
        return self._values.get('subnets')

    @builtins.property
    def type(self) -> "VpcSubnetGroupType":
        """The type of the subnet group.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcSubnetGroup(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/cx-api.VpcSubnetGroupType")
class VpcSubnetGroupType(enum.Enum):
    """The type of subnet group.

    Same as SubnetType in the @aws-cdk/aws-ec2 package,
    but we can't use that because of cyclical dependencies.

    stability
    :stability: experimental
    """
    PUBLIC = "PUBLIC"
    """Public subnet group type.

    stability
    :stability: experimental
    """
    PRIVATE = "PRIVATE"
    """Private subnet group type.

    stability
    :stability: experimental
    """
    ISOLATED = "ISOLATED"
    """Isolated subnet group type.

    stability
    :stability: experimental
    """

__all__ = ["AmiContextQuery", "ArtifactManifest", "ArtifactType", "AssemblyBuildOptions", "AssemblyManifest", "AvailabilityZonesContextQuery", "AwsCloudFormationStackProperties", "CloudArtifact", "CloudAssembly", "CloudAssemblyBuilder", "CloudFormationStackArtifact", "ContainerImageAssetMetadataEntry", "Environment", "EnvironmentUtils", "FileAssetMetadataEntry", "HostedZoneContextQuery", "MetadataEntry", "MetadataEntryResult", "MissingContext", "RuntimeInfo", "SSMParameterContextQuery", "SynthesisMessage", "SynthesisMessageLevel", "TreeCloudArtifact", "VpcContextQuery", "VpcContextResponse", "VpcSubnet", "VpcSubnetGroup", "VpcSubnetGroupType", "__jsii_assembly__"]

publication.publish()
