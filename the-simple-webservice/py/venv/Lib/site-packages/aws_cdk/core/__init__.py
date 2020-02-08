"""
## AWS Cloud Development Kit Core Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library includes the basic building blocks of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) (AWS CDK). It defines the core classes that are used in the rest of the
AWS Construct Library.

See the [AWS CDK Developer
Guide](https://docs.aws.amazon.com/cdk/latest/guide/home.html) for
information of most of the capabilities of this library. The rest of this
README will only cover topics not already covered in the Developer Guide.

## Durations

To make specifications of time intervals unambiguous, a single class called
`Duration` is used throughout the AWS Construct Library by all constructs
that that take a time interval as a parameter (be it for a timeout, a
rate, or something else).

An instance of Duration is constructed by using one of the static factory
methods on it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Duration.seconds(300)# 5 minutes
Duration.minutes(5)# 5 minutes
Duration.hours(1)# 1 hour
Duration.days(7)# 7 days
Duration.parse("PT5M")
```

## Secrets

To help avoid accidental storage of secrets as plain text, we use the `SecretValue` type to
represent secrets. Any construct that takes a value that should be a secret (such as
a password or an access key) will take a parameter of type `SecretValue`.

The best practice is to store secrets in AWS Secrets Manager and reference them using `SecretValue.secretsManager`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
secret = SecretValue.secrets_manager("secretId",
    json_field="password", # optional: key of a JSON field to retrieve (defaults to all content),
    version_id="id", # optional: id of the version (default AWSCURRENT)
    version_stage="stage"
)
```

Using AWS Secrets Manager is the recommended way to reference secrets in a CDK app.
`SecretValue` also supports the following secret sources:

* `SecretValue.plainText(secret)`: stores the secret as plain text in your app and the resulting template (not recommended).
* `SecretValue.ssmSecure(param, version)`: refers to a secret stored as a SecureString in the SSM Parameter Store.
* `SecretValue.cfnParameter(param)`: refers to a secret passed through a CloudFormation parameter (must have `NoEcho: true`).
* `SecretValue.cfnDynamicReference(dynref)`: refers to a secret described by a CloudFormation dynamic reference (used by `ssmSecure` and `secretsManager`).

## ARN manipulation

Sometimes you will need to put together or pick apart Amazon Resource Names
(ARNs). The functions `stack.formatArn()` and `stack.parseArn()` exist for
this purpose.

`formatArn()` can be used to build an ARN from components. It will automatically
use the region and account of the stack you're calling it on:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Builds "arn:<PARTITION>:lambda:<REGION>:<ACCOUNT>:function:MyFunction"
stack.format_arn(
    service="lambda",
    resource="function",
    sep=":",
    resource_name="MyFunction"
)
```

`parseArn()` can be used to get a single component from an ARN. `parseArn()`
will correctly deal with both literal ARNs and deploy-time values (tokens),
but in case of a deploy-time value be aware that the result will be another
deploy-time value which cannot be inspected in the CDK application.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Extracts the function name out of an AWS Lambda Function ARN
arn_components = stack.parse_arn(arn, ":")
function_name = arn_components.resource_name
```

Note that depending on the service, the resource separator can be either
`:` or `/`, and the resource name can be either the 6th or 7th
component in the ARN. When using these functions, you will need to know
the format of the ARN you are dealing with.

For an exhaustive list of ARN formats used in AWS, see [AWS ARNs and
Namespaces](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)
in the AWS General Reference.

## Dependencies

### Construct Dependencies

Sometimes AWS resources depend on other resources, and the creation of one
resource must be completed before the next one can be started.

In general, CloudFormation will correctly infer the dependency relationship
between resources based on the property values that are used. In the cases where
it doesn't, the AWS Construct Library will add the dependency relationship for
you.

If you need to add an ordering dependency that is not automatically inferred,
you do so by adding a dependency relationship using
`constructA.node.addDependency(constructB)`. This will add a dependency
relationship between all resources in the scope of `constructA` and all
resources in the scope of `constructB`.

If you want a single object to represent a set of constructs that are not
necessarily in the same scope, you can use a `ConcreteDependable`. The
following creates a single object that represents a dependency on two
construts, `constructB` and `constructC`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Declare the dependable object
b_and_c = ConcreteDependable()
b_and_c.add(construct_b)
b_and_c.add(construct_c)

# Take the dependency
construct_a.node.add_dependency(b_and_c)
```

### Stack Dependencies

Two different stack instances can have a dependency on one another. This
happens when an resource from one stack is referenced in another stack. In
that case, CDK records the cross-stack referencing of resources,
automatically produces the right CloudFormation primitives, and adds a
dependency between the two stacks. You can also manually add a dependency
between two stacks by using the `stackA.addDependency(stackB)` method.

A stack dependency has the following implications:

* Cyclic dependencies are not allowed, so if `stackA` is using resources from
  `stackB`, the reverse is not possible anymore.
* Stacks with dependencies between them are treated specially by the CDK
  toolkit:

  * If `stackA` depends on `stackB`, running `cdk deploy stackA` will also
    automatically deploy `stackB`.
  * `stackB`'s deployment will be performed *before* `stackA`'s deployment.

## AWS CloudFormation features

A CDK stack synthesizes to an AWS CloudFormation Template. This section
explains how this module allows users to access low-level CloudFormation
features when needed.

### Stack Outputs

CloudFormation [stack outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html) and exports are created using
the `CfnOutput` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CfnOutput(self, "OutputName",
    value=bucket.bucket_name,
    description="The name of an S3 bucket", # Optional
    export_name="TheAwesomeBucket"
)
```

### Parameters

CloudFormation templates support the use of [Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html) to
customize a template. They enable CloudFormation users to input custom values to
a template each time a stack is created or updated. While the CDK design
philosophy favors using build-time parameterization, users may need to use
CloudFormation in a number of cases (for example, when migrating an existing
stack to the AWS CDK).

Template parameters can be added to a stack by using the `CfnParameter` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CfnParameter(self, "MyParameter",
    type="Number",
    default=1337
)
```

The value of parameters can then be obtained using one of the `value` methods.
As parameters are only resolved at deployment time, the values obtained are
placeholder tokens for the real value (`Token.isUnresolved()` would return `true`
for those):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
param = CfnParameter(self, "ParameterName")

# If the parameter is a String
param.value_as_string

# If the parameter is a Number
param.value_as_number

# If the parameter is a List
param.value_as_list
```

### Pseudo Parameters

CloudFormation supports a number of [pseudo parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html),
which resolve to useful values at deployment time. CloudFormation pseudo
parameters can be obtained from static members of the `Aws` class.

It is generally recommended to access pseudo parameters from the scope's `stack`
instead, which guarantees the values produced are qualifying the designated
stack, which is essential in cases where resources are shared cross-stack:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# "this" is the current construct
stack = Stack.of(self)

stack.account# Returns the AWS::AccountId for this stack (or the literal value if known)
stack.region# Returns the AWS::Region for this stack (or the literal value if known)
stack.partition
```

### Resource Options

CloudFormation resources can also specify [resource
attributes](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-attribute-reference.html). The `CfnResource` class allows
accessing those through the `cfnOptions` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
raw_bucket = s3.CfnBucket(self, "Bucket")
# -or-
raw_bucket = bucket.node.default_child

# then
raw_bucket.cfn_options.condition = CfnCondition(self, "EnableBucket")
raw_bucket.cfn_options.metadata = {
    "metadata_key": "MetadataValue"
}
```

Resource dependencies (the `DependsOn` attribute) is modified using the
`cfnResource.addDependsOn` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
resource_a = CfnResource(self, "ResourceA")
resource_b = CfnResource(self, "ResourceB")

resource_b.add_depends_on(resource_a)
```

### Intrinsic Functions and Condition Expressions

CloudFormation supports [intrinsic functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html). These functions
can be accessed from the `Fn` class, which provides type-safe methods for each
intrinsic function as well as condition expressions:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# To use Fn::Base64
Fn.base64("SGVsbG8gQ0RLIQo=")

# To compose condition expressions:
environment_parameter = CfnParameter(self, "Environment")
Fn.condition_and(
    # The "Environment" CloudFormation template parameter evaluates to "Production"
    Fn.condition_equals("Production", environment_parameter),
    # The AWS::Region pseudo-parameter value is NOT equal to "us-east-1"
    Fn.condition_not(Fn.condition_equals("us-east-1", Aws.REGION)))
```

When working with deploy-time values (those for which `Token.isUnresolved`
returns `true`), idiomatic conditionals from the programming language cannot be
used (the value will not be known until deployment time). When conditional logic
needs to be expressed with un-resolved values, it is necessary to use
CloudFormation conditions by means of the `CfnCondition` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
environment_parameter = CfnParameter(self, "Environment")
is_prod = CfnCondition(self, "IsProduction",
    expression=Fn.condition_equals("Production", environment_parameter)
)

# Configuration value that is a different string based on IsProduction
stage = Fn.condition_if(is_prod.logical_id, "Beta", "Prod").to_string()

# Make Bucket creation condition to IsProduction by accessing
# and overriding the CloudFormation resource
bucket = s3.Bucket(self, "Bucket")
cfn_bucket = bucket.node.default_child
cfn_bucket.cfn_options.condition = is_prod
```

### Mappings

CloudFormation [mappings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html) are created and queried using the
`CfnMappings` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mapping = CfnMapping(self, "MappingTable",
    mapping={
        "region_name": {
            "us-east-1": "US East (N. Virginia)",
            "us-east-2": "US East (Ohio)"
        }
    }
)

mapping.find_in_map("regionName", Aws.REGION)
```

### Dynamic References

CloudFormation supports [dynamically resolving](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html) values
for SSM parameters (including secure strings) and Secrets Manager. Encoding such
references is done using the `CfnDynamicReference` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CfnDynamicReference(self, "SecureStringValue",
    service=CfnDynamicReferenceService.SECRETS_MANAGER,
    reference_key="secret-id:secret-string:json-key:version-stage:version-id"
)
```

### Template Options & Transform

CloudFormation templates support a number of options, including which Macros or
[Transforms](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-section-structure.html) to use when deploying the stack. Those can be
configured using the `stack.templateOptions` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = Stack(app, "StackName")

stack.template_options.description = "This will appear in the AWS console"
stack.template_options.transforms = ["AWS::Serverless-2016-10-31"]
stack.template_options.metadata = {
    "metadata_key": "MetadataValue"
}
```

### Emitting Raw Resources

The `CfnResource` class allows emitting arbitrary entries in the
[Resources][cfn-resources] section of the CloudFormation template.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CfnResource(self, "ResourceId",
    type="AWS::S3::Bucket",
    properties={
        "BucketName": "bucket-name"
    }
)
```

As for any other resource, the logical ID in the CloudFormation template will be
generated by the AWS CDK, but the type and properties will be copied verbatim in
the synthesized template.

### Including raw CloudFormation template fragments

When migrating a CloudFormation stack to the AWS CDK, it can be useful to
include fragments of an existing template verbatim in the synthesized template.
This can be achieved using the `CfnInclude` class.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CfnInclude(self, "ID",
    template={
        "Resources": {
            "Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "my-shiny-bucket"
                }
            }
        }
    }
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.cx_api

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/core", "1.23.0", __name__, "core@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/core.AppProps", jsii_struct_bases=[], name_mapping={'auto_synth': 'autoSynth', 'context': 'context', 'outdir': 'outdir', 'runtime_info': 'runtimeInfo', 'stack_traces': 'stackTraces', 'tree_metadata': 'treeMetadata'})
class AppProps():
    def __init__(self, *, auto_synth: typing.Optional[bool]=None, context: typing.Optional[typing.Mapping[str,str]]=None, outdir: typing.Optional[str]=None, runtime_info: typing.Optional[bool]=None, stack_traces: typing.Optional[bool]=None, tree_metadata: typing.Optional[bool]=None):
        """Initialization props for apps.

        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param runtime_info: Include runtime versioning information in cloud assembly manifest. Default: true runtime info is included unless ``aws:cdk:disable-runtime-info`` is set in the context.
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        """
        self._values = {
        }
        if auto_synth is not None: self._values["auto_synth"] = auto_synth
        if context is not None: self._values["context"] = context
        if outdir is not None: self._values["outdir"] = outdir
        if runtime_info is not None: self._values["runtime_info"] = runtime_info
        if stack_traces is not None: self._values["stack_traces"] = stack_traces
        if tree_metadata is not None: self._values["tree_metadata"] = tree_metadata

    @builtins.property
    def auto_synth(self) -> typing.Optional[bool]:
        """Automatically call ``synth()`` before the program exits.

        If you set this, you don't have to call ``synth()`` explicitly. Note that
        this feature is only available for certain programming languages, and
        calling ``synth()`` is still recommended.

        default
        :default:

        true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false``
        otherwise
        """
        return self._values.get('auto_synth')

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Additional context values for the application.

        Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence.

        Context can be read from any construct using ``node.getContext(key)``.

        default
        :default: - no additional context
        """
        return self._values.get('context')

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The output directory into which to emit synthesized artifacts.

        default
        :default:

        - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``.
          If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        """
        return self._values.get('outdir')

    @builtins.property
    def runtime_info(self) -> typing.Optional[bool]:
        """Include runtime versioning information in cloud assembly manifest.

        default
        :default: true runtime info is included unless ``aws:cdk:disable-runtime-info`` is set in the context.
        """
        return self._values.get('runtime_info')

    @builtins.property
    def stack_traces(self) -> typing.Optional[bool]:
        """Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs.

        default
        :default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        """
        return self._values.get('stack_traces')

    @builtins.property
    def tree_metadata(self) -> typing.Optional[bool]:
        """Include construct tree metadata as part of the Cloud Assembly.

        default
        :default: true
        """
        return self._values.get('tree_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Arn(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Arn"):
    @jsii.member(jsii_name="format")
    @builtins.classmethod
    def format(cls, components: "ArnComponents", stack: "Stack") -> str:
        """Creates an ARN from components.

        If ``partition``, ``region`` or ``account`` are not specified, the stack's
        partition, region and account will be used.

        If any component is the empty string, an empty string will be inserted
        into the generated ARN at the location that component corresponds to.

        The ARN will be formatted as follows:

        arn:{partition}:{service}:{region}:{account}:{resource}{sep}{resource-name}

        The required ARN pieces that are omitted will be taken from the stack that
        the 'scope' is attached to. If all ARN pieces are supplied, the supplied scope
        can be 'undefined'.

        :param components: -
        :param stack: -
        """
        return jsii.sinvoke(cls, "format", [components, stack])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, arn: str, sep_if_token: typing.Optional[str]=None, has_name: typing.Optional[bool]=None) -> "ArnComponents":
        """Given an ARN, parses it and returns components.

        If the ARN is a concrete string, it will be parsed and validated. The
        separator (``sep``) will be set to '/' if the 6th component includes a '/',
        in which case, ``resource`` will be set to the value before the '/' and
        ``resourceName`` will be the rest. In case there is no '/', ``resource`` will
        be set to the 6th components and ``resourceName`` will be set to the rest
        of the string.

        If the ARN includes tokens (or is a token), the ARN cannot be validated,
        since we don't have the actual value yet at the time of this function
        call. You will have to know the separator and the type of ARN. The
        resulting ``ArnComponents`` object will contain tokens for the
        subexpressions of the ARN, not string literals. In this case this
        function cannot properly parse the complete final resourceName (path) out
        of ARNs that use '/' to both separate the 'resource' from the
        'resourceName' AND to subdivide the resourceName further. For example, in
        S3 ARNs::

           arn:aws:s3:::my_corporate_bucket/path/to/exampleobject.png

        After parsing the resourceName will not contain
        'path/to/exampleobject.png' but simply 'path'. This is a limitation
        because there is no slicing functionality in CloudFormation templates.

        :param arn: The ARN to parse.
        :param sep_if_token: The separator used to separate resource from resourceName.
        :param has_name: Whether there is a name component in the ARN at all. For example, SNS Topics ARNs have the 'resource' component contain the topic name, and no 'resourceName' component.

        return
        :return:

        an ArnComponents object which allows access to the various
        components of the ARN.
        """
        return jsii.sinvoke(cls, "parse", [arn, sep_if_token, has_name])


@jsii.data_type(jsii_type="@aws-cdk/core.ArnComponents", jsii_struct_bases=[], name_mapping={'resource': 'resource', 'service': 'service', 'account': 'account', 'partition': 'partition', 'region': 'region', 'resource_name': 'resourceName', 'sep': 'sep'})
class ArnComponents():
    def __init__(self, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None):
        """
        :param resource: Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.
        :param service: The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').
        :param account: The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the ARNs for some resources don't require an account number, so this component might be omitted. Default: The account the stack is deployed to.
        :param partition: The partition that the resource is in. For standard AWS regions, the partition is aws. If you have resources in other partitions, the partition is aws-partitionname. For example, the partition for resources in the China (Beijing) region is aws-cn. Default: The AWS partition the stack is deployed to.
        :param region: The region the resource resides in. Note that the ARNs for some resources do not require a region, so this component might be omitted. Default: The region the stack is deployed to.
        :param resource_name: Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.
        :param sep: Separator between resource type and the resource. Can be either '/', ':' or an empty string. Will only be used if resourceName is defined. Default: '/'
        """
        self._values = {
            'resource': resource,
            'service': service,
        }
        if account is not None: self._values["account"] = account
        if partition is not None: self._values["partition"] = partition
        if region is not None: self._values["region"] = region
        if resource_name is not None: self._values["resource_name"] = resource_name
        if sep is not None: self._values["sep"] = sep

    @builtins.property
    def resource(self) -> str:
        """Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name."""
        return self._values.get('resource')

    @builtins.property
    def service(self) -> str:
        """The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline')."""
        return self._values.get('service')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The ID of the AWS account that owns the resource, without the hyphens.

        For example, 123456789012. Note that the ARNs for some resources don't
        require an account number, so this component might be omitted.

        default
        :default: The account the stack is deployed to.
        """
        return self._values.get('account')

    @builtins.property
    def partition(self) -> typing.Optional[str]:
        """The partition that the resource is in.

        For standard AWS regions, the
        partition is aws. If you have resources in other partitions, the
        partition is aws-partitionname. For example, the partition for resources
        in the China (Beijing) region is aws-cn.

        default
        :default: The AWS partition the stack is deployed to.
        """
        return self._values.get('partition')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region the resource resides in.

        Note that the ARNs for some resources
        do not require a region, so this component might be omitted.

        default
        :default: The region the stack is deployed to.
        """
        return self._values.get('region')

    @builtins.property
    def resource_name(self) -> typing.Optional[str]:
        """Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent."""
        return self._values.get('resource_name')

    @builtins.property
    def sep(self) -> typing.Optional[str]:
        """Separator between resource type and the resource.

        Can be either '/', ':' or an empty string. Will only be used if resourceName is defined.

        default
        :default: '/'
        """
        return self._values.get('sep')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArnComponents(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Aws(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Aws"):
    """Accessor for pseudo parameters.

    Since pseudo parameters need to be anchored to a stack somewhere in the
    construct tree, this class takes an scope parameter; the pseudo parameter
    values can be obtained as properties from an scoped object.
    """
    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCOUNT_ID")
    def ACCOUNT_ID(cls) -> str:
        return jsii.sget(cls, "ACCOUNT_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NO_VALUE")
    def NO_VALUE(cls) -> str:
        return jsii.sget(cls, "NO_VALUE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NOTIFICATION_ARNS")
    def NOTIFICATION_ARNS(cls) -> typing.List[str]:
        return jsii.sget(cls, "NOTIFICATION_ARNS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARTITION")
    def PARTITION(cls) -> str:
        return jsii.sget(cls, "PARTITION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGION")
    def REGION(cls) -> str:
        return jsii.sget(cls, "REGION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STACK_ID")
    def STACK_ID(cls) -> str:
        return jsii.sget(cls, "STACK_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="STACK_NAME")
    def STACK_NAME(cls) -> str:
        return jsii.sget(cls, "STACK_NAME")

    @jsii.python.classproperty
    @jsii.member(jsii_name="URL_SUFFIX")
    def URL_SUFFIX(cls) -> str:
        return jsii.sget(cls, "URL_SUFFIX")


@jsii.data_type(jsii_type="@aws-cdk/core.CfnAutoScalingReplacingUpdate", jsii_struct_bases=[], name_mapping={'will_replace': 'willReplace'})
class CfnAutoScalingReplacingUpdate():
    def __init__(self, *, will_replace: typing.Optional[bool]=None):
        """Specifies whether an Auto Scaling group and the instances it contains are replaced during an update.

        During replacement,
        AWS CloudFormation retains the old group until it finishes creating the new one. If the update fails, AWS CloudFormation
        can roll back to the old Auto Scaling group and delete the new Auto Scaling group.

        While AWS CloudFormation creates the new group, it doesn't detach or attach any instances. After successfully creating
        the new Auto Scaling group, AWS CloudFormation deletes the old Auto Scaling group during the cleanup process.

        When you set the WillReplace parameter, remember to specify a matching CreationPolicy. If the minimum number of
        instances (specified by the MinSuccessfulInstancesPercent property) don't signal success within the Timeout period
        (specified in the CreationPolicy policy), the replacement update fails and AWS CloudFormation rolls back to the old
        Auto Scaling group.

        :param will_replace: 
        """
        self._values = {
        }
        if will_replace is not None: self._values["will_replace"] = will_replace

    @builtins.property
    def will_replace(self) -> typing.Optional[bool]:
        return self._values.get('will_replace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingReplacingUpdate(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnAutoScalingRollingUpdate", jsii_struct_bases=[], name_mapping={'max_batch_size': 'maxBatchSize', 'min_instances_in_service': 'minInstancesInService', 'min_successful_instances_percent': 'minSuccessfulInstancesPercent', 'pause_time': 'pauseTime', 'suspend_processes': 'suspendProcesses', 'wait_on_resource_signals': 'waitOnResourceSignals'})
class CfnAutoScalingRollingUpdate():
    def __init__(self, *, max_batch_size: typing.Optional[jsii.Number]=None, min_instances_in_service: typing.Optional[jsii.Number]=None, min_successful_instances_percent: typing.Optional[jsii.Number]=None, pause_time: typing.Optional[str]=None, suspend_processes: typing.Optional[typing.List[str]]=None, wait_on_resource_signals: typing.Optional[bool]=None):
        """To specify how AWS CloudFormation handles rolling updates for an Auto Scaling group, use the AutoScalingRollingUpdate policy.

        Rolling updates enable you to specify whether AWS CloudFormation updates instances that are in an Auto Scaling
        group in batches or all at once.

        :param max_batch_size: Specifies the maximum number of instances that AWS CloudFormation updates.
        :param min_instances_in_service: Specifies the minimum number of instances that must be in service within the Auto Scaling group while AWS CloudFormation updates old instances.
        :param min_successful_instances_percent: Specifies the percentage of instances in an Auto Scaling rolling update that must signal success for an update to succeed. You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent. For example, if you update five instances with a minimum successful percentage of 50, three instances must signal success. If an instance doesn't send a signal within the time specified in the PauseTime property, AWS CloudFormation assumes that the instance wasn't updated. If you specify this property, you must also enable the WaitOnResourceSignals and PauseTime properties.
        :param pause_time: The amount of time that AWS CloudFormation pauses after making a change to a batch of instances to give those instances time to start software applications. For example, you might need to specify PauseTime when scaling up the number of instances in an Auto Scaling group. If you enable the WaitOnResourceSignals property, PauseTime is the amount of time that AWS CloudFormation should wait for the Auto Scaling group to receive the required number of valid signals from added or replaced instances. If the PauseTime is exceeded before the Auto Scaling group receives the required number of signals, the update fails. For best results, specify a time period that gives your applications sufficient time to get started. If the update needs to be rolled back, a short PauseTime can cause the rollback to fail. Specify PauseTime in the ISO8601 duration format (in the format PT#H#M#S, where each # is the number of hours, minutes, and seconds, respectively). The maximum PauseTime is one hour (PT1H).
        :param suspend_processes: Specifies the Auto Scaling processes to suspend during a stack update. Suspending processes prevents Auto Scaling from interfering with a stack update. For example, you can suspend alarming so that Auto Scaling doesn't execute scaling policies associated with an alarm. For valid values, see the ScalingProcesses.member.N parameter for the SuspendProcesses action in the Auto Scaling API Reference.
        :param wait_on_resource_signals: Specifies whether the Auto Scaling group waits on signals from new instances during an update. Use this property to ensure that instances have completed installing and configuring applications before the Auto Scaling group update proceeds. AWS CloudFormation suspends the update of an Auto Scaling group after new EC2 instances are launched into the group. AWS CloudFormation must receive a signal from each new instance within the specified PauseTime before continuing the update. To signal the Auto Scaling group, use the cfn-signal helper script or SignalResource API. To have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template.
        """
        self._values = {
        }
        if max_batch_size is not None: self._values["max_batch_size"] = max_batch_size
        if min_instances_in_service is not None: self._values["min_instances_in_service"] = min_instances_in_service
        if min_successful_instances_percent is not None: self._values["min_successful_instances_percent"] = min_successful_instances_percent
        if pause_time is not None: self._values["pause_time"] = pause_time
        if suspend_processes is not None: self._values["suspend_processes"] = suspend_processes
        if wait_on_resource_signals is not None: self._values["wait_on_resource_signals"] = wait_on_resource_signals

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        """Specifies the maximum number of instances that AWS CloudFormation updates."""
        return self._values.get('max_batch_size')

    @builtins.property
    def min_instances_in_service(self) -> typing.Optional[jsii.Number]:
        """Specifies the minimum number of instances that must be in service within the Auto Scaling group while AWS CloudFormation updates old instances."""
        return self._values.get('min_instances_in_service')

    @builtins.property
    def min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Specifies the percentage of instances in an Auto Scaling rolling update that must signal success for an update to succeed.

        You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent. For example, if you
        update five instances with a minimum successful percentage of 50, three instances must signal success.

        If an instance doesn't send a signal within the time specified in the PauseTime property, AWS CloudFormation assumes
        that the instance wasn't updated.

        If you specify this property, you must also enable the WaitOnResourceSignals and PauseTime properties.
        """
        return self._values.get('min_successful_instances_percent')

    @builtins.property
    def pause_time(self) -> typing.Optional[str]:
        """The amount of time that AWS CloudFormation pauses after making a change to a batch of instances to give those instances time to start software applications.

        For example, you might need to specify PauseTime when scaling up the number of
        instances in an Auto Scaling group.

        If you enable the WaitOnResourceSignals property, PauseTime is the amount of time that AWS CloudFormation should wait
        for the Auto Scaling group to receive the required number of valid signals from added or replaced instances. If the
        PauseTime is exceeded before the Auto Scaling group receives the required number of signals, the update fails. For best
        results, specify a time period that gives your applications sufficient time to get started. If the update needs to be
        rolled back, a short PauseTime can cause the rollback to fail.

        Specify PauseTime in the ISO8601 duration format (in the format PT#H#M#S, where each # is the number of hours, minutes,
        and seconds, respectively). The maximum PauseTime is one hour (PT1H).
        """
        return self._values.get('pause_time')

    @builtins.property
    def suspend_processes(self) -> typing.Optional[typing.List[str]]:
        """Specifies the Auto Scaling processes to suspend during a stack update.

        Suspending processes prevents Auto Scaling from
        interfering with a stack update. For example, you can suspend alarming so that Auto Scaling doesn't execute scaling
        policies associated with an alarm. For valid values, see the ScalingProcesses.member.N parameter for the SuspendProcesses
        action in the Auto Scaling API Reference.
        """
        return self._values.get('suspend_processes')

    @builtins.property
    def wait_on_resource_signals(self) -> typing.Optional[bool]:
        """Specifies whether the Auto Scaling group waits on signals from new instances during an update.

        Use this property to
        ensure that instances have completed installing and configuring applications before the Auto Scaling group update proceeds.
        AWS CloudFormation suspends the update of an Auto Scaling group after new EC2 instances are launched into the group.
        AWS CloudFormation must receive a signal from each new instance within the specified PauseTime before continuing the update.
        To signal the Auto Scaling group, use the cfn-signal helper script or SignalResource API.

        To have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check
        verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling
        rolling updates sample template.
        """
        return self._values.get('wait_on_resource_signals')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingRollingUpdate(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnAutoScalingScheduledAction", jsii_struct_bases=[], name_mapping={'ignore_unmodified_group_size_properties': 'ignoreUnmodifiedGroupSizeProperties'})
class CfnAutoScalingScheduledAction():
    def __init__(self, *, ignore_unmodified_group_size_properties: typing.Optional[bool]=None):
        """With scheduled actions, the group size properties of an Auto Scaling group can change at any time.

        When you update a
        stack with an Auto Scaling group and scheduled action, AWS CloudFormation always sets the group size property values of
        your Auto Scaling group to the values that are defined in the AWS::AutoScaling::AutoScalingGroup resource of your template,
        even if a scheduled action is in effect.

        If you do not want AWS CloudFormation to change any of the group size property values when you have a scheduled action in
        effect, use the AutoScalingScheduledAction update policy to prevent AWS CloudFormation from changing the MinSize, MaxSize,
        or DesiredCapacity properties unless you have modified these values in your template.\

        :param ignore_unmodified_group_size_properties: 
        """
        self._values = {
        }
        if ignore_unmodified_group_size_properties is not None: self._values["ignore_unmodified_group_size_properties"] = ignore_unmodified_group_size_properties

    @builtins.property
    def ignore_unmodified_group_size_properties(self) -> typing.Optional[bool]:
        return self._values.get('ignore_unmodified_group_size_properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingScheduledAction(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnCodeDeployLambdaAliasUpdate", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName', 'deployment_group_name': 'deploymentGroupName', 'after_allow_traffic_hook': 'afterAllowTrafficHook', 'before_allow_traffic_hook': 'beforeAllowTrafficHook'})
class CfnCodeDeployLambdaAliasUpdate():
    def __init__(self, *, application_name: str, deployment_group_name: str, after_allow_traffic_hook: typing.Optional[str]=None, before_allow_traffic_hook: typing.Optional[str]=None):
        """To perform an AWS CodeDeploy deployment when the version changes on an AWS::Lambda::Alias resource, use the CodeDeployLambdaAliasUpdate update policy.

        :param application_name: The name of the AWS CodeDeploy application.
        :param deployment_group_name: The name of the AWS CodeDeploy deployment group. This is where the traffic-shifting policy is set.
        :param after_allow_traffic_hook: The name of the Lambda function to run after traffic routing completes.
        :param before_allow_traffic_hook: The name of the Lambda function to run before traffic routing starts.
        """
        self._values = {
            'application_name': application_name,
            'deployment_group_name': deployment_group_name,
        }
        if after_allow_traffic_hook is not None: self._values["after_allow_traffic_hook"] = after_allow_traffic_hook
        if before_allow_traffic_hook is not None: self._values["before_allow_traffic_hook"] = before_allow_traffic_hook

    @builtins.property
    def application_name(self) -> str:
        """The name of the AWS CodeDeploy application."""
        return self._values.get('application_name')

    @builtins.property
    def deployment_group_name(self) -> str:
        """The name of the AWS CodeDeploy deployment group.

        This is where the traffic-shifting policy is set.
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def after_allow_traffic_hook(self) -> typing.Optional[str]:
        """The name of the Lambda function to run after traffic routing completes."""
        return self._values.get('after_allow_traffic_hook')

    @builtins.property
    def before_allow_traffic_hook(self) -> typing.Optional[str]:
        """The name of the Lambda function to run before traffic routing starts."""
        return self._values.get('before_allow_traffic_hook')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCodeDeployLambdaAliasUpdate(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnConditionProps", jsii_struct_bases=[], name_mapping={'expression': 'expression'})
class CfnConditionProps():
    def __init__(self, *, expression: typing.Optional["ICfnConditionExpression"]=None):
        """
        :param expression: The expression that the condition will evaluate. Default: - None.
        """
        self._values = {
        }
        if expression is not None: self._values["expression"] = expression

    @builtins.property
    def expression(self) -> typing.Optional["ICfnConditionExpression"]:
        """The expression that the condition will evaluate.

        default
        :default: - None.
        """
        return self._values.get('expression')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnConditionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnCreationPolicy", jsii_struct_bases=[], name_mapping={'auto_scaling_creation_policy': 'autoScalingCreationPolicy', 'resource_signal': 'resourceSignal'})
class CfnCreationPolicy():
    def __init__(self, *, auto_scaling_creation_policy: typing.Optional["CfnResourceAutoScalingCreationPolicy"]=None, resource_signal: typing.Optional["CfnResourceSignal"]=None):
        """Associate the CreationPolicy attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

        To signal a
        resource, you can use the cfn-signal helper script or SignalResource API. AWS CloudFormation publishes valid signals
        to the stack events so that you track the number of signals sent.

        The creation policy is invoked only when AWS CloudFormation creates the associated resource. Currently, the only
        AWS CloudFormation resources that support creation policies are AWS::AutoScaling::AutoScalingGroup, AWS::EC2::Instance,
        and AWS::CloudFormation::WaitCondition.

        Use the CreationPolicy attribute when you want to wait on resource configuration actions before stack creation proceeds.
        For example, if you install and configure software applications on an EC2 instance, you might want those applications to
        be running before proceeding. In such cases, you can add a CreationPolicy attribute to the instance, and then send a success
        signal to the instance after the applications are installed and configured. For a detailed example, see Deploying Applications
        on Amazon EC2 with AWS CloudFormation.

        :param auto_scaling_creation_policy: For an Auto Scaling group replacement update, specifies how many instances must signal success for the update to succeed.
        :param resource_signal: When AWS CloudFormation creates the associated resource, configures the number of required success signals and the length of time that AWS CloudFormation waits for those signals.
        """
        if isinstance(auto_scaling_creation_policy, dict): auto_scaling_creation_policy = CfnResourceAutoScalingCreationPolicy(**auto_scaling_creation_policy)
        if isinstance(resource_signal, dict): resource_signal = CfnResourceSignal(**resource_signal)
        self._values = {
        }
        if auto_scaling_creation_policy is not None: self._values["auto_scaling_creation_policy"] = auto_scaling_creation_policy
        if resource_signal is not None: self._values["resource_signal"] = resource_signal

    @builtins.property
    def auto_scaling_creation_policy(self) -> typing.Optional["CfnResourceAutoScalingCreationPolicy"]:
        """For an Auto Scaling group replacement update, specifies how many instances must signal success for the update to succeed."""
        return self._values.get('auto_scaling_creation_policy')

    @builtins.property
    def resource_signal(self) -> typing.Optional["CfnResourceSignal"]:
        """When AWS CloudFormation creates the associated resource, configures the number of required success signals and the length of time that AWS CloudFormation waits for those signals."""
        return self._values.get('resource_signal')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCreationPolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/core.CfnDeletionPolicy")
class CfnDeletionPolicy(enum.Enum):
    """With the DeletionPolicy attribute you can preserve or (in some cases) backup a resource when its stack is deleted.

    You specify a DeletionPolicy attribute for each resource that you want to control. If a resource has no DeletionPolicy
    attribute, AWS CloudFormation deletes the resource by default. Note that this capability also applies to update operations
    that lead to resources being removed.
    """
    DELETE = "DELETE"
    """AWS CloudFormation deletes the resource and all its content if applicable during stack deletion.

    You can add this
    deletion policy to any resource type. By default, if you don't specify a DeletionPolicy, AWS CloudFormation deletes
    your resources. However, be aware of the following considerations:
    """
    RETAIN = "RETAIN"
    """AWS CloudFormation keeps the resource without deleting the resource or its contents when its stack is deleted.

    You can add this deletion policy to any resource type. Note that when AWS CloudFormation completes the stack deletion,
    the stack will be in Delete_Complete state; however, resources that are retained continue to exist and continue to incur
    applicable charges until you delete those resources.
    """
    SNAPSHOT = "SNAPSHOT"
    """For resources that support snapshots (AWS::EC2::Volume, AWS::ElastiCache::CacheCluster, AWS::ElastiCache::ReplicationGroup, AWS::RDS::DBInstance, AWS::RDS::DBCluster, and AWS::Redshift::Cluster), AWS CloudFormation creates a snapshot for the resource before deleting it.

    Note that when AWS CloudFormation completes the stack deletion, the stack will be in the
    Delete_Complete state; however, the snapshots that are created with this policy continue to exist and continue to
    incur applicable charges until you delete those snapshots.
    """

@jsii.data_type(jsii_type="@aws-cdk/core.CfnDynamicReferenceProps", jsii_struct_bases=[], name_mapping={'reference_key': 'referenceKey', 'service': 'service'})
class CfnDynamicReferenceProps():
    def __init__(self, *, reference_key: str, service: "CfnDynamicReferenceService"):
        """Properties for a Dynamic Reference.

        :param reference_key: The reference key of the dynamic reference.
        :param service: The service to retrieve the dynamic reference from.
        """
        self._values = {
            'reference_key': reference_key,
            'service': service,
        }

    @builtins.property
    def reference_key(self) -> str:
        """The reference key of the dynamic reference."""
        return self._values.get('reference_key')

    @builtins.property
    def service(self) -> "CfnDynamicReferenceService":
        """The service to retrieve the dynamic reference from."""
        return self._values.get('service')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDynamicReferenceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/core.CfnDynamicReferenceService")
class CfnDynamicReferenceService(enum.Enum):
    """The service to retrieve the dynamic reference from."""
    SSM = "SSM"
    """Plaintext value stored in AWS Systems Manager Parameter Store."""
    SSM_SECURE = "SSM_SECURE"
    """Secure string stored in AWS Systems Manager Parameter Store."""
    SECRETS_MANAGER = "SECRETS_MANAGER"
    """Secret stored in AWS Secrets Manager."""

@jsii.data_type(jsii_type="@aws-cdk/core.CfnIncludeProps", jsii_struct_bases=[], name_mapping={'template': 'template'})
class CfnIncludeProps():
    def __init__(self, *, template: typing.Mapping[typing.Any, typing.Any]):
        """
        :param template: The CloudFormation template to include in the stack (as is).
        """
        self._values = {
            'template': template,
        }

    @builtins.property
    def template(self) -> typing.Mapping[typing.Any, typing.Any]:
        """The CloudFormation template to include in the stack (as is)."""
        return self._values.get('template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIncludeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnMappingProps", jsii_struct_bases=[], name_mapping={'mapping': 'mapping'})
class CfnMappingProps():
    def __init__(self, *, mapping: typing.Optional[typing.Mapping[str,typing.Mapping[str,typing.Any]]]=None):
        """
        :param mapping: Mapping of key to a set of corresponding set of named values. The key identifies a map of name-value pairs and must be unique within the mapping. For example, if you want to set values based on a region, you can create a mapping that uses the region name as a key and contains the values you want to specify for each specific region. Default: - No mapping.
        """
        self._values = {
        }
        if mapping is not None: self._values["mapping"] = mapping

    @builtins.property
    def mapping(self) -> typing.Optional[typing.Mapping[str,typing.Mapping[str,typing.Any]]]:
        """Mapping of key to a set of corresponding set of named values.

        The key identifies a map of name-value pairs and must be unique within the mapping.

        For example, if you want to set values based on a region, you can create a mapping
        that uses the region name as a key and contains the values you want to specify for
        each specific region.

        default
        :default: - No mapping.
        """
        return self._values.get('mapping')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnOutputProps", jsii_struct_bases=[], name_mapping={'value': 'value', 'condition': 'condition', 'description': 'description', 'export_name': 'exportName'})
class CfnOutputProps():
    def __init__(self, *, value: str, condition: typing.Optional["CfnCondition"]=None, description: typing.Optional[str]=None, export_name: typing.Optional[str]=None):
        """
        :param value: The value of the property returned by the aws cloudformation describe-stacks command. The value of an output can include literals, parameter references, pseudo-parameters, a mapping value, or intrinsic functions.
        :param condition: A condition to associate with this output value. If the condition evaluates to ``false``, this output value will not be included in the stack. Default: - No condition is associated with the output.
        :param description: A String type that describes the output value. The description can be a maximum of 4 K in length. Default: - No description.
        :param export_name: The name used to export the value of this output across stacks. To import the value from another stack, use ``Fn.importValue(exportName)``. Default: - the output is not exported
        """
        self._values = {
            'value': value,
        }
        if condition is not None: self._values["condition"] = condition
        if description is not None: self._values["description"] = description
        if export_name is not None: self._values["export_name"] = export_name

    @builtins.property
    def value(self) -> str:
        """The value of the property returned by the aws cloudformation describe-stacks command.

        The value of an output can include literals, parameter references, pseudo-parameters,
        a mapping value, or intrinsic functions.
        """
        return self._values.get('value')

    @builtins.property
    def condition(self) -> typing.Optional["CfnCondition"]:
        """A condition to associate with this output value.

        If the condition evaluates
        to ``false``, this output value will not be included in the stack.

        default
        :default: - No condition is associated with the output.
        """
        return self._values.get('condition')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A String type that describes the output value.

        The description can be a maximum of 4 K in length.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def export_name(self) -> typing.Optional[str]:
        """The name used to export the value of this output across stacks.

        To import the value from another stack, use ``Fn.importValue(exportName)``.

        default
        :default: - the output is not exported
        """
        return self._values.get('export_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnOutputProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnParameterProps", jsii_struct_bases=[], name_mapping={'allowed_pattern': 'allowedPattern', 'allowed_values': 'allowedValues', 'constraint_description': 'constraintDescription', 'default': 'default', 'description': 'description', 'max_length': 'maxLength', 'max_value': 'maxValue', 'min_length': 'minLength', 'min_value': 'minValue', 'no_echo': 'noEcho', 'type': 'type'})
class CfnParameterProps():
    def __init__(self, *, allowed_pattern: typing.Optional[str]=None, allowed_values: typing.Optional[typing.List[str]]=None, constraint_description: typing.Optional[str]=None, default: typing.Any=None, description: typing.Optional[str]=None, max_length: typing.Optional[jsii.Number]=None, max_value: typing.Optional[jsii.Number]=None, min_length: typing.Optional[jsii.Number]=None, min_value: typing.Optional[jsii.Number]=None, no_echo: typing.Optional[bool]=None, type: typing.Optional[str]=None):
        """
        :param allowed_pattern: A regular expression that represents the patterns to allow for String types. Default: - No constraints on patterns allowed for parameter.
        :param allowed_values: An array containing the list of values allowed for the parameter. Default: - No constraints on values allowed for parameter.
        :param constraint_description: A string that explains a constraint when the constraint is violated. For example, without a constraint description, a parameter that has an allowed pattern of [A-Za-z0-9]+ displays the following error message when the user specifies an invalid value: Default: - No description with customized error message when user specifies invalid values.
        :param default: A value of the appropriate type for the template to use if no value is specified when a stack is created. If you define constraints for the parameter, you must specify a value that adheres to those constraints. Default: - No default value for parameter.
        :param description: A string of up to 4000 characters that describes the parameter. Default: - No description for the parameter.
        :param max_length: An integer value that determines the largest number of characters you want to allow for String types. Default: - None.
        :param max_value: A numeric value that determines the largest numeric value you want to allow for Number types. Default: - None.
        :param min_length: An integer value that determines the smallest number of characters you want to allow for String types. Default: - None.
        :param min_value: A numeric value that determines the smallest numeric value you want to allow for Number types. Default: - None.
        :param no_echo: Whether to mask the parameter value when anyone makes a call that describes the stack. If you set the value to ``true``, the parameter value is masked with asterisks (``*****``). Default: - Parameter values are not masked.
        :param type: The data type for the parameter (DataType). Default: String
        """
        self._values = {
        }
        if allowed_pattern is not None: self._values["allowed_pattern"] = allowed_pattern
        if allowed_values is not None: self._values["allowed_values"] = allowed_values
        if constraint_description is not None: self._values["constraint_description"] = constraint_description
        if default is not None: self._values["default"] = default
        if description is not None: self._values["description"] = description
        if max_length is not None: self._values["max_length"] = max_length
        if max_value is not None: self._values["max_value"] = max_value
        if min_length is not None: self._values["min_length"] = min_length
        if min_value is not None: self._values["min_value"] = min_value
        if no_echo is not None: self._values["no_echo"] = no_echo
        if type is not None: self._values["type"] = type

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[str]:
        """A regular expression that represents the patterns to allow for String types.

        default
        :default: - No constraints on patterns allowed for parameter.
        """
        return self._values.get('allowed_pattern')

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[str]]:
        """An array containing the list of values allowed for the parameter.

        default
        :default: - No constraints on values allowed for parameter.
        """
        return self._values.get('allowed_values')

    @builtins.property
    def constraint_description(self) -> typing.Optional[str]:
        """A string that explains a constraint when the constraint is violated.

        For example, without a constraint description, a parameter that has an allowed
        pattern of [A-Za-z0-9]+ displays the following error message when the user specifies
        an invalid value:

        default
        :default: - No description with customized error message when user specifies invalid values.
        """
        return self._values.get('constraint_description')

    @builtins.property
    def default(self) -> typing.Any:
        """A value of the appropriate type for the template to use if no value is specified when a stack is created.

        If you define constraints for the parameter, you must specify
        a value that adheres to those constraints.

        default
        :default: - No default value for parameter.
        """
        return self._values.get('default')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A string of up to 4000 characters that describes the parameter.

        default
        :default: - No description for the parameter.
        """
        return self._values.get('description')

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        """An integer value that determines the largest number of characters you want to allow for String types.

        default
        :default: - None.
        """
        return self._values.get('max_length')

    @builtins.property
    def max_value(self) -> typing.Optional[jsii.Number]:
        """A numeric value that determines the largest numeric value you want to allow for Number types.

        default
        :default: - None.
        """
        return self._values.get('max_value')

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        """An integer value that determines the smallest number of characters you want to allow for String types.

        default
        :default: - None.
        """
        return self._values.get('min_length')

    @builtins.property
    def min_value(self) -> typing.Optional[jsii.Number]:
        """A numeric value that determines the smallest numeric value you want to allow for Number types.

        default
        :default: - None.
        """
        return self._values.get('min_value')

    @builtins.property
    def no_echo(self) -> typing.Optional[bool]:
        """Whether to mask the parameter value when anyone makes a call that describes the stack.

        If you set the value to ``true``, the parameter value is masked with asterisks (``*****``).

        default
        :default: - Parameter values are not masked.
        """
        return self._values.get('no_echo')

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """The data type for the parameter (DataType).

        default
        :default: String
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnParameterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnResourceAutoScalingCreationPolicy", jsii_struct_bases=[], name_mapping={'min_successful_instances_percent': 'minSuccessfulInstancesPercent'})
class CfnResourceAutoScalingCreationPolicy():
    def __init__(self, *, min_successful_instances_percent: typing.Optional[jsii.Number]=None):
        """For an Auto Scaling group replacement update, specifies how many instances must signal success for the update to succeed.

        :param min_successful_instances_percent: Specifies the percentage of instances in an Auto Scaling replacement update that must signal success for the update to succeed. You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent. For example, if you update five instances with a minimum successful percentage of 50, three instances must signal success. If an instance doesn't send a signal within the time specified by the Timeout property, AWS CloudFormation assumes that the instance wasn't created.
        """
        self._values = {
        }
        if min_successful_instances_percent is not None: self._values["min_successful_instances_percent"] = min_successful_instances_percent

    @builtins.property
    def min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Specifies the percentage of instances in an Auto Scaling replacement update that must signal success for the update to succeed.

        You can specify a value from 0 to 100. AWS CloudFormation rounds to the nearest tenth of a percent.
        For example, if you update five instances with a minimum successful percentage of 50, three instances must signal success.
        If an instance doesn't send a signal within the time specified by the Timeout property, AWS CloudFormation assumes that the
        instance wasn't created.
        """
        return self._values.get('min_successful_instances_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceAutoScalingCreationPolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnResourceProps", jsii_struct_bases=[], name_mapping={'type': 'type', 'properties': 'properties'})
class CfnResourceProps():
    def __init__(self, *, type: str, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None):
        """
        :param type: CloudFormation resource type (e.g. ``AWS::S3::Bucket``).
        :param properties: Resource properties. Default: - No resource properties.
        """
        self._values = {
            'type': type,
        }
        if properties is not None: self._values["properties"] = properties

    @builtins.property
    def type(self) -> str:
        """CloudFormation resource type (e.g. ``AWS::S3::Bucket``)."""
        return self._values.get('type')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Resource properties.

        default
        :default: - No resource properties.
        """
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnResourceSignal", jsii_struct_bases=[], name_mapping={'count': 'count', 'timeout': 'timeout'})
class CfnResourceSignal():
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, timeout: typing.Optional[str]=None):
        """When AWS CloudFormation creates the associated resource, configures the number of required success signals and the length of time that AWS CloudFormation waits for those signals.

        :param count: The number of success signals AWS CloudFormation must receive before it sets the resource status as CREATE_COMPLETE. If the resource receives a failure signal or doesn't receive the specified number of signals before the timeout period expires, the resource creation fails and AWS CloudFormation rolls the stack back.
        :param timeout: The length of time that AWS CloudFormation waits for the number of signals that was specified in the Count property. The timeout period starts after AWS CloudFormation starts creating the resource, and the timeout expires no sooner than the time you specify but can occur shortly thereafter. The maximum time that you can specify is 12 hours.
        """
        self._values = {
        }
        if count is not None: self._values["count"] = count
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """The number of success signals AWS CloudFormation must receive before it sets the resource status as CREATE_COMPLETE.

        If the resource receives a failure signal or doesn't receive the specified number of signals before the timeout period
        expires, the resource creation fails and AWS CloudFormation rolls the stack back.
        """
        return self._values.get('count')

    @builtins.property
    def timeout(self) -> typing.Optional[str]:
        """The length of time that AWS CloudFormation waits for the number of signals that was specified in the Count property.

        The timeout period starts after AWS CloudFormation starts creating the resource, and the timeout expires no sooner
        than the time you specify but can occur shortly thereafter. The maximum time that you can specify is 12 hours.
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceSignal(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnRuleAssertion", jsii_struct_bases=[], name_mapping={'assert_': 'assert', 'assert_description': 'assertDescription'})
class CfnRuleAssertion():
    def __init__(self, *, assert_: "ICfnConditionExpression", assert_description: str):
        """A rule assertion.

        :param assert_: The assertion.
        :param assert_description: The assertion description.
        """
        self._values = {
            'assert_': assert_,
            'assert_description': assert_description,
        }

    @builtins.property
    def assert_(self) -> "ICfnConditionExpression":
        """The assertion."""
        return self._values.get('assert_')

    @builtins.property
    def assert_description(self) -> str:
        """The assertion description."""
        return self._values.get('assert_description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRuleAssertion(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnRuleProps", jsii_struct_bases=[], name_mapping={'assertions': 'assertions', 'rule_condition': 'ruleCondition'})
class CfnRuleProps():
    def __init__(self, *, assertions: typing.Optional[typing.List["CfnRuleAssertion"]]=None, rule_condition: typing.Optional["ICfnConditionExpression"]=None):
        """A rule can include a RuleCondition property and must include an Assertions property.

        For each rule, you can define only one rule condition; you can define one or more asserts within the Assertions property.
        You define a rule condition and assertions by using rule-specific intrinsic functions.

        You can use the following rule-specific intrinsic functions to define rule conditions and assertions:

        Fn::And
        Fn::Contains
        Fn::EachMemberEquals
        Fn::EachMemberIn
        Fn::Equals
        Fn::If
        Fn::Not
        Fn::Or
        Fn::RefAll
        Fn::ValueOf
        Fn::ValueOfAll

        https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html

        :param assertions: Assertions which define the rule. Default: - No assertions for the rule.
        :param rule_condition: If the rule condition evaluates to false, the rule doesn't take effect. If the function in the rule condition evaluates to true, expressions in each assert are evaluated and applied. Default: - Rule's assertions will always take effect.
        """
        self._values = {
        }
        if assertions is not None: self._values["assertions"] = assertions
        if rule_condition is not None: self._values["rule_condition"] = rule_condition

    @builtins.property
    def assertions(self) -> typing.Optional[typing.List["CfnRuleAssertion"]]:
        """Assertions which define the rule.

        default
        :default: - No assertions for the rule.
        """
        return self._values.get('assertions')

    @builtins.property
    def rule_condition(self) -> typing.Optional["ICfnConditionExpression"]:
        """If the rule condition evaluates to false, the rule doesn't take effect.

        If the function in the rule condition evaluates to true, expressions in each assert are evaluated and applied.

        default
        :default: - Rule's assertions will always take effect.
        """
        return self._values.get('rule_condition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnTag", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
class CfnTag():
    def __init__(self, *, key: str, value: str):
        """
        :param key: 
        :param value: 

        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html
        """
        self._values = {
            'key': key,
            'value': value,
        }

    @builtins.property
    def key(self) -> str:
        """
        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html#cfn-resource-tags-key
        """
        return self._values.get('key')

    @builtins.property
    def value(self) -> str:
        """
        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html#cfn-resource-tags-value
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTag(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.CfnUpdatePolicy", jsii_struct_bases=[], name_mapping={'auto_scaling_replacing_update': 'autoScalingReplacingUpdate', 'auto_scaling_rolling_update': 'autoScalingRollingUpdate', 'auto_scaling_scheduled_action': 'autoScalingScheduledAction', 'code_deploy_lambda_alias_update': 'codeDeployLambdaAliasUpdate', 'use_online_resharding': 'useOnlineResharding'})
class CfnUpdatePolicy():
    def __init__(self, *, auto_scaling_replacing_update: typing.Optional["CfnAutoScalingReplacingUpdate"]=None, auto_scaling_rolling_update: typing.Optional["CfnAutoScalingRollingUpdate"]=None, auto_scaling_scheduled_action: typing.Optional["CfnAutoScalingScheduledAction"]=None, code_deploy_lambda_alias_update: typing.Optional["CfnCodeDeployLambdaAliasUpdate"]=None, use_online_resharding: typing.Optional[bool]=None):
        """Use the UpdatePolicy attribute to specify how AWS CloudFormation handles updates to the AWS::AutoScaling::AutoScalingGroup resource.

        AWS CloudFormation invokes one of three update policies depending on the type of change you make or whether a
        scheduled action is associated with the Auto Scaling group.

        :param auto_scaling_replacing_update: Specifies whether an Auto Scaling group and the instances it contains are replaced during an update. During replacement, AWS CloudFormation retains the old group until it finishes creating the new one. If the update fails, AWS CloudFormation can roll back to the old Auto Scaling group and delete the new Auto Scaling group.
        :param auto_scaling_rolling_update: To specify how AWS CloudFormation handles rolling updates for an Auto Scaling group, use the AutoScalingRollingUpdate policy. Rolling updates enable you to specify whether AWS CloudFormation updates instances that are in an Auto Scaling group in batches or all at once.
        :param auto_scaling_scheduled_action: To specify how AWS CloudFormation handles updates for the MinSize, MaxSize, and DesiredCapacity properties when the AWS::AutoScaling::AutoScalingGroup resource has an associated scheduled action, use the AutoScalingScheduledAction policy.
        :param code_deploy_lambda_alias_update: To perform an AWS CodeDeploy deployment when the version changes on an AWS::Lambda::Alias resource, use the CodeDeployLambdaAliasUpdate update policy.
        :param use_online_resharding: To modify a replication group's shards by adding or removing shards, rather than replacing the entire AWS::ElastiCache::ReplicationGroup resource, use the UseOnlineResharding update policy.
        """
        if isinstance(auto_scaling_replacing_update, dict): auto_scaling_replacing_update = CfnAutoScalingReplacingUpdate(**auto_scaling_replacing_update)
        if isinstance(auto_scaling_rolling_update, dict): auto_scaling_rolling_update = CfnAutoScalingRollingUpdate(**auto_scaling_rolling_update)
        if isinstance(auto_scaling_scheduled_action, dict): auto_scaling_scheduled_action = CfnAutoScalingScheduledAction(**auto_scaling_scheduled_action)
        if isinstance(code_deploy_lambda_alias_update, dict): code_deploy_lambda_alias_update = CfnCodeDeployLambdaAliasUpdate(**code_deploy_lambda_alias_update)
        self._values = {
        }
        if auto_scaling_replacing_update is not None: self._values["auto_scaling_replacing_update"] = auto_scaling_replacing_update
        if auto_scaling_rolling_update is not None: self._values["auto_scaling_rolling_update"] = auto_scaling_rolling_update
        if auto_scaling_scheduled_action is not None: self._values["auto_scaling_scheduled_action"] = auto_scaling_scheduled_action
        if code_deploy_lambda_alias_update is not None: self._values["code_deploy_lambda_alias_update"] = code_deploy_lambda_alias_update
        if use_online_resharding is not None: self._values["use_online_resharding"] = use_online_resharding

    @builtins.property
    def auto_scaling_replacing_update(self) -> typing.Optional["CfnAutoScalingReplacingUpdate"]:
        """Specifies whether an Auto Scaling group and the instances it contains are replaced during an update.

        During replacement,
        AWS CloudFormation retains the old group until it finishes creating the new one. If the update fails, AWS CloudFormation
        can roll back to the old Auto Scaling group and delete the new Auto Scaling group.
        """
        return self._values.get('auto_scaling_replacing_update')

    @builtins.property
    def auto_scaling_rolling_update(self) -> typing.Optional["CfnAutoScalingRollingUpdate"]:
        """To specify how AWS CloudFormation handles rolling updates for an Auto Scaling group, use the AutoScalingRollingUpdate policy.

        Rolling updates enable you to specify whether AWS CloudFormation updates instances that are in an Auto Scaling
        group in batches or all at once.
        """
        return self._values.get('auto_scaling_rolling_update')

    @builtins.property
    def auto_scaling_scheduled_action(self) -> typing.Optional["CfnAutoScalingScheduledAction"]:
        """To specify how AWS CloudFormation handles updates for the MinSize, MaxSize, and DesiredCapacity properties when the AWS::AutoScaling::AutoScalingGroup resource has an associated scheduled action, use the AutoScalingScheduledAction policy."""
        return self._values.get('auto_scaling_scheduled_action')

    @builtins.property
    def code_deploy_lambda_alias_update(self) -> typing.Optional["CfnCodeDeployLambdaAliasUpdate"]:
        """To perform an AWS CodeDeploy deployment when the version changes on an AWS::Lambda::Alias resource, use the CodeDeployLambdaAliasUpdate update policy."""
        return self._values.get('code_deploy_lambda_alias_update')

    @builtins.property
    def use_online_resharding(self) -> typing.Optional[bool]:
        """To modify a replication group's shards by adding or removing shards, rather than replacing the entire AWS::ElastiCache::ReplicationGroup resource, use the UseOnlineResharding update policy."""
        return self._values.get('use_online_resharding')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUpdatePolicy(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ConstructNode(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.ConstructNode"):
    """Represents the construct node in the scope tree."""
    def __init__(self, host: "Construct", scope: "IConstruct", id: str) -> None:
        """
        :param host: -
        :param scope: -
        :param id: -
        """
        jsii.create(ConstructNode, self, [host, scope, id])

    @jsii.member(jsii_name="prepare")
    @builtins.classmethod
    def prepare(cls, node: "ConstructNode") -> None:
        """Invokes "prepare" on all constructs (depth-first, post-order) in the tree under ``node``.

        :param node: The root node.
        """
        return jsii.sinvoke(cls, "prepare", [node])

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, root: "ConstructNode", *, outdir: typing.Optional[str]=None, skip_validation: typing.Optional[bool]=None, runtime_info: typing.Optional[aws_cdk.cx_api.RuntimeInfo]=None) -> aws_cdk.cx_api.CloudAssembly:
        """Synthesizes a CloudAssembly from a construct tree.

        :param root: The root of the construct tree.
        :param outdir: The output directory into which to synthesize the cloud assembly. Default: - creates a temporary directory
        :param skip_validation: Whether synthesis should skip the validation phase. Default: false
        :param runtime_info: Include the specified runtime information (module versions) in manifest. Default: - if this option is not specified, runtime info will not be included
        """
        options = SynthesisOptions(outdir=outdir, skip_validation=skip_validation, runtime_info=runtime_info)

        return jsii.sinvoke(cls, "synth", [root, options])

    @jsii.member(jsii_name="validate")
    @builtins.classmethod
    def validate(cls, node: "ConstructNode") -> typing.List["ValidationError"]:
        """Invokes "validate" on all constructs in the tree (depth-first, pre-order) and returns the list of all errors.

        An empty list indicates that there are no errors.

        :param node: The root node.
        """
        return jsii.sinvoke(cls, "validate", [node])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: "IDependable") -> None:
        """Add an ordering dependency on another Construct.

        All constructs in the dependency's scope will be deployed before any
        construct in this construct's scope.

        :param dependencies: -
        """
        return jsii.invoke(self, "addDependency", [*dependencies])

    @jsii.member(jsii_name="addError")
    def add_error(self, message: str) -> None:
        """Adds an { error:  } metadata entry to this construct.

        The toolkit will fail synthesis when errors are reported.

        :param message: The error message.
        """
        return jsii.invoke(self, "addError", [message])

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: str) -> None:
        """Adds a { "aws:cdk:info":  } metadata entry to this construct.

        The toolkit will display the info message when apps are synthesized.

        :param message: The info message.
        """
        return jsii.invoke(self, "addInfo", [message])

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(self, type: str, data: typing.Any, from_: typing.Any=None) -> None:
        """Adds a metadata entry to this construct.

        Entries are arbitrary values and will also include a stack trace to allow tracing back to
        the code location for when the entry was added. It can be used, for example, to include source
        mapping in CloudFormation templates to improve diagnostics.

        :param type: a string denoting the type of metadata.
        :param data: the value of the metadata (can be a Token). If null/undefined, metadata will not be added.
        :param from_: a function under which to restrict the metadata entry's stack trace (defaults to this.addMetadata).
        """
        return jsii.invoke(self, "addMetadata", [type, data, from_])

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: str) -> None:
        """Adds a { warning:  } metadata entry to this construct.

        The toolkit will display the warning when an app is synthesized, or fail
        if run in --strict mode.

        :param message: The warning message.
        """
        return jsii.invoke(self, "addWarning", [message])

    @jsii.member(jsii_name="applyAspect")
    def apply_aspect(self, aspect: "IAspect") -> None:
        """Applies the aspect to this Constructs node.

        :param aspect: -
        """
        return jsii.invoke(self, "applyAspect", [aspect])

    @jsii.member(jsii_name="findAll")
    def find_all(self, order: typing.Optional["ConstructOrder"]=None) -> typing.List["IConstruct"]:
        """Return this construct and all of its children in the given order.

        :param order: -
        """
        return jsii.invoke(self, "findAll", [order])

    @jsii.member(jsii_name="findChild")
    def find_child(self, id: str) -> "IConstruct":
        """Return a direct child by id.

        Throws an error if the child is not found.

        :param id: Identifier of direct child.

        return
        :return: Child with the given id.
        """
        return jsii.invoke(self, "findChild", [id])

    @jsii.member(jsii_name="setContext")
    def set_context(self, key: str, value: typing.Any) -> None:
        """This can be used to set contextual values.

        Context must be set before any children are added, since children may consult context info during construction.
        If the key already exists, it will be overridden.

        :param key: The context key.
        :param value: The context value.
        """
        return jsii.invoke(self, "setContext", [key, value])

    @jsii.member(jsii_name="tryFindChild")
    def try_find_child(self, id: str) -> typing.Optional["IConstruct"]:
        """Return a direct child by id, or undefined.

        :param id: Identifier of direct child.

        return
        :return: the child if found, or undefined
        """
        return jsii.invoke(self, "tryFindChild", [id])

    @jsii.member(jsii_name="tryGetContext")
    def try_get_context(self, key: str) -> typing.Any:
        """Retrieves a value from tree context.

        Context is usually initialized at the root, but can be overridden at any point in the tree.

        :param key: The context key.

        return
        :return: The context value or ``undefined`` if there is no context value for thie key.
        """
        return jsii.invoke(self, "tryGetContext", [key])

    @jsii.member(jsii_name="tryRemoveChild")
    def try_remove_child(self, child_name: str) -> bool:
        """Remove the child with the given name, if present.

        :param child_name: -

        return
        :return: Whether a child with the given name was deleted.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "tryRemoveChild", [child_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH_SEP")
    def PATH_SEP(cls) -> str:
        """Separator used to delimit construct path components."""
        return jsii.sget(cls, "PATH_SEP")

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List["IConstruct"]:
        """All direct children of this construct."""
        return jsii.get(self, "children")

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Dependency"]:
        """Return all dependencies registered on this node or any of its children."""
        return jsii.get(self, "dependencies")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """The id of this construct within the current scope.

        This is a a scope-unique id. To obtain an app-unique id for this construct, use ``uniqueId``.
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> bool:
        """Returns true if this construct or the scopes in which it is defined are locked."""
        return jsii.get(self, "locked")

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List[aws_cdk.cx_api.MetadataEntry]:
        """An immutable array of metadata objects associated with this construct.

        This can be used, for example, to implement support for deprecation notices, source mapping, etc.
        """
        return jsii.get(self, "metadata")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The full, absolute path of this construct in the tree.

        Components are separated by '/'.
        """
        return jsii.get(self, "path")

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "IConstruct":
        """
        return
        :return: The root of the construct tree.
        """
        return jsii.get(self, "root")

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List["IConstruct"]:
        """All parent scopes of this construct.

        return
        :return:

        a list of parent scopes. The last element in the list will always
        be the current construct and the first element will be the root of the
        tree.
        """
        return jsii.get(self, "scopes")

    @builtins.property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A tree-global unique alphanumeric identifier for this construct.

        Includes all components of the tree.
        """
        return jsii.get(self, "uniqueId")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional["IConstruct"]:
        """Returns the scope in which this construct is defined.

        The value is ``undefined`` at the root of the construct scope tree.
        """
        return jsii.get(self, "scope")

    @builtins.property
    @jsii.member(jsii_name="defaultChild")
    def default_child(self) -> typing.Optional["IConstruct"]:
        """Returns the child construct that has the id ``Default`` or ``Resource"``.

        This is usually the construct that provides the bulk of the underlying functionality.
        Useful for modifications of the underlying construct that are not available at the higher levels.
        Override the defaultChild property.

        This should only be used in the cases where the correct
        default child is not named 'Resource' or 'Default' as it
        should be.

        If you set this to undefined, the default behavior of finding
        the child named 'Resource' or 'Default' will be used.

        return
        :return: a construct or undefined if there is no default child

        throws:
        :throws:: if there is more than one child
        """
        return jsii.get(self, "defaultChild")

    @default_child.setter
    def default_child(self, value: typing.Optional["IConstruct"]):
        jsii.set(self, "defaultChild", value)


@jsii.enum(jsii_type="@aws-cdk/core.ConstructOrder")
class ConstructOrder(enum.Enum):
    """In what order to return constructs."""
    PREORDER = "PREORDER"
    """Depth-first, pre-order."""
    POSTORDER = "POSTORDER"
    """Depth-first, post-order (leaf nodes first)."""

class ContextProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.ContextProvider"):
    """Base class for the model side of context providers.

    Instances of this class communicate with context provider plugins in the 'cdk
    toolkit' via context variables (input), outputting specialized queries for
    more context variables (output).

    ContextProvider needs access to a Construct to hook into the context mechanism.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="getKey")
    @builtins.classmethod
    def get_key(cls, scope: "Construct", *, provider: str, props: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> "GetContextKeyResult":
        """
        :param scope: -
        :param provider: The context provider to query.
        :param props: Provider-specific properties.

        return
        :return: the context key or undefined if a key cannot be rendered (due to tokens used in any of the props)

        stability
        :stability: experimental
        """
        options = GetContextKeyOptions(provider=provider, props=props)

        return jsii.sinvoke(cls, "getKey", [scope, options])

    @jsii.member(jsii_name="getValue")
    @builtins.classmethod
    def get_value(cls, scope: "Construct", *, dummy_value: typing.Any, provider: str, props: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> "GetContextValueResult":
        """
        :param scope: -
        :param dummy_value: The value to return if the context value was not found and a missing context is reported. This should be a dummy value that should preferably fail during deployment since it represents an invalid state.
        :param provider: The context provider to query.
        :param props: Provider-specific properties.

        stability
        :stability: experimental
        """
        options = GetContextValueOptions(dummy_value=dummy_value, provider=provider, props=props)

        return jsii.sinvoke(cls, "getValue", [scope, options])


class DependableTrait(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/core.DependableTrait"):
    """Trait for IDependable.

    Traits are interfaces that are privately implemented by objects. Instead of
    showing up in the public interface of a class, they need to be queried
    explicitly. This is used to implement certain framework features that are
    not intended to be used by Construct consumers, and so should be hidden
    from accidental use.

    stability
    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # Usage
        roots = DependableTrait.get(construct).dependency_roots
        
        # Definition
        DependableTrait.implement(construct, get dependencyRoots() { return []; }
        )
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _DependableTraitProxy

    def __init__(self) -> None:
        jsii.create(DependableTrait, self, [])

    @jsii.member(jsii_name="get")
    @builtins.classmethod
    def get(cls, instance: "IDependable") -> "DependableTrait":
        """Return the matching DependableTrait for the given class instance.

        :param instance: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "get", [instance])

    @jsii.member(jsii_name="implement")
    @builtins.classmethod
    def implement(cls, instance: "IDependable", trait: "DependableTrait") -> None:
        """Register ``instance`` to have the given DependableTrait.

        Should be called in the class constructor.

        :param instance: -
        :param trait: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "implement", [instance, trait])

    @builtins.property
    @jsii.member(jsii_name="dependencyRoots")
    @abc.abstractmethod
    def dependency_roots(self) -> typing.List["IConstruct"]:
        """The set of constructs that form the root of this dependable.

        All resources under all returned constructs are included in the ordering
        dependency.

        stability
        :stability: experimental
        """
        ...


class _DependableTraitProxy(DependableTrait):
    @builtins.property
    @jsii.member(jsii_name="dependencyRoots")
    def dependency_roots(self) -> typing.List["IConstruct"]:
        """The set of constructs that form the root of this dependable.

        All resources under all returned constructs are included in the ordering
        dependency.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dependencyRoots")


@jsii.data_type(jsii_type="@aws-cdk/core.Dependency", jsii_struct_bases=[], name_mapping={'source': 'source', 'target': 'target'})
class Dependency():
    def __init__(self, *, source: "IConstruct", target: "IConstruct"):
        """A single dependency.

        :param source: Source the dependency.
        :param target: Target of the dependency.
        """
        self._values = {
            'source': source,
            'target': target,
        }

    @builtins.property
    def source(self) -> "IConstruct":
        """Source the dependency."""
        return self._values.get('source')

    @builtins.property
    def target(self) -> "IConstruct":
        """Target of the dependency."""
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Dependency(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.DockerImageAssetLocation", jsii_struct_bases=[], name_mapping={'image_uri': 'imageUri', 'repository_name': 'repositoryName'})
class DockerImageAssetLocation():
    def __init__(self, *, image_uri: str, repository_name: str):
        """The location of the published docker image.

        This is where the image can be
        consumed at runtime.

        :param image_uri: The URI of the image in Amazon ECR.
        :param repository_name: The name of the ECR repository.
        """
        self._values = {
            'image_uri': image_uri,
            'repository_name': repository_name,
        }

    @builtins.property
    def image_uri(self) -> str:
        """The URI of the image in Amazon ECR."""
        return self._values.get('image_uri')

    @builtins.property
    def repository_name(self) -> str:
        """The name of the ECR repository."""
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAssetLocation(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.DockerImageAssetSource", jsii_struct_bases=[], name_mapping={'directory_name': 'directoryName', 'source_hash': 'sourceHash', 'docker_build_args': 'dockerBuildArgs', 'docker_build_target': 'dockerBuildTarget', 'docker_file': 'dockerFile', 'repository_name': 'repositoryName'})
class DockerImageAssetSource():
    def __init__(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str,str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None):
        """
        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.
        """
        self._values = {
            'directory_name': directory_name,
            'source_hash': source_hash,
        }
        if docker_build_args is not None: self._values["docker_build_args"] = docker_build_args
        if docker_build_target is not None: self._values["docker_build_target"] = docker_build_target
        if docker_file is not None: self._values["docker_file"] = docker_file
        if repository_name is not None: self._values["repository_name"] = repository_name

    @builtins.property
    def directory_name(self) -> str:
        """The directory where the Dockerfile is stored, must be relative to the cloud assembly root."""
        return self._values.get('directory_name')

    @builtins.property
    def source_hash(self) -> str:
        """The hash of the contents of the docker build context.

        This hash is used
        throughout the system to identify this image and avoid duplicate work
        in case the source did not change.

        NOTE: this means that if you wish to update your docker image, you
        must make a modification to the source (e.g. add some metadata to your Dockerfile).
        """
        return self._values.get('source_hash')

    @builtins.property
    def docker_build_args(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        default
        :default: - no build args are passed
        """
        return self._values.get('docker_build_args')

    @builtins.property
    def docker_build_target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: - no target
        """
        return self._values.get('docker_build_target')

    @builtins.property
    def docker_file(self) -> typing.Optional[str]:
        """Path to the Dockerfile (relative to the directory).

        default
        :default: - no file
        """
        return self._values.get('docker_file')

    @builtins.property
    def repository_name(self) -> typing.Optional[str]:
        """ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        default
        :default: - automatically derived from the asset's ID.

        deprecated
        :deprecated: repository name should be specified at the environment-level and not at the image level

        stability
        :stability: deprecated
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAssetSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Duration(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Duration"):
    """Represents a length of time.

    The amount can be specified either as a literal value (e.g: ``10``) which
    cannot be negative, or as an unresolved number token.

    Whent he amount is passed as an token, unit conversion is not possible.
    """
    @jsii.member(jsii_name="days")
    @builtins.classmethod
    def days(cls, amount: jsii.Number) -> "Duration":
        """
        :param amount: the amount of Days the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Days.
        """
        return jsii.sinvoke(cls, "days", [amount])

    @jsii.member(jsii_name="hours")
    @builtins.classmethod
    def hours(cls, amount: jsii.Number) -> "Duration":
        """
        :param amount: the amount of Hours the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Hours.
        """
        return jsii.sinvoke(cls, "hours", [amount])

    @jsii.member(jsii_name="millis")
    @builtins.classmethod
    def millis(cls, amount: jsii.Number) -> "Duration":
        """
        :param amount: the amount of Milliseconds the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` ms.
        """
        return jsii.sinvoke(cls, "millis", [amount])

    @jsii.member(jsii_name="minutes")
    @builtins.classmethod
    def minutes(cls, amount: jsii.Number) -> "Duration":
        """
        :param amount: the amount of Minutes the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Minutes.
        """
        return jsii.sinvoke(cls, "minutes", [amount])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, duration: str) -> "Duration":
        """Parse a period formatted according to the ISO 8601 standard (see https://www.iso.org/fr/standard/70907.html).

        :param duration: an ISO-formtted duration to be parsed.

        return
        :return: the parsed ``Duration``.
        """
        return jsii.sinvoke(cls, "parse", [duration])

    @jsii.member(jsii_name="seconds")
    @builtins.classmethod
    def seconds(cls, amount: jsii.Number) -> "Duration":
        """
        :param amount: the amount of Seconds the ``Duration`` will represent.

        return
        :return: a new ``Duration`` representing ``amount`` Seconds.
        """
        return jsii.sinvoke(cls, "seconds", [amount])

    @jsii.member(jsii_name="toDays")
    def to_days(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """
        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Days.
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toDays", [opts])

    @jsii.member(jsii_name="toHours")
    def to_hours(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """
        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Hours.
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toHours", [opts])

    @jsii.member(jsii_name="toISOString")
    def to_iso_string(self) -> str:
        """
        return
        :return: an ISO 8601 representation of this period (see https://www.iso.org/fr/standard/70907.html).
        """
        return jsii.invoke(self, "toISOString", [])

    @jsii.member(jsii_name="toMilliseconds")
    def to_milliseconds(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """
        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Milliseconds.
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toMilliseconds", [opts])

    @jsii.member(jsii_name="toMinutes")
    def to_minutes(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """
        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Minutes.
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toMinutes", [opts])

    @jsii.member(jsii_name="toSeconds")
    def to_seconds(self, *, integral: typing.Optional[bool]=None) -> jsii.Number:
        """
        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer. Default: true

        return
        :return: the value of this ``Duration`` expressed in Seconds.
        """
        opts = TimeConversionOptions(integral=integral)

        return jsii.invoke(self, "toSeconds", [opts])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of this ``Duration`` that is also a Token that cannot be successfully resolved.

        This
        protects users against inadvertently stringifying a ``Duration`` object, when they should have called one of the
        ``to*`` methods instead.
        """
        return jsii.invoke(self, "toString", [])


@jsii.data_type(jsii_type="@aws-cdk/core.EncodingOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint'})
class EncodingOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None):
        """Properties to string encodings.

        :param display_hint: A hint for the Token's purpose when stringifying it.
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """A hint for the Token's purpose when stringifying it."""
        return self._values.get('display_hint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EncodingOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.Environment", jsii_struct_bases=[], name_mapping={'account': 'account', 'region': 'region'})
class Environment():
    def __init__(self, *, account: typing.Optional[str]=None, region: typing.Optional[str]=None):
        """The deployment environment for a stack.

        :param account: The AWS account ID for this environment. This can be either a concrete value such as ``585191031104`` or ``Aws.accountId`` which indicates that account ID will only be determined during deployment (it will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::AccountId"}``). Note that certain features, such as cross-stack references and environmental context providers require concerete region information and will cause this stack to emit synthesis errors. Default: Aws.accountId which means that the stack will be account-agnostic.
        :param region: The AWS region for this environment. This can be either a concrete value such as ``eu-west-2`` or ``Aws.region`` which indicates that account ID will only be determined during deployment (it will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::Region"}``). Note that certain features, such as cross-stack references and environmental context providers require concerete region information and will cause this stack to emit synthesis errors. Default: Aws.region which means that the stack will be region-agnostic.
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if region is not None: self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """The AWS account ID for this environment.

        This can be either a concrete value such as ``585191031104`` or ``Aws.accountId`` which
        indicates that account ID will only be determined during deployment (it
        will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::AccountId"}``).
        Note that certain features, such as cross-stack references and
        environmental context providers require concerete region information and
        will cause this stack to emit synthesis errors.

        default
        :default: Aws.accountId which means that the stack will be account-agnostic.
        """
        return self._values.get('account')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The AWS region for this environment.

        This can be either a concrete value such as ``eu-west-2`` or ``Aws.region``
        which indicates that account ID will only be determined during deployment
        (it will resolve to the CloudFormation intrinsic ``{"Ref":"AWS::Region"}``).
        Note that certain features, such as cross-stack references and
        environmental context providers require concerete region information and
        will cause this stack to emit synthesis errors.

        default
        :default: Aws.region which means that the stack will be region-agnostic.
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Environment(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.FileAssetLocation", jsii_struct_bases=[], name_mapping={'bucket_name': 'bucketName', 'object_key': 'objectKey', 's3_url': 's3Url'})
class FileAssetLocation():
    def __init__(self, *, bucket_name: str, object_key: str, s3_url: str):
        """The location of the published file asset.

        This is where the asset
        can be consumed at runtime.

        :param bucket_name: The name of the Amazon S3 bucket.
        :param object_key: The Amazon S3 object key.
        :param s3_url: The HTTP URL of this asset on Amazon S3.
        """
        self._values = {
            'bucket_name': bucket_name,
            'object_key': object_key,
            's3_url': s3_url,
        }

    @builtins.property
    def bucket_name(self) -> str:
        """The name of the Amazon S3 bucket."""
        return self._values.get('bucket_name')

    @builtins.property
    def object_key(self) -> str:
        """The Amazon S3 object key."""
        return self._values.get('object_key')

    @builtins.property
    def s3_url(self) -> str:
        """The HTTP URL of this asset on Amazon S3.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return self._values.get('s3_url')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAssetLocation(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/core.FileAssetPackaging")
class FileAssetPackaging(enum.Enum):
    """Packaging modes for file assets."""
    ZIP_DIRECTORY = "ZIP_DIRECTORY"
    """The asset source path points to a directory, which should be archived using zip and and then uploaded to Amazon S3."""
    FILE = "FILE"
    """The asset source path points to a single file, which should be uploaded to Amazon S3."""

@jsii.data_type(jsii_type="@aws-cdk/core.FileAssetSource", jsii_struct_bases=[], name_mapping={'file_name': 'fileName', 'packaging': 'packaging', 'source_hash': 'sourceHash'})
class FileAssetSource():
    def __init__(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str):
        """Represents the source for a file asset.

        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.
        """
        self._values = {
            'file_name': file_name,
            'packaging': packaging,
            'source_hash': source_hash,
        }

    @builtins.property
    def file_name(self) -> str:
        """The path, relative to the root of the cloud assembly, in which this asset source resides.

        This can be a path to a file or a directory, dependning on the
        packaging type.
        """
        return self._values.get('file_name')

    @builtins.property
    def packaging(self) -> "FileAssetPackaging":
        """Which type of packaging to perform."""
        return self._values.get('packaging')

    @builtins.property
    def source_hash(self) -> str:
        """A hash on the content source.

        This hash is used to uniquely identify this
        asset throughout the system. If this value doesn't change, the asset will
        not be rebuilt or republished.
        """
        return self._values.get('source_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAssetSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Fn(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Fn"):
    """CloudFormation intrinsic functions.

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html
    """
    @jsii.member(jsii_name="base64")
    @builtins.classmethod
    def base64(cls, data: str) -> str:
        """The intrinsic function ``Fn::Base64`` returns the Base64 representation of the input string.

        This function is typically used to pass encoded data to
        Amazon EC2 instances by way of the UserData property.

        :param data: The string value you want to convert to Base64.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "base64", [data])

    @jsii.member(jsii_name="cidr")
    @builtins.classmethod
    def cidr(cls, ip_block: str, count: jsii.Number, size_mask: typing.Optional[str]=None) -> typing.List[str]:
        """The intrinsic function ``Fn::Cidr`` returns the specified Cidr address block.

        :param ip_block: The user-specified default Cidr address block.
        :param count: The number of subnets' Cidr block wanted. Count can be 1 to 256.
        :param size_mask: The digit covered in the subnet.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "cidr", [ip_block, count, size_mask])

    @jsii.member(jsii_name="conditionAnd")
    @builtins.classmethod
    def condition_and(cls, *conditions: "ICfnConditionExpression") -> "ICfnConditionExpression":
        """Returns true if all the specified conditions evaluate to true, or returns false if any one of the conditions evaluates to false.

        ``Fn::And`` acts as
        an AND operator. The minimum number of conditions that you can include is
        2, and the maximum is 10.

        :param conditions: conditions to AND.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionAnd", [*conditions])

    @jsii.member(jsii_name="conditionContains")
    @builtins.classmethod
    def condition_contains(cls, list_of_strings: typing.List[str], value: str) -> "ICfnConditionExpression":
        """Returns true if a specified string matches at least one value in a list of strings.

        :param list_of_strings: A list of strings, such as "A", "B", "C".
        :param value: A string, such as "A", that you want to compare against a list of strings.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionContains", [list_of_strings, value])

    @jsii.member(jsii_name="conditionEachMemberEquals")
    @builtins.classmethod
    def condition_each_member_equals(cls, list_of_strings: typing.List[str], value: str) -> "ICfnConditionExpression":
        """Returns true if a specified string matches all values in a list.

        :param list_of_strings: A list of strings, such as "A", "B", "C".
        :param value: A string, such as "A", that you want to compare against a list of strings.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionEachMemberEquals", [list_of_strings, value])

    @jsii.member(jsii_name="conditionEachMemberIn")
    @builtins.classmethod
    def condition_each_member_in(cls, strings_to_check: typing.List[str], strings_to_match: typing.List[str]) -> "ICfnConditionExpression":
        """Returns true if each member in a list of strings matches at least one value in a second list of strings.

        :param strings_to_check: A list of strings, such as "A", "B", "C". AWS CloudFormation checks whether each member in the strings_to_check parameter is in the strings_to_match parameter.
        :param strings_to_match: A list of strings, such as "A", "B", "C". Each member in the strings_to_match parameter is compared against the members of the strings_to_check parameter.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionEachMemberIn", [strings_to_check, strings_to_match])

    @jsii.member(jsii_name="conditionEquals")
    @builtins.classmethod
    def condition_equals(cls, lhs: typing.Any, rhs: typing.Any) -> "ICfnConditionExpression":
        """Compares if two values are equal.

        Returns true if the two values are equal
        or false if they aren't.

        :param lhs: A value of any type that you want to compare.
        :param rhs: A value of any type that you want to compare.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionEquals", [lhs, rhs])

    @jsii.member(jsii_name="conditionIf")
    @builtins.classmethod
    def condition_if(cls, condition_id: str, value_if_true: typing.Any, value_if_false: typing.Any) -> "ICfnConditionExpression":
        """Returns one value if the specified condition evaluates to true and another value if the specified condition evaluates to false.

        Currently, AWS
        CloudFormation supports the ``Fn::If`` intrinsic function in the metadata
        attribute, update policy attribute, and property values in the Resources
        section and Outputs sections of a template. You can use the AWS::NoValue
        pseudo parameter as a return value to remove the corresponding property.

        :param condition_id: A reference to a condition in the Conditions section. Use the condition's name to reference it.
        :param value_if_true: A value to be returned if the specified condition evaluates to true.
        :param value_if_false: A value to be returned if the specified condition evaluates to false.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionIf", [condition_id, value_if_true, value_if_false])

    @jsii.member(jsii_name="conditionNot")
    @builtins.classmethod
    def condition_not(cls, condition: "ICfnConditionExpression") -> "ICfnConditionExpression":
        """Returns true for a condition that evaluates to false or returns false for a condition that evaluates to true.

        ``Fn::Not`` acts as a NOT operator.

        :param condition: A condition such as ``Fn::Equals`` that evaluates to true or false.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionNot", [condition])

    @jsii.member(jsii_name="conditionOr")
    @builtins.classmethod
    def condition_or(cls, *conditions: "ICfnConditionExpression") -> "ICfnConditionExpression":
        """Returns true if any one of the specified conditions evaluate to true, or returns false if all of the conditions evaluates to false.

        ``Fn::Or`` acts
        as an OR operator. The minimum number of conditions that you can include is
        2, and the maximum is 10.

        :param conditions: conditions that evaluates to true or false.

        return
        :return: an FnCondition token
        """
        return jsii.sinvoke(cls, "conditionOr", [*conditions])

    @jsii.member(jsii_name="findInMap")
    @builtins.classmethod
    def find_in_map(cls, map_name: str, top_level_key: str, second_level_key: str) -> str:
        """The intrinsic function ``Fn::FindInMap`` returns the value corresponding to keys in a two-level map that is declared in the Mappings section.

        :param map_name: -
        :param top_level_key: -
        :param second_level_key: -

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "findInMap", [map_name, top_level_key, second_level_key])

    @jsii.member(jsii_name="getAtt")
    @builtins.classmethod
    def get_att(cls, logical_name_of_resource: str, attribute_name: str) -> "IResolvable":
        """The ``Fn::GetAtt`` intrinsic function returns the value of an attribute from a resource in the template.

        :param logical_name_of_resource: The logical name (also called logical ID) of the resource that contains the attribute that you want.
        :param attribute_name: The name of the resource-specific attribute whose value you want. See the resource's reference page for details about the attributes available for that resource type.

        return
        :return: an IResolvable object
        """
        return jsii.sinvoke(cls, "getAtt", [logical_name_of_resource, attribute_name])

    @jsii.member(jsii_name="getAzs")
    @builtins.classmethod
    def get_azs(cls, region: typing.Optional[str]=None) -> typing.List[str]:
        """The intrinsic function ``Fn::GetAZs`` returns an array that lists Availability Zones for a specified region.

        Because customers have access to
        different Availability Zones, the intrinsic function ``Fn::GetAZs`` enables
        template authors to write templates that adapt to the calling user's
        access. That way you don't have to hard-code a full list of Availability
        Zones for a specified region.

        :param region: The name of the region for which you want to get the Availability Zones. You can use the AWS::Region pseudo parameter to specify the region in which the stack is created. Specifying an empty string is equivalent to specifying AWS::Region.

        return
        :return: a token represented as a string array
        """
        return jsii.sinvoke(cls, "getAzs", [region])

    @jsii.member(jsii_name="importValue")
    @builtins.classmethod
    def import_value(cls, shared_value_to_import: str) -> str:
        """The intrinsic function ``Fn::ImportValue`` returns the value of an output exported by another stack.

        You typically use this function to create
        cross-stack references. In the following example template snippets, Stack A
        exports VPC security group values and Stack B imports them.

        :param shared_value_to_import: The stack output value that you want to import.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "importValue", [shared_value_to_import])

    @jsii.member(jsii_name="join")
    @builtins.classmethod
    def join(cls, delimiter: str, list_of_values: typing.List[str]) -> str:
        """The intrinsic function ``Fn::Join`` appends a set of values into a single value, separated by the specified delimiter.

        If a delimiter is the empty
        string, the set of values are concatenated with no delimiter.

        :param delimiter: The value you want to occur between fragments. The delimiter will occur between fragments only. It will not terminate the final value.
        :param list_of_values: The list of values you want combined.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "join", [delimiter, list_of_values])

    @jsii.member(jsii_name="ref")
    @builtins.classmethod
    def ref(cls, logical_name: str) -> str:
        """The ``Ref`` intrinsic function returns the value of the specified parameter or resource.

        Note that it doesn't validate the logicalName, it mainly serves paremeter/resource reference defined in a ``CfnInclude`` template.

        :param logical_name: The logical name of a parameter/resource for which you want to retrieve its value.
        """
        return jsii.sinvoke(cls, "ref", [logical_name])

    @jsii.member(jsii_name="refAll")
    @builtins.classmethod
    def ref_all(cls, parameter_type: str) -> typing.List[str]:
        """Returns all values for a specified parameter type.

        :param parameter_type: An AWS-specific parameter type, such as AWS::EC2::SecurityGroup::Id or AWS::EC2::VPC::Id. For more information, see Parameters in the AWS CloudFormation User Guide.

        return
        :return: a token represented as a string array
        """
        return jsii.sinvoke(cls, "refAll", [parameter_type])

    @jsii.member(jsii_name="select")
    @builtins.classmethod
    def select(cls, index: jsii.Number, array: typing.List[str]) -> str:
        """The intrinsic function ``Fn::Select`` returns a single object from a list of objects by index.

        :param index: The index of the object to retrieve. This must be a value from zero to N-1, where N represents the number of elements in the array.
        :param array: The list of objects to select from. This list must not be null, nor can it have null entries.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "select", [index, array])

    @jsii.member(jsii_name="split")
    @builtins.classmethod
    def split(cls, delimiter: str, source: str) -> typing.List[str]:
        """To split a string into a list of string values so that you can select an element from the resulting string list, use the ``Fn::Split`` intrinsic function.

        Specify the location of splits
        with a delimiter, such as , (a comma). After you split a string, use the ``Fn::Select`` function
        to pick a specific element.

        :param delimiter: A string value that determines where the source string is divided.
        :param source: The string value that you want to split.

        return
        :return: a token represented as a string array
        """
        return jsii.sinvoke(cls, "split", [delimiter, source])

    @jsii.member(jsii_name="sub")
    @builtins.classmethod
    def sub(cls, body: str, variables: typing.Optional[typing.Mapping[str,str]]=None) -> str:
        """The intrinsic function ``Fn::Sub`` substitutes variables in an input string with values that you specify.

        In your templates, you can use this function
        to construct commands or outputs that include values that aren't available
        until you create or update a stack.

        :param body: A string with variables that AWS CloudFormation substitutes with their associated values at runtime. Write variables as ${MyVarName}. Variables can be template parameter names, resource logical IDs, resource attributes, or a variable in a key-value map. If you specify only template parameter names, resource logical IDs, and resource attributes, don't specify a key-value map.
        :param variables: The name of a variable that you included in the String parameter. The value that AWS CloudFormation substitutes for the associated variable name at runtime.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "sub", [body, variables])

    @jsii.member(jsii_name="valueOf")
    @builtins.classmethod
    def value_of(cls, parameter_or_logical_id: str, attribute: str) -> str:
        """Returns an attribute value or list of values for a specific parameter and attribute.

        :param parameter_or_logical_id: The name of a parameter for which you want to retrieve attribute values. The parameter must be declared in the Parameters section of the template.
        :param attribute: The name of an attribute from which you want to retrieve a value.

        return
        :return: a token represented as a string
        """
        return jsii.sinvoke(cls, "valueOf", [parameter_or_logical_id, attribute])

    @jsii.member(jsii_name="valueOfAll")
    @builtins.classmethod
    def value_of_all(cls, parameter_type: str, attribute: str) -> typing.List[str]:
        """Returns a list of all attribute values for a given parameter type and attribute.

        :param parameter_type: An AWS-specific parameter type, such as AWS::EC2::SecurityGroup::Id or AWS::EC2::VPC::Id. For more information, see Parameters in the AWS CloudFormation User Guide.
        :param attribute: The name of an attribute from which you want to retrieve a value. For more information about attributes, see Supported Attributes.

        return
        :return: a token represented as a string array
        """
        return jsii.sinvoke(cls, "valueOfAll", [parameter_type, attribute])


@jsii.data_type(jsii_type="@aws-cdk/core.GetContextKeyOptions", jsii_struct_bases=[], name_mapping={'provider': 'provider', 'props': 'props'})
class GetContextKeyOptions():
    def __init__(self, *, provider: str, props: typing.Optional[typing.Mapping[str,typing.Any]]=None):
        """
        :param provider: The context provider to query.
        :param props: Provider-specific properties.

        stability
        :stability: experimental
        """
        self._values = {
            'provider': provider,
        }
        if props is not None: self._values["props"] = props

    @builtins.property
    def provider(self) -> str:
        """The context provider to query.

        stability
        :stability: experimental
        """
        return self._values.get('provider')

    @builtins.property
    def props(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Provider-specific properties.

        stability
        :stability: experimental
        """
        return self._values.get('props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextKeyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.GetContextKeyResult", jsii_struct_bases=[], name_mapping={'key': 'key', 'props': 'props'})
class GetContextKeyResult():
    def __init__(self, *, key: str, props: typing.Mapping[str,typing.Any]):
        """
        :param key: 
        :param props: 

        stability
        :stability: experimental
        """
        self._values = {
            'key': key,
            'props': props,
        }

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('key')

    @builtins.property
    def props(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextKeyResult(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.GetContextValueOptions", jsii_struct_bases=[GetContextKeyOptions], name_mapping={'provider': 'provider', 'props': 'props', 'dummy_value': 'dummyValue'})
class GetContextValueOptions(GetContextKeyOptions):
    def __init__(self, *, provider: str, props: typing.Optional[typing.Mapping[str,typing.Any]]=None, dummy_value: typing.Any):
        """
        :param provider: The context provider to query.
        :param props: Provider-specific properties.
        :param dummy_value: The value to return if the context value was not found and a missing context is reported. This should be a dummy value that should preferably fail during deployment since it represents an invalid state.

        stability
        :stability: experimental
        """
        self._values = {
            'provider': provider,
            'dummy_value': dummy_value,
        }
        if props is not None: self._values["props"] = props

    @builtins.property
    def provider(self) -> str:
        """The context provider to query.

        stability
        :stability: experimental
        """
        return self._values.get('provider')

    @builtins.property
    def props(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Provider-specific properties.

        stability
        :stability: experimental
        """
        return self._values.get('props')

    @builtins.property
    def dummy_value(self) -> typing.Any:
        """The value to return if the context value was not found and a missing context is reported.

        This should be a dummy value that should preferably
        fail during deployment since it represents an invalid state.

        stability
        :stability: experimental
        """
        return self._values.get('dummy_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.GetContextValueResult", jsii_struct_bases=[], name_mapping={'value': 'value'})
class GetContextValueResult():
    def __init__(self, *, value: typing.Any=None):
        """
        :param value: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if value is not None: self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GetContextValueResult(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/core.IAnyProducer")
class IAnyProducer(jsii.compat.Protocol):
    """Interface for lazy untyped value producers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAnyProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -
        """
        ...


class _IAnyProducerProxy():
    """Interface for lazy untyped value producers."""
    __jsii_type__ = "@aws-cdk/core.IAnyProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="@aws-cdk/core.IAspect")
class IAspect(jsii.compat.Protocol):
    """Represents an Aspect."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAspectProxy

    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param node: -
        """
        ...


class _IAspectProxy():
    """Represents an Aspect."""
    __jsii_type__ = "@aws-cdk/core.IAspect"
    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param node: -
        """
        return jsii.invoke(self, "visit", [node])


@jsii.interface(jsii_type="@aws-cdk/core.ICfnResourceOptions")
class ICfnResourceOptions(jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICfnResourceOptionsProxy

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        """A condition to associate with this resource.

        This means that only if the condition evaluates to 'true' when the stack
        is deployed, the resource will be included. This is provided to allow CDK projects to produce legacy templates, but noramlly
        there is no need to use it in CDK projects.
        """
        ...

    @condition.setter
    def condition(self, value: typing.Optional["CfnCondition"]):
        ...

    @builtins.property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(self) -> typing.Optional["CfnCreationPolicy"]:
        """Associate the CreationPolicy attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

        To signal a
        resource, you can use the cfn-signal helper script or SignalResource API. AWS CloudFormation publishes valid signals
        to the stack events so that you track the number of signals sent.
        """
        ...

    @creation_policy.setter
    def creation_policy(self, value: typing.Optional["CfnCreationPolicy"]):
        ...

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """With the DeletionPolicy attribute you can preserve or (in some cases) backup a resource when its stack is deleted.

        You specify a DeletionPolicy attribute for each resource that you want to control. If a resource has no DeletionPolicy
        attribute, AWS CloudFormation deletes the resource by default. Note that this capability also applies to update operations
        that lead to resources being removed.
        """
        ...

    @deletion_policy.setter
    def deletion_policy(self, value: typing.Optional["CfnDeletionPolicy"]):
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Metadata associated with the CloudFormation resource.

        This is not the same as the construct metadata which can be added
        using construct.addMetadata(), but would not appear in the CloudFormation template automatically.
        """
        ...

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        ...

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> typing.Optional["CfnUpdatePolicy"]:
        """Use the UpdatePolicy attribute to specify how AWS CloudFormation handles updates to the AWS::AutoScaling::AutoScalingGroup resource.

        AWS CloudFormation invokes one of three update policies depending on the type of change you make or whether a
        scheduled action is associated with the Auto Scaling group.
        """
        ...

    @update_policy.setter
    def update_policy(self, value: typing.Optional["CfnUpdatePolicy"]):
        ...

    @builtins.property
    @jsii.member(jsii_name="updateReplacePolicy")
    def update_replace_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """Use the UpdateReplacePolicy attribute to retain or (in some cases) backup the existing physical instance of a resource when it is replaced during a stack update operation."""
        ...

    @update_replace_policy.setter
    def update_replace_policy(self, value: typing.Optional["CfnDeletionPolicy"]):
        ...


class _ICfnResourceOptionsProxy():
    __jsii_type__ = "@aws-cdk/core.ICfnResourceOptions"
    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        """A condition to associate with this resource.

        This means that only if the condition evaluates to 'true' when the stack
        is deployed, the resource will be included. This is provided to allow CDK projects to produce legacy templates, but noramlly
        there is no need to use it in CDK projects.
        """
        return jsii.get(self, "condition")

    @condition.setter
    def condition(self, value: typing.Optional["CfnCondition"]):
        jsii.set(self, "condition", value)

    @builtins.property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(self) -> typing.Optional["CfnCreationPolicy"]:
        """Associate the CreationPolicy attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

        To signal a
        resource, you can use the cfn-signal helper script or SignalResource API. AWS CloudFormation publishes valid signals
        to the stack events so that you track the number of signals sent.
        """
        return jsii.get(self, "creationPolicy")

    @creation_policy.setter
    def creation_policy(self, value: typing.Optional["CfnCreationPolicy"]):
        jsii.set(self, "creationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """With the DeletionPolicy attribute you can preserve or (in some cases) backup a resource when its stack is deleted.

        You specify a DeletionPolicy attribute for each resource that you want to control. If a resource has no DeletionPolicy
        attribute, AWS CloudFormation deletes the resource by default. Note that this capability also applies to update operations
        that lead to resources being removed.
        """
        return jsii.get(self, "deletionPolicy")

    @deletion_policy.setter
    def deletion_policy(self, value: typing.Optional["CfnDeletionPolicy"]):
        jsii.set(self, "deletionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Metadata associated with the CloudFormation resource.

        This is not the same as the construct metadata which can be added
        using construct.addMetadata(), but would not appear in the CloudFormation template automatically.
        """
        return jsii.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> typing.Optional["CfnUpdatePolicy"]:
        """Use the UpdatePolicy attribute to specify how AWS CloudFormation handles updates to the AWS::AutoScaling::AutoScalingGroup resource.

        AWS CloudFormation invokes one of three update policies depending on the type of change you make or whether a
        scheduled action is associated with the Auto Scaling group.
        """
        return jsii.get(self, "updatePolicy")

    @update_policy.setter
    def update_policy(self, value: typing.Optional["CfnUpdatePolicy"]):
        jsii.set(self, "updatePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="updateReplacePolicy")
    def update_replace_policy(self) -> typing.Optional["CfnDeletionPolicy"]:
        """Use the UpdateReplacePolicy attribute to retain or (in some cases) backup the existing physical instance of a resource when it is replaced during a stack update operation."""
        return jsii.get(self, "updateReplacePolicy")

    @update_replace_policy.setter
    def update_replace_policy(self, value: typing.Optional["CfnDeletionPolicy"]):
        jsii.set(self, "updateReplacePolicy", value)


@jsii.interface(jsii_type="@aws-cdk/core.IDependable")
class IDependable(jsii.compat.Protocol):
    """Trait marker for classes that can be depended upon.

    The presence of this interface indicates that an object has
    an ``IDependableTrait`` implementation.

    This interface can be used to take an (ordering) dependency on a set of
    constructs. An ordering dependency implies that the resources represented by
    those constructs are deployed before the resources depending ON them are
    deployed.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDependableProxy

    pass

class _IDependableProxy():
    """Trait marker for classes that can be depended upon.

    The presence of this interface indicates that an object has
    an ``IDependableTrait`` implementation.

    This interface can be used to take an (ordering) dependency on a set of
    constructs. An ordering dependency implies that the resources represented by
    those constructs are deployed before the resources depending ON them are
    deployed.
    """
    __jsii_type__ = "@aws-cdk/core.IDependable"
    pass

@jsii.implements(IDependable)
class ConcreteDependable(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.ConcreteDependable"):
    """A set of constructs to be used as a dependable.

    This class can be used when a set of constructs which are disjoint in the
    construct tree needs to be combined to be used as a single dependable.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(ConcreteDependable, self, [])

    @jsii.member(jsii_name="add")
    def add(self, construct: "IConstruct") -> None:
        """Add a construct to the dependency roots.

        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "add", [construct])


@jsii.interface(jsii_type="@aws-cdk/core.IConstruct")
class IConstruct(IDependable, jsii.compat.Protocol):
    """Represents a construct."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IConstructProxy

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        """The construct node in the tree."""
        ...


class _IConstructProxy(jsii.proxy_for(IDependable)):
    """Represents a construct."""
    __jsii_type__ = "@aws-cdk/core.IConstruct"
    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        """The construct node in the tree."""
        return jsii.get(self, "node")


@jsii.implements(IConstruct)
class Construct(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Construct"):
    """Represents the building block of the construct graph.

    All constructs besides the root construct must be created within the scope of
    another construct.
    """
    def __init__(self, scope: "Construct", id: str) -> None:
        """Creates a new construct node.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        """
        jsii.create(Construct, self, [scope, id])

    @jsii.member(jsii_name="isConstruct")
    @builtins.classmethod
    def is_construct(cls, x: typing.Any) -> bool:
        """Return whether the given object is a Construct.

        :param x: -
        """
        return jsii.sinvoke(cls, "isConstruct", [x])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        """Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.
        """
        return jsii.invoke(self, "prepare", [])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: "ISynthesisSession") -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: The synthesis session.
        """
        return jsii.invoke(self, "synthesize", [session])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of this construct."""
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        return
        :return: An array of validation error messages, or an empty array if there the construct is valid.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        """Construct tree node which offers APIs for interacting with the construct tree."""
        return jsii.get(self, "node")


class App(Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.App"):
    """A construct which represents an entire CDK app. This construct is normally the root of the construct tree.

    You would normally define an ``App`` instance in your program's entrypoint,
    then define constructs where the app is used as the parent scope.

    After all the child constructs are defined within the app, you should call
    ``app.synth()`` which will emit a "cloud assembly" from this app into the
    directory specified by ``outdir``. Cloud assemblies includes artifacts such as
    CloudFormation templates and assets that are needed to deploy this app into
    the AWS cloud.

    see
    :see: https://docs.aws.amazon.com/cdk/latest/guide/apps.html
    """
    def __init__(self, *, auto_synth: typing.Optional[bool]=None, context: typing.Optional[typing.Mapping[str,str]]=None, outdir: typing.Optional[str]=None, runtime_info: typing.Optional[bool]=None, stack_traces: typing.Optional[bool]=None, tree_metadata: typing.Optional[bool]=None) -> None:
        """Initializes a CDK application.

        :param auto_synth: Automatically call ``synth()`` before the program exits. If you set this, you don't have to call ``synth()`` explicitly. Note that this feature is only available for certain programming languages, and calling ``synth()`` is still recommended. Default: true if running via CDK CLI (``CDK_OUTDIR`` is set), ``false`` otherwise
        :param context: Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdk.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: The output directory into which to emit synthesized artifacts. Default: - If this value is *not* set, considers the environment variable ``CDK_OUTDIR``. If ``CDK_OUTDIR`` is not defined, uses a temp directory.
        :param runtime_info: Include runtime versioning information in cloud assembly manifest. Default: true runtime info is included unless ``aws:cdk:disable-runtime-info`` is set in the context.
        :param stack_traces: Include construct creation stack trace in the ``aws:cdk:trace`` metadata key of all constructs. Default: true stack traces are included unless ``aws:cdk:disable-stack-trace`` is set in the context.
        :param tree_metadata: Include construct tree metadata as part of the Cloud Assembly. Default: true
        """
        props = AppProps(auto_synth=auto_synth, context=context, outdir=outdir, runtime_info=runtime_info, stack_traces=stack_traces, tree_metadata=tree_metadata)

        jsii.create(App, self, [props])

    @jsii.member(jsii_name="isApp")
    @builtins.classmethod
    def is_app(cls, obj: typing.Any) -> bool:
        """Checks if an object is an instance of the ``App`` class.

        :param obj: The object to evaluate.

        return
        :return: ``true`` if ``obj`` is an ``App``.
        """
        return jsii.sinvoke(cls, "isApp", [obj])

    @jsii.member(jsii_name="synth")
    def synth(self) -> aws_cdk.cx_api.CloudAssembly:
        """Synthesizes a cloud assembly for this app.

        Emits it to the directory
        specified by ``outdir``.

        return
        :return:

        a ``CloudAssembly`` which can be used to inspect synthesized
        artifacts such as CloudFormation templates and assets.
        """
        return jsii.invoke(self, "synth", [])


class CfnElement(Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/core.CfnElement"):
    """An element of a CloudFormation stack."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CfnElementProxy

    def __init__(self, scope: "Construct", id: str) -> None:
        """Creates an entity and binds it to a tree.

        Note that the root of the tree must be a Stack object (not just any Root).

        :param scope: The parent construct.
        :param id: -
        """
        jsii.create(CfnElement, self, [scope, id])

    @jsii.member(jsii_name="isCfnElement")
    @builtins.classmethod
    def is_cfn_element(cls, x: typing.Any) -> bool:
        """Returns ``true`` if a construct is a stack element (i.e. part of the synthesized cloudformation template).

        Uses duck-typing instead of ``instanceof`` to allow stack elements from different
        versions of this library to be included in the same stack.

        :param x: -

        return
        :return: The construct as a stack element or undefined if it is not a stack element.
        """
        return jsii.sinvoke(cls, "isCfnElement", [x])

    @jsii.member(jsii_name="overrideLogicalId")
    def override_logical_id(self, new_logical_id: str) -> None:
        """Overrides the auto-generated logical ID with a specific ID.

        :param new_logical_id: The new logical ID to use for this stack element.
        """
        return jsii.invoke(self, "overrideLogicalId", [new_logical_id])

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """
        return
        :return:

        the stack trace of the point where this Resource was created from, sourced
        from the +metadata+ entry typed +aws:cdk:logicalId+, and with the bottom-most
        node +internal+ entries filtered.
        """
        return jsii.get(self, "creationStack")

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> str:
        """The logical ID for this CloudFormation stack element.

        The logical ID of the element
        is calculated from the path of the resource node in the construct tree.

        To override this value, use ``overrideLogicalId(newLogicalId)``.

        return
        :return:

        the logical ID as a stringified token. This value will only get
        resolved during synthesis.
        """
        return jsii.get(self, "logicalId")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this element is defined.

        CfnElements must be defined within a stack scope (directly or indirectly).
        """
        return jsii.get(self, "stack")


class _CfnElementProxy(CfnElement):
    pass

class CfnInclude(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnInclude"):
    """Includes a CloudFormation template into a stack.

    All elements of the template will be merged into
    the current stack, together with any elements created programmatically.
    """
    def __init__(self, scope: "Construct", id: str, *, template: typing.Mapping[typing.Any, typing.Any]) -> None:
        """Creates an adopted template construct.

        The template will be incorporated into the stack as-is with no changes at all.
        This means that logical IDs of entities within this template may conflict with logical IDs of entities that are part of the
        stack.

        :param scope: The parent construct of this template.
        :param id: The ID of this construct.
        :param template: The CloudFormation template to include in the stack (as is).
        """
        props = CfnIncludeProps(template=template)

        jsii.create(CfnInclude, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Mapping[typing.Any, typing.Any]:
        """The included template."""
        return jsii.get(self, "template")


class CfnOutput(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnOutput"):
    def __init__(self, scope: "Construct", id: str, *, value: str, condition: typing.Optional["CfnCondition"]=None, description: typing.Optional[str]=None, export_name: typing.Optional[str]=None) -> None:
        """Creates an CfnOutput value for this stack.

        :param scope: The parent construct.
        :param id: -
        :param value: The value of the property returned by the aws cloudformation describe-stacks command. The value of an output can include literals, parameter references, pseudo-parameters, a mapping value, or intrinsic functions.
        :param condition: A condition to associate with this output value. If the condition evaluates to ``false``, this output value will not be included in the stack. Default: - No condition is associated with the output.
        :param description: A String type that describes the output value. The description can be a maximum of 4 K in length. Default: - No description.
        :param export_name: The name used to export the value of this output across stacks. To import the value from another stack, use ``Fn.importValue(exportName)``. Default: - the output is not exported
        """
        props = CfnOutputProps(value=value, condition=condition, description=description, export_name=export_name)

        jsii.create(CfnOutput, self, [scope, id, props])


class CfnParameter(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnParameter"):
    """A CloudFormation parameter.

    Use the optional Parameters section to customize your templates.
    Parameters enable you to input custom values to your template each time you create or
    update a stack.
    """
    def __init__(self, scope: "Construct", id: str, *, allowed_pattern: typing.Optional[str]=None, allowed_values: typing.Optional[typing.List[str]]=None, constraint_description: typing.Optional[str]=None, default: typing.Any=None, description: typing.Optional[str]=None, max_length: typing.Optional[jsii.Number]=None, max_value: typing.Optional[jsii.Number]=None, min_length: typing.Optional[jsii.Number]=None, min_value: typing.Optional[jsii.Number]=None, no_echo: typing.Optional[bool]=None, type: typing.Optional[str]=None) -> None:
        """Creates a parameter construct.

        Note that the name (logical ID) of the parameter will derive from it's ``coname`` and location
        within the stack. Therefore, it is recommended that parameters are defined at the stack level.

        :param scope: The parent construct.
        :param id: -
        :param allowed_pattern: A regular expression that represents the patterns to allow for String types. Default: - No constraints on patterns allowed for parameter.
        :param allowed_values: An array containing the list of values allowed for the parameter. Default: - No constraints on values allowed for parameter.
        :param constraint_description: A string that explains a constraint when the constraint is violated. For example, without a constraint description, a parameter that has an allowed pattern of [A-Za-z0-9]+ displays the following error message when the user specifies an invalid value: Default: - No description with customized error message when user specifies invalid values.
        :param default: A value of the appropriate type for the template to use if no value is specified when a stack is created. If you define constraints for the parameter, you must specify a value that adheres to those constraints. Default: - No default value for parameter.
        :param description: A string of up to 4000 characters that describes the parameter. Default: - No description for the parameter.
        :param max_length: An integer value that determines the largest number of characters you want to allow for String types. Default: - None.
        :param max_value: A numeric value that determines the largest numeric value you want to allow for Number types. Default: - None.
        :param min_length: An integer value that determines the smallest number of characters you want to allow for String types. Default: - None.
        :param min_value: A numeric value that determines the smallest numeric value you want to allow for Number types. Default: - None.
        :param no_echo: Whether to mask the parameter value when anyone makes a call that describes the stack. If you set the value to ``true``, the parameter value is masked with asterisks (``*****``). Default: - Parameter values are not masked.
        :param type: The data type for the parameter (DataType). Default: String
        """
        props = CfnParameterProps(allowed_pattern=allowed_pattern, allowed_values=allowed_values, constraint_description=constraint_description, default=default, description=description, max_length=max_length, max_value=max_value, min_length=min_length, min_value=min_value, no_echo=no_echo, type=type)

        jsii.create(CfnParameter, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: "IResolveContext") -> typing.Any:
        """
        :param _context: -
        """
        return jsii.invoke(self, "resolve", [_context])

    @builtins.property
    @jsii.member(jsii_name="noEcho")
    def no_echo(self) -> bool:
        """Indicates if this parameter is configured with "NoEcho" enabled."""
        return jsii.get(self, "noEcho")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> "IResolvable":
        """The parameter value as a Token."""
        return jsii.get(self, "value")

    @builtins.property
    @jsii.member(jsii_name="valueAsList")
    def value_as_list(self) -> typing.List[str]:
        """The parameter value, if it represents a string list."""
        return jsii.get(self, "valueAsList")

    @builtins.property
    @jsii.member(jsii_name="valueAsNumber")
    def value_as_number(self) -> jsii.Number:
        """The parameter value, if it represents a number."""
        return jsii.get(self, "valueAsNumber")

    @builtins.property
    @jsii.member(jsii_name="valueAsString")
    def value_as_string(self) -> str:
        """The parameter value, if it represents a string."""
        return jsii.get(self, "valueAsString")


class CfnRefElement(CfnElement, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/core.CfnRefElement"):
    """Base class for referenceable CloudFormation constructs which are not Resources.

    These constructs are things like Conditions and Parameters, can be
    referenced by taking the ``.ref`` attribute.

    Resource constructs do not inherit from CfnRefElement because they have their
    own, more specific types returned from the .ref attribute. Also, some
    resources aren't referenceable at all (such as BucketPolicies or GatewayAttachments).
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CfnRefElementProxy

    def __init__(self, scope: "Construct", id: str) -> None:
        """Creates an entity and binds it to a tree.

        Note that the root of the tree must be a Stack object (not just any Root).

        :param scope: The parent construct.
        :param id: -
        """
        jsii.create(CfnRefElement, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        """Return a string that will be resolved to a CloudFormation ``{ Ref }`` for this element.

        If, by any chance, the intrinsic reference of a resource is not a string, you could
        coerce it to an IResolvable through ``Lazy.any({ produce: resource.ref })``.
        """
        return jsii.get(self, "ref")


class _CfnRefElementProxy(CfnRefElement, jsii.proxy_for(CfnElement)):
    pass

class CfnMapping(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnMapping"):
    """Represents a CloudFormation mapping."""
    def __init__(self, scope: "Construct", id: str, *, mapping: typing.Optional[typing.Mapping[str,typing.Mapping[str,typing.Any]]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mapping: Mapping of key to a set of corresponding set of named values. The key identifies a map of name-value pairs and must be unique within the mapping. For example, if you want to set values based on a region, you can create a mapping that uses the region name as a key and contains the values you want to specify for each specific region. Default: - No mapping.
        """
        props = CfnMappingProps(mapping=mapping)

        jsii.create(CfnMapping, self, [scope, id, props])

    @jsii.member(jsii_name="findInMap")
    def find_in_map(self, key1: str, key2: str) -> str:
        """
        :param key1: -
        :param key2: -

        return
        :return: A reference to a value in the map based on the two keys.
        """
        return jsii.invoke(self, "findInMap", [key1, key2])

    @jsii.member(jsii_name="setValue")
    def set_value(self, key1: str, key2: str, value: typing.Any) -> None:
        """Sets a value in the map based on the two keys.

        :param key1: -
        :param key2: -
        :param value: -
        """
        return jsii.invoke(self, "setValue", [key1, key2, value])


class CfnResource(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnResource"):
    """Represents a CloudFormation resource."""
    def __init__(self, scope: "Construct", id: str, *, type: str, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """Creates a resource construct.

        :param scope: -
        :param id: -
        :param type: CloudFormation resource type (e.g. ``AWS::S3::Bucket``).
        :param properties: Resource properties. Default: - No resource properties.
        """
        props = CfnResourceProps(type=type, properties=properties)

        jsii.create(CfnResource, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnResource")
    @builtins.classmethod
    def is_cfn_resource(cls, construct: "IConstruct") -> bool:
        """Check whether the given construct is a CfnResource.

        :param construct: -
        """
        return jsii.sinvoke(cls, "isCfnResource", [construct])

    @jsii.member(jsii_name="addDeletionOverride")
    def add_deletion_override(self, path: str) -> None:
        """Syntactic sugar for ``addOverride(path, undefined)``.

        :param path: The path of the value to delete.
        """
        return jsii.invoke(self, "addDeletionOverride", [path])

    @jsii.member(jsii_name="addDependsOn")
    def add_depends_on(self, target: "CfnResource") -> None:
        """Indicates that this resource depends on another resource and cannot be provisioned unless the other resource has been successfully provisioned.

        This can be used for resources across stacks (or nested stack) boundaries
        and the dependency will automatically be transferred to the relevant scope.

        :param target: -
        """
        return jsii.invoke(self, "addDependsOn", [target])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """Adds an override to the synthesized CloudFormation resource.

        To add a
        property override, either use ``addPropertyOverride`` or prefix ``path`` with
        "Properties." (i.e. ``Properties.TopicName``).

        If the override is nested, separate each nested level using a dot (.) in the path parameter.
        If there is an array as part of the nesting, specify the index in the path.

        For example::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           add_override("Properties.GlobalSecondaryIndexes.0.Projection.NonKeyAttributes", ["myattribute"])
           add_override("Properties.GlobalSecondaryIndexes.1.ProjectionType", "INCLUDE")

        would add the overrides Example::

           "Properties": {
              "GlobalSecondaryIndexes": [
                {
                  "Projection": {
                    "NonKeyAttributes": [ "myattribute" ]
                    ...
                  }
                  ...
                },
                {
                  "ProjectionType": "INCLUDE"
                  ...
                },
              ]
              ...
           }

        :param path: - The path of the property, you can use dot notation to override values in complex types. Any intermdediate keys will be created as needed.
        :param value: - The value. Could be primitive or complex.
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="addPropertyDeletionOverride")
    def add_property_deletion_override(self, property_path: str) -> None:
        """Adds an override that deletes the value of a property from the resource definition.

        :param property_path: The path to the property.
        """
        return jsii.invoke(self, "addPropertyDeletionOverride", [property_path])

    @jsii.member(jsii_name="addPropertyOverride")
    def add_property_override(self, property_path: str, value: typing.Any) -> None:
        """Adds an override to a resource property.

        Syntactic sugar for ``addOverride("Properties.<...>", value)``.

        :param property_path: The path of the property.
        :param value: The value.
        """
        return jsii.invoke(self, "addPropertyOverride", [property_path, value])

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: typing.Optional["RemovalPolicy"]=None, *, apply_to_update_replace_policy: typing.Optional[bool]=None, default: typing.Optional["RemovalPolicy"]=None) -> None:
        """Sets the deletion policy of the resource based on the removal policy specified.

        :param policy: -
        :param apply_to_update_replace_policy: Apply the same deletion policy to the resource's "UpdateReplacePolicy". Default: true
        :param default: The default policy to apply in case the removal policy is not defined. Default: - Default value is resource specific. To determine the default value for a resoure, please consult that specific resource's documentation.
        """
        options = RemovalPolicyOptions(apply_to_update_replace_policy=apply_to_update_replace_policy, default=default)

        return jsii.invoke(self, "applyRemovalPolicy", [policy, options])

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: str) -> "Reference":
        """Returns a token for an runtime attribute of this resource.

        Ideally, use generated attribute accessors (e.g. ``resource.arn``), but this can be used for future compatibility
        in case there is no generated attribute.

        :param attribute_name: The name of the attribute.
        """
        return jsii.invoke(self, "getAtt", [attribute_name])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of this construct.

        return
        :return: a string representation of this resource
        """
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="validateProperties")
    def _validate_properties(self, _properties: typing.Any) -> None:
        """
        :param _properties: -
        """
        return jsii.invoke(self, "validateProperties", [_properties])

    @builtins.property
    @jsii.member(jsii_name="cfnOptions")
    def cfn_options(self) -> "ICfnResourceOptions":
        """Options for this resource, such as condition, update policy etc."""
        return jsii.get(self, "cfnOptions")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="cfnResourceType")
    def cfn_resource_type(self) -> str:
        """AWS resource type."""
        return jsii.get(self, "cfnResourceType")

    @builtins.property
    @jsii.member(jsii_name="updatedProperites")
    def _updated_properites(self) -> typing.Mapping[str,typing.Any]:
        """Return properties modified after initiation.

        Resources that expose mutable properties should override this function to
        collect and return the properties object for this resource.
        """
        return jsii.get(self, "updatedProperites")


class CfnRule(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnRule"):
    """The Rules that define template constraints in an AWS Service Catalog portfolio describe when end users can use the template and which values they can specify for parameters that are declared in the AWS CloudFormation template used to create the product they are attempting to use.

    Rules
    are useful for preventing end users from inadvertently specifying an incorrect value.
    For example, you can add a rule to verify whether end users specified a valid subnet in a
    given VPC or used m1.small instance types for test environments. AWS CloudFormation uses
    rules to validate parameter values before it creates the resources for the product.

    A rule can include a RuleCondition property and must include an Assertions property.
    For each rule, you can define only one rule condition; you can define one or more asserts within the Assertions property.
    You define a rule condition and assertions by using rule-specific intrinsic functions.

    link:
    :link:: https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html
    """
    def __init__(self, scope: "Construct", id: str, *, assertions: typing.Optional[typing.List["CfnRuleAssertion"]]=None, rule_condition: typing.Optional["ICfnConditionExpression"]=None) -> None:
        """Creates and adds a rule.

        :param scope: The parent construct.
        :param id: -
        :param assertions: Assertions which define the rule. Default: - No assertions for the rule.
        :param rule_condition: If the rule condition evaluates to false, the rule doesn't take effect. If the function in the rule condition evaluates to true, expressions in each assert are evaluated and applied. Default: - Rule's assertions will always take effect.
        """
        props = CfnRuleProps(assertions=assertions, rule_condition=rule_condition)

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="addAssertion")
    def add_assertion(self, condition: "ICfnConditionExpression", description: str) -> None:
        """Adds an assertion to the rule.

        :param condition: The expression to evaluation.
        :param description: The description of the assertion.
        """
        return jsii.invoke(self, "addAssertion", [condition, description])


@jsii.interface(jsii_type="@aws-cdk/core.IFragmentConcatenator")
class IFragmentConcatenator(jsii.compat.Protocol):
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFragmentConcatenatorProxy

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        ...


class _IFragmentConcatenatorProxy():
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/core.IFragmentConcatenator"
    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.interface(jsii_type="@aws-cdk/core.IInspectable")
class IInspectable(jsii.compat.Protocol):
    """Interface for examining a construct and exposing metadata."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IInspectableProxy

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
        """Examines construct.

        :param inspector: - tree inspector to collect and process attributes.
        """
        ...


class _IInspectableProxy():
    """Interface for examining a construct and exposing metadata."""
    __jsii_type__ = "@aws-cdk/core.IInspectable"
    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "TreeInspector") -> None:
        """Examines construct.

        :param inspector: - tree inspector to collect and process attributes.
        """
        return jsii.invoke(self, "inspect", [inspector])


@jsii.interface(jsii_type="@aws-cdk/core.IListProducer")
class IListProducer(jsii.compat.Protocol):
    """Interface for lazy list producers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -
        """
        ...


class _IListProducerProxy():
    """Interface for lazy list producers."""
    __jsii_type__ = "@aws-cdk/core.IListProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="@aws-cdk/core.INumberProducer")
class INumberProducer(jsii.compat.Protocol):
    """Interface for lazy number producers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INumberProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -
        """
        ...


class _INumberProducerProxy():
    """Interface for lazy number producers."""
    __jsii_type__ = "@aws-cdk/core.INumberProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="@aws-cdk/core.IPostProcessor")
class IPostProcessor(jsii.compat.Protocol):
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPostProcessorProxy

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -
        """
        ...


class _IPostProcessorProxy():
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it."""
    __jsii_type__ = "@aws-cdk/core.IPostProcessor"
    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -
        """
        return jsii.invoke(self, "postProcess", [input, context])


@jsii.interface(jsii_type="@aws-cdk/core.IResolvable")
class IResolvable(jsii.compat.Protocol):
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolvableProxy

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -
        """
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.
        """
        ...


class _IResolvableProxy():
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.
    """
    __jsii_type__ = "@aws-cdk/core.IResolvable"
    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.
        """
        return jsii.get(self, "creationStack")

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -
        """
        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.
        """
        return jsii.invoke(self, "toString", [])


@jsii.interface(jsii_type="@aws-cdk/core.ICfnConditionExpression")
class ICfnConditionExpression(IResolvable, jsii.compat.Protocol):
    """Represents a CloudFormation element that can be used within a Condition.

    You can use intrinsic functions, such as ``Fn.conditionIf``,
    ``Fn.conditionEquals``, and ``Fn.conditionNot``, to conditionally create
    stack resources. These conditions are evaluated based on input parameters
    that you declare when you create or update a stack. After you define all your
    conditions, you can associate them with resources or resource properties in
    the Resources and Outputs sections of a template.

    You define all conditions in the Conditions section of a template except for
    ``Fn.conditionIf`` conditions. You can use the ``Fn.conditionIf`` condition
    in the metadata attribute, update policy attribute, and property values in
    the Resources section and Outputs sections of a template.

    You might use conditions when you want to reuse a template that can create
    resources in different contexts, such as a test environment versus a
    production environment. In your template, you can add an EnvironmentType
    input parameter, which accepts either prod or test as inputs. For the
    production environment, you might include Amazon EC2 instances with certain
    capabilities; however, for the test environment, you want to use less
    capabilities to save costs. With conditions, you can define which resources
    are created and how they're configured for each environment type.

    You can use ``toString`` when you wish to embed a condition expression
    in a property value that accepts a ``string``. For example::

       # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
       sqs.Queue(self, "MyQueue",
           queue_name=Fn.condition_if("Condition", "Hello", "World").to_string()
       )
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICfnConditionExpressionProxy

    pass

class _ICfnConditionExpressionProxy(jsii.proxy_for(IResolvable)):
    """Represents a CloudFormation element that can be used within a Condition.

    You can use intrinsic functions, such as ``Fn.conditionIf``,
    ``Fn.conditionEquals``, and ``Fn.conditionNot``, to conditionally create
    stack resources. These conditions are evaluated based on input parameters
    that you declare when you create or update a stack. After you define all your
    conditions, you can associate them with resources or resource properties in
    the Resources and Outputs sections of a template.

    You define all conditions in the Conditions section of a template except for
    ``Fn.conditionIf`` conditions. You can use the ``Fn.conditionIf`` condition
    in the metadata attribute, update policy attribute, and property values in
    the Resources section and Outputs sections of a template.

    You might use conditions when you want to reuse a template that can create
    resources in different contexts, such as a test environment versus a
    production environment. In your template, you can add an EnvironmentType
    input parameter, which accepts either prod or test as inputs. For the
    production environment, you might include Amazon EC2 instances with certain
    capabilities; however, for the test environment, you want to use less
    capabilities to save costs. With conditions, you can define which resources
    are created and how they're configured for each environment type.

    You can use ``toString`` when you wish to embed a condition expression
    in a property value that accepts a ``string``. For example::

       # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
       sqs.Queue(self, "MyQueue",
           queue_name=Fn.condition_if("Condition", "Hello", "World").to_string()
       )
    """
    __jsii_type__ = "@aws-cdk/core.ICfnConditionExpression"
    pass

@jsii.implements(ICfnConditionExpression, IResolvable)
class CfnCondition(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnCondition"):
    """Represents a CloudFormation condition, for resources which must be conditionally created and the determination must be made at deploy time."""
    def __init__(self, scope: "Construct", id: str, *, expression: typing.Optional["ICfnConditionExpression"]=None) -> None:
        """Build a new condition.

        The condition must be constructed with a condition token,
        that the condition is based on.

        :param scope: -
        :param id: -
        :param expression: The expression that the condition will evaluate. Default: - None.
        """
        props = CfnConditionProps(expression=expression)

        jsii.create(CfnCondition, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: "IResolveContext") -> typing.Any:
        """Synthesizes the condition.

        :param _context: -
        """
        return jsii.invoke(self, "resolve", [_context])

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> typing.Optional["ICfnConditionExpression"]:
        """The condition statement."""
        return jsii.get(self, "expression")

    @expression.setter
    def expression(self, value: typing.Optional["ICfnConditionExpression"]):
        jsii.set(self, "expression", value)


@jsii.interface(jsii_type="@aws-cdk/core.IResolveContext")
class IResolveContext(jsii.compat.Protocol):
    """Current resolution context for tokens."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolveContextProxy

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output."""
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "IConstruct":
        """The scope from which resolution has been initiated."""
        ...

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -
        """
        ...


class _IResolveContextProxy():
    """Current resolution context for tokens."""
    __jsii_type__ = "@aws-cdk/core.IResolveContext"
    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output."""
        return jsii.get(self, "preparing")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "IConstruct":
        """The scope from which resolution has been initiated."""
        return jsii.get(self, "scope")

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -
        """
        return jsii.invoke(self, "registerPostProcessor", [post_processor])

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -
        """
        return jsii.invoke(self, "resolve", [x])


@jsii.interface(jsii_type="@aws-cdk/core.IResource")
class IResource(IConstruct, jsii.compat.Protocol):
    """Interface for the Resource construct."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourceProxy

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this resource is defined."""
        ...


class _IResourceProxy(jsii.proxy_for(IConstruct)):
    """Interface for the Resource construct."""
    __jsii_type__ = "@aws-cdk/core.IResource"
    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this resource is defined."""
        return jsii.get(self, "stack")


@jsii.interface(jsii_type="@aws-cdk/core.IStringProducer")
class IStringProducer(jsii.compat.Protocol):
    """Interface for lazy string producers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -
        """
        ...


class _IStringProducerProxy():
    """Interface for lazy string producers."""
    __jsii_type__ = "@aws-cdk/core.IStringProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="@aws-cdk/core.ISynthesisSession")
class ISynthesisSession(jsii.compat.Protocol):
    """Represents a single session of synthesis.

    Passed into ``Construct.synthesize()`` methods.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISynthesisSessionProxy

    @builtins.property
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> aws_cdk.cx_api.CloudAssemblyBuilder:
        """The cloud assembly being synthesized."""
        ...

    @assembly.setter
    def assembly(self, value: aws_cdk.cx_api.CloudAssemblyBuilder):
        ...


class _ISynthesisSessionProxy():
    """Represents a single session of synthesis.

    Passed into ``Construct.synthesize()`` methods.
    """
    __jsii_type__ = "@aws-cdk/core.ISynthesisSession"
    @builtins.property
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> aws_cdk.cx_api.CloudAssemblyBuilder:
        """The cloud assembly being synthesized."""
        return jsii.get(self, "assembly")

    @assembly.setter
    def assembly(self, value: aws_cdk.cx_api.CloudAssemblyBuilder):
        jsii.set(self, "assembly", value)


@jsii.interface(jsii_type="@aws-cdk/core.ITaggable")
class ITaggable(jsii.compat.Protocol):
    """Interface to implement tags."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITaggableProxy

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        """TagManager to set, remove and format tags."""
        ...


class _ITaggableProxy():
    """Interface to implement tags."""
    __jsii_type__ = "@aws-cdk/core.ITaggable"
    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        """TagManager to set, remove and format tags."""
        return jsii.get(self, "tags")


@jsii.interface(jsii_type="@aws-cdk/core.ITemplateOptions")
class ITemplateOptions(jsii.compat.Protocol):
    """CloudFormation template options for a stack."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITemplateOptionsProxy

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """Gets or sets the description of this stack.

        If provided, it will be included in the CloudFormation template's "Description" attribute.
        """
        ...

    @description.setter
    def description(self, value: typing.Optional[str]):
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Metadata associated with the CloudFormation template."""
        ...

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        ...

    @builtins.property
    @jsii.member(jsii_name="templateFormatVersion")
    def template_format_version(self) -> typing.Optional[str]:
        """Gets or sets the AWSTemplateFormatVersion field of the CloudFormation template."""
        ...

    @template_format_version.setter
    def template_format_version(self, value: typing.Optional[str]):
        ...

    @builtins.property
    @jsii.member(jsii_name="transform")
    def transform(self) -> typing.Optional[str]:
        """Gets or sets the top-level template transform for this stack (e.g. "AWS::Serverless-2016-10-31").

        deprecated
        :deprecated: use ``transforms`` instead.

        stability
        :stability: deprecated
        """
        ...

    @transform.setter
    def transform(self, value: typing.Optional[str]):
        ...

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.Optional[typing.List[str]]:
        """Gets or sets the top-level template transform(s) for this stack (e.g. ``["AWS::Serverless-2016-10-31"]``)."""
        ...

    @transforms.setter
    def transforms(self, value: typing.Optional[typing.List[str]]):
        ...


class _ITemplateOptionsProxy():
    """CloudFormation template options for a stack."""
    __jsii_type__ = "@aws-cdk/core.ITemplateOptions"
    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """Gets or sets the description of this stack.

        If provided, it will be included in the CloudFormation template's "Description" attribute.
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Metadata associated with the CloudFormation template."""
        return jsii.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="templateFormatVersion")
    def template_format_version(self) -> typing.Optional[str]:
        """Gets or sets the AWSTemplateFormatVersion field of the CloudFormation template."""
        return jsii.get(self, "templateFormatVersion")

    @template_format_version.setter
    def template_format_version(self, value: typing.Optional[str]):
        jsii.set(self, "templateFormatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="transform")
    def transform(self) -> typing.Optional[str]:
        """Gets or sets the top-level template transform for this stack (e.g. "AWS::Serverless-2016-10-31").

        deprecated
        :deprecated: use ``transforms`` instead.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "transform")

    @transform.setter
    def transform(self, value: typing.Optional[str]):
        jsii.set(self, "transform", value)

    @builtins.property
    @jsii.member(jsii_name="transforms")
    def transforms(self) -> typing.Optional[typing.List[str]]:
        """Gets or sets the top-level template transform(s) for this stack (e.g. ``["AWS::Serverless-2016-10-31"]``)."""
        return jsii.get(self, "transforms")

    @transforms.setter
    def transforms(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "transforms", value)


@jsii.interface(jsii_type="@aws-cdk/core.ITokenMapper")
class ITokenMapper(jsii.compat.Protocol):
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenMapperProxy

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -
        """
        ...


class _ITokenMapperProxy():
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.
    """
    __jsii_type__ = "@aws-cdk/core.ITokenMapper"
    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -
        """
        return jsii.invoke(self, "mapToken", [t])


@jsii.interface(jsii_type="@aws-cdk/core.ITokenResolver")
class ITokenResolver(jsii.compat.Protocol):
    """How to resolve tokens."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenResolverProxy

    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, l: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -
        """
        ...

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, s: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -
        """
        ...

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -
        """
        ...


class _ITokenResolverProxy():
    """How to resolve tokens."""
    __jsii_type__ = "@aws-cdk/core.ITokenResolver"
    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, l: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -
        """
        return jsii.invoke(self, "resolveList", [l, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, s: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -
        """
        return jsii.invoke(self, "resolveString", [s, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


@jsii.implements(ITokenResolver)
class DefaultTokenResolver(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.DefaultTokenResolver"):
    """Default resolver implementation.

    stability
    :stability: experimental
    """
    def __init__(self, concat: "IFragmentConcatenator") -> None:
        """
        :param concat: -

        stability
        :stability: experimental
        """
        jsii.create(DefaultTokenResolver, self, [concat])

    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, xs: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param xs: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [xs, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, fragments: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve string fragments to Tokens.

        :param fragments: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [fragments, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Default Token resolution.

        Resolve the Token, recurse into whatever it returns,
        then finally post-process it.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


@jsii.implements(IResolvable)
class Intrinsic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Intrinsic"):
    """Token subclass that represents values intrinsic to the target document language.

    WARNING: this class should not be externally exposed, but is currently visible
    because of a limitation of jsii (https://github.com/aws/jsii/issues/524).

    This class will disappear in a future release and should not be used.

    stability
    :stability: experimental
    """
    def __init__(self, value: typing.Any) -> None:
        """
        :param value: -

        stability
        :stability: experimental
        """
        jsii.create(Intrinsic, self, [value])

    @jsii.member(jsii_name="newError")
    def _new_error(self, message: str) -> typing.Any:
        """Creates a throwable Error object that contains the token creation stack trace.

        :param message: Error message.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "newError", [message])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param _context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [_context])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        """Turn this Token into JSON.

        Called automatically when JSON.stringify() is called on a Token.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Convert an instance of this Token to a string.

        This method will be called implicitly by language runtimes if the object
        is embedded into a string. We treat it the same as an explicit
        stringification.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The captured stack trace which represents the location in which this token was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")


class CfnDynamicReference(Intrinsic, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.CfnDynamicReference"):
    """References a dynamically retrieved value.

    This is a Construct so that subclasses will (eventually) be able to attach
    metadata to themselves without having to change call signatures.

    see
    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html
    """
    def __init__(self, service: "CfnDynamicReferenceService", key: str) -> None:
        """
        :param service: -
        :param key: -
        """
        jsii.create(CfnDynamicReference, self, [service, key])


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Lazy"):
    """Lazily produce a value.

    Can be used to return a string, list or numeric value whose actual value
    will only be calculated later, during synthesis.
    """
    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(cls, producer: "IAnyProducer", *, display_hint: typing.Optional[str]=None, omit_empty_array: typing.Optional[bool]=None) -> "IResolvable":
        """
        :param producer: -
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false
        """
        options = LazyAnyValueOptions(display_hint=display_hint, omit_empty_array=omit_empty_array)

        return jsii.sinvoke(cls, "anyValue", [producer, options])

    @jsii.member(jsii_name="listValue")
    @builtins.classmethod
    def list_value(cls, producer: "IListProducer", *, display_hint: typing.Optional[str]=None, omit_empty: typing.Optional[bool]=None) -> typing.List[str]:
        """
        :param producer: -
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false
        """
        options = LazyListValueOptions(display_hint=display_hint, omit_empty=omit_empty)

        return jsii.sinvoke(cls, "listValue", [producer, options])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, producer: "INumberProducer") -> jsii.Number:
        """
        :param producer: -
        """
        return jsii.sinvoke(cls, "numberValue", [producer])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(cls, producer: "IStringProducer", *, display_hint: typing.Optional[str]=None) -> str:
        """
        :param producer: -
        :param display_hint: Use the given name as a display hint. Default: - No hint
        """
        options = LazyStringValueOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "stringValue", [producer, options])


@jsii.data_type(jsii_type="@aws-cdk/core.LazyAnyValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint', 'omit_empty_array': 'omitEmptyArray'})
class LazyAnyValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None, omit_empty_array: typing.Optional[bool]=None):
        """Options for creating lazy untyped tokens.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint
        if omit_empty_array is not None: self._values["omit_empty_array"] = omit_empty_array

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint
        """
        return self._values.get('display_hint')

    @builtins.property
    def omit_empty_array(self) -> typing.Optional[bool]:
        """If the produced value is an array and it is empty, return 'undefined' instead.

        default
        :default: false
        """
        return self._values.get('omit_empty_array')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyAnyValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.LazyListValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint', 'omit_empty': 'omitEmpty'})
class LazyListValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None, omit_empty: typing.Optional[bool]=None):
        """Options for creating a lazy list token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint
        if omit_empty is not None: self._values["omit_empty"] = omit_empty

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint
        """
        return self._values.get('display_hint')

    @builtins.property
    def omit_empty(self) -> typing.Optional[bool]:
        """If the produced list is empty, return 'undefined' instead.

        default
        :default: false
        """
        return self._values.get('omit_empty')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyListValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.LazyStringValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint'})
class LazyStringValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None):
        """Options for creating a lazy string token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint
        """
        return self._values.get('display_hint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyStringValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class PhysicalName(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.PhysicalName"):
    """Includes special markers for automatic generation of physical names."""
    @jsii.python.classproperty
    @jsii.member(jsii_name="GENERATE_IF_NEEDED")
    def GENERATE_IF_NEEDED(cls) -> str:
        """Use this to automatically generate a physical name for an AWS resource only if the resource is referenced across environments (account/region).

        Otherwise, the name will be allocated during deployment by CloudFormation.

        If you are certain that a resource will be referenced across environments,
        you may also specify an explicit physical name for it. This option is
        mostly designed for reusable constructs which may or may not be referenced
        acrossed environments.
        """
        return jsii.sget(cls, "GENERATE_IF_NEEDED")


class Reference(Intrinsic, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/core.Reference"):
    """An intrinsic Token that represents a reference to a construct.

    References are recorded.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ReferenceProxy

    def __init__(self, value: typing.Any, target: "IConstruct", display_name: typing.Optional[str]=None) -> None:
        """
        :param value: -
        :param target: -
        :param display_name: -
        """
        jsii.create(Reference, self, [value, target, display_name])

    @jsii.member(jsii_name="isReference")
    @builtins.classmethod
    def is_reference(cls, x: typing.Any) -> bool:
        """Check whether this is actually a Reference.

        :param x: -
        """
        return jsii.sinvoke(cls, "isReference", [x])

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> str:
        return jsii.get(self, "displayName")

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "IConstruct":
        return jsii.get(self, "target")


class _ReferenceProxy(Reference):
    pass

@jsii.enum(jsii_type="@aws-cdk/core.RemovalPolicy")
class RemovalPolicy(enum.Enum):
    DESTROY = "DESTROY"
    """This is the default removal policy.

    It means that when the resource is
    removed from the app, it will be physically destroyed.
    """
    RETAIN = "RETAIN"
    """This uses the 'Retain' DeletionPolicy, which will cause the resource to be retained in the account, but orphaned from the stack."""

@jsii.data_type(jsii_type="@aws-cdk/core.RemovalPolicyOptions", jsii_struct_bases=[], name_mapping={'apply_to_update_replace_policy': 'applyToUpdateReplacePolicy', 'default': 'default'})
class RemovalPolicyOptions():
    def __init__(self, *, apply_to_update_replace_policy: typing.Optional[bool]=None, default: typing.Optional["RemovalPolicy"]=None):
        """
        :param apply_to_update_replace_policy: Apply the same deletion policy to the resource's "UpdateReplacePolicy". Default: true
        :param default: The default policy to apply in case the removal policy is not defined. Default: - Default value is resource specific. To determine the default value for a resoure, please consult that specific resource's documentation.
        """
        self._values = {
        }
        if apply_to_update_replace_policy is not None: self._values["apply_to_update_replace_policy"] = apply_to_update_replace_policy
        if default is not None: self._values["default"] = default

    @builtins.property
    def apply_to_update_replace_policy(self) -> typing.Optional[bool]:
        """Apply the same deletion policy to the resource's "UpdateReplacePolicy".

        default
        :default: true
        """
        return self._values.get('apply_to_update_replace_policy')

    @builtins.property
    def default(self) -> typing.Optional["RemovalPolicy"]:
        """The default policy to apply in case the removal policy is not defined.

        default
        :default:

        - Default value is resource specific. To determine the default value for a resoure,
          please consult that specific resource's documentation.
        """
        return self._values.get('default')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RemovalPolicyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IAspect)
class RemoveTag(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.RemoveTag"):
    """The RemoveTag Aspect will handle removing tags from this node and children."""
    def __init__(self, key: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """
        :param key: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        jsii.create(RemoveTag, self, [key, props])

    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        """
        :param resource: -
        """
        return jsii.invoke(self, "applyTag", [resource])

    @jsii.member(jsii_name="visit")
    def visit(self, construct: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param construct: -
        """
        return jsii.invoke(self, "visit", [construct])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        """The string key for the tag."""
        return jsii.get(self, "key")

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TagProps":
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="@aws-cdk/core.ResolveOptions", jsii_struct_bases=[], name_mapping={'resolver': 'resolver', 'scope': 'scope', 'preparing': 'preparing'})
class ResolveOptions():
    def __init__(self, *, resolver: "ITokenResolver", scope: "IConstruct", preparing: typing.Optional[bool]=None):
        """Options to the resolve() operation.

        NOT the same as the ResolveContext; ResolveContext is exposed to Token
        implementors and resolution hooks, whereas this struct is just to bundle
        a number of things that would otherwise be arguments to resolve() in a
        readable way.

        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false
        """
        self._values = {
            'resolver': resolver,
            'scope': scope,
        }
        if preparing is not None: self._values["preparing"] = preparing

    @builtins.property
    def resolver(self) -> "ITokenResolver":
        """The resolver to apply to any resolvable tokens found."""
        return self._values.get('resolver')

    @builtins.property
    def scope(self) -> "IConstruct":
        """The scope from which resolution is performed."""
        return self._values.get('scope')

    @builtins.property
    def preparing(self) -> typing.Optional[bool]:
        """Whether the resolution is being executed during the prepare phase or not.

        default
        :default: false
        """
        return self._values.get('preparing')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResolveOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IResource)
class Resource(Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/core.Resource"):
    """A construct which represents an AWS resource."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ResourceProxy

    def __init__(self, scope: "Construct", id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = ResourceProps(physical_name=physical_name)

        jsii.create(Resource, self, [scope, id, props])

    @jsii.member(jsii_name="generatePhysicalName")
    def _generate_physical_name(self) -> str:
        return jsii.invoke(self, "generatePhysicalName", [])

    @jsii.member(jsii_name="getResourceArnAttribute")
    def _get_resource_arn_attribute(self, arn_attr: str, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None) -> str:
        """Returns an environment-sensitive token that should be used for the resource's "ARN" attribute (e.g. ``bucket.bucketArn``).

        Normally, this token will resolve to ``arnAttr``, but if the resource is
        referenced across environments, ``arnComponents`` will be used to synthesize
        a concrete ARN with the resource's physical name. Make sure to reference
        ``this.physicalName`` in ``arnComponents``.

        :param arn_attr: The CFN attribute which resolves to the ARN of the resource. Commonly it will be called "Arn" (e.g. ``resource.attrArn``), but sometimes it's the CFN resource's ``ref``.
        :param resource: Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.
        :param service: The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').
        :param account: The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the ARNs for some resources don't require an account number, so this component might be omitted. Default: The account the stack is deployed to.
        :param partition: The partition that the resource is in. For standard AWS regions, the partition is aws. If you have resources in other partitions, the partition is aws-partitionname. For example, the partition for resources in the China (Beijing) region is aws-cn. Default: The AWS partition the stack is deployed to.
        :param region: The region the resource resides in. Note that the ARNs for some resources do not require a region, so this component might be omitted. Default: The region the stack is deployed to.
        :param resource_name: Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.
        :param sep: Separator between resource type and the resource. Can be either '/', ':' or an empty string. Will only be used if resourceName is defined. Default: '/'

        stability
        :stability: experimental
        """
        arn_components = ArnComponents(resource=resource, service=service, account=account, partition=partition, region=region, resource_name=resource_name, sep=sep)

        return jsii.invoke(self, "getResourceArnAttribute", [arn_attr, arn_components])

    @jsii.member(jsii_name="getResourceNameAttribute")
    def _get_resource_name_attribute(self, name_attr: str) -> str:
        """Returns an environment-sensitive token that should be used for the resource's "name" attribute (e.g. ``bucket.bucketName``).

        Normally, this token will resolve to ``nameAttr``, but if the resource is
        referenced across environments, it will be resolved to ``this.physicalName``,
        which will be a concrete name.

        :param name_attr: The CFN attribute which resolves to the resource's name. Commonly this is the resource's ``ref``.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResourceNameAttribute", [name_attr])

    @builtins.property
    @jsii.member(jsii_name="physicalName")
    def _physical_name(self) -> str:
        """Returns a string-encoded token that resolves to the physical name that should be passed to the CloudFormation resource.

        This value will resolve to one of the following:

        - a concrete value (e.g. ``"my-awesome-bucket"``)
        - ``undefined``, when a name should be generated by CloudFormation
        - a concrete name generated automatically during synthesis, in
          cross-environment scenarios.

        stability
        :stability: experimental
        """
        return jsii.get(self, "physicalName")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        """The stack in which this resource is defined."""
        return jsii.get(self, "stack")


class _ResourceProxy(Resource):
    pass

@jsii.data_type(jsii_type="@aws-cdk/core.ResourceProps", jsii_struct_bases=[], name_mapping={'physical_name': 'physicalName'})
class ResourceProps():
    def __init__(self, *, physical_name: typing.Optional[str]=None):
        """Construction properties for {@link Resource}.

        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        self._values = {
        }
        if physical_name is not None: self._values["physical_name"] = physical_name

    @builtins.property
    def physical_name(self) -> typing.Optional[str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        default
        :default: - The physical name will be allocated by CloudFormation at deployment time
        """
        return self._values.get('physical_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScopedAws(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.ScopedAws"):
    """Accessor for scoped pseudo parameters.

    These pseudo parameters are anchored to a stack somewhere in the construct
    tree, and their values will be exported automatically.
    """
    def __init__(self, scope: "Construct") -> None:
        """
        :param scope: -
        """
        jsii.create(ScopedAws, self, [scope])

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> str:
        return jsii.get(self, "accountId")

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[str]:
        return jsii.get(self, "notificationArns")

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> str:
        return jsii.get(self, "partition")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        return jsii.get(self, "region")

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        return jsii.get(self, "stackId")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(self) -> str:
        return jsii.get(self, "urlSuffix")


class SecretValue(Intrinsic, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.SecretValue"):
    """Work with secret values in the CDK.

    Secret values in the CDK (such as those retrieved from SecretsManager) are
    represented as regular strings, just like other values that are only
    available at deployment time.

    To help you avoid accidental mistakes which would lead to you putting your
    secret values directly into a CloudFormation template, constructs that take
    secret values will not allow you to pass in a literal secret value. They do
    so by calling ``Secret.assertSafeSecret()``.

    You can escape the check by calling ``Secret.plainText()``, but doing
    so is highly discouraged.
    """
    def __init__(self, value: typing.Any) -> None:
        """
        :param value: -

        stability
        :stability: experimental
        """
        jsii.create(SecretValue, self, [value])

    @jsii.member(jsii_name="cfnDynamicReference")
    @builtins.classmethod
    def cfn_dynamic_reference(cls, ref: "CfnDynamicReference") -> "SecretValue":
        """Obtain the secret value through a CloudFormation dynamic reference.

        If possible, use ``SecretValue.ssmSecure`` or ``SecretValue.secretsManager`` directly.

        :param ref: The dynamic reference to use.
        """
        return jsii.sinvoke(cls, "cfnDynamicReference", [ref])

    @jsii.member(jsii_name="cfnParameter")
    @builtins.classmethod
    def cfn_parameter(cls, param: "CfnParameter") -> "SecretValue":
        """Obtain the secret value through a CloudFormation parameter.

        Generally, this is not a recommended approach. AWS Secrets Manager is the
        recommended way to reference secrets.

        :param param: The CloudFormation parameter to use.
        """
        return jsii.sinvoke(cls, "cfnParameter", [param])

    @jsii.member(jsii_name="plainText")
    @builtins.classmethod
    def plain_text(cls, secret: str) -> "SecretValue":
        """Construct a literal secret value for use with secret-aware constructs.

        *Do not use this method for any secrets that you care about.*

        The only reasonable use case for using this method is when you are testing.

        :param secret: -
        """
        return jsii.sinvoke(cls, "plainText", [secret])

    @jsii.member(jsii_name="secretsManager")
    @builtins.classmethod
    def secrets_manager(cls, secret_id: str, *, json_field: typing.Optional[str]=None, version_id: typing.Optional[str]=None, version_stage: typing.Optional[str]=None) -> "SecretValue":
        """Creates a ``SecretValue`` with a value which is dynamically loaded from AWS Secrets Manager.

        :param secret_id: The ID or ARN of the secret.
        :param json_field: The key of a JSON field to retrieve. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.
        :param version_id: Specifies the unique identifier of the version of the secret you want to use. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT
        :param version_stage: Specified the secret version that you want to retrieve by the staging label attached to the version. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT
        """
        options = SecretsManagerSecretOptions(json_field=json_field, version_id=version_id, version_stage=version_stage)

        return jsii.sinvoke(cls, "secretsManager", [secret_id, options])

    @jsii.member(jsii_name="ssmSecure")
    @builtins.classmethod
    def ssm_secure(cls, parameter_name: str, version: str) -> "SecretValue":
        """Use a secret value stored from a Systems Manager (SSM) parameter.

        :param parameter_name: The name of the parameter in the Systems Manager Parameter Store. The parameter name is case-sensitive.
        :param version: An integer that specifies the version of the parameter to use. You must specify the exact version. You cannot currently specify that AWS CloudFormation use the latest version of a parameter.
        """
        return jsii.sinvoke(cls, "ssmSecure", [parameter_name, version])


@jsii.data_type(jsii_type="@aws-cdk/core.SecretsManagerSecretOptions", jsii_struct_bases=[], name_mapping={'json_field': 'jsonField', 'version_id': 'versionId', 'version_stage': 'versionStage'})
class SecretsManagerSecretOptions():
    def __init__(self, *, json_field: typing.Optional[str]=None, version_id: typing.Optional[str]=None, version_stage: typing.Optional[str]=None):
        """Options for referencing a secret value from Secrets Manager.

        :param json_field: The key of a JSON field to retrieve. This can only be used if the secret stores a JSON object. Default: - returns all the content stored in the Secrets Manager secret.
        :param version_id: Specifies the unique identifier of the version of the secret you want to use. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT
        :param version_stage: Specified the secret version that you want to retrieve by the staging label attached to the version. Can specify at most one of ``versionId`` and ``versionStage``. Default: AWSCURRENT
        """
        self._values = {
        }
        if json_field is not None: self._values["json_field"] = json_field
        if version_id is not None: self._values["version_id"] = version_id
        if version_stage is not None: self._values["version_stage"] = version_stage

    @builtins.property
    def json_field(self) -> typing.Optional[str]:
        """The key of a JSON field to retrieve.

        This can only be used if the secret
        stores a JSON object.

        default
        :default: - returns all the content stored in the Secrets Manager secret.
        """
        return self._values.get('json_field')

    @builtins.property
    def version_id(self) -> typing.Optional[str]:
        """Specifies the unique identifier of the version of the secret you want to use.

        Can specify at most one of ``versionId`` and ``versionStage``.

        default
        :default: AWSCURRENT
        """
        return self._values.get('version_id')

    @builtins.property
    def version_stage(self) -> typing.Optional[str]:
        """Specified the secret version that you want to retrieve by the staging label attached to the version.

        Can specify at most one of ``versionId`` and ``versionStage``.

        default
        :default: AWSCURRENT
        """
        return self._values.get('version_stage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretsManagerSecretOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ITaggable)
class Stack(Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Stack"):
    """A root construct which represents a single CloudFormation stack."""
    def __init__(self, scope: typing.Optional["Construct"]=None, id: typing.Optional[str]=None, *, description: typing.Optional[str]=None, env: typing.Optional["Environment"]=None, stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        """Creates a new stack.

        :param scope: Parent of this stack, usually a Program instance.
        :param id: The construct ID of this stack. If ``stackName`` is not explicitly defined, this id (and any parent IDs) will be used to determine the physical ID of the stack.
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        """
        props = StackProps(description=description, env=env, stack_name=stack_name, tags=tags)

        jsii.create(Stack, self, [scope, id, props])

    @jsii.member(jsii_name="isStack")
    @builtins.classmethod
    def is_stack(cls, x: typing.Any) -> bool:
        """Return whether the given object is a Stack.

        We do attribute detection since we can't reliably use 'instanceof'.

        :param x: -
        """
        return jsii.sinvoke(cls, "isStack", [x])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: "IConstruct") -> "Stack":
        """Looks up the first stack scope in which ``construct`` is defined.

        Fails if there is no stack up the tree.

        :param construct: The construct to start the search from.
        """
        return jsii.sinvoke(cls, "of", [construct])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, target: "Stack", reason: typing.Optional[str]=None) -> None:
        """Add a dependency between this stack and another stack.

        This can be used to define dependencies between any two stacks within an
        app, and also supports nested stacks.

        :param target: -
        :param reason: -
        """
        return jsii.invoke(self, "addDependency", [target, reason])

    @jsii.member(jsii_name="addDockerImageAsset")
    def add_docker_image_asset(self, *, directory_name: str, source_hash: str, docker_build_args: typing.Optional[typing.Mapping[str,str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None) -> "DockerImageAssetLocation":
        """
        :param directory_name: The directory where the Dockerfile is stored, must be relative to the cloud assembly root.
        :param source_hash: The hash of the contents of the docker build context. This hash is used throughout the system to identify this image and avoid duplicate work in case the source did not change. NOTE: this means that if you wish to update your docker image, you must make a modification to the source (e.g. add some metadata to your Dockerfile).
        :param docker_build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param docker_build_target: Docker target to build to. Default: - no target
        :param docker_file: Path to the Dockerfile (relative to the directory). Default: - no file
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.
        """
        asset = DockerImageAssetSource(directory_name=directory_name, source_hash=source_hash, docker_build_args=docker_build_args, docker_build_target=docker_build_target, docker_file=docker_file, repository_name=repository_name)

        return jsii.invoke(self, "addDockerImageAsset", [asset])

    @jsii.member(jsii_name="addFileAsset")
    def add_file_asset(self, *, file_name: str, packaging: "FileAssetPackaging", source_hash: str) -> "FileAssetLocation":
        """
        :param file_name: The path, relative to the root of the cloud assembly, in which this asset source resides. This can be a path to a file or a directory, dependning on the packaging type.
        :param packaging: Which type of packaging to perform.
        :param source_hash: A hash on the content source. This hash is used to uniquely identify this asset throughout the system. If this value doesn't change, the asset will not be rebuilt or republished.
        """
        asset = FileAssetSource(file_name=file_name, packaging=packaging, source_hash=source_hash)

        return jsii.invoke(self, "addFileAsset", [asset])

    @jsii.member(jsii_name="addTransform")
    def add_transform(self, transform: str) -> None:
        """Add a Transform to this stack. A Transform is a macro that AWS CloudFormation uses to process your template.

        Duplicate values are removed when stack is synthesized.

        :param transform: The transform to add.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-section-structure.html

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            add_transform("AWS::Serverless-2016-10-31")
        """
        return jsii.invoke(self, "addTransform", [transform])

    @jsii.member(jsii_name="allocateLogicalId")
    def _allocate_logical_id(self, cfn_element: "CfnElement") -> str:
        """Returns the naming scheme used to allocate logical IDs.

        By default, uses
        the ``HashedAddressingScheme`` but this method can be overridden to customize
        this behavior.

        In order to make sure logical IDs are unique and stable, we hash the resource
        construct tree path (i.e. toplevel/secondlevel/.../myresource) and add it as
        a suffix to the path components joined without a separator (CloudFormation
        IDs only allow alphanumeric characters).

        The result will be:

        <path.join('')><md5(path.join('/')>
        "human"      "hash"

        If the "human" part of the ID exceeds 240 characters, we simply trim it so
        the total ID doesn't exceed CloudFormation's 255 character limit.

        We only take 8 characters from the md5 hash (0.000005 chance of collision).

        Special cases:

        - If the path only contains a single component (i.e. it's a top-level
          resource), we won't add the hash to it. The hash is not needed for
          disamiguation and also, it allows for a more straightforward migration an
          existing CloudFormation template to a CDK stack without logical ID changes
          (or renames).
        - For aesthetic reasons, if the last components of the path are the same
          (i.e. ``L1/L2/Pipeline/Pipeline``), they will be de-duplicated to make the
          resulting human portion of the ID more pleasing: ``L1L2Pipeline<HASH>``
          instead of ``L1L2PipelinePipeline<HASH>``
        - If a component is named "Default" it will be omitted from the path. This
          allows refactoring higher level abstractions around constructs without affecting
          the IDs of already deployed resources.
        - If a component is named "Resource" it will be omitted from the user-visible
          path, but included in the hash. This reduces visual noise in the human readable
          part of the identifier.

        :param cfn_element: The element for which the logical ID is allocated.
        """
        return jsii.invoke(self, "allocateLogicalId", [cfn_element])

    @jsii.member(jsii_name="formatArn")
    def format_arn(self, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None) -> str:
        """Creates an ARN from components.

        If ``partition``, ``region`` or ``account`` are not specified, the stack's
        partition, region and account will be used.

        If any component is the empty string, an empty string will be inserted
        into the generated ARN at the location that component corresponds to.

        The ARN will be formatted as follows:

        arn:{partition}:{service}:{region}:{account}:{resource}{sep}}{resource-name}

        The required ARN pieces that are omitted will be taken from the stack that
        the 'scope' is attached to. If all ARN pieces are supplied, the supplied scope
        can be 'undefined'.

        :param resource: Resource type (e.g. "table", "autoScalingGroup", "certificate"). For some resource types, e.g. S3 buckets, this field defines the bucket name.
        :param service: The service namespace that identifies the AWS product (for example, 's3', 'iam', 'codepipline').
        :param account: The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the ARNs for some resources don't require an account number, so this component might be omitted. Default: The account the stack is deployed to.
        :param partition: The partition that the resource is in. For standard AWS regions, the partition is aws. If you have resources in other partitions, the partition is aws-partitionname. For example, the partition for resources in the China (Beijing) region is aws-cn. Default: The AWS partition the stack is deployed to.
        :param region: The region the resource resides in. Note that the ARNs for some resources do not require a region, so this component might be omitted. Default: The region the stack is deployed to.
        :param resource_name: Resource name or path within the resource (i.e. S3 bucket object key) or a wildcard such as ``"*"``. This is service-dependent.
        :param sep: Separator between resource type and the resource. Can be either '/', ':' or an empty string. Will only be used if resourceName is defined. Default: '/'
        """
        components = ArnComponents(resource=resource, service=service, account=account, partition=partition, region=region, resource_name=resource_name, sep=sep)

        return jsii.invoke(self, "formatArn", [components])

    @jsii.member(jsii_name="getLogicalId")
    def get_logical_id(self, element: "CfnElement") -> str:
        """Allocates a stack-unique CloudFormation-compatible logical identity for a specific resource.

        This method is called when a ``CfnElement`` is created and used to render the
        initial logical identity of resources. Logical ID renames are applied at
        this stage.

        This method uses the protected method ``allocateLogicalId`` to render the
        logical ID for an element. To modify the naming scheme, extend the ``Stack``
        class and override this method.

        :param element: The CloudFormation element for which a logical identity is needed.
        """
        return jsii.invoke(self, "getLogicalId", [element])

    @jsii.member(jsii_name="parseArn")
    def parse_arn(self, arn: str, sep_if_token: typing.Optional[str]=None, has_name: typing.Optional[bool]=None) -> "ArnComponents":
        """Given an ARN, parses it and returns components.

        If the ARN is a concrete string, it will be parsed and validated. The
        separator (``sep``) will be set to '/' if the 6th component includes a '/',
        in which case, ``resource`` will be set to the value before the '/' and
        ``resourceName`` will be the rest. In case there is no '/', ``resource`` will
        be set to the 6th components and ``resourceName`` will be set to the rest
        of the string.

        If the ARN includes tokens (or is a token), the ARN cannot be validated,
        since we don't have the actual value yet at the time of this function
        call. You will have to know the separator and the type of ARN. The
        resulting ``ArnComponents`` object will contain tokens for the
        subexpressions of the ARN, not string literals. In this case this
        function cannot properly parse the complete final resourceName (path) out
        of ARNs that use '/' to both separate the 'resource' from the
        'resourceName' AND to subdivide the resourceName further. For example, in
        S3 ARNs::

           arn:aws:s3:::my_corporate_bucket/path/to/exampleobject.png

        After parsing the resourceName will not contain
        'path/to/exampleobject.png' but simply 'path'. This is a limitation
        because there is no slicing functionality in CloudFormation templates.

        :param arn: The ARN string to parse.
        :param sep_if_token: The separator used to separate resource from resourceName.
        :param has_name: Whether there is a name component in the ARN at all. For example, SNS Topics ARNs have the 'resource' component contain the topic name, and no 'resourceName' component.

        return
        :return:

        an ArnComponents object which allows access to the various
        components of the ARN.
        """
        return jsii.invoke(self, "parseArn", [arn, sep_if_token, has_name])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        """Prepare stack.

        Find all CloudFormation references and tell them we're consuming them.

        Find all dependencies as well and add the appropriate DependsOn fields.
        """
        return jsii.invoke(self, "prepare", [])

    @jsii.member(jsii_name="prepareCrossReference")
    def _prepare_cross_reference(self, source_stack: "Stack", reference: "Reference") -> "IResolvable":
        """Exports a resolvable value for use in another stack.

        :param source_stack: -
        :param reference: -

        return
        :return: a token that can be used to reference the value from the producing stack.
        """
        return jsii.invoke(self, "prepareCrossReference", [source_stack, reference])

    @jsii.member(jsii_name="renameLogicalId")
    def rename_logical_id(self, old_id: str, new_id: str) -> None:
        """Rename a generated logical identities.

        To modify the naming scheme strategy, extend the ``Stack`` class and
        override the ``createNamingScheme`` method.

        :param old_id: -
        :param new_id: -
        """
        return jsii.invoke(self, "renameLogicalId", [old_id, new_id])

    @jsii.member(jsii_name="reportMissingContext")
    def report_missing_context(self, *, key: str, props: typing.Mapping[str,typing.Any], provider: str) -> None:
        """Indicate that a context key was expected.

        Contains instructions which will be emitted into the cloud assembly on how
        the key should be supplied.

        :param key: The missing context key.
        :param props: A set of provider-specific options.
        :param provider: The provider from which we expect this context key to be obtained.
        """
        report = aws_cdk.cx_api.MissingContext(key=key, props=props, provider=provider)

        return jsii.invoke(self, "reportMissingContext", [report])

    @jsii.member(jsii_name="resolve")
    def resolve(self, obj: typing.Any) -> typing.Any:
        """Resolve a tokenized value in the context of the current stack.

        :param obj: -
        """
        return jsii.invoke(self, "resolve", [obj])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: "ISynthesisSession") -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -
        """
        return jsii.invoke(self, "synthesize", [session])

    @jsii.member(jsii_name="toJsonString")
    def to_json_string(self, obj: typing.Any, space: typing.Optional[jsii.Number]=None) -> str:
        """Convert an object, potentially containing tokens, to a JSON string.

        :param obj: -
        :param space: -
        """
        return jsii.invoke(self, "toJsonString", [obj, space])

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> str:
        """The AWS account into which this stack will be deployed.

        This value is resolved according to the following rules:

        1. The value provided to ``env.account`` when the stack is defined. This can
           either be a concerete account (e.g. ``585695031111``) or the
           ``Aws.accountId`` token.
        2. ``Aws.accountId``, which represents the CloudFormation intrinsic reference
           ``{ "Ref": "AWS::AccountId" }`` encoded as a string token.

        Preferably, you should use the return value as an opaque string and not
        attempt to parse it to implement your logic. If you do, you must first
        check that it is a concerete value an not an unresolved token. If this
        value is an unresolved token (``Token.isUnresolved(stack.account)`` returns
        ``true``), this implies that the user wishes that this stack will synthesize
        into a **account-agnostic template**. In this case, your code should either
        fail (throw an error, emit a synth error using ``node.addError``) or
        implement some other region-agnostic behavior.
        """
        return jsii.get(self, "account")

    @builtins.property
    @jsii.member(jsii_name="artifactId")
    def artifact_id(self) -> str:
        """The ID of the cloud assembly artifact for this stack."""
        return jsii.get(self, "artifactId")

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        """Returnst the list of AZs that are availability in the AWS environment (account/region) associated with this stack.

        If the stack is environment-agnostic (either account and/or region are
        tokens), this property will return an array with 2 tokens that will resolve
        at deploy-time to the first two availability zones returned from CloudFormation's
        ``Fn::GetAZs`` intrinsic function.

        If they are not available in the context, returns a set of dummy values and
        reports them as missing, and let the CLI resolve them by calling EC2
        ``DescribeAvailabilityZones`` on the target environment.
        """
        return jsii.get(self, "availabilityZones")

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Stack"]:
        """Return the stacks this stack depends on."""
        return jsii.get(self, "dependencies")

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> str:
        """The environment coordinates in which this stack is deployed.

        In the form
        ``aws://account/region``. Use ``stack.account`` and ``stack.region`` to obtain
        the specific values, no need to parse.

        You can use this value to determine if two stacks are targeting the same
        environment.

        If either ``stack.account`` or ``stack.region`` are not concrete values (e.g.
        ``Aws.account`` or ``Aws.region``) the special strings ``unknown-account`` and/or
        ``unknown-region`` will be used respectively to indicate this stack is
        region/account-agnostic.
        """
        return jsii.get(self, "environment")

    @builtins.property
    @jsii.member(jsii_name="nested")
    def nested(self) -> bool:
        """Indicates if this is a nested stack, in which case ``parentStack`` will include a reference to it's parent."""
        return jsii.get(self, "nested")

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[str]:
        """Returns the list of notification Amazon Resource Names (ARNs) for the current stack."""
        return jsii.get(self, "notificationArns")

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> str:
        """The partition in which this stack is defined."""
        return jsii.get(self, "partition")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """The AWS region into which this stack will be deployed (e.g. ``us-west-2``).

        This value is resolved according to the following rules:

        1. The value provided to ``env.region`` when the stack is defined. This can
           either be a concerete region (e.g. ``us-west-2``) or the ``Aws.region``
           token.
        2. ``Aws.region``, which is represents the CloudFormation intrinsic reference
           ``{ "Ref": "AWS::Region" }`` encoded as a string token.

        Preferably, you should use the return value as an opaque string and not
        attempt to parse it to implement your logic. If you do, you must first
        check that it is a concerete value an not an unresolved token. If this
        value is an unresolved token (``Token.isUnresolved(stack.region)`` returns
        ``true``), this implies that the user wishes that this stack will synthesize
        into a **region-agnostic template**. In this case, your code should either
        fail (throw an error, emit a synth error using ``node.addError``) or
        implement some other region-agnostic behavior.
        """
        return jsii.get(self, "region")

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """The ID of the stack.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Afterresolving , lookslikearn:aws:cloudformation:us-west-2123456789012stack / teststack / 51af3dc0 - da77 - 11e4 - 872e-1234567db123
        """
        return jsii.get(self, "stackId")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        """The concrete CloudFormation physical stack name.

        This is either the name defined explicitly in the ``stackName`` prop or
        allocated based on the stack's location in the construct tree. Stacks that
        are directly defined under the app use their construct ``id`` as their stack
        name. Stacks that are defined deeper within the tree will use a hashed naming
        scheme based on the construct path to ensure uniqueness.

        If you wish to obtain the deploy-time AWS::StackName intrinsic,
        you can use ``Aws.stackName`` directly.
        """
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        """Tags to be applied to the stack."""
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="templateFile")
    def template_file(self) -> str:
        """The name of the CloudFormation template file emitted to the output directory during synthesis.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            MyStack.template.json
        """
        return jsii.get(self, "templateFile")

    @builtins.property
    @jsii.member(jsii_name="templateOptions")
    def template_options(self) -> "ITemplateOptions":
        """Options for CloudFormation template (like version, transform, description)."""
        return jsii.get(self, "templateOptions")

    @builtins.property
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> str:
        """An attribute (late-bound) that represents the URL of the template file in the deployment bucket.

        stability
        :stability: experimental
        """
        return jsii.get(self, "templateUrl")

    @builtins.property
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(self) -> str:
        """The Amazon domain suffix for the region in which this stack is defined."""
        return jsii.get(self, "urlSuffix")

    @builtins.property
    @jsii.member(jsii_name="nestedStackParent")
    def nested_stack_parent(self) -> typing.Optional["Stack"]:
        """If this is a nested stack, returns it's parent stack."""
        return jsii.get(self, "nestedStackParent")

    @builtins.property
    @jsii.member(jsii_name="nestedStackResource")
    def nested_stack_resource(self) -> typing.Optional["CfnResource"]:
        """If this is a nested stack, this represents its ``AWS::CloudFormation::Stack`` resource.

        ``undefined`` for top-level (non-nested) stacks.

        stability
        :stability: experimental
        """
        return jsii.get(self, "nestedStackResource")

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> typing.Optional["Stack"]:
        """Returns the parent of a nested stack.

        deprecated
        :deprecated: use ``nestedStackParent``

        stability
        :stability: deprecated
        """
        return jsii.get(self, "parentStack")


@jsii.data_type(jsii_type="@aws-cdk/core.StackProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'env': 'env', 'stack_name': 'stackName', 'tags': 'tags'})
class StackProps():
    def __init__(self, *, description: typing.Optional[str]=None, env: typing.Optional["Environment"]=None, stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str,str]]=None):
        """
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        """
        if isinstance(env, dict): env = Environment(**env)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if env is not None: self._values["env"] = env
        if stack_name is not None: self._values["stack_name"] = stack_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the stack.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def env(self) -> typing.Optional["Environment"]:
        """The AWS environment (account/region) where this stack will be deployed.

        default
        :default:

        - The ``default-account`` and ``default-region`` context parameters will be
          used. If they are undefined, it will not be possible to deploy the stack.
        """
        return self._values.get('env')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """Name to deploy the stack with.

        default
        :default: - Derived from construct path.
        """
        return self._values.get('stack_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Stack tags that will be applied to all the taggable resources and the stack itself.

        default
        :default: {}
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StackProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IFragmentConcatenator)
class StringConcat(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.StringConcat"):
    """Converts all fragments to strings and concats those.

    Drops 'undefined's.
    """
    def __init__(self) -> None:
        jsii.create(StringConcat, self, [])

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.data_type(jsii_type="@aws-cdk/core.SynthesisOptions", jsii_struct_bases=[aws_cdk.cx_api.AssemblyBuildOptions], name_mapping={'runtime_info': 'runtimeInfo', 'outdir': 'outdir', 'skip_validation': 'skipValidation'})
class SynthesisOptions(aws_cdk.cx_api.AssemblyBuildOptions):
    def __init__(self, *, runtime_info: typing.Optional[aws_cdk.cx_api.RuntimeInfo]=None, outdir: typing.Optional[str]=None, skip_validation: typing.Optional[bool]=None):
        """Options for synthesis.

        :param runtime_info: Include the specified runtime information (module versions) in manifest. Default: - if this option is not specified, runtime info will not be included
        :param outdir: The output directory into which to synthesize the cloud assembly. Default: - creates a temporary directory
        :param skip_validation: Whether synthesis should skip the validation phase. Default: false
        """
        if isinstance(runtime_info, dict): runtime_info = aws_cdk.cx_api.RuntimeInfo(**runtime_info)
        self._values = {
        }
        if runtime_info is not None: self._values["runtime_info"] = runtime_info
        if outdir is not None: self._values["outdir"] = outdir
        if skip_validation is not None: self._values["skip_validation"] = skip_validation

    @builtins.property
    def runtime_info(self) -> typing.Optional[aws_cdk.cx_api.RuntimeInfo]:
        """Include the specified runtime information (module versions) in manifest.

        default
        :default: - if this option is not specified, runtime info will not be included

        stability
        :stability: experimental
        """
        return self._values.get('runtime_info')

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The output directory into which to synthesize the cloud assembly.

        default
        :default: - creates a temporary directory
        """
        return self._values.get('outdir')

    @builtins.property
    def skip_validation(self) -> typing.Optional[bool]:
        """Whether synthesis should skip the validation phase.

        default
        :default: false
        """
        return self._values.get('skip_validation')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SynthesisOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IAspect)
class Tag(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Tag"):
    """The Tag Aspect will handle adding a tag to this node and cascading tags to children."""
    def __init__(self, key: str, value: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """
        :param key: -
        :param value: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        jsii.create(Tag, self, [key, value, props])

    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, scope: "Construct", key: str, value: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """add tags to the node of a construct and all its the taggable children.

        :param scope: -
        :param key: -
        :param value: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        return jsii.sinvoke(cls, "add", [scope, key, value, props])

    @jsii.member(jsii_name="remove")
    @builtins.classmethod
    def remove(cls, scope: "Construct", key: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """remove tags to the node of a construct and all its the taggable children.

        :param scope: -
        :param key: -
        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources
        """
        props = TagProps(apply_to_launched_instances=apply_to_launched_instances, exclude_resource_types=exclude_resource_types, include_resource_types=include_resource_types, priority=priority)

        return jsii.sinvoke(cls, "remove", [scope, key, props])

    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        """
        :param resource: -
        """
        return jsii.invoke(self, "applyTag", [resource])

    @jsii.member(jsii_name="visit")
    def visit(self, construct: "IConstruct") -> None:
        """All aspects can visit an IConstruct.

        :param construct: -
        """
        return jsii.invoke(self, "visit", [construct])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        """The string key for the tag."""
        return jsii.get(self, "key")

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TagProps":
        return jsii.get(self, "props")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        """The string value of the tag."""
        return jsii.get(self, "value")


class TagManager(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.TagManager"):
    """TagManager facilitates a common implementation of tagging for Constructs."""
    def __init__(self, tag_type: "TagType", resource_type_name: str, tag_structure: typing.Any=None, *, tag_property_name: typing.Optional[str]=None) -> None:
        """
        :param tag_type: -
        :param resource_type_name: -
        :param tag_structure: -
        :param tag_property_name: The name of the property in CloudFormation for these tags. Normally this is ``tags``, but Cognito UserPool uses UserPoolTags Default: "tags"
        """
        options = TagManagerOptions(tag_property_name=tag_property_name)

        jsii.create(TagManager, self, [tag_type, resource_type_name, tag_structure, options])

    @jsii.member(jsii_name="isTaggable")
    @builtins.classmethod
    def is_taggable(cls, construct: typing.Any) -> bool:
        """Check whether the given construct is Taggable.

        :param construct: -
        """
        return jsii.sinvoke(cls, "isTaggable", [construct])

    @jsii.member(jsii_name="applyTagAspectHere")
    def apply_tag_aspect_here(self, include: typing.Optional[typing.List[str]]=None, exclude: typing.Optional[typing.List[str]]=None) -> bool:
        """Determine if the aspect applies here.

        Looks at the include and exclude resourceTypeName arrays to determine if
        the aspect applies here

        :param include: -
        :param exclude: -
        """
        return jsii.invoke(self, "applyTagAspectHere", [include, exclude])

    @jsii.member(jsii_name="hasTags")
    def has_tags(self) -> bool:
        """Returns true if there are any tags defined."""
        return jsii.invoke(self, "hasTags", [])

    @jsii.member(jsii_name="removeTag")
    def remove_tag(self, key: str, priority: jsii.Number) -> None:
        """Removes the specified tag from the array if it exists.

        :param key: The tag to remove.
        :param priority: The priority of the remove operation.
        """
        return jsii.invoke(self, "removeTag", [key, priority])

    @jsii.member(jsii_name="renderTags")
    def render_tags(self) -> typing.Any:
        """Renders tags into the proper format based on TagType."""
        return jsii.invoke(self, "renderTags", [])

    @jsii.member(jsii_name="setTag")
    def set_tag(self, key: str, value: str, priority: typing.Optional[jsii.Number]=None, apply_to_launched_instances: typing.Optional[bool]=None) -> None:
        """Adds the specified tag to the array of tags.

        :param key: -
        :param value: -
        :param priority: -
        :param apply_to_launched_instances: -
        """
        return jsii.invoke(self, "setTag", [key, value, priority, apply_to_launched_instances])

    @builtins.property
    @jsii.member(jsii_name="tagPropertyName")
    def tag_property_name(self) -> str:
        """The property name for tag values.

        Normally this is ``tags`` but some resources choose a different name. Cognito
        UserPool uses UserPoolTags
        """
        return jsii.get(self, "tagPropertyName")


@jsii.data_type(jsii_type="@aws-cdk/core.TagManagerOptions", jsii_struct_bases=[], name_mapping={'tag_property_name': 'tagPropertyName'})
class TagManagerOptions():
    def __init__(self, *, tag_property_name: typing.Optional[str]=None):
        """Options to configure TagManager behavior.

        :param tag_property_name: The name of the property in CloudFormation for these tags. Normally this is ``tags``, but Cognito UserPool uses UserPoolTags Default: "tags"
        """
        self._values = {
        }
        if tag_property_name is not None: self._values["tag_property_name"] = tag_property_name

    @builtins.property
    def tag_property_name(self) -> typing.Optional[str]:
        """The name of the property in CloudFormation for these tags.

        Normally this is ``tags``, but Cognito UserPool uses UserPoolTags

        default
        :default: "tags"
        """
        return self._values.get('tag_property_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TagManagerOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/core.TagProps", jsii_struct_bases=[], name_mapping={'apply_to_launched_instances': 'applyToLaunchedInstances', 'exclude_resource_types': 'excludeResourceTypes', 'include_resource_types': 'includeResourceTypes', 'priority': 'priority'})
class TagProps():
    def __init__(self, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None):
        """Properties for a tag.

        :param apply_to_launched_instances: Whether the tag should be applied to instances in an AutoScalingGroup. Default: true
        :param exclude_resource_types: An array of Resource Types that will not receive this tag. An empty array will allow this tag to be applied to all resources. A non-empty array will apply this tag only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types that will receive this tag. An empty array will match any Resource. A non-empty array will apply this tag only to Resource types that are included in this array. Default: []
        :param priority: Priority of the tag operation. Higher or equal priority tags will take precedence. Setting priority will enable the user to control tags when they need to not follow the default precedence pattern of last applied and closest to the construct in the tree. Default: Default priorities: - 100 for {@link SetTag} - 200 for {@link RemoveTag} - 50 for tags added directly to CloudFormation resources
        """
        self._values = {
        }
        if apply_to_launched_instances is not None: self._values["apply_to_launched_instances"] = apply_to_launched_instances
        if exclude_resource_types is not None: self._values["exclude_resource_types"] = exclude_resource_types
        if include_resource_types is not None: self._values["include_resource_types"] = include_resource_types
        if priority is not None: self._values["priority"] = priority

    @builtins.property
    def apply_to_launched_instances(self) -> typing.Optional[bool]:
        """Whether the tag should be applied to instances in an AutoScalingGroup.

        default
        :default: true
        """
        return self._values.get('apply_to_launched_instances')

    @builtins.property
    def exclude_resource_types(self) -> typing.Optional[typing.List[str]]:
        """An array of Resource Types that will not receive this tag.

        An empty array will allow this tag to be applied to all resources. A
        non-empty array will apply this tag only if the Resource type is not in
        this array.

        default
        :default: []
        """
        return self._values.get('exclude_resource_types')

    @builtins.property
    def include_resource_types(self) -> typing.Optional[typing.List[str]]:
        """An array of Resource Types that will receive this tag.

        An empty array will match any Resource. A non-empty array will apply this
        tag only to Resource types that are included in this array.

        default
        :default: []
        """
        return self._values.get('include_resource_types')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of the tag operation.

        Higher or equal priority tags will take precedence.

        Setting priority will enable the user to control tags when they need to not
        follow the default precedence pattern of last applied and closest to the
        construct in the tree.

        default
        :default:

        Default priorities:

        - 100 for {@link SetTag}
        - 200 for {@link RemoveTag}
        - 50 for tags added directly to CloudFormation resources
        """
        return self._values.get('priority')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TagProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/core.TagType")
class TagType(enum.Enum):
    STANDARD = "STANDARD"
    AUTOSCALING_GROUP = "AUTOSCALING_GROUP"
    MAP = "MAP"
    KEY_VALUE = "KEY_VALUE"
    NOT_TAGGABLE = "NOT_TAGGABLE"

@jsii.data_type(jsii_type="@aws-cdk/core.TimeConversionOptions", jsii_struct_bases=[], name_mapping={'integral': 'integral'})
class TimeConversionOptions():
    def __init__(self, *, integral: typing.Optional[bool]=None):
        """Options for how to convert time to a different unit.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer. Default: true
        """
        self._values = {
        }
        if integral is not None: self._values["integral"] = integral

    @builtins.property
    def integral(self) -> typing.Optional[bool]:
        """If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Mintues``) will fail if the result is not an integer.

        default
        :default: true
        """
        return self._values.get('integral')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TimeConversionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Token(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Token"):
    """Represents a special or lazily-evaluated value.

    Can be used to delay evaluation of a certain value in case, for example,
    that it requires some context or late-bound data. Can also be used to
    mark values that need special processing at document rendering time.

    Tokens can be embedded into strings while retaining their original
    semantics.
    """
    @jsii.member(jsii_name="asAny")
    @builtins.classmethod
    def as_any(cls, value: typing.Any) -> "IResolvable":
        """Return a resolvable representation of the given value.

        :param value: -
        """
        return jsii.sinvoke(cls, "asAny", [value])

    @jsii.member(jsii_name="asList")
    @builtins.classmethod
    def as_list(cls, value: typing.Any, *, display_hint: typing.Optional[str]=None) -> typing.List[str]:
        """Return a reversible list representation of this token.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it.
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asList", [value, options])

    @jsii.member(jsii_name="asNumber")
    @builtins.classmethod
    def as_number(cls, value: typing.Any) -> jsii.Number:
        """Return a reversible number representation of this token.

        :param value: -
        """
        return jsii.sinvoke(cls, "asNumber", [value])

    @jsii.member(jsii_name="asString")
    @builtins.classmethod
    def as_string(cls, value: typing.Any, *, display_hint: typing.Optional[str]=None) -> str:
        """Return a reversible string representation of this token.

        If the Token is initialized with a literal, the stringified value of the
        literal is returned. Otherwise, a special quoted string representation
        of the Token is returned that can be embedded into other strings.

        Strings with quoted Tokens in them can be restored back into
        complex values with the Tokens restored by calling ``resolve()``
        on the string.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it.
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asString", [value, options])

    @jsii.member(jsii_name="isUnresolved")
    @builtins.classmethod
    def is_unresolved(cls, obj: typing.Any) -> bool:
        """Returns true if obj represents an unresolved value.

        One of these must be true:

        - ``obj`` is an IResolvable
        - ``obj`` is a string containing at least one encoded ``IResolvable``
        - ``obj`` is either an encoded number or list

        This does NOT recurse into lists or objects to see if they
        containing resolvables.

        :param obj: The object to test.
        """
        return jsii.sinvoke(cls, "isUnresolved", [obj])


class Tokenization(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.Tokenization"):
    """Less oft-needed functions to manipulate Tokens."""
    @jsii.member(jsii_name="isResolvable")
    @builtins.classmethod
    def is_resolvable(cls, obj: typing.Any) -> bool:
        """Return whether the given object is an IResolvable object.

        This is different from Token.isUnresolved() which will also check for
        encoded Tokens, whereas this method will only do a type check on the given
        object.

        :param obj: -
        """
        return jsii.sinvoke(cls, "isResolvable", [obj])

    @jsii.member(jsii_name="resolve")
    @builtins.classmethod
    def resolve(cls, obj: typing.Any, *, resolver: "ITokenResolver", scope: "IConstruct", preparing: typing.Optional[bool]=None) -> typing.Any:
        """Resolves an object by evaluating all tokens and removing any undefined or empty objects or arrays.

        Values can only be primitives, arrays or tokens. Other objects (i.e. with methods) will be rejected.

        :param obj: The object to resolve.
        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false
        """
        options = ResolveOptions(resolver=resolver, scope=scope, preparing=preparing)

        return jsii.sinvoke(cls, "resolve", [obj, options])

    @jsii.member(jsii_name="reverseList")
    @builtins.classmethod
    def reverse_list(cls, l: typing.List[str]) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a list.

        :param l: -
        """
        return jsii.sinvoke(cls, "reverseList", [l])

    @jsii.member(jsii_name="reverseNumber")
    @builtins.classmethod
    def reverse_number(cls, n: jsii.Number) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a number.

        :param n: -
        """
        return jsii.sinvoke(cls, "reverseNumber", [n])

    @jsii.member(jsii_name="reverseString")
    @builtins.classmethod
    def reverse_string(cls, s: str) -> "TokenizedStringFragments":
        """Un-encode a string potentially containing encoded tokens.

        :param s: -
        """
        return jsii.sinvoke(cls, "reverseString", [s])

    @jsii.member(jsii_name="stringifyNumber")
    @builtins.classmethod
    def stringify_number(cls, x: jsii.Number) -> str:
        """Stringify a number directly or lazily if it's a Token.

        If it is an object (i.e., { Ref: 'SomeLogicalId' }), return it as-is.

        :param x: -
        """
        return jsii.sinvoke(cls, "stringifyNumber", [x])


class TokenizedStringFragments(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.TokenizedStringFragments"):
    """Fragments of a concatenated string containing stringified Tokens."""
    def __init__(self) -> None:
        jsii.create(TokenizedStringFragments, self, [])

    @jsii.member(jsii_name="addIntrinsic")
    def add_intrinsic(self, value: typing.Any) -> None:
        """
        :param value: -
        """
        return jsii.invoke(self, "addIntrinsic", [value])

    @jsii.member(jsii_name="addLiteral")
    def add_literal(self, lit: typing.Any) -> None:
        """
        :param lit: -
        """
        return jsii.invoke(self, "addLiteral", [lit])

    @jsii.member(jsii_name="addToken")
    def add_token(self, token: "IResolvable") -> None:
        """
        :param token: -
        """
        return jsii.invoke(self, "addToken", [token])

    @jsii.member(jsii_name="join")
    def join(self, concat: "IFragmentConcatenator") -> typing.Any:
        """Combine the string fragments using the given joiner.

        If there are any

        :param concat: -
        """
        return jsii.invoke(self, "join", [concat])

    @jsii.member(jsii_name="mapTokens")
    def map_tokens(self, mapper: "ITokenMapper") -> "TokenizedStringFragments":
        """Apply a transformation function to all tokens in the string.

        :param mapper: -
        """
        return jsii.invoke(self, "mapTokens", [mapper])

    @builtins.property
    @jsii.member(jsii_name="firstValue")
    def first_value(self) -> typing.Any:
        return jsii.get(self, "firstValue")

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return jsii.get(self, "length")

    @builtins.property
    @jsii.member(jsii_name="tokens")
    def tokens(self) -> typing.List["IResolvable"]:
        """Return all Tokens from this string."""
        return jsii.get(self, "tokens")

    @builtins.property
    @jsii.member(jsii_name="firstToken")
    def first_token(self) -> typing.Optional["IResolvable"]:
        return jsii.get(self, "firstToken")


class TreeInspector(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.TreeInspector"):
    """Inspector that maintains an attribute bag."""
    def __init__(self) -> None:
        jsii.create(TreeInspector, self, [])

    @jsii.member(jsii_name="addAttribute")
    def add_attribute(self, key: str, value: typing.Any) -> None:
        """Adds attribute to bag.

        Keys should be added by convention to prevent conflicts
        i.e. L1 constructs will contain attributes with keys prefixed with aws:cdk:cloudformation

        :param key: - key for metadata.
        :param value: - value of metadata.
        """
        return jsii.invoke(self, "addAttribute", [key, value])

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[str,typing.Any]:
        """Represents the bag of attributes as key-value pairs."""
        return jsii.get(self, "attributes")


@jsii.data_type(jsii_type="@aws-cdk/core.ValidationError", jsii_struct_bases=[], name_mapping={'message': 'message', 'source': 'source'})
class ValidationError():
    def __init__(self, *, message: str, source: "Construct"):
        """An error returned during the validation phase.

        :param message: The error message.
        :param source: The construct which emitted the error.
        """
        self._values = {
            'message': message,
            'source': source,
        }

    @builtins.property
    def message(self) -> str:
        """The error message."""
        return self._values.get('message')

    @builtins.property
    def source(self) -> "Construct":
        """The construct which emitted the error."""
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ValidationError(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ValidationResult(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.ValidationResult"):
    """Representation of validation results.

    Models a tree of validation errors so that we have as much information as possible
    about the failure that occurred.
    """
    def __init__(self, error_message: typing.Optional[str]=None, results: typing.Optional["ValidationResults"]=None) -> None:
        """
        :param error_message: -
        :param results: -
        """
        jsii.create(ValidationResult, self, [error_message, results])

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        """Turn a failed validation into an exception."""
        return jsii.invoke(self, "assertSuccess", [])

    @jsii.member(jsii_name="errorTree")
    def error_tree(self) -> str:
        """Return a string rendering of the tree of validation failures."""
        return jsii.invoke(self, "errorTree", [])

    @jsii.member(jsii_name="prefix")
    def prefix(self, message: str) -> "ValidationResult":
        """Wrap this result with an error message, if it concerns an error.

        :param message: -
        """
        return jsii.invoke(self, "prefix", [message])

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> str:
        return jsii.get(self, "errorMessage")

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> bool:
        return jsii.get(self, "isSuccess")

    @builtins.property
    @jsii.member(jsii_name="results")
    def results(self) -> "ValidationResults":
        return jsii.get(self, "results")


class ValidationResults(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/core.ValidationResults"):
    """A collection of validation results."""
    def __init__(self, results: typing.Optional[typing.List["ValidationResult"]]=None) -> None:
        """
        :param results: -
        """
        jsii.create(ValidationResults, self, [results])

    @jsii.member(jsii_name="collect")
    def collect(self, result: "ValidationResult") -> None:
        """
        :param result: -
        """
        return jsii.invoke(self, "collect", [result])

    @jsii.member(jsii_name="errorTreeList")
    def error_tree_list(self) -> str:
        return jsii.invoke(self, "errorTreeList", [])

    @jsii.member(jsii_name="wrap")
    def wrap(self, message: str) -> "ValidationResult":
        """Wrap up all validation results into a single tree node.

        If there are failures in the collection, add a message, otherwise
        return a success.

        :param message: -
        """
        return jsii.invoke(self, "wrap", [message])

    @builtins.property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> bool:
        return jsii.get(self, "isSuccess")

    @builtins.property
    @jsii.member(jsii_name="results")
    def results(self) -> typing.List["ValidationResult"]:
        return jsii.get(self, "results")

    @results.setter
    def results(self, value: typing.List["ValidationResult"]):
        jsii.set(self, "results", value)


__all__ = ["App", "AppProps", "Arn", "ArnComponents", "Aws", "CfnAutoScalingReplacingUpdate", "CfnAutoScalingRollingUpdate", "CfnAutoScalingScheduledAction", "CfnCodeDeployLambdaAliasUpdate", "CfnCondition", "CfnConditionProps", "CfnCreationPolicy", "CfnDeletionPolicy", "CfnDynamicReference", "CfnDynamicReferenceProps", "CfnDynamicReferenceService", "CfnElement", "CfnInclude", "CfnIncludeProps", "CfnMapping", "CfnMappingProps", "CfnOutput", "CfnOutputProps", "CfnParameter", "CfnParameterProps", "CfnRefElement", "CfnResource", "CfnResourceAutoScalingCreationPolicy", "CfnResourceProps", "CfnResourceSignal", "CfnRule", "CfnRuleAssertion", "CfnRuleProps", "CfnTag", "CfnUpdatePolicy", "ConcreteDependable", "Construct", "ConstructNode", "ConstructOrder", "ContextProvider", "DefaultTokenResolver", "DependableTrait", "Dependency", "DockerImageAssetLocation", "DockerImageAssetSource", "Duration", "EncodingOptions", "Environment", "FileAssetLocation", "FileAssetPackaging", "FileAssetSource", "Fn", "GetContextKeyOptions", "GetContextKeyResult", "GetContextValueOptions", "GetContextValueResult", "IAnyProducer", "IAspect", "ICfnConditionExpression", "ICfnResourceOptions", "IConstruct", "IDependable", "IFragmentConcatenator", "IInspectable", "IListProducer", "INumberProducer", "IPostProcessor", "IResolvable", "IResolveContext", "IResource", "IStringProducer", "ISynthesisSession", "ITaggable", "ITemplateOptions", "ITokenMapper", "ITokenResolver", "Intrinsic", "Lazy", "LazyAnyValueOptions", "LazyListValueOptions", "LazyStringValueOptions", "PhysicalName", "Reference", "RemovalPolicy", "RemovalPolicyOptions", "RemoveTag", "ResolveOptions", "Resource", "ResourceProps", "ScopedAws", "SecretValue", "SecretsManagerSecretOptions", "Stack", "StackProps", "StringConcat", "SynthesisOptions", "Tag", "TagManager", "TagManagerOptions", "TagProps", "TagType", "TimeConversionOptions", "Token", "Tokenization", "TokenizedStringFragments", "TreeInspector", "ValidationError", "ValidationResult", "ValidationResults", "__jsii_assembly__"]

publication.publish()
