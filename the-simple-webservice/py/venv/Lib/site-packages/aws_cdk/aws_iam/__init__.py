"""
## AWS Identity and Access Management Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Define a role and add permissions to it. This will automatically create and
attach an IAM policy to the role:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
role = Role(self, "MyRole",
    assumed_by=ServicePrincipal("sns.amazonaws.com")
)

role.add_to_policy(PolicyStatement(
    resources=["*"],
    actions=["lambda:InvokeFunction"]
))
```

Define a policy and attach it to groups, users and roles. Note that it is possible to attach
the policy either by calling `xxx.attachInlinePolicy(policy)` or `policy.attachToXxx(xxx)`.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
user = User(self, "MyUser", password=cdk.SecretValue.plain_text("1234"))
group = Group(self, "MyGroup")

policy = Policy(self, "MyPolicy")
policy.attach_to_user(user)
group.attach_inline_policy(policy)
```

Managed policies can be attached using `xxx.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
group = Group(self, "MyGroup")
group.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
```

### Granting permissions to resources

Many of the AWS CDK resources have `grant*` methods that allow you to grant other resources access to that resource. As an example, the following code gives a Lambda function write permissions (Put, Update, Delete) to a DynamoDB table.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn = lambda.Function(...)
table = dynamodb.Table(...)

table.grant_write_data(fn)
```

The more generic `grant` method allows you to give specific permissions to a resource:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn = lambda.Function(...)
table = dynamodb.Table(...)

table.grant(fn, "dynamodb:PutItem")
```

The `grant*` methods accept an `IGrantable` object. This interface is implemented by IAM principlal resources (groups, users and roles) and resources that assume a role such as a Lambda function, EC2 instance or a Codebuild project.

You can find which `grant*` methods exist for a resource in the [AWS CDK API Reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html).

### Roles

Many AWS resources require *Roles* to operate. These Roles define the AWS API
calls an instance or other AWS service is allowed to make.

Creating Roles and populating them with the right permissions *Statements* is
a necessary but tedious part of setting up AWS infrastructure. In order to
help you focus on your business logic, CDK will take care of creating
roles and populating them with least-privilege permissions automatically.

All constructs that require Roles will create one for you if don't specify
one at construction time. Permissions will be added to that role
automatically if you associate the construct with other constructs from the
AWS Construct Library (for example, if you tell an *AWS CodePipeline* to trigger
an *AWS Lambda Function*, the Pipeline's Role will automatically get
`lambda:InvokeFunction` permissions on that particular Lambda Function),
or if you explicitly grant permissions using `grant` functions (see the
previous section).

#### Opting out of automatic permissions management

You may prefer to manage a Role's permissions yourself instead of having the
CDK automatically manage them for you. This may happen in one of the
following cases:

* You don't like the permissions that CDK automatically generates and
  want to substitute your own set.
* The least-permissions policy that the CDK generates is becoming too
  big for IAM to store, and you need to add some wildcards to keep the
  policy size down.

To prevent constructs from updating your Role's policy, pass the object
returned by `myRole.withoutPolicyUpdates()` instead of `myRole` itself.

For example, to have an AWS CodePipeline *not* automatically add the required
permissions to trigger the expected targets, do the following:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com")
)

codepipeline.Pipeline(self, "Pipeline",
    # Give the Pipeline an immutable view of the Role
    role=role.without_policy_updates()
)

# You now have to manage the Role policies yourself
role.add_to_policy(iam.PolicyStatement(
    action=[],
    resource=[]
))
```

#### Using existing roles

If there are Roles in your account that have already been created which you
would like to use in your CDK application, you can use `Role.fromRoleArn` to
import them, as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::123456789012:role/MyExistingRole",
    # Set 'mutable' to 'false' to use the role as-is and prevent adding new
    # policies to it. The default is 'true', which means the role may be
    # modified as part of the deployment.
    mutable=False
)
```

### Configuring an ExternalId

If you need to create Roles that will be assumed by 4rd parties, it is generally a good idea to [require an `ExternalId`
to assume them](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).  Configuring
an `ExternalId` works like this:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
role = iam.Role(self, "MyRole",
    assumed_by=iam.AccountPrincipal("123456789012"),
    external_ids=["SUPPLY-ME"]
)
```

### Principals vs Identities

When we say *Principal*, we mean an entity you grant permissions to. This
entity can be an AWS Service, a Role, or something more abstract such as "all
users in this account" or even "all users in this organization". An
*Identity* is an IAM representing a single IAM entity that can have
a policy attached, one of `Role`, `User`, or `Group`.

### IAM Principals

When defining policy statements as part of an AssumeRole policy or as part of a
resource policy, statements would usually refer to a specific IAM principal
under `Principal`.

IAM principals are modeled as classes that derive from the `iam.PolicyPrincipal`
abstract class. Principal objects include principal type (string) and value
(array of string), optional set of conditions and the action that this principal
requires when it is used in an assume role policy document.

To add a principal to a policy statement you can either use the abstract
`statement.addPrincipal`, one of the concrete `addXxxPrincipal` methods:

* `addAwsPrincipal`, `addArnPrincipal` or `new ArnPrincipal(arn)` for `{ "AWS": arn }`
* `addAwsAccountPrincipal` or `new AccountPrincipal(accountId)` for `{ "AWS": account-arn }`
* `addServicePrincipal` or `new ServicePrincipal(service)` for `{ "Service": service }`
* `addAccountRootPrincipal` or `new AccountRootPrincipal()` for `{ "AWS": { "Ref: "AWS::AccountId" } }`
* `addCanonicalUserPrincipal` or `new CanonicalUserPrincipal(id)` for `{ "CanonicalUser": id }`
* `addFederatedPrincipal` or `new FederatedPrincipal(federated, conditions, assumeAction)` for
  `{ "Federated": arn }` and a set of optional conditions and the assume role action to use.
* `addAnyPrincipal` or `new AnyPrincipal` for `{ "AWS": "*" }`

If multiple principals are added to the policy statement, they will be merged together:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement = PolicyStatement()
statement.add_service_principal("cloudwatch.amazonaws.com")
statement.add_service_principal("ec2.amazonaws.com")
statement.add_arn_principal("arn:aws:boom:boom")
```

Will result in:

```json
{
  "Principal": {
    "Service": [ "cloudwatch.amazonaws.com", "ec2.amazonaws.com" ],
    "AWS": "arn:aws:boom:boom"
  }
}
```

The `CompositePrincipal` class can also be used to define complex principals, for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
role = iam.Role(self, "MyRole",
    assumed_by=iam.CompositePrincipal(
        iam.ServicePrincipal("ec2.amazonaws.com"),
        iam.AccountPrincipal("1818188181818187272"))
)
```

### Features

* Policy name uniqueness is enforced. If two policies by the same name are attached to the same
  principal, the attachment will fail.
* Policy names are not required - the CDK logical ID will be used and ensured to be unique.
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
import aws_cdk.region_info

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iam", "1.23.0", __name__, "aws-iam@1.23.0.jsii.tgz")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccessKey(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnAccessKey"):
    """A CloudFormation ``AWS::IAM::AccessKey``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::AccessKey
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, user_name: str, serial: typing.Optional[jsii.Number]=None, status: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IAM::AccessKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_name: ``AWS::IAM::AccessKey.UserName``.
        :param serial: ``AWS::IAM::AccessKey.Serial``.
        :param status: ``AWS::IAM::AccessKey.Status``.
        """
        props = CfnAccessKeyProps(user_name=user_name, serial=serial, status=status)

        jsii.create(CfnAccessKey, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrSecretAccessKey")
    def attr_secret_access_key(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SecretAccessKey
        """
        return jsii.get(self, "attrSecretAccessKey")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        """``AWS::IAM::AccessKey.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-username
        """
        return jsii.get(self, "userName")

    @user_name.setter
    def user_name(self, value: str):
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="serial")
    def serial(self) -> typing.Optional[jsii.Number]:
        """``AWS::IAM::AccessKey.Serial``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-serial
        """
        return jsii.get(self, "serial")

    @serial.setter
    def serial(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "serial", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[str]:
        """``AWS::IAM::AccessKey.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-status
        """
        return jsii.get(self, "status")

    @status.setter
    def status(self, value: typing.Optional[str]):
        jsii.set(self, "status", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnAccessKeyProps", jsii_struct_bases=[], name_mapping={'user_name': 'userName', 'serial': 'serial', 'status': 'status'})
class CfnAccessKeyProps():
    def __init__(self, *, user_name: str, serial: typing.Optional[jsii.Number]=None, status: typing.Optional[str]=None):
        """Properties for defining a ``AWS::IAM::AccessKey``.

        :param user_name: ``AWS::IAM::AccessKey.UserName``.
        :param serial: ``AWS::IAM::AccessKey.Serial``.
        :param status: ``AWS::IAM::AccessKey.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html
        """
        self._values = {
            'user_name': user_name,
        }
        if serial is not None: self._values["serial"] = serial
        if status is not None: self._values["status"] = status

    @builtins.property
    def user_name(self) -> str:
        """``AWS::IAM::AccessKey.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-username
        """
        return self._values.get('user_name')

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        """``AWS::IAM::AccessKey.Serial``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-serial
        """
        return self._values.get('serial')

    @builtins.property
    def status(self) -> typing.Optional[str]:
        """``AWS::IAM::AccessKey.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-status
        """
        return self._values.get('status')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAccessKeyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnGroup"):
    """A CloudFormation ``AWS::IAM::Group``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::Group
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, group_name: typing.Optional[str]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]=None) -> None:
        """Create a new ``AWS::IAM::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: ``AWS::IAM::Group.GroupName``.
        :param managed_policy_arns: ``AWS::IAM::Group.ManagedPolicyArns``.
        :param path: ``AWS::IAM::Group.Path``.
        :param policies: ``AWS::IAM::Group.Policies``.
        """
        props = CfnGroupProps(group_name=group_name, managed_policy_arns=managed_policy_arns, path=path, policies=policies)

        jsii.create(CfnGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[str]:
        """``AWS::IAM::Group.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-groupname
        """
        return jsii.get(self, "groupName")

    @group_name.setter
    def group_name(self, value: typing.Optional[str]):
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Group.ManagedPolicyArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-managepolicyarns
        """
        return jsii.get(self, "managedPolicyArns")

    @managed_policy_arns.setter
    def managed_policy_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::Group.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-path
        """
        return jsii.get(self, "path")

    @path.setter
    def path(self, value: typing.Optional[str]):
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]:
        """``AWS::IAM::Group.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-policies
        """
        return jsii.get(self, "policies")

    @policies.setter
    def policies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]):
        jsii.set(self, "policies", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnGroup.PolicyProperty", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'policy_name': 'policyName'})
    class PolicyProperty():
        def __init__(self, *, policy_document: typing.Any, policy_name: str):
            """
            :param policy_document: ``CfnGroup.PolicyProperty.PolicyDocument``.
            :param policy_name: ``CfnGroup.PolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            """
            self._values = {
                'policy_document': policy_document,
                'policy_name': policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            """``CfnGroup.PolicyProperty.PolicyDocument``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            """
            return self._values.get('policy_document')

        @builtins.property
        def policy_name(self) -> str:
            """``CfnGroup.PolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            """
            return self._values.get('policy_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnGroupProps", jsii_struct_bases=[], name_mapping={'group_name': 'groupName', 'managed_policy_arns': 'managedPolicyArns', 'path': 'path', 'policies': 'policies'})
class CfnGroupProps():
    def __init__(self, *, group_name: typing.Optional[str]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGroup.PolicyProperty"]]]]]=None):
        """Properties for defining a ``AWS::IAM::Group``.

        :param group_name: ``AWS::IAM::Group.GroupName``.
        :param managed_policy_arns: ``AWS::IAM::Group.ManagedPolicyArns``.
        :param path: ``AWS::IAM::Group.Path``.
        :param policies: ``AWS::IAM::Group.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html
        """
        self._values = {
        }
        if group_name is not None: self._values["group_name"] = group_name
        if managed_policy_arns is not None: self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None: self._values["path"] = path
        if policies is not None: self._values["policies"] = policies

    @builtins.property
    def group_name(self) -> typing.Optional[str]:
        """``AWS::IAM::Group.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-groupname
        """
        return self._values.get('group_name')

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Group.ManagedPolicyArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-managepolicyarns
        """
        return self._values.get('managed_policy_arns')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::Group.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-path
        """
        return self._values.get('path')

    @builtins.property
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGroup.PolicyProperty"]]]]]:
        """``AWS::IAM::Group.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-policies
        """
        return self._values.get('policies')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnInstanceProfile(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnInstanceProfile"):
    """A CloudFormation ``AWS::IAM::InstanceProfile``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::InstanceProfile
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, roles: typing.List[str], instance_profile_name: typing.Optional[str]=None, path: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IAM::InstanceProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param roles: ``AWS::IAM::InstanceProfile.Roles``.
        :param instance_profile_name: ``AWS::IAM::InstanceProfile.InstanceProfileName``.
        :param path: ``AWS::IAM::InstanceProfile.Path``.
        """
        props = CfnInstanceProfileProps(roles=roles, instance_profile_name=instance_profile_name, path=path)

        jsii.create(CfnInstanceProfile, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[str]:
        """``AWS::IAM::InstanceProfile.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        """
        return jsii.get(self, "roles")

    @roles.setter
    def roles(self, value: typing.List[str]):
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="instanceProfileName")
    def instance_profile_name(self) -> typing.Optional[str]:
        """``AWS::IAM::InstanceProfile.InstanceProfileName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        """
        return jsii.get(self, "instanceProfileName")

    @instance_profile_name.setter
    def instance_profile_name(self, value: typing.Optional[str]):
        jsii.set(self, "instanceProfileName", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::InstanceProfile.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        """
        return jsii.get(self, "path")

    @path.setter
    def path(self, value: typing.Optional[str]):
        jsii.set(self, "path", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnInstanceProfileProps", jsii_struct_bases=[], name_mapping={'roles': 'roles', 'instance_profile_name': 'instanceProfileName', 'path': 'path'})
class CfnInstanceProfileProps():
    def __init__(self, *, roles: typing.List[str], instance_profile_name: typing.Optional[str]=None, path: typing.Optional[str]=None):
        """Properties for defining a ``AWS::IAM::InstanceProfile``.

        :param roles: ``AWS::IAM::InstanceProfile.Roles``.
        :param instance_profile_name: ``AWS::IAM::InstanceProfile.InstanceProfileName``.
        :param path: ``AWS::IAM::InstanceProfile.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
        """
        self._values = {
            'roles': roles,
        }
        if instance_profile_name is not None: self._values["instance_profile_name"] = instance_profile_name
        if path is not None: self._values["path"] = path

    @builtins.property
    def roles(self) -> typing.List[str]:
        """``AWS::IAM::InstanceProfile.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        """
        return self._values.get('roles')

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[str]:
        """``AWS::IAM::InstanceProfile.InstanceProfileName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        """
        return self._values.get('instance_profile_name')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::InstanceProfile.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        """
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnInstanceProfileProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnManagedPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnManagedPolicy"):
    """A CloudFormation ``AWS::IAM::ManagedPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::ManagedPolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_document: typing.Any, description: typing.Optional[str]=None, groups: typing.Optional[typing.List[str]]=None, managed_policy_name: typing.Optional[str]=None, path: typing.Optional[str]=None, roles: typing.Optional[typing.List[str]]=None, users: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::IAM::ManagedPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: ``AWS::IAM::ManagedPolicy.PolicyDocument``.
        :param description: ``AWS::IAM::ManagedPolicy.Description``.
        :param groups: ``AWS::IAM::ManagedPolicy.Groups``.
        :param managed_policy_name: ``AWS::IAM::ManagedPolicy.ManagedPolicyName``.
        :param path: ``AWS::IAM::ManagedPolicy.Path``.
        :param roles: ``AWS::IAM::ManagedPolicy.Roles``.
        :param users: ``AWS::IAM::ManagedPolicy.Users``.
        """
        props = CfnManagedPolicyProps(policy_document=policy_document, description=description, groups=groups, managed_policy_name=managed_policy_name, path=path, roles=roles, users=users)

        jsii.create(CfnManagedPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        """``AWS::IAM::ManagedPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter
    def policy_document(self, value: typing.Any):
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::IAM::ManagedPolicy.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::ManagedPolicy.Groups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        """
        return jsii.get(self, "groups")

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> typing.Optional[str]:
        """``AWS::IAM::ManagedPolicy.ManagedPolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        """
        return jsii.get(self, "managedPolicyName")

    @managed_policy_name.setter
    def managed_policy_name(self, value: typing.Optional[str]):
        jsii.set(self, "managedPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::ManagedPolicy.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-ec2-dhcpoptions-path
        """
        return jsii.get(self, "path")

    @path.setter
    def path(self, value: typing.Optional[str]):
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::ManagedPolicy.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        """
        return jsii.get(self, "roles")

    @roles.setter
    def roles(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::ManagedPolicy.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        """
        return jsii.get(self, "users")

    @users.setter
    def users(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "users", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnManagedPolicyProps", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'description': 'description', 'groups': 'groups', 'managed_policy_name': 'managedPolicyName', 'path': 'path', 'roles': 'roles', 'users': 'users'})
class CfnManagedPolicyProps():
    def __init__(self, *, policy_document: typing.Any, description: typing.Optional[str]=None, groups: typing.Optional[typing.List[str]]=None, managed_policy_name: typing.Optional[str]=None, path: typing.Optional[str]=None, roles: typing.Optional[typing.List[str]]=None, users: typing.Optional[typing.List[str]]=None):
        """Properties for defining a ``AWS::IAM::ManagedPolicy``.

        :param policy_document: ``AWS::IAM::ManagedPolicy.PolicyDocument``.
        :param description: ``AWS::IAM::ManagedPolicy.Description``.
        :param groups: ``AWS::IAM::ManagedPolicy.Groups``.
        :param managed_policy_name: ``AWS::IAM::ManagedPolicy.ManagedPolicyName``.
        :param path: ``AWS::IAM::ManagedPolicy.Path``.
        :param roles: ``AWS::IAM::ManagedPolicy.Roles``.
        :param users: ``AWS::IAM::ManagedPolicy.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
        """
        self._values = {
            'policy_document': policy_document,
        }
        if description is not None: self._values["description"] = description
        if groups is not None: self._values["groups"] = groups
        if managed_policy_name is not None: self._values["managed_policy_name"] = managed_policy_name
        if path is not None: self._values["path"] = path
        if roles is not None: self._values["roles"] = roles
        if users is not None: self._values["users"] = users

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::IAM::ManagedPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        """
        return self._values.get('policy_document')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::IAM::ManagedPolicy.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        """
        return self._values.get('description')

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::ManagedPolicy.Groups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        """
        return self._values.get('groups')

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[str]:
        """``AWS::IAM::ManagedPolicy.ManagedPolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        """
        return self._values.get('managed_policy_name')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::ManagedPolicy.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-ec2-dhcpoptions-path
        """
        return self._values.get('path')

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::ManagedPolicy.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        """
        return self._values.get('roles')

    @builtins.property
    def users(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::ManagedPolicy.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        """
        return self._values.get('users')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnManagedPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnPolicy"):
    """A CloudFormation ``AWS::IAM::Policy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::Policy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_document: typing.Any, policy_name: str, groups: typing.Optional[typing.List[str]]=None, roles: typing.Optional[typing.List[str]]=None, users: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::IAM::Policy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: ``AWS::IAM::Policy.PolicyDocument``.
        :param policy_name: ``AWS::IAM::Policy.PolicyName``.
        :param groups: ``AWS::IAM::Policy.Groups``.
        :param roles: ``AWS::IAM::Policy.Roles``.
        :param users: ``AWS::IAM::Policy.Users``.
        """
        props = CfnPolicyProps(policy_document=policy_document, policy_name=policy_name, groups=groups, roles=roles, users=users)

        jsii.create(CfnPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        """``AWS::IAM::Policy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter
    def policy_document(self, value: typing.Any):
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        """``AWS::IAM::Policy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        """
        return jsii.get(self, "policyName")

    @policy_name.setter
    def policy_name(self, value: str):
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Policy.Groups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        """
        return jsii.get(self, "groups")

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Policy.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        """
        return jsii.get(self, "roles")

    @roles.setter
    def roles(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Policy.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        """
        return jsii.get(self, "users")

    @users.setter
    def users(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "users", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnPolicyProps", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'policy_name': 'policyName', 'groups': 'groups', 'roles': 'roles', 'users': 'users'})
class CfnPolicyProps():
    def __init__(self, *, policy_document: typing.Any, policy_name: str, groups: typing.Optional[typing.List[str]]=None, roles: typing.Optional[typing.List[str]]=None, users: typing.Optional[typing.List[str]]=None):
        """Properties for defining a ``AWS::IAM::Policy``.

        :param policy_document: ``AWS::IAM::Policy.PolicyDocument``.
        :param policy_name: ``AWS::IAM::Policy.PolicyName``.
        :param groups: ``AWS::IAM::Policy.Groups``.
        :param roles: ``AWS::IAM::Policy.Roles``.
        :param users: ``AWS::IAM::Policy.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
        """
        self._values = {
            'policy_document': policy_document,
            'policy_name': policy_name,
        }
        if groups is not None: self._values["groups"] = groups
        if roles is not None: self._values["roles"] = roles
        if users is not None: self._values["users"] = users

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::IAM::Policy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        """
        return self._values.get('policy_document')

    @builtins.property
    def policy_name(self) -> str:
        """``AWS::IAM::Policy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        """
        return self._values.get('policy_name')

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Policy.Groups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        """
        return self._values.get('groups')

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Policy.Roles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        """
        return self._values.get('roles')

    @builtins.property
    def users(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Policy.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        """
        return self._values.get('users')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRole(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnRole"):
    """A CloudFormation ``AWS::IAM::Role``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::Role
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assume_role_policy_document: typing.Any, description: typing.Optional[str]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, max_session_duration: typing.Optional[jsii.Number]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]=None, role_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::IAM::Role``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assume_role_policy_document: ``AWS::IAM::Role.AssumeRolePolicyDocument``.
        :param description: ``AWS::IAM::Role.Description``.
        :param managed_policy_arns: ``AWS::IAM::Role.ManagedPolicyArns``.
        :param max_session_duration: ``AWS::IAM::Role.MaxSessionDuration``.
        :param path: ``AWS::IAM::Role.Path``.
        :param permissions_boundary: ``AWS::IAM::Role.PermissionsBoundary``.
        :param policies: ``AWS::IAM::Role.Policies``.
        :param role_name: ``AWS::IAM::Role.RoleName``.
        :param tags: ``AWS::IAM::Role.Tags``.
        """
        props = CfnRoleProps(assume_role_policy_document=assume_role_policy_document, description=description, managed_policy_arns=managed_policy_arns, max_session_duration=max_session_duration, path=path, permissions_boundary=permissions_boundary, policies=policies, role_name=role_name, tags=tags)

        jsii.create(CfnRole, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrRoleId")
    def attr_role_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RoleId
        """
        return jsii.get(self, "attrRoleId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::IAM::Role.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicyDocument")
    def assume_role_policy_document(self) -> typing.Any:
        """``AWS::IAM::Role.AssumeRolePolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        """
        return jsii.get(self, "assumeRolePolicyDocument")

    @assume_role_policy_document.setter
    def assume_role_policy_document(self, value: typing.Any):
        jsii.set(self, "assumeRolePolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Role.ManagedPolicyArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managepolicyarns
        """
        return jsii.get(self, "managedPolicyArns")

    @managed_policy_arns.setter
    def managed_policy_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="maxSessionDuration")
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        """``AWS::IAM::Role.MaxSessionDuration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        """
        return jsii.get(self, "maxSessionDuration")

    @max_session_duration.setter
    def max_session_duration(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "maxSessionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        """
        return jsii.get(self, "path")

    @path.setter
    def path(self, value: typing.Optional[str]):
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.PermissionsBoundary``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        """
        return jsii.get(self, "permissionsBoundary")

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[str]):
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]:
        """``AWS::IAM::Role.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        """
        return jsii.get(self, "policies")

    @policies.setter
    def policies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]):
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.RoleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        """
        return jsii.get(self, "roleName")

    @role_name.setter
    def role_name(self, value: typing.Optional[str]):
        jsii.set(self, "roleName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnRole.PolicyProperty", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'policy_name': 'policyName'})
    class PolicyProperty():
        def __init__(self, *, policy_document: typing.Any, policy_name: str):
            """
            :param policy_document: ``CfnRole.PolicyProperty.PolicyDocument``.
            :param policy_name: ``CfnRole.PolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            """
            self._values = {
                'policy_document': policy_document,
                'policy_name': policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            """``CfnRole.PolicyProperty.PolicyDocument``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            """
            return self._values.get('policy_document')

        @builtins.property
        def policy_name(self) -> str:
            """``CfnRole.PolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            """
            return self._values.get('policy_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnRoleProps", jsii_struct_bases=[], name_mapping={'assume_role_policy_document': 'assumeRolePolicyDocument', 'description': 'description', 'managed_policy_arns': 'managedPolicyArns', 'max_session_duration': 'maxSessionDuration', 'path': 'path', 'permissions_boundary': 'permissionsBoundary', 'policies': 'policies', 'role_name': 'roleName', 'tags': 'tags'})
class CfnRoleProps():
    def __init__(self, *, assume_role_policy_document: typing.Any, description: typing.Optional[str]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, max_session_duration: typing.Optional[jsii.Number]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRole.PolicyProperty"]]]]]=None, role_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::IAM::Role``.

        :param assume_role_policy_document: ``AWS::IAM::Role.AssumeRolePolicyDocument``.
        :param description: ``AWS::IAM::Role.Description``.
        :param managed_policy_arns: ``AWS::IAM::Role.ManagedPolicyArns``.
        :param max_session_duration: ``AWS::IAM::Role.MaxSessionDuration``.
        :param path: ``AWS::IAM::Role.Path``.
        :param permissions_boundary: ``AWS::IAM::Role.PermissionsBoundary``.
        :param policies: ``AWS::IAM::Role.Policies``.
        :param role_name: ``AWS::IAM::Role.RoleName``.
        :param tags: ``AWS::IAM::Role.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
        """
        self._values = {
            'assume_role_policy_document': assume_role_policy_document,
        }
        if description is not None: self._values["description"] = description
        if managed_policy_arns is not None: self._values["managed_policy_arns"] = managed_policy_arns
        if max_session_duration is not None: self._values["max_session_duration"] = max_session_duration
        if path is not None: self._values["path"] = path
        if permissions_boundary is not None: self._values["permissions_boundary"] = permissions_boundary
        if policies is not None: self._values["policies"] = policies
        if role_name is not None: self._values["role_name"] = role_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        """``AWS::IAM::Role.AssumeRolePolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        """
        return self._values.get('assume_role_policy_document')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        """
        return self._values.get('description')

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::Role.ManagedPolicyArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managepolicyarns
        """
        return self._values.get('managed_policy_arns')

    @builtins.property
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        """``AWS::IAM::Role.MaxSessionDuration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        """
        return self._values.get('max_session_duration')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        """
        return self._values.get('path')

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.PermissionsBoundary``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        """
        return self._values.get('permissions_boundary')

    @builtins.property
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRole.PolicyProperty"]]]]]:
        """``AWS::IAM::Role.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        """
        return self._values.get('policies')

    @builtins.property
    def role_name(self) -> typing.Optional[str]:
        """``AWS::IAM::Role.RoleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        """
        return self._values.get('role_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::IAM::Role.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRoleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnServiceLinkedRole(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnServiceLinkedRole"):
    """A CloudFormation ``AWS::IAM::ServiceLinkedRole``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::ServiceLinkedRole
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, aws_service_name: str, custom_suffix: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IAM::ServiceLinkedRole``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param aws_service_name: ``AWS::IAM::ServiceLinkedRole.AWSServiceName``.
        :param custom_suffix: ``AWS::IAM::ServiceLinkedRole.CustomSuffix``.
        :param description: ``AWS::IAM::ServiceLinkedRole.Description``.
        """
        props = CfnServiceLinkedRoleProps(aws_service_name=aws_service_name, custom_suffix=custom_suffix, description=description)

        jsii.create(CfnServiceLinkedRole, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="awsServiceName")
    def aws_service_name(self) -> str:
        """``AWS::IAM::ServiceLinkedRole.AWSServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        """
        return jsii.get(self, "awsServiceName")

    @aws_service_name.setter
    def aws_service_name(self, value: str):
        jsii.set(self, "awsServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="customSuffix")
    def custom_suffix(self) -> typing.Optional[str]:
        """``AWS::IAM::ServiceLinkedRole.CustomSuffix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        """
        return jsii.get(self, "customSuffix")

    @custom_suffix.setter
    def custom_suffix(self, value: typing.Optional[str]):
        jsii.set(self, "customSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::IAM::ServiceLinkedRole.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnServiceLinkedRoleProps", jsii_struct_bases=[], name_mapping={'aws_service_name': 'awsServiceName', 'custom_suffix': 'customSuffix', 'description': 'description'})
class CfnServiceLinkedRoleProps():
    def __init__(self, *, aws_service_name: str, custom_suffix: typing.Optional[str]=None, description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::IAM::ServiceLinkedRole``.

        :param aws_service_name: ``AWS::IAM::ServiceLinkedRole.AWSServiceName``.
        :param custom_suffix: ``AWS::IAM::ServiceLinkedRole.CustomSuffix``.
        :param description: ``AWS::IAM::ServiceLinkedRole.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
        """
        self._values = {
            'aws_service_name': aws_service_name,
        }
        if custom_suffix is not None: self._values["custom_suffix"] = custom_suffix
        if description is not None: self._values["description"] = description

    @builtins.property
    def aws_service_name(self) -> str:
        """``AWS::IAM::ServiceLinkedRole.AWSServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        """
        return self._values.get('aws_service_name')

    @builtins.property
    def custom_suffix(self) -> typing.Optional[str]:
        """``AWS::IAM::ServiceLinkedRole.CustomSuffix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        """
        return self._values.get('custom_suffix')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::IAM::ServiceLinkedRole.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnServiceLinkedRoleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUser(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnUser"):
    """A CloudFormation ``AWS::IAM::User``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::User
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, groups: typing.Optional[typing.List[str]]=None, login_profile: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoginProfileProperty"]]]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, user_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IAM::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param groups: ``AWS::IAM::User.Groups``.
        :param login_profile: ``AWS::IAM::User.LoginProfile``.
        :param managed_policy_arns: ``AWS::IAM::User.ManagedPolicyArns``.
        :param path: ``AWS::IAM::User.Path``.
        :param permissions_boundary: ``AWS::IAM::User.PermissionsBoundary``.
        :param policies: ``AWS::IAM::User.Policies``.
        :param tags: ``AWS::IAM::User.Tags``.
        :param user_name: ``AWS::IAM::User.UserName``.
        """
        props = CfnUserProps(groups=groups, login_profile=login_profile, managed_policy_arns=managed_policy_arns, path=path, permissions_boundary=permissions_boundary, policies=policies, tags=tags, user_name=user_name)

        jsii.create(CfnUser, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::IAM::User.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::User.Groups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-groups
        """
        return jsii.get(self, "groups")

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="loginProfile")
    def login_profile(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoginProfileProperty"]]]:
        """``AWS::IAM::User.LoginProfile``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-loginprofile
        """
        return jsii.get(self, "loginProfile")

    @login_profile.setter
    def login_profile(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoginProfileProperty"]]]):
        jsii.set(self, "loginProfile", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::User.ManagedPolicyArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-managepolicyarns
        """
        return jsii.get(self, "managedPolicyArns")

    @managed_policy_arns.setter
    def managed_policy_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::User.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-path
        """
        return jsii.get(self, "path")

    @path.setter
    def path(self, value: typing.Optional[str]):
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[str]:
        """``AWS::IAM::User.PermissionsBoundary``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-permissionsboundary
        """
        return jsii.get(self, "permissionsBoundary")

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[str]):
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]:
        """``AWS::IAM::User.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-policies
        """
        return jsii.get(self, "policies")

    @policies.setter
    def policies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PolicyProperty"]]]]]):
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> typing.Optional[str]:
        """``AWS::IAM::User.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-username
        """
        return jsii.get(self, "userName")

    @user_name.setter
    def user_name(self, value: typing.Optional[str]):
        jsii.set(self, "userName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUser.LoginProfileProperty", jsii_struct_bases=[], name_mapping={'password': 'password', 'password_reset_required': 'passwordResetRequired'})
    class LoginProfileProperty():
        def __init__(self, *, password: str, password_reset_required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param password: ``CfnUser.LoginProfileProperty.Password``.
            :param password_reset_required: ``CfnUser.LoginProfileProperty.PasswordResetRequired``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html
            """
            self._values = {
                'password': password,
            }
            if password_reset_required is not None: self._values["password_reset_required"] = password_reset_required

        @builtins.property
        def password(self) -> str:
            """``CfnUser.LoginProfileProperty.Password``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-password
            """
            return self._values.get('password')

        @builtins.property
        def password_reset_required(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnUser.LoginProfileProperty.PasswordResetRequired``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-passwordresetrequired
            """
            return self._values.get('password_reset_required')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoginProfileProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUser.PolicyProperty", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'policy_name': 'policyName'})
    class PolicyProperty():
        def __init__(self, *, policy_document: typing.Any, policy_name: str):
            """
            :param policy_document: ``CfnUser.PolicyProperty.PolicyDocument``.
            :param policy_name: ``CfnUser.PolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            """
            self._values = {
                'policy_document': policy_document,
                'policy_name': policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            """``CfnUser.PolicyProperty.PolicyDocument``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            """
            return self._values.get('policy_document')

        @builtins.property
        def policy_name(self) -> str:
            """``CfnUser.PolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            """
            return self._values.get('policy_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUserProps", jsii_struct_bases=[], name_mapping={'groups': 'groups', 'login_profile': 'loginProfile', 'managed_policy_arns': 'managedPolicyArns', 'path': 'path', 'permissions_boundary': 'permissionsBoundary', 'policies': 'policies', 'tags': 'tags', 'user_name': 'userName'})
class CfnUserProps():
    def __init__(self, *, groups: typing.Optional[typing.List[str]]=None, login_profile: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUser.LoginProfileProperty"]]]=None, managed_policy_arns: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUser.PolicyProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, user_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::IAM::User``.

        :param groups: ``AWS::IAM::User.Groups``.
        :param login_profile: ``AWS::IAM::User.LoginProfile``.
        :param managed_policy_arns: ``AWS::IAM::User.ManagedPolicyArns``.
        :param path: ``AWS::IAM::User.Path``.
        :param permissions_boundary: ``AWS::IAM::User.PermissionsBoundary``.
        :param policies: ``AWS::IAM::User.Policies``.
        :param tags: ``AWS::IAM::User.Tags``.
        :param user_name: ``AWS::IAM::User.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html
        """
        self._values = {
        }
        if groups is not None: self._values["groups"] = groups
        if login_profile is not None: self._values["login_profile"] = login_profile
        if managed_policy_arns is not None: self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None: self._values["path"] = path
        if permissions_boundary is not None: self._values["permissions_boundary"] = permissions_boundary
        if policies is not None: self._values["policies"] = policies
        if tags is not None: self._values["tags"] = tags
        if user_name is not None: self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::User.Groups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-groups
        """
        return self._values.get('groups')

    @builtins.property
    def login_profile(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUser.LoginProfileProperty"]]]:
        """``AWS::IAM::User.LoginProfile``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-loginprofile
        """
        return self._values.get('login_profile')

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::IAM::User.ManagedPolicyArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-managepolicyarns
        """
        return self._values.get('managed_policy_arns')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """``AWS::IAM::User.Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-path
        """
        return self._values.get('path')

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[str]:
        """``AWS::IAM::User.PermissionsBoundary``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-permissionsboundary
        """
        return self._values.get('permissions_boundary')

    @builtins.property
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUser.PolicyProperty"]]]]]:
        """``AWS::IAM::User.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-policies
        """
        return self._values.get('policies')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::IAM::User.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-tags
        """
        return self._values.get('tags')

    @builtins.property
    def user_name(self) -> typing.Optional[str]:
        """``AWS::IAM::User.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-username
        """
        return self._values.get('user_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserToGroupAddition(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CfnUserToGroupAddition"):
    """A CloudFormation ``AWS::IAM::UserToGroupAddition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::IAM::UserToGroupAddition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, group_name: str, users: typing.List[str]) -> None:
        """Create a new ``AWS::IAM::UserToGroupAddition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: ``AWS::IAM::UserToGroupAddition.GroupName``.
        :param users: ``AWS::IAM::UserToGroupAddition.Users``.
        """
        props = CfnUserToGroupAdditionProps(group_name=group_name, users=users)

        jsii.create(CfnUserToGroupAddition, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        """``AWS::IAM::UserToGroupAddition.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-groupname
        """
        return jsii.get(self, "groupName")

    @group_name.setter
    def group_name(self, value: str):
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[str]:
        """``AWS::IAM::UserToGroupAddition.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-users
        """
        return jsii.get(self, "users")

    @users.setter
    def users(self, value: typing.List[str]):
        jsii.set(self, "users", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CfnUserToGroupAdditionProps", jsii_struct_bases=[], name_mapping={'group_name': 'groupName', 'users': 'users'})
class CfnUserToGroupAdditionProps():
    def __init__(self, *, group_name: str, users: typing.List[str]):
        """Properties for defining a ``AWS::IAM::UserToGroupAddition``.

        :param group_name: ``AWS::IAM::UserToGroupAddition.GroupName``.
        :param users: ``AWS::IAM::UserToGroupAddition.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html
        """
        self._values = {
            'group_name': group_name,
            'users': users,
        }

    @builtins.property
    def group_name(self) -> str:
        """``AWS::IAM::UserToGroupAddition.GroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-groupname
        """
        return self._values.get('group_name')

    @builtins.property
    def users(self) -> typing.List[str]:
        """``AWS::IAM::UserToGroupAddition.Users``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-users
        """
        return self._values.get('users')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserToGroupAdditionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.CommonGrantOptions", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'grantee': 'grantee', 'resource_arns': 'resourceArns'})
class CommonGrantOptions():
    def __init__(self, *, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]):
        """Basic options for a grant operation.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.

        stability
        :stability: experimental
        """
        self._values = {
            'actions': actions,
            'grantee': grantee,
            'resource_arns': resource_arns,
        }

    @builtins.property
    def actions(self) -> typing.List[str]:
        """The actions to grant.

        stability
        :stability: experimental
        """
        return self._values.get('actions')

    @builtins.property
    def grantee(self) -> "IGrantable":
        """The principal to grant to.

        default
        :default: if principal is undefined, no work is done.

        stability
        :stability: experimental
        """
        return self._values.get('grantee')

    @builtins.property
    def resource_arns(self) -> typing.List[str]:
        """The resource ARNs to grant to.

        stability
        :stability: experimental
        """
        return self._values.get('resource_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonGrantOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-iam.Effect")
class Effect(enum.Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

@jsii.data_type(jsii_type="@aws-cdk/aws-iam.FromRoleArnOptions", jsii_struct_bases=[], name_mapping={'mutable': 'mutable'})
class FromRoleArnOptions():
    def __init__(self, *, mutable: typing.Optional[bool]=None):
        """Options allowing customizing the behavior of {@link Role.fromRoleArn}.

        :param mutable: Whether the imported role can be modified by attaching policy resources to it. Default: true
        """
        self._values = {
        }
        if mutable is not None: self._values["mutable"] = mutable

    @builtins.property
    def mutable(self) -> typing.Optional[bool]:
        """Whether the imported role can be modified by attaching policy resources to it.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('mutable')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FromRoleArnOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Grant(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Grant"):
    """Result of a grant() operation.

    This class is not instantiable by consumers on purpose, so that they will be
    required to call the Grant factory functions.
    """
    @jsii.member(jsii_name="addToPrincipal")
    @builtins.classmethod
    def add_to_principal(cls, *, scope: typing.Optional[aws_cdk.core.IConstruct]=None, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]) -> "Grant":
        """Try to grant the given permissions to the given principal.

        Absence of a principal leads to a warning, but failing to add
        the permissions to a present principal is not an error.

        :param scope: Construct to report warnings on in case grant could not be registered.
        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        """
        options = GrantOnPrincipalOptions(scope=scope, actions=actions, grantee=grantee, resource_arns=resource_arns)

        return jsii.sinvoke(cls, "addToPrincipal", [options])

    @jsii.member(jsii_name="addToPrincipalAndResource")
    @builtins.classmethod
    def add_to_principal_and_resource(cls, *, resource: "IResourceWithPolicy", resource_policy_principal: typing.Optional["IPrincipal"]=None, resource_self_arns: typing.Optional[typing.List[str]]=None, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]) -> "Grant":
        """Add a grant both on the principal and on the resource.

        As long as any principal is given, granting on the pricipal may fail (in
        case of a non-identity principal), but granting on the resource will
        never fail.

        Statement will be the resource statement.

        :param resource: The resource with a resource policy. The statement will always be added to the resource policy.
        :param resource_policy_principal: The principal to use in the statement for the resource policy. Default: - the principal of the grantee will be used
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs
        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        """
        options = GrantOnPrincipalAndResourceOptions(resource=resource, resource_policy_principal=resource_policy_principal, resource_self_arns=resource_self_arns, actions=actions, grantee=grantee, resource_arns=resource_arns)

        return jsii.sinvoke(cls, "addToPrincipalAndResource", [options])

    @jsii.member(jsii_name="addToPrincipalOrResource")
    @builtins.classmethod
    def add_to_principal_or_resource(cls, *, resource: "IResourceWithPolicy", resource_self_arns: typing.Optional[typing.List[str]]=None, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str]) -> "Grant":
        """Grant the given permissions to the principal.

        The permissions will be added to the principal policy primarily, falling
        back to the resource policy if necessary. The permissions must be granted
        somewhere.

        - Trying to grant permissions to a principal that does not admit adding to
          the principal policy while not providing a resource with a resource policy
          is an error.
        - Trying to grant permissions to an absent principal (possible in the
          case of imported resources) leads to a warning being added to the
          resource construct.

        :param resource: The resource with a resource policy. The statement will be added to the resource policy if it couldn't be added to the principal policy.
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs
        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        """
        options = GrantWithResourceOptions(resource=resource, resource_self_arns=resource_self_arns, actions=actions, grantee=grantee, resource_arns=resource_arns)

        return jsii.sinvoke(cls, "addToPrincipalOrResource", [options])

    @jsii.member(jsii_name="drop")
    @builtins.classmethod
    def drop(cls, grantee: "IGrantable", _intent: str) -> "Grant":
        """Returns a "no-op" ``Grant`` object which represents a "dropped grant".

        This can be used for e.g. imported resources where you may not be able to modify
        the resource's policy or some underlying policy which you don't know about.

        :param grantee: The intended grantee.
        :param _intent: The user's intent (will be ignored at the moment).
        """
        return jsii.sinvoke(cls, "drop", [grantee, _intent])

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        """Throw an error if this grant wasn't successful."""
        return jsii.invoke(self, "assertSuccess", [])

    @builtins.property
    @jsii.member(jsii_name="success")
    def success(self) -> bool:
        """Whether the grant operation was successful."""
        return jsii.get(self, "success")

    @builtins.property
    @jsii.member(jsii_name="principalStatement")
    def principal_statement(self) -> typing.Optional["PolicyStatement"]:
        """The statement that was added to the principal's policy.

        Can be accessed to (e.g.) add additional conditions to the statement.
        """
        return jsii.get(self, "principalStatement")

    @builtins.property
    @jsii.member(jsii_name="resourceStatement")
    def resource_statement(self) -> typing.Optional["PolicyStatement"]:
        """The statement that was added to the resource policy.

        Can be accessed to (e.g.) add additional conditions to the statement.
        """
        return jsii.get(self, "resourceStatement")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GrantOnPrincipalAndResourceOptions", jsii_struct_bases=[CommonGrantOptions], name_mapping={'actions': 'actions', 'grantee': 'grantee', 'resource_arns': 'resourceArns', 'resource': 'resource', 'resource_policy_principal': 'resourcePolicyPrincipal', 'resource_self_arns': 'resourceSelfArns'})
class GrantOnPrincipalAndResourceOptions(CommonGrantOptions):
    def __init__(self, *, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str], resource: "IResourceWithPolicy", resource_policy_principal: typing.Optional["IPrincipal"]=None, resource_self_arns: typing.Optional[typing.List[str]]=None):
        """Options for a grant operation to both identity and resource.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        :param resource: The resource with a resource policy. The statement will always be added to the resource policy.
        :param resource_policy_principal: The principal to use in the statement for the resource policy. Default: - the principal of the grantee will be used
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs

        stability
        :stability: experimental
        """
        self._values = {
            'actions': actions,
            'grantee': grantee,
            'resource_arns': resource_arns,
            'resource': resource,
        }
        if resource_policy_principal is not None: self._values["resource_policy_principal"] = resource_policy_principal
        if resource_self_arns is not None: self._values["resource_self_arns"] = resource_self_arns

    @builtins.property
    def actions(self) -> typing.List[str]:
        """The actions to grant.

        stability
        :stability: experimental
        """
        return self._values.get('actions')

    @builtins.property
    def grantee(self) -> "IGrantable":
        """The principal to grant to.

        default
        :default: if principal is undefined, no work is done.

        stability
        :stability: experimental
        """
        return self._values.get('grantee')

    @builtins.property
    def resource_arns(self) -> typing.List[str]:
        """The resource ARNs to grant to.

        stability
        :stability: experimental
        """
        return self._values.get('resource_arns')

    @builtins.property
    def resource(self) -> "IResourceWithPolicy":
        """The resource with a resource policy.

        The statement will always be added to the resource policy.

        stability
        :stability: experimental
        """
        return self._values.get('resource')

    @builtins.property
    def resource_policy_principal(self) -> typing.Optional["IPrincipal"]:
        """The principal to use in the statement for the resource policy.

        default
        :default: - the principal of the grantee will be used

        stability
        :stability: experimental
        """
        return self._values.get('resource_policy_principal')

    @builtins.property
    def resource_self_arns(self) -> typing.Optional[typing.List[str]]:
        """When referring to the resource in a resource policy, use this as ARN.

        (Depending on the resource type, this needs to be '*' in a resource policy).

        default
        :default: Same as regular resource ARNs

        stability
        :stability: experimental
        """
        return self._values.get('resource_self_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GrantOnPrincipalAndResourceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GrantOnPrincipalOptions", jsii_struct_bases=[CommonGrantOptions], name_mapping={'actions': 'actions', 'grantee': 'grantee', 'resource_arns': 'resourceArns', 'scope': 'scope'})
class GrantOnPrincipalOptions(CommonGrantOptions):
    def __init__(self, *, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str], scope: typing.Optional[aws_cdk.core.IConstruct]=None):
        """Options for a grant operation that only applies to principals.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        :param scope: Construct to report warnings on in case grant could not be registered.

        stability
        :stability: experimental
        """
        self._values = {
            'actions': actions,
            'grantee': grantee,
            'resource_arns': resource_arns,
        }
        if scope is not None: self._values["scope"] = scope

    @builtins.property
    def actions(self) -> typing.List[str]:
        """The actions to grant.

        stability
        :stability: experimental
        """
        return self._values.get('actions')

    @builtins.property
    def grantee(self) -> "IGrantable":
        """The principal to grant to.

        default
        :default: if principal is undefined, no work is done.

        stability
        :stability: experimental
        """
        return self._values.get('grantee')

    @builtins.property
    def resource_arns(self) -> typing.List[str]:
        """The resource ARNs to grant to.

        stability
        :stability: experimental
        """
        return self._values.get('resource_arns')

    @builtins.property
    def scope(self) -> typing.Optional[aws_cdk.core.IConstruct]:
        """Construct to report warnings on in case grant could not be registered.

        stability
        :stability: experimental
        """
        return self._values.get('scope')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GrantOnPrincipalOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GrantWithResourceOptions", jsii_struct_bases=[CommonGrantOptions], name_mapping={'actions': 'actions', 'grantee': 'grantee', 'resource_arns': 'resourceArns', 'resource': 'resource', 'resource_self_arns': 'resourceSelfArns'})
class GrantWithResourceOptions(CommonGrantOptions):
    def __init__(self, *, actions: typing.List[str], grantee: "IGrantable", resource_arns: typing.List[str], resource: "IResourceWithPolicy", resource_self_arns: typing.Optional[typing.List[str]]=None):
        """Options for a grant operation.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        :param resource: The resource with a resource policy. The statement will be added to the resource policy if it couldn't be added to the principal policy.
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs

        stability
        :stability: experimental
        """
        self._values = {
            'actions': actions,
            'grantee': grantee,
            'resource_arns': resource_arns,
            'resource': resource,
        }
        if resource_self_arns is not None: self._values["resource_self_arns"] = resource_self_arns

    @builtins.property
    def actions(self) -> typing.List[str]:
        """The actions to grant.

        stability
        :stability: experimental
        """
        return self._values.get('actions')

    @builtins.property
    def grantee(self) -> "IGrantable":
        """The principal to grant to.

        default
        :default: if principal is undefined, no work is done.

        stability
        :stability: experimental
        """
        return self._values.get('grantee')

    @builtins.property
    def resource_arns(self) -> typing.List[str]:
        """The resource ARNs to grant to.

        stability
        :stability: experimental
        """
        return self._values.get('resource_arns')

    @builtins.property
    def resource(self) -> "IResourceWithPolicy":
        """The resource with a resource policy.

        The statement will be added to the resource policy if it couldn't be
        added to the principal policy.

        stability
        :stability: experimental
        """
        return self._values.get('resource')

    @builtins.property
    def resource_self_arns(self) -> typing.Optional[typing.List[str]]:
        """When referring to the resource in a resource policy, use this as ARN.

        (Depending on the resource type, this needs to be '*' in a resource policy).

        default
        :default: Same as regular resource ARNs

        stability
        :stability: experimental
        """
        return self._values.get('resource_self_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GrantWithResourceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.GroupProps", jsii_struct_bases=[], name_mapping={'group_name': 'groupName', 'managed_policies': 'managedPolicies', 'path': 'path'})
class GroupProps():
    def __init__(self, *, group_name: typing.Optional[str]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, path: typing.Optional[str]=None):
        """
        :param group_name: A name for the IAM group. For valid values, see the GroupName parameter for the CreateGroup action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: Generated by CloudFormation (recommended)
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param path: The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_ in the IAM User Guide. Default: /
        """
        self._values = {
        }
        if group_name is not None: self._values["group_name"] = group_name
        if managed_policies is not None: self._values["managed_policies"] = managed_policies
        if path is not None: self._values["path"] = path

    @builtins.property
    def group_name(self) -> typing.Optional[str]:
        """A name for the IAM group.

        For valid values, see the GroupName parameter
        for the CreateGroup action in the IAM API Reference. If you don't specify
        a name, AWS CloudFormation generates a unique physical ID and uses that
        ID for the group name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        default
        :default: Generated by CloudFormation (recommended)
        """
        return self._values.get('group_name')

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List["IManagedPolicy"]]:
        """A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        default
        :default: - No managed policies.
        """
        return self._values.get('managed_policies')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path to the group.

        For more information about paths, see `IAM
        Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_
        in the IAM User Guide.

        default
        :default: /
        """
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IGrantable")
class IGrantable(jsii.compat.Protocol):
    """Any object that has an associated principal that a permission can be granted to."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IGrantableProxy

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        ...


class _IGrantableProxy():
    """Any object that has an associated principal that a permission can be granted to."""
    __jsii_type__ = "@aws-cdk/aws-iam.IGrantable"
    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IManagedPolicy")
class IManagedPolicy(jsii.compat.Protocol):
    """A managed policy."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IManagedPolicyProxy

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> str:
        """The ARN of the managed policy.

        attribute:
        :attribute:: true
        """
        ...


class _IManagedPolicyProxy():
    """A managed policy."""
    __jsii_type__ = "@aws-cdk/aws-iam.IManagedPolicy"
    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> str:
        """The ARN of the managed policy.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "managedPolicyArn")


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IPolicy")
class IPolicy(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPolicyProxy

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _IPolicyProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-iam.IPolicy"
    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "policyName")


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IPrincipal")
class IPrincipal(IGrantable, jsii.compat.Protocol):
    """Represents a logical IAM principal.

    An IPrincipal describes a logical entity that can perform AWS API calls
    against sets of resources, optionally under certain conditions.

    Examples of simple principals are IAM objects that you create, such
    as Users or Roles.

    An example of a more complex principals is a ``ServicePrincipal`` (such as
    ``new ServicePrincipal("sns.amazonaws.com")``, which represents the Simple
    Notifications Service).

    A single logical Principal may also map to a set of physical principals.
    For example, ``new OrganizationPrincipal('o-1234')`` represents all
    identities that are part of the given AWS Organization.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPrincipalProxy

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        ...

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        ...

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Add to the policy of this principal.

        :param statement: -

        return
        :return:

        true if the statement was added, false if the principal in
        question does not have a policy document to add the statement to.
        """
        ...


class _IPrincipalProxy(jsii.proxy_for(IGrantable)):
    """Represents a logical IAM principal.

    An IPrincipal describes a logical entity that can perform AWS API calls
    against sets of resources, optionally under certain conditions.

    Examples of simple principals are IAM objects that you create, such
    as Users or Roles.

    An example of a more complex principals is a ``ServicePrincipal`` (such as
    ``new ServicePrincipal("sns.amazonaws.com")``, which represents the Simple
    Notifications Service).

    A single logical Principal may also map to a set of physical principals.
    For example, ``new OrganizationPrincipal('o-1234')`` represents all
    identities that are part of the given AWS Organization.
    """
    __jsii_type__ = "@aws-cdk/aws-iam.IPrincipal"
    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Add to the policy of this principal.

        :param statement: -

        return
        :return:

        true if the statement was added, false if the principal in
        question does not have a policy document to add the statement to.
        """
        return jsii.invoke(self, "addToPolicy", [statement])


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IIdentity")
class IIdentity(IPrincipal, aws_cdk.core.IResource, jsii.compat.Protocol):
    """A construct that represents an IAM principal, such as a user, group or role."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IIdentityProxy

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: "IManagedPolicy") -> None:
        """Attaches a managed policy to this principal.

        :param policy: The managed policy.
        """
        ...

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        """Attaches an inline policy to this principal.

        This is the same as calling ``policy.addToXxx(principal)``.

        :param policy: The policy resource to attach to this principal [disable-awslint:ref-via-interface].
        """
        ...


class _IIdentityProxy(jsii.proxy_for(IPrincipal), jsii.proxy_for(aws_cdk.core.IResource)):
    """A construct that represents an IAM principal, such as a user, group or role."""
    __jsii_type__ = "@aws-cdk/aws-iam.IIdentity"
    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: "IManagedPolicy") -> None:
        """Attaches a managed policy to this principal.

        :param policy: The managed policy.
        """
        return jsii.invoke(self, "addManagedPolicy", [policy])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        """Attaches an inline policy to this principal.

        This is the same as calling ``policy.addToXxx(principal)``.

        :param policy: The policy resource to attach to this principal [disable-awslint:ref-via-interface].
        """
        return jsii.invoke(self, "attachInlinePolicy", [policy])


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IGroup")
class IGroup(IIdentity, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IGroupProxy

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> str:
        """Returns the IAM Group ARN.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        """Returns the IAM Group Name.

        attribute:
        :attribute:: true
        """
        ...


class _IGroupProxy(jsii.proxy_for(IIdentity)):
    __jsii_type__ = "@aws-cdk/aws-iam.IGroup"
    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> str:
        """Returns the IAM Group ARN.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "groupArn")

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        """Returns the IAM Group Name.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "groupName")


@jsii.implements(IGroup)
class Group(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Group"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, group_name: typing.Optional[str]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param group_name: A name for the IAM group. For valid values, see the GroupName parameter for the CreateGroup action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: Generated by CloudFormation (recommended)
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param path: The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_ in the IAM User Guide. Default: /
        """
        props = GroupProps(group_name=group_name, managed_policies=managed_policies, path=path)

        jsii.create(Group, self, [scope, id, props])

    @jsii.member(jsii_name="fromGroupArn")
    @builtins.classmethod
    def from_group_arn(cls, scope: aws_cdk.core.Construct, id: str, group_arn: str) -> "IGroup":
        """Imports a group from ARN.

        :param scope: -
        :param id: -
        :param group_arn: (e.g. ``arn:aws:iam::account-id:group/group-name``).
        """
        return jsii.sinvoke(cls, "fromGroupArn", [scope, id, group_arn])

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: "IManagedPolicy") -> None:
        """Attaches a managed policy to this group.

        :param policy: The managed policy to attach.
        """
        return jsii.invoke(self, "addManagedPolicy", [policy])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Adds an IAM statement to the default policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="addUser")
    def add_user(self, user: "IUser") -> None:
        """Adds a user to this group.

        :param user: -
        """
        return jsii.invoke(self, "addUser", [user])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        """Attaches a policy to this group.

        :param policy: The policy to attach.
        """
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> str:
        """Returns the IAM Group ARN."""
        return jsii.get(self, "groupArn")

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        """Returns the IAM Group Name."""
        return jsii.get(self, "groupName")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IResourceWithPolicy")
class IResourceWithPolicy(aws_cdk.core.IConstruct, jsii.compat.Protocol):
    """A resource with a resource policy that can be added to."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourceWithPolicyProxy

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: "PolicyStatement") -> None:
        """Add a statement to the resource's resource policy.

        :param statement: -
        """
        ...


class _IResourceWithPolicyProxy(jsii.proxy_for(aws_cdk.core.IConstruct)):
    """A resource with a resource policy that can be added to."""
    __jsii_type__ = "@aws-cdk/aws-iam.IResourceWithPolicy"
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: "PolicyStatement") -> None:
        """Add a statement to the resource's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IRole")
class IRole(IIdentity, jsii.compat.Protocol):
    """A Role object."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRoleProxy

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """Returns the ARN of this role.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        """Returns the name of this role.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: "IPrincipal", *actions: str) -> "Grant":
        """Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -
        """
        ...

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: "IPrincipal") -> "Grant":
        """Grant permissions to the given principal to pass this role.

        :param grantee: -
        """
        ...


class _IRoleProxy(jsii.proxy_for(IIdentity)):
    """A Role object."""
    __jsii_type__ = "@aws-cdk/aws-iam.IRole"
    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """Returns the ARN of this role.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "roleArn")

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        """Returns the name of this role.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "roleName")

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: "IPrincipal", *actions: str) -> "Grant":
        """Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: "IPrincipal") -> "Grant":
        """Grant permissions to the given principal to pass this role.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPassRole", [grantee])


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IUser")
class IUser(IIdentity, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserProxy

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> str:
        """The user's ARN.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        """The user's name.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        """Adds this user to a group.

        :param group: -
        """
        ...


class _IUserProxy(jsii.proxy_for(IIdentity)):
    __jsii_type__ = "@aws-cdk/aws-iam.IUser"
    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> str:
        """The user's ARN.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userArn")

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        """The user's name.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userName")

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        """Adds this user to a group.

        :param group: -
        """
        return jsii.invoke(self, "addToGroup", [group])


@jsii.implements(IRole)
class LazyRole(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.LazyRole"):
    """An IAM role that only gets attached to the construct tree once it gets used, not before.

    This construct can be used to simplify logic in other constructs
    which need to create a role but only if certain configurations occur
    (such as when AutoScaling is configured). The role can be configured in one
    place, but if it never gets used it doesn't get instantiated and will
    not be synthesized or deployed.

    resource:
    :resource:: AWS::IAM::Role
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assumed_by: "IPrincipal", external_id: typing.Optional[str]=None, external_ids: typing.Optional[typing.List[str]]=None, inline_policies: typing.Optional[typing.Mapping[str,"PolicyDocument"]]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, max_session_duration: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional["IManagedPolicy"]=None, role_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param external_id: ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        """
        props = LazyRoleProps(assumed_by=assumed_by, external_id=external_id, external_ids=external_ids, inline_policies=inline_policies, managed_policies=managed_policies, max_session_duration=max_session_duration, path=path, permissions_boundary=permissions_boundary, role_name=role_name)

        jsii.create(LazyRole, self, [scope, id, props])

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: "IManagedPolicy") -> None:
        """Attaches a managed policy to this role.

        :param policy: The managed policy to attach.
        """
        return jsii.invoke(self, "addManagedPolicy", [policy])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Adds a permission to the role's default policy document.

        If there is no default policy attached to this role, it will be created.

        :param statement: The permission statement to add to the policy document.
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        """Attaches a policy to this role.

        :param policy: The policy to attach.
        """
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="grant")
    def grant(self, identity: "IPrincipal", *actions: str) -> "Grant":
        """Grant the actions defined in actions to the identity Principal on this resource.

        :param identity: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [identity, *actions])

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: "IPrincipal") -> "Grant":
        """Grant permissions to the given principal to pass this role.

        :param identity: -
        """
        return jsii.invoke(self, "grantPassRole", [identity])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """Returns the ARN of this role."""
        return jsii.get(self, "roleArn")

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        """
        attribute:
        :attribute:: RoleId
        """
        return jsii.get(self, "roleId")

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        """Returns the name of this role."""
        return jsii.get(self, "roleName")


@jsii.implements(IManagedPolicy)
class ManagedPolicy(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.ManagedPolicy"):
    """Managed policy."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, groups: typing.Optional[typing.List["IGroup"]]=None, managed_policy_name: typing.Optional[str]=None, path: typing.Optional[str]=None, roles: typing.Optional[typing.List["IRole"]]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None, users: typing.Optional[typing.List["IUser"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param description: A description of the managed policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed. Default: - empty
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param managed_policy_name: The name of the managed policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - A name is automatically generated.
        :param path: The path for the policy. This parameter allows (through its regex pattern) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: - "/"
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.
        """
        props = ManagedPolicyProps(description=description, groups=groups, managed_policy_name=managed_policy_name, path=path, roles=roles, statements=statements, users=users)

        jsii.create(ManagedPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="fromAwsManagedPolicyName")
    @builtins.classmethod
    def from_aws_managed_policy_name(cls, managed_policy_name: str) -> "IManagedPolicy":
        """Construct a managed policy from one of the policies that AWS manages.

        For this managed policy, you only need to know the name to be able to use it.

        Some managed policy names start with "service-role/", some start with
        "job-function/", and some don't start with anything. Do include the
        prefix when constructing this object.

        :param managed_policy_name: -
        """
        return jsii.sinvoke(cls, "fromAwsManagedPolicyName", [managed_policy_name])

    @jsii.member(jsii_name="fromManagedPolicyName")
    @builtins.classmethod
    def from_managed_policy_name(cls, scope: aws_cdk.core.Construct, id: str, managed_policy_name: str) -> "IManagedPolicy":
        """Construct a customer managed policy from the managedPolicyName.

        For this managed policy, you only need to know the name to be able to use it.

        :param scope: -
        :param id: -
        :param managed_policy_name: -
        """
        return jsii.sinvoke(cls, "fromManagedPolicyName", [scope, id, managed_policy_name])

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        """Adds a statement to the policy document.

        :param statement: -
        """
        return jsii.invoke(self, "addStatements", [*statement])

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "IGroup") -> None:
        """Attaches this policy to a group.

        :param group: -
        """
        return jsii.invoke(self, "attachToGroup", [group])

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        """Attaches this policy to a role.

        :param role: -
        """
        return jsii.invoke(self, "attachToRole", [role])

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "IUser") -> None:
        """Attaches this policy to a user.

        :param user: -
        """
        return jsii.invoke(self, "attachToUser", [user])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """The description of this policy.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "description")

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        """The policy document."""
        return jsii.get(self, "document")

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> str:
        """Returns the ARN of this managed policy.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "managedPolicyArn")

    @builtins.property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> str:
        """The name of this policy.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "managedPolicyName")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The path of this policy.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "path")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.ManagedPolicyProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'groups': 'groups', 'managed_policy_name': 'managedPolicyName', 'path': 'path', 'roles': 'roles', 'statements': 'statements', 'users': 'users'})
class ManagedPolicyProps():
    def __init__(self, *, description: typing.Optional[str]=None, groups: typing.Optional[typing.List["IGroup"]]=None, managed_policy_name: typing.Optional[str]=None, path: typing.Optional[str]=None, roles: typing.Optional[typing.List["IRole"]]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None, users: typing.Optional[typing.List["IUser"]]=None):
        """
        :param description: A description of the managed policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed. Default: - empty
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param managed_policy_name: The name of the managed policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - A name is automatically generated.
        :param path: The path for the policy. This parameter allows (through its regex pattern) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: - "/"
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if groups is not None: self._values["groups"] = groups
        if managed_policy_name is not None: self._values["managed_policy_name"] = managed_policy_name
        if path is not None: self._values["path"] = path
        if roles is not None: self._values["roles"] = roles
        if statements is not None: self._values["statements"] = statements
        if users is not None: self._values["users"] = users

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the managed policy.

        Typically used to store information about the
        permissions defined in the policy. For example, "Grants access to production DynamoDB tables."
        The policy description is immutable. After a value is assigned, it cannot be changed.

        default
        :default: - empty
        """
        return self._values.get('description')

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        """Groups to attach this policy to.

        You can also use ``attachToGroup(group)`` to attach this policy to a group.

        default
        :default: - No groups.
        """
        return self._values.get('groups')

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[str]:
        """The name of the managed policy.

        If you specify multiple policies for an entity,
        specify unique names. For example, if you specify a list of policies for
        an IAM role, each policy must have a unique name.

        default
        :default: - A name is automatically generated.
        """
        return self._values.get('managed_policy_name')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path for the policy.

        This parameter allows (through its regex pattern) a string of characters
        consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes.
        In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F),
        including most punctuation characters, digits, and upper and lowercased letters.

        For more information about paths, see IAM Identifiers in the IAM User Guide.

        default
        :default: - "/"
        """
        return self._values.get('path')

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["IRole"]]:
        """Roles to attach this policy to.

        You can also use ``attachToRole(role)`` to attach this policy to a role.

        default
        :default: - No roles.
        """
        return self._values.get('roles')

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        """Initial set of permissions to add to this policy document.

        You can also use ``addPermission(statement)`` to add permissions later.

        default
        :default: - No statements.
        """
        return self._values.get('statements')

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IUser"]]:
        """Users to attach this policy to.

        You can also use ``attachToUser(user)`` to attach this policy to a user.

        default
        :default: - No users.
        """
        return self._values.get('users')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ManagedPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPolicy)
class Policy(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Policy"):
    """The AWS::IAM::Policy resource associates an IAM policy with IAM users, roles, or groups.

    For more information about IAM policies, see `Overview of IAM
    Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies_overview.html>`_
    in the IAM User Guide guide.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, force: typing.Optional[bool]=None, groups: typing.Optional[typing.List["IGroup"]]=None, policy_name: typing.Optional[str]=None, roles: typing.Optional[typing.List["IRole"]]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None, users: typing.Optional[typing.List["IUser"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param force: Force creation of an ``AWS::IAM::Policy``. Unless set to ``true``, this ``Policy`` construct will not materialize to an ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect (for example, if it remains unattached to an IAM identity or if it has no statements). This is generally desired behavior, since it prevents creating invalid--and hence undeployable--CloudFormation templates. In cases where you know the policy must be created and it is actually an error if no statements have been added to it, you can se this to ``true``. Default: false
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param policy_name: The name of the policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - Uses the logical ID of the policy resource, which is ensured to be unique within the stack.
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.
        """
        props = PolicyProps(force=force, groups=groups, policy_name=policy_name, roles=roles, statements=statements, users=users)

        jsii.create(Policy, self, [scope, id, props])

    @jsii.member(jsii_name="fromPolicyName")
    @builtins.classmethod
    def from_policy_name(cls, scope: aws_cdk.core.Construct, id: str, policy_name: str) -> "IPolicy":
        """
        :param scope: -
        :param id: -
        :param policy_name: -
        """
        return jsii.sinvoke(cls, "fromPolicyName", [scope, id, policy_name])

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        """Adds a statement to the policy document.

        :param statement: -
        """
        return jsii.invoke(self, "addStatements", [*statement])

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "IGroup") -> None:
        """Attaches this policy to a group.

        :param group: -
        """
        return jsii.invoke(self, "attachToGroup", [group])

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        """Attaches this policy to a role.

        :param role: -
        """
        return jsii.invoke(self, "attachToRole", [role])

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "IUser") -> None:
        """Attaches this policy to a user.

        :param user: -
        """
        return jsii.invoke(self, "attachToUser", [user])

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

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        """The policy document."""
        return jsii.get(self, "document")

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        """The name of this policy.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "policyName")


@jsii.implements(aws_cdk.core.IResolvable)
class PolicyDocument(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.PolicyDocument"):
    """A PolicyDocument is a collection of statements."""
    def __init__(self, *, assign_sids: typing.Optional[bool]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None) -> None:
        """
        :param assign_sids: Automatically assign Statement Ids to all statements. Default: false
        :param statements: Initial statements to add to the policy document. Default: - No statements
        """
        props = PolicyDocumentProps(assign_sids=assign_sids, statements=statements)

        jsii.create(PolicyDocument, self, [props])

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        """Adds a statement to the policy document.

        :param statement: the statement to add.
        """
        return jsii.invoke(self, "addStatements", [*statement])

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: aws_cdk.core.IResolveContext) -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -
        """
        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        """JSON-ify the document.

        Used when JSON.stringify() is called
        """
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Encode the policy document as a string."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.
        """
        return jsii.get(self, "creationStack")

    @builtins.property
    @jsii.member(jsii_name="isEmpty")
    def is_empty(self) -> bool:
        return jsii.get(self, "isEmpty")

    @builtins.property
    @jsii.member(jsii_name="statementCount")
    def statement_count(self) -> jsii.Number:
        """The number of statements already added to this policy.

        Can be used, for example, to generate uniuqe "sid"s within the policy.
        """
        return jsii.get(self, "statementCount")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.PolicyDocumentProps", jsii_struct_bases=[], name_mapping={'assign_sids': 'assignSids', 'statements': 'statements'})
class PolicyDocumentProps():
    def __init__(self, *, assign_sids: typing.Optional[bool]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None):
        """Properties for a new PolicyDocument.

        :param assign_sids: Automatically assign Statement Ids to all statements. Default: false
        :param statements: Initial statements to add to the policy document. Default: - No statements
        """
        self._values = {
        }
        if assign_sids is not None: self._values["assign_sids"] = assign_sids
        if statements is not None: self._values["statements"] = statements

    @builtins.property
    def assign_sids(self) -> typing.Optional[bool]:
        """Automatically assign Statement Ids to all statements.

        default
        :default: false
        """
        return self._values.get('assign_sids')

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        """Initial statements to add to the policy document.

        default
        :default: - No statements
        """
        return self._values.get('statements')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PolicyDocumentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.PolicyProps", jsii_struct_bases=[], name_mapping={'force': 'force', 'groups': 'groups', 'policy_name': 'policyName', 'roles': 'roles', 'statements': 'statements', 'users': 'users'})
class PolicyProps():
    def __init__(self, *, force: typing.Optional[bool]=None, groups: typing.Optional[typing.List["IGroup"]]=None, policy_name: typing.Optional[str]=None, roles: typing.Optional[typing.List["IRole"]]=None, statements: typing.Optional[typing.List["PolicyStatement"]]=None, users: typing.Optional[typing.List["IUser"]]=None):
        """
        :param force: Force creation of an ``AWS::IAM::Policy``. Unless set to ``true``, this ``Policy`` construct will not materialize to an ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect (for example, if it remains unattached to an IAM identity or if it has no statements). This is generally desired behavior, since it prevents creating invalid--and hence undeployable--CloudFormation templates. In cases where you know the policy must be created and it is actually an error if no statements have been added to it, you can se this to ``true``. Default: false
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param policy_name: The name of the policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - Uses the logical ID of the policy resource, which is ensured to be unique within the stack.
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.
        """
        self._values = {
        }
        if force is not None: self._values["force"] = force
        if groups is not None: self._values["groups"] = groups
        if policy_name is not None: self._values["policy_name"] = policy_name
        if roles is not None: self._values["roles"] = roles
        if statements is not None: self._values["statements"] = statements
        if users is not None: self._values["users"] = users

    @builtins.property
    def force(self) -> typing.Optional[bool]:
        """Force creation of an ``AWS::IAM::Policy``.

        Unless set to ``true``, this ``Policy`` construct will not materialize to an
        ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect
        (for example, if it remains unattached to an IAM identity or if it has no
        statements). This is generally desired behavior, since it prevents
        creating invalid--and hence undeployable--CloudFormation templates.

        In cases where you know the policy must be created and it is actually
        an error if no statements have been added to it, you can se this to ``true``.

        default
        :default: false
        """
        return self._values.get('force')

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        """Groups to attach this policy to.

        You can also use ``attachToGroup(group)`` to attach this policy to a group.

        default
        :default: - No groups.
        """
        return self._values.get('groups')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """The name of the policy.

        If you specify multiple policies for an entity,
        specify unique names. For example, if you specify a list of policies for
        an IAM role, each policy must have a unique name.

        default
        :default:

        - Uses the logical ID of the policy resource, which is ensured
          to be unique within the stack.
        """
        return self._values.get('policy_name')

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["IRole"]]:
        """Roles to attach this policy to.

        You can also use ``attachToRole(role)`` to attach this policy to a role.

        default
        :default: - No roles.
        """
        return self._values.get('roles')

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        """Initial set of permissions to add to this policy document.

        You can also use ``addPermission(statement)`` to add permissions later.

        default
        :default: - No statements.
        """
        return self._values.get('statements')

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IUser"]]:
        """Users to attach this policy to.

        You can also use ``attachToUser(user)`` to attach this policy to a user.

        default
        :default: - No users.
        """
        return self._values.get('users')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class PolicyStatement(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.PolicyStatement"):
    """Represents a statement in an IAM policy document."""
    def __init__(self, *, actions: typing.Optional[typing.List[str]]=None, conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None, effect: typing.Optional["Effect"]=None, not_actions: typing.Optional[typing.List[str]]=None, not_principals: typing.Optional[typing.List["IPrincipal"]]=None, not_resources: typing.Optional[typing.List[str]]=None, principals: typing.Optional[typing.List["IPrincipal"]]=None, resources: typing.Optional[typing.List[str]]=None) -> None:
        """
        :param actions: List of actions to add to the statement. Default: - no actions
        :param conditions: Conditions to add to the statement. Default: - no condition
        :param effect: Whether to allow or deny the actions in this statement. Default: - allow
        :param not_actions: List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: List of not principals to add to the statement. Default: - no not principals
        :param not_resources: NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: List of principals to add to the statement. Default: - no principals
        :param resources: Resource ARNs to add to the statement. Default: - no resources
        """
        props = PolicyStatementProps(actions=actions, conditions=conditions, effect=effect, not_actions=not_actions, not_principals=not_principals, not_resources=not_resources, principals=principals, resources=resources)

        jsii.create(PolicyStatement, self, [props])

    @jsii.member(jsii_name="addAccountCondition")
    def add_account_condition(self, account_id: str) -> None:
        """Add a condition that limits to a given account.

        :param account_id: -
        """
        return jsii.invoke(self, "addAccountCondition", [account_id])

    @jsii.member(jsii_name="addAccountRootPrincipal")
    def add_account_root_principal(self) -> None:
        return jsii.invoke(self, "addAccountRootPrincipal", [])

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: str) -> None:
        """
        :param actions: -
        """
        return jsii.invoke(self, "addActions", [*actions])

    @jsii.member(jsii_name="addAllResources")
    def add_all_resources(self) -> None:
        """Adds a ``"*"`` resource to this statement."""
        return jsii.invoke(self, "addAllResources", [])

    @jsii.member(jsii_name="addAnyPrincipal")
    def add_any_principal(self) -> None:
        return jsii.invoke(self, "addAnyPrincipal", [])

    @jsii.member(jsii_name="addArnPrincipal")
    def add_arn_principal(self, arn: str) -> None:
        """
        :param arn: -
        """
        return jsii.invoke(self, "addArnPrincipal", [arn])

    @jsii.member(jsii_name="addAwsAccountPrincipal")
    def add_aws_account_principal(self, account_id: str) -> None:
        """
        :param account_id: -
        """
        return jsii.invoke(self, "addAwsAccountPrincipal", [account_id])

    @jsii.member(jsii_name="addCanonicalUserPrincipal")
    def add_canonical_user_principal(self, canonical_user_id: str) -> None:
        """
        :param canonical_user_id: -
        """
        return jsii.invoke(self, "addCanonicalUserPrincipal", [canonical_user_id])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, key: str, value: typing.Any) -> None:
        """Add a condition to the Policy.

        :param key: -
        :param value: -
        """
        return jsii.invoke(self, "addCondition", [key, value])

    @jsii.member(jsii_name="addConditions")
    def add_conditions(self, conditions: typing.Mapping[str,typing.Any]) -> None:
        """Add multiple conditions to the Policy.

        :param conditions: -
        """
        return jsii.invoke(self, "addConditions", [conditions])

    @jsii.member(jsii_name="addFederatedPrincipal")
    def add_federated_principal(self, federated: typing.Any, conditions: typing.Mapping[str,typing.Any]) -> None:
        """
        :param federated: -
        :param conditions: -
        """
        return jsii.invoke(self, "addFederatedPrincipal", [federated, conditions])

    @jsii.member(jsii_name="addNotActions")
    def add_not_actions(self, *not_actions: str) -> None:
        """
        :param not_actions: -
        """
        return jsii.invoke(self, "addNotActions", [*not_actions])

    @jsii.member(jsii_name="addNotPrincipals")
    def add_not_principals(self, *not_principals: "IPrincipal") -> None:
        """
        :param not_principals: -
        """
        return jsii.invoke(self, "addNotPrincipals", [*not_principals])

    @jsii.member(jsii_name="addNotResources")
    def add_not_resources(self, *arns: str) -> None:
        """
        :param arns: -
        """
        return jsii.invoke(self, "addNotResources", [*arns])

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: "IPrincipal") -> None:
        """
        :param principals: -
        """
        return jsii.invoke(self, "addPrincipals", [*principals])

    @jsii.member(jsii_name="addResources")
    def add_resources(self, *arns: str) -> None:
        """
        :param arns: -
        """
        return jsii.invoke(self, "addResources", [*arns])

    @jsii.member(jsii_name="addServicePrincipal")
    def add_service_principal(self, service: str, *, conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None) -> None:
        """Adds a service principal to this policy statement.

        :param service: the service name for which a service principal is requested (e.g: ``s3.amazonaws.com``).
        :param conditions: Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: The region in which the service is operating. Default: the current Stack's region.
        """
        opts = ServicePrincipalOpts(conditions=conditions, region=region)

        return jsii.invoke(self, "addServicePrincipal", [service, opts])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        """JSON-ify the statement.

        Used when JSON.stringify() is called
        """
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toStatementJson")
    def to_statement_json(self) -> typing.Any:
        return jsii.invoke(self, "toStatementJson", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="hasPrincipal")
    def has_principal(self) -> bool:
        """Indicates if this permission has a "Principal" section."""
        return jsii.get(self, "hasPrincipal")

    @builtins.property
    @jsii.member(jsii_name="hasResource")
    def has_resource(self) -> bool:
        """Indicates if this permission as at least one resource associated with it."""
        return jsii.get(self, "hasResource")

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> "Effect":
        return jsii.get(self, "effect")

    @effect.setter
    def effect(self, value: "Effect"):
        jsii.set(self, "effect", value)

    @builtins.property
    @jsii.member(jsii_name="sid")
    def sid(self) -> typing.Optional[str]:
        """Statement ID for this statement."""
        return jsii.get(self, "sid")

    @sid.setter
    def sid(self, value: typing.Optional[str]):
        jsii.set(self, "sid", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.PolicyStatementProps", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'conditions': 'conditions', 'effect': 'effect', 'not_actions': 'notActions', 'not_principals': 'notPrincipals', 'not_resources': 'notResources', 'principals': 'principals', 'resources': 'resources'})
class PolicyStatementProps():
    def __init__(self, *, actions: typing.Optional[typing.List[str]]=None, conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None, effect: typing.Optional["Effect"]=None, not_actions: typing.Optional[typing.List[str]]=None, not_principals: typing.Optional[typing.List["IPrincipal"]]=None, not_resources: typing.Optional[typing.List[str]]=None, principals: typing.Optional[typing.List["IPrincipal"]]=None, resources: typing.Optional[typing.List[str]]=None):
        """Interface for creating a policy statement.

        :param actions: List of actions to add to the statement. Default: - no actions
        :param conditions: Conditions to add to the statement. Default: - no condition
        :param effect: Whether to allow or deny the actions in this statement. Default: - allow
        :param not_actions: List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: List of not principals to add to the statement. Default: - no not principals
        :param not_resources: NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: List of principals to add to the statement. Default: - no principals
        :param resources: Resource ARNs to add to the statement. Default: - no resources
        """
        self._values = {
        }
        if actions is not None: self._values["actions"] = actions
        if conditions is not None: self._values["conditions"] = conditions
        if effect is not None: self._values["effect"] = effect
        if not_actions is not None: self._values["not_actions"] = not_actions
        if not_principals is not None: self._values["not_principals"] = not_principals
        if not_resources is not None: self._values["not_resources"] = not_resources
        if principals is not None: self._values["principals"] = principals
        if resources is not None: self._values["resources"] = resources

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[str]]:
        """List of actions to add to the statement.

        default
        :default: - no actions
        """
        return self._values.get('actions')

    @builtins.property
    def conditions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Conditions to add to the statement.

        default
        :default: - no condition
        """
        return self._values.get('conditions')

    @builtins.property
    def effect(self) -> typing.Optional["Effect"]:
        """Whether to allow or deny the actions in this statement.

        default
        :default: - allow
        """
        return self._values.get('effect')

    @builtins.property
    def not_actions(self) -> typing.Optional[typing.List[str]]:
        """List of not actions to add to the statement.

        default
        :default: - no not-actions
        """
        return self._values.get('not_actions')

    @builtins.property
    def not_principals(self) -> typing.Optional[typing.List["IPrincipal"]]:
        """List of not principals to add to the statement.

        default
        :default: - no not principals
        """
        return self._values.get('not_principals')

    @builtins.property
    def not_resources(self) -> typing.Optional[typing.List[str]]:
        """NotResource ARNs to add to the statement.

        default
        :default: - no not-resources
        """
        return self._values.get('not_resources')

    @builtins.property
    def principals(self) -> typing.Optional[typing.List["IPrincipal"]]:
        """List of principals to add to the statement.

        default
        :default: - no principals
        """
        return self._values.get('principals')

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[str]]:
        """Resource ARNs to add to the statement.

        default
        :default: - no resources
        """
        return self._values.get('resources')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PolicyStatementProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPrincipal)
class PrincipalBase(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-iam.PrincipalBase"):
    """Base class for policy principals."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _PrincipalBaseProxy

    def __init__(self) -> None:
        jsii.create(PrincipalBase, self, [])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, _statement: "PolicyStatement") -> bool:
        """Add to the policy of this principal.

        :param _statement: -
        """
        return jsii.invoke(self, "addToPolicy", [_statement])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[str,typing.List[str]]:
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    @abc.abstractmethod
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        ...


class _PrincipalBaseProxy(PrincipalBase):
    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


class ArnPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.ArnPrincipal"):
    def __init__(self, arn: str) -> None:
        """
        :param arn: -
        """
        jsii.create(ArnPrincipal, self, [arn])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        return jsii.get(self, "arn")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


class AccountPrincipal(ArnPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AccountPrincipal"):
    def __init__(self, account_id: typing.Any) -> None:
        """
        :param account_id: -
        """
        jsii.create(AccountPrincipal, self, [account_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> typing.Any:
        return jsii.get(self, "accountId")


class AccountRootPrincipal(AccountPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AccountRootPrincipal"):
    def __init__(self) -> None:
        jsii.create(AccountRootPrincipal, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])


class AnyPrincipal(ArnPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.AnyPrincipal"):
    """A principal representing all identities in all accounts."""
    def __init__(self) -> None:
        jsii.create(AnyPrincipal, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])


class Anyone(AnyPrincipal, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Anyone"):
    """A principal representing all identities in all accounts.

    deprecated
    :deprecated: use ``AnyPrincipal``

    stability
    :stability: deprecated
    """
    def __init__(self) -> None:
        jsii.create(Anyone, self, [])


class CanonicalUserPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CanonicalUserPrincipal"):
    """A policy prinicipal for canonicalUserIds - useful for S3 bucket policies that use Origin Access identities.

    See https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html

    and

    https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

    for more details.
    """
    def __init__(self, canonical_user_id: str) -> None:
        """
        :param canonical_user_id: -
        """
        jsii.create(CanonicalUserPrincipal, self, [canonical_user_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="canonicalUserId")
    def canonical_user_id(self) -> str:
        return jsii.get(self, "canonicalUserId")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


class CompositePrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.CompositePrincipal"):
    def __init__(self, *principals: "PrincipalBase") -> None:
        """
        :param principals: -
        """
        jsii.create(CompositePrincipal, self, [*principals])

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: "PrincipalBase") -> "CompositePrincipal":
        """
        :param principals: -
        """
        return jsii.invoke(self, "addPrincipals", [*principals])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


class FederatedPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.FederatedPrincipal"):
    def __init__(self, federated: str, conditions: typing.Mapping[str,typing.Any], assume_role_action: typing.Optional[str]=None) -> None:
        """
        :param federated: -
        :param conditions: -
        :param assume_role_action: -
        """
        jsii.create(FederatedPrincipal, self, [federated, conditions, assume_role_action])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "conditions")

    @builtins.property
    @jsii.member(jsii_name="federated")
    def federated(self) -> str:
        return jsii.get(self, "federated")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


class OrganizationPrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.OrganizationPrincipal"):
    """A principal that represents an AWS Organization."""
    def __init__(self, organization_id: str) -> None:
        """
        :param organization_id: -
        """
        jsii.create(OrganizationPrincipal, self, [organization_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> str:
        return jsii.get(self, "organizationId")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


class PrincipalPolicyFragment(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.PrincipalPolicyFragment"):
    """A collection of the fields in a PolicyStatement that can be used to identify a principal.

    This consists of the JSON used in the "Principal" field, and optionally a
    set of "Condition"s that need to be applied to the policy.
    """
    def __init__(self, principal_json: typing.Mapping[str,typing.List[str]], conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        :param principal_json: -
        :param conditions: -
        """
        jsii.create(PrincipalPolicyFragment, self, [principal_json, conditions])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "conditions")

    @builtins.property
    @jsii.member(jsii_name="principalJson")
    def principal_json(self) -> typing.Mapping[str,typing.List[str]]:
        return jsii.get(self, "principalJson")


@jsii.implements(IRole)
class Role(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Role"):
    """IAM Role.

    Defines an IAM role. The role is created with an assume policy document associated with
    the specified AWS service principal defined in ``serviceAssumeRole``.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assumed_by: "IPrincipal", external_id: typing.Optional[str]=None, external_ids: typing.Optional[typing.List[str]]=None, inline_policies: typing.Optional[typing.Mapping[str,"PolicyDocument"]]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, max_session_duration: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional["IManagedPolicy"]=None, role_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param external_id: ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        """
        props = RoleProps(assumed_by=assumed_by, external_id=external_id, external_ids=external_ids, inline_policies=inline_policies, managed_policies=managed_policies, max_session_duration=max_session_duration, path=path, permissions_boundary=permissions_boundary, role_name=role_name)

        jsii.create(Role, self, [scope, id, props])

    @jsii.member(jsii_name="fromRoleArn")
    @builtins.classmethod
    def from_role_arn(cls, scope: aws_cdk.core.Construct, id: str, role_arn: str, *, mutable: typing.Optional[bool]=None) -> "IRole":
        """Imports an external role by ARN.

        :param scope: construct scope.
        :param id: construct id.
        :param role_arn: the ARN of the role to import.
        :param mutable: Whether the imported role can be modified by attaching policy resources to it. Default: true
        """
        options = FromRoleArnOptions(mutable=mutable)

        return jsii.sinvoke(cls, "fromRoleArn", [scope, id, role_arn, options])

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: "IManagedPolicy") -> None:
        """Attaches a managed policy to this role.

        :param policy: The the managed policy to attach.
        """
        return jsii.invoke(self, "addManagedPolicy", [policy])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Adds a permission to the role's default policy document.

        If there is no default policy attached to this role, it will be created.

        :param statement: The permission statement to add to the policy document.
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        """Attaches a policy to this role.

        :param policy: The policy to attach.
        """
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: "IPrincipal", *actions: str) -> "Grant":
        """Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: "IPrincipal") -> "Grant":
        """Grant permissions to the given principal to pass this role.

        :param identity: -
        """
        return jsii.invoke(self, "grantPassRole", [identity])

    @jsii.member(jsii_name="withoutPolicyUpdates")
    def without_policy_updates(self) -> "IRole":
        """Return a copy of this Role object whose Policies will not be updated.

        Use the object returned by this method if you want this Role to be used by
        a construct without it automatically updating the Role's Policies.

        If you do, you are responsible for adding the correct statements to the
        Role's policies yourself.
        """
        return jsii.invoke(self, "withoutPolicyUpdates", [])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Returns the role."""
        return jsii.get(self, "policyFragment")

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """Returns the ARN of this role."""
        return jsii.get(self, "roleArn")

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> str:
        """Returns the stable and unique string identifying the role.

        For example,
        AIDAJQABLZS4A3QDU576Q.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "roleId")

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> str:
        """Returns the name of the role."""
        return jsii.get(self, "roleName")

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicy")
    def assume_role_policy(self) -> typing.Optional["PolicyDocument"]:
        """The assume role policy document associated with this role."""
        return jsii.get(self, "assumeRolePolicy")

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional["IManagedPolicy"]:
        """Returns the permissions boundary attached to this role."""
        return jsii.get(self, "permissionsBoundary")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.RoleProps", jsii_struct_bases=[], name_mapping={'assumed_by': 'assumedBy', 'external_id': 'externalId', 'external_ids': 'externalIds', 'inline_policies': 'inlinePolicies', 'managed_policies': 'managedPolicies', 'max_session_duration': 'maxSessionDuration', 'path': 'path', 'permissions_boundary': 'permissionsBoundary', 'role_name': 'roleName'})
class RoleProps():
    def __init__(self, *, assumed_by: "IPrincipal", external_id: typing.Optional[str]=None, external_ids: typing.Optional[typing.List[str]]=None, inline_policies: typing.Optional[typing.Mapping[str,"PolicyDocument"]]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, max_session_duration: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional["IManagedPolicy"]=None, role_name: typing.Optional[str]=None):
        """
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param external_id: ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        """
        self._values = {
            'assumed_by': assumed_by,
        }
        if external_id is not None: self._values["external_id"] = external_id
        if external_ids is not None: self._values["external_ids"] = external_ids
        if inline_policies is not None: self._values["inline_policies"] = inline_policies
        if managed_policies is not None: self._values["managed_policies"] = managed_policies
        if max_session_duration is not None: self._values["max_session_duration"] = max_session_duration
        if path is not None: self._values["path"] = path
        if permissions_boundary is not None: self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None: self._values["role_name"] = role_name

    @builtins.property
    def assumed_by(self) -> "IPrincipal":
        """The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role.

        You can later modify the assume role policy document by accessing it via
        the ``assumeRolePolicy`` property.
        """
        return self._values.get('assumed_by')

    @builtins.property
    def external_id(self) -> typing.Optional[str]:
        """ID that the role assumer needs to provide when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        default
        :default: No external ID required

        deprecated
        :deprecated: see {@link externalIds}

        stability
        :stability: deprecated
        """
        return self._values.get('external_id')

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[str]]:
        """List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        default
        :default: No external ID required
        """
        return self._values.get('external_ids')

    @builtins.property
    def inline_policies(self) -> typing.Optional[typing.Mapping[str,"PolicyDocument"]]:
        """A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        default
        :default: - No policy is inlined in the Role resource.
        """
        return self._values.get('inline_policies')

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List["IManagedPolicy"]]:
        """A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        default
        :default: - No managed policies.
        """
        return self._values.get('managed_policies')

    @builtins.property
    def max_session_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        default
        :default: Duration.hours(1)

        link:
        :link:: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        """
        return self._values.get('max_session_duration')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        default
        :default: /
        """
        return self._values.get('path')

    @builtins.property
    def permissions_boundary(self) -> typing.Optional["IManagedPolicy"]:
        """AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        default
        :default: - No permissions boundary.

        link:
        :link:: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        """
        return self._values.get('permissions_boundary')

    @builtins.property
    def role_name(self) -> typing.Optional[str]:
        """A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
          for the group name.
        """
        return self._values.get('role_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RoleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.LazyRoleProps", jsii_struct_bases=[RoleProps], name_mapping={'assumed_by': 'assumedBy', 'external_id': 'externalId', 'external_ids': 'externalIds', 'inline_policies': 'inlinePolicies', 'managed_policies': 'managedPolicies', 'max_session_duration': 'maxSessionDuration', 'path': 'path', 'permissions_boundary': 'permissionsBoundary', 'role_name': 'roleName'})
class LazyRoleProps(RoleProps):
    def __init__(self, *, assumed_by: "IPrincipal", external_id: typing.Optional[str]=None, external_ids: typing.Optional[typing.List[str]]=None, inline_policies: typing.Optional[typing.Mapping[str,"PolicyDocument"]]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, max_session_duration: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional["IManagedPolicy"]=None, role_name: typing.Optional[str]=None):
        """
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param external_id: ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        """
        self._values = {
            'assumed_by': assumed_by,
        }
        if external_id is not None: self._values["external_id"] = external_id
        if external_ids is not None: self._values["external_ids"] = external_ids
        if inline_policies is not None: self._values["inline_policies"] = inline_policies
        if managed_policies is not None: self._values["managed_policies"] = managed_policies
        if max_session_duration is not None: self._values["max_session_duration"] = max_session_duration
        if path is not None: self._values["path"] = path
        if permissions_boundary is not None: self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None: self._values["role_name"] = role_name

    @builtins.property
    def assumed_by(self) -> "IPrincipal":
        """The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role.

        You can later modify the assume role policy document by accessing it via
        the ``assumeRolePolicy`` property.
        """
        return self._values.get('assumed_by')

    @builtins.property
    def external_id(self) -> typing.Optional[str]:
        """ID that the role assumer needs to provide when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        default
        :default: No external ID required

        deprecated
        :deprecated: see {@link externalIds}

        stability
        :stability: deprecated
        """
        return self._values.get('external_id')

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[str]]:
        """List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        default
        :default: No external ID required
        """
        return self._values.get('external_ids')

    @builtins.property
    def inline_policies(self) -> typing.Optional[typing.Mapping[str,"PolicyDocument"]]:
        """A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        default
        :default: - No policy is inlined in the Role resource.
        """
        return self._values.get('inline_policies')

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List["IManagedPolicy"]]:
        """A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        default
        :default: - No managed policies.
        """
        return self._values.get('managed_policies')

    @builtins.property
    def max_session_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        default
        :default: Duration.hours(1)

        link:
        :link:: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        """
        return self._values.get('max_session_duration')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        default
        :default: /
        """
        return self._values.get('path')

    @builtins.property
    def permissions_boundary(self) -> typing.Optional["IManagedPolicy"]:
        """AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        default
        :default: - No permissions boundary.

        link:
        :link:: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        """
        return self._values.get('permissions_boundary')

    @builtins.property
    def role_name(self) -> typing.Optional[str]:
        """A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
          for the group name.
        """
        return self._values.get('role_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyRoleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ServicePrincipal(PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.ServicePrincipal"):
    """An IAM principal that represents an AWS service (i.e. sqs.amazonaws.com)."""
    def __init__(self, service: str, *, conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None) -> None:
        """
        :param service: -
        :param conditions: Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: The region in which the service is operating. Default: the current Stack's region.
        """
        opts = ServicePrincipalOpts(conditions=conditions, region=region)

        jsii.create(ServicePrincipal, self, [service, opts])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> str:
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.ServicePrincipalOpts", jsii_struct_bases=[], name_mapping={'conditions': 'conditions', 'region': 'region'})
class ServicePrincipalOpts():
    def __init__(self, *, conditions: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None):
        """Options for a service principal.

        :param conditions: Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: The region in which the service is operating. Default: the current Stack's region.
        """
        self._values = {
        }
        if conditions is not None: self._values["conditions"] = conditions
        if region is not None: self._values["region"] = region

    @builtins.property
    def conditions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Additional conditions to add to the Service Principal.

        default
        :default: - No conditions
        """
        return self._values.get('conditions')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region in which the service is operating.

        default
        :default: the current Stack's region.
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServicePrincipalOpts(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPrincipal)
class UnknownPrincipal(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.UnknownPrincipal"):
    """A principal for use in resources that need to have a role but it's unknown.

    Some resources have roles associated with them which they assume, such as
    Lambda Functions, CodeBuild projects, StepFunctions machines, etc.

    When those resources are imported, their actual roles are not always
    imported with them. When that happens, we use an instance of this class
    instead, which will add user warnings when statements are attempted to be
    added to it.
    """
    def __init__(self, *, resource: aws_cdk.core.IConstruct) -> None:
        """
        :param resource: The resource the role proxy is for.
        """
        props = UnknownPrincipalProps(resource=resource)

        jsii.create(UnknownPrincipal, self, [props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Add to the policy of this principal.

        :param statement: -
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.UnknownPrincipalProps", jsii_struct_bases=[], name_mapping={'resource': 'resource'})
class UnknownPrincipalProps():
    def __init__(self, *, resource: aws_cdk.core.IConstruct):
        """Properties for an UnknownPrincipal.

        :param resource: The resource the role proxy is for.
        """
        self._values = {
            'resource': resource,
        }

    @builtins.property
    def resource(self) -> aws_cdk.core.IConstruct:
        """The resource the role proxy is for."""
        return self._values.get('resource')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UnknownPrincipalProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IIdentity, IUser)
class User(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.User"):
    """Define a new IAM user."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, groups: typing.Optional[typing.List["IGroup"]]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, password: typing.Optional[aws_cdk.core.SecretValue]=None, password_reset_required: typing.Optional[bool]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional["IManagedPolicy"]=None, user_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param groups: Groups to add this user to. You can also use ``addToGroup`` to add this user to a group. Default: - No groups.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param password: The password for the user. This is required so the user can access the AWS Management Console. You can use ``SecretValue.plainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - User won't be able to access the management console without a password.
        :param password_reset_required: Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console. If this is set to 'true', you must also specify "initialPassword". Default: false
        :param path: The path for the user name. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param user_name: A name for the IAM user. For valid values, see the UserName parameter for the CreateUser action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - Generated by CloudFormation (recommended)
        """
        props = UserProps(groups=groups, managed_policies=managed_policies, password=password, password_reset_required=password_reset_required, path=path, permissions_boundary=permissions_boundary, user_name=user_name)

        jsii.create(User, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserName")
    @builtins.classmethod
    def from_user_name(cls, scope: aws_cdk.core.Construct, id: str, user_name: str) -> "IUser":
        """Import an existing user given a username.

        :param scope: -
        :param id: -
        :param user_name: -
        """
        return jsii.sinvoke(cls, "fromUserName", [scope, id, user_name])

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: "IManagedPolicy") -> None:
        """Attaches a managed policy to the user.

        :param policy: The managed policy to attach.
        """
        return jsii.invoke(self, "addManagedPolicy", [policy])

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        """Adds this user to a group.

        :param group: -
        """
        return jsii.invoke(self, "addToGroup", [group])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> bool:
        """Adds an IAM statement to the default policy.

        :param statement: -

        return
        :return: true
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: "Policy") -> None:
        """Attaches a policy to this user.

        :param policy: -
        """
        return jsii.invoke(self, "attachInlinePolicy", [policy])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use."""
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> str:
        """An attribute that represents the user's ARN.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userArn")

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        """An attribute that represents the user name.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "userName")

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional["IManagedPolicy"]:
        """Returns the permissions boundary attached to this user."""
        return jsii.get(self, "permissionsBoundary")


@jsii.data_type(jsii_type="@aws-cdk/aws-iam.UserProps", jsii_struct_bases=[], name_mapping={'groups': 'groups', 'managed_policies': 'managedPolicies', 'password': 'password', 'password_reset_required': 'passwordResetRequired', 'path': 'path', 'permissions_boundary': 'permissionsBoundary', 'user_name': 'userName'})
class UserProps():
    def __init__(self, *, groups: typing.Optional[typing.List["IGroup"]]=None, managed_policies: typing.Optional[typing.List["IManagedPolicy"]]=None, password: typing.Optional[aws_cdk.core.SecretValue]=None, password_reset_required: typing.Optional[bool]=None, path: typing.Optional[str]=None, permissions_boundary: typing.Optional["IManagedPolicy"]=None, user_name: typing.Optional[str]=None):
        """
        :param groups: Groups to add this user to. You can also use ``addToGroup`` to add this user to a group. Default: - No groups.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param password: The password for the user. This is required so the user can access the AWS Management Console. You can use ``SecretValue.plainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - User won't be able to access the management console without a password.
        :param password_reset_required: Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console. If this is set to 'true', you must also specify "initialPassword". Default: false
        :param path: The path for the user name. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param user_name: A name for the IAM user. For valid values, see the UserName parameter for the CreateUser action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - Generated by CloudFormation (recommended)
        """
        self._values = {
        }
        if groups is not None: self._values["groups"] = groups
        if managed_policies is not None: self._values["managed_policies"] = managed_policies
        if password is not None: self._values["password"] = password
        if password_reset_required is not None: self._values["password_reset_required"] = password_reset_required
        if path is not None: self._values["path"] = path
        if permissions_boundary is not None: self._values["permissions_boundary"] = permissions_boundary
        if user_name is not None: self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        """Groups to add this user to.

        You can also use ``addToGroup`` to add this
        user to a group.

        default
        :default: - No groups.
        """
        return self._values.get('groups')

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List["IManagedPolicy"]]:
        """A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        default
        :default: - No managed policies.
        """
        return self._values.get('managed_policies')

    @builtins.property
    def password(self) -> typing.Optional[aws_cdk.core.SecretValue]:
        """The password for the user. This is required so the user can access the AWS Management Console.

        You can use ``SecretValue.plainText`` to specify a password in plain text or
        use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in
        Secrets Manager.

        default
        :default: - User won't be able to access the management console without a password.
        """
        return self._values.get('password')

    @builtins.property
    def password_reset_required(self) -> typing.Optional[bool]:
        """Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console.

        If this is set to 'true', you must also specify "initialPassword".

        default
        :default: false
        """
        return self._values.get('password_reset_required')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path for the user name.

        For more information about paths, see IAM
        Identifiers in the IAM User Guide.

        default
        :default: /
        """
        return self._values.get('path')

    @builtins.property
    def permissions_boundary(self) -> typing.Optional["IManagedPolicy"]:
        """AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        default
        :default: - No permissions boundary.

        link:
        :link:: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        """
        return self._values.get('permissions_boundary')

    @builtins.property
    def user_name(self) -> typing.Optional[str]:
        """A name for the IAM user.

        For valid values, see the UserName parameter for
        the CreateUser action in the IAM API Reference. If you don't specify a
        name, AWS CloudFormation generates a unique physical ID and uses that ID
        for the user name.

        If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        default
        :default: - Generated by CloudFormation (recommended)
        """
        return self._values.get('user_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AccountPrincipal", "AccountRootPrincipal", "AnyPrincipal", "Anyone", "ArnPrincipal", "CanonicalUserPrincipal", "CfnAccessKey", "CfnAccessKeyProps", "CfnGroup", "CfnGroupProps", "CfnInstanceProfile", "CfnInstanceProfileProps", "CfnManagedPolicy", "CfnManagedPolicyProps", "CfnPolicy", "CfnPolicyProps", "CfnRole", "CfnRoleProps", "CfnServiceLinkedRole", "CfnServiceLinkedRoleProps", "CfnUser", "CfnUserProps", "CfnUserToGroupAddition", "CfnUserToGroupAdditionProps", "CommonGrantOptions", "CompositePrincipal", "Effect", "FederatedPrincipal", "FromRoleArnOptions", "Grant", "GrantOnPrincipalAndResourceOptions", "GrantOnPrincipalOptions", "GrantWithResourceOptions", "Group", "GroupProps", "IGrantable", "IGroup", "IIdentity", "IManagedPolicy", "IPolicy", "IPrincipal", "IResourceWithPolicy", "IRole", "IUser", "LazyRole", "LazyRoleProps", "ManagedPolicy", "ManagedPolicyProps", "OrganizationPrincipal", "Policy", "PolicyDocument", "PolicyDocumentProps", "PolicyProps", "PolicyStatement", "PolicyStatementProps", "PrincipalBase", "PrincipalPolicyFragment", "Role", "RoleProps", "ServicePrincipal", "ServicePrincipalOpts", "UnknownPrincipal", "UnknownPrincipalProps", "User", "UserProps", "__jsii_assembly__"]

publication.publish()
