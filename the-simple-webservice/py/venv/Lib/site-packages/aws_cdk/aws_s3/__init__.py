"""
## Amazon S3 Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Define an unencrypted S3 bucket.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Bucket(self, "MyFirstBucket")
```

`Bucket` constructs expose the following deploy-time attributes:

* `bucketArn` - the ARN of the bucket (i.e. `arn:aws:s3:::bucket_name`)
* `bucketName` - the name of the bucket (i.e. `bucket_name`)
* `bucketWebsiteUrl` - the Website URL of the bucket (i.e.
  `http://bucket_name.s3-website-us-west-1.amazonaws.com`)
* `bucketDomainName` - the URL of the bucket (i.e. `bucket_name.s3.amazonaws.com`)
* `bucketDualStackDomainName` - the dual-stack URL of the bucket (i.e.
  `bucket_name.s3.dualstack.eu-west-1.amazonaws.com`)
* `bucketRegionalDomainName` - the regional URL of the bucket (i.e.
  `bucket_name.s3.eu-west-1.amazonaws.com`)
* `arnForObjects(pattern)` - the ARN of an object or objects within the bucket (i.e.
  `arn:aws:s3:::bucket_name/exampleobject.png` or
  `arn:aws:s3:::bucket_name/Development/*`)
* `urlForObject(key)` - the URL of an object within the bucket (i.e.
  `https://s3.cn-north-1.amazonaws.com.cn/china-bucket/mykey`)

### Encryption

Define a KMS-encrypted bucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyUnencryptedBucket",
    encryption=BucketEncryption.KMS
)

# you can access the encryption key:
assert(bucket.encryption_key instanceof kms.Key)
```

You can also supply your own key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_kms_key = kms.Key(self, "MyKey")

bucket = Bucket(self, "MyEncryptedBucket",
    encryption=BucketEncryption.KMS,
    encryption_key=my_kms_key
)

assert(bucket.encryption_key === my_kms_key)
```

Use `BucketEncryption.ManagedKms` to use the S3 master KMS key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "Buck",
    encryption=BucketEncryption.KMS_MANAGED
)

assert(bucket.encryption_key == null)
```

### Permissions

A bucket policy will be automatically created for the bucket upon the first call to
`addToResourcePolicy(statement)`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBucket")
bucket.add_to_resource_policy(iam.PolicyStatement(
    actions=["s3:GetObject"],
    resources=[bucket.arn_for_objects("file.txt")],
    principals=[iam.AccountRootPrincipal()]
))
```

Most of the time, you won't have to manipulate the bucket policy directly.
Instead, buckets have "grant" methods called to give prepackaged sets of permissions
to other resources. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda = lambda.Function(self, "Lambda")

bucket = Bucket(self, "MyBucket")
bucket.grant_read_write(lambda)
```

Will give the Lambda's execution role permissions to read and write
from the bucket.

### Sharing buckets between stacks

To use a bucket in a different stack in the same CDK application, pass the object to the other stack:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
#
# Stack that defines the bucket
#
class Producer(cdk.Stack):

    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags)

        bucket = s3.Bucket(self, "MyBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        self.my_bucket = bucket

#
# Stack that consumes the bucket
#
class Consumer(cdk.Stack):
    def __init__(self, scope, id, *, userBucket, description=None, env=None, stackName=None, tags=None):
        super().__init__(scope, id, userBucket=userBucket, description=description, env=env, stackName=stackName, tags=tags)

        user = iam.User(self, "MyUser")
        user_bucket.grant_read_write(user)

producer = Producer(app, "ProducerStack")
Consumer(app, "ConsumerStack", user_bucket=producer.my_bucket)
```

### Importing existing buckets

To import an existing bucket into your CDK application, use the `Bucket.fromBucketAttributes`
factory method. This method accepts `BucketAttributes` which describes the properties of an already
existing bucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket.from_bucket_attributes(self, "ImportedBucket",
    bucket_arn="arn:aws:s3:::my-bucket"
)

# now you can just call methods on the bucket
bucket.grant_read_write(user)
```

Alternatively, short-hand factories are available as `Bucket.fromBucketName` and
`Bucket.fromBucketArn`, which will derive all bucket attributes from the bucket
name or ARN respectively:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
by_name = Bucket.from_bucket_name(self, "BucketByName", "my-bucket")
by_arn = Bucket.from_bucket_arn(self, "BucketByArn", "arn:aws:s3:::my-bucket")
```

### Bucket Notifications

The Amazon S3 notification feature enables you to receive notifications when
certain events happen in your bucket as described under [S3 Bucket
Notifications](https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html) of the S3 Developer Guide.

To subscribe for bucket notifications, use the `bucket.addEventNotification` method. The
`bucket.addObjectCreatedNotification` and `bucket.addObjectRemovedNotification` can also be used for
these common use cases.

The following example will subscribe an SNS topic to be notified of all `s3:ObjectCreated:*` events:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3_notifications as s3n

my_topic = sns.Topic(self, "MyTopic")
bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.SnsDestination(topic))
```

This call will also ensure that the topic policy can accept notifications for
this specific bucket.

Supported S3 notification targets are exposed by the `@aws-cdk/aws-s3-notifications` package.

It is also possible to specify S3 object key filters when subscribing. The
following example will notify `myQueue` when objects prefixed with `foo/` and
have the `.jpg` suffix are removed from the bucket.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket.add_event_notification(s3.EventType.OBJECT_REMOVED,
    s3n.SqsDestination(my_queue), prefix="foo/", suffix=".jpg")
```

### Block Public Access

Use `blockPublicAccess` to specify [block public access settings](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html) on the bucket.

Enable all block public access settings:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBlockedBucket",
    block_public_access=BlockPublicAccess.BLOCK_ALL
)
```

Block and ignore public ACLs:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBlockedBucket",
    block_public_access=BlockPublicAccess.BLOCK_ACLS
)
```

Alternatively, specify the settings manually:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBlockedBucket",
    block_public_access=BlockPublicAccess(block_public_policy=True)
)
```

When `blockPublicPolicy` is set to `true`, `grantPublicRead()` throws an error.

### Logging configuration

Use `serverAccessLogsBucket` to describe where server access logs are to be stored.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
access_logs_bucket = Bucket(self, "AccessLogsBucket")

bucket = Bucket(self, "MyBucket",
    server_access_logs_bucket=access_logs_bucket
)
```

It's also possible to specify a prefix for Amazon S3 to assign to all log object keys.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBucket",
    server_access_logs_bucket=access_logs_bucket,
    server_access_logs_prefix="logs"
)
```

### Website redirection

You can use the two following properties to specify the bucket [redirection policy](https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html#advanced-conditional-redirects). Please note that these methods cannot both be applied to the same bucket.

#### Static redirection

You can statically redirect a to a given Bucket URL or any other host name with `websiteRedirect`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyRedirectedBucket",
    website_redirect={"host_name": "www.example.com"}
)
```

#### Routing rules

Alternatively, you can also define multiple `websiteRoutingRules`, to define complex, conditional redirections:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyRedirectedBucket",
    website_routing_rules=[{
        "host_name": "www.example.com",
        "http_redirect_code": "302",
        "protocol": RedirectProtocol.HTTPS,
        "replace_key": ReplaceKey.prefix_with("test/"),
        "condition": {
            "http_error_code_returned_equals": "200",
            "key_prefix_equals": "prefix"
        }
    }]
)
```

### Filling the bucket as part of deployment

To put files into a bucket as part of a deployment (for example, to host a
website), see the `@aws-cdk/aws-s3-deployment` package, which provides a
resource that can do just that.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3", "1.23.0", __name__, "aws-s3@1.23.0.jsii.tgz")


class BlockPublicAccess(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.BlockPublicAccess"):
    def __init__(self, *, block_public_acls: typing.Optional[bool]=None, block_public_policy: typing.Optional[bool]=None, ignore_public_acls: typing.Optional[bool]=None, restrict_public_buckets: typing.Optional[bool]=None) -> None:
        """
        :param block_public_acls: Whether to block public ACLs.
        :param block_public_policy: Whether to block public policy.
        :param ignore_public_acls: Whether to ignore public ACLs.
        :param restrict_public_buckets: Whether to restrict public access.
        """
        options = BlockPublicAccessOptions(block_public_acls=block_public_acls, block_public_policy=block_public_policy, ignore_public_acls=ignore_public_acls, restrict_public_buckets=restrict_public_buckets)

        jsii.create(BlockPublicAccess, self, [options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="BLOCK_ACLS")
    def BLOCK_ACLS(cls) -> "BlockPublicAccess":
        return jsii.sget(cls, "BLOCK_ACLS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="BLOCK_ALL")
    def BLOCK_ALL(cls) -> "BlockPublicAccess":
        return jsii.sget(cls, "BLOCK_ALL")

    @builtins.property
    @jsii.member(jsii_name="blockPublicAcls")
    def block_public_acls(self) -> typing.Optional[bool]:
        return jsii.get(self, "blockPublicAcls")

    @block_public_acls.setter
    def block_public_acls(self, value: typing.Optional[bool]):
        jsii.set(self, "blockPublicAcls", value)

    @builtins.property
    @jsii.member(jsii_name="blockPublicPolicy")
    def block_public_policy(self) -> typing.Optional[bool]:
        return jsii.get(self, "blockPublicPolicy")

    @block_public_policy.setter
    def block_public_policy(self, value: typing.Optional[bool]):
        jsii.set(self, "blockPublicPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="ignorePublicAcls")
    def ignore_public_acls(self) -> typing.Optional[bool]:
        return jsii.get(self, "ignorePublicAcls")

    @ignore_public_acls.setter
    def ignore_public_acls(self, value: typing.Optional[bool]):
        jsii.set(self, "ignorePublicAcls", value)

    @builtins.property
    @jsii.member(jsii_name="restrictPublicBuckets")
    def restrict_public_buckets(self) -> typing.Optional[bool]:
        return jsii.get(self, "restrictPublicBuckets")

    @restrict_public_buckets.setter
    def restrict_public_buckets(self, value: typing.Optional[bool]):
        jsii.set(self, "restrictPublicBuckets", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BlockPublicAccessOptions", jsii_struct_bases=[], name_mapping={'block_public_acls': 'blockPublicAcls', 'block_public_policy': 'blockPublicPolicy', 'ignore_public_acls': 'ignorePublicAcls', 'restrict_public_buckets': 'restrictPublicBuckets'})
class BlockPublicAccessOptions():
    def __init__(self, *, block_public_acls: typing.Optional[bool]=None, block_public_policy: typing.Optional[bool]=None, ignore_public_acls: typing.Optional[bool]=None, restrict_public_buckets: typing.Optional[bool]=None):
        """
        :param block_public_acls: Whether to block public ACLs.
        :param block_public_policy: Whether to block public policy.
        :param ignore_public_acls: Whether to ignore public ACLs.
        :param restrict_public_buckets: Whether to restrict public access.
        """
        self._values = {
        }
        if block_public_acls is not None: self._values["block_public_acls"] = block_public_acls
        if block_public_policy is not None: self._values["block_public_policy"] = block_public_policy
        if ignore_public_acls is not None: self._values["ignore_public_acls"] = ignore_public_acls
        if restrict_public_buckets is not None: self._values["restrict_public_buckets"] = restrict_public_buckets

    @builtins.property
    def block_public_acls(self) -> typing.Optional[bool]:
        """Whether to block public ACLs.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        """
        return self._values.get('block_public_acls')

    @builtins.property
    def block_public_policy(self) -> typing.Optional[bool]:
        """Whether to block public policy.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        """
        return self._values.get('block_public_policy')

    @builtins.property
    def ignore_public_acls(self) -> typing.Optional[bool]:
        """Whether to ignore public ACLs.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        """
        return self._values.get('ignore_public_acls')

    @builtins.property
    def restrict_public_buckets(self) -> typing.Optional[bool]:
        """Whether to restrict public access.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        """
        return self._values.get('restrict_public_buckets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BlockPublicAccessOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-s3.BucketAccessControl")
class BucketAccessControl(enum.Enum):
    """Default bucket access control types.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
    """
    PRIVATE = "PRIVATE"
    """Owner gets FULL_CONTROL.

    No one else has access rights.
    """
    PUBLIC_READ = "PUBLIC_READ"
    """Owner gets FULL_CONTROL.

    The AllUsers group gets READ access.
    """
    PUBLIC_READ_WRITE = "PUBLIC_READ_WRITE"
    """Owner gets FULL_CONTROL.

    The AllUsers group gets READ and WRITE access.
    Granting this on a bucket is generally not recommended.
    """
    AUTHENTICATED_READ = "AUTHENTICATED_READ"
    """Owner gets FULL_CONTROL.

    The AuthenticatedUsers group gets READ access.
    """
    LOG_DELIVERY_WRITE = "LOG_DELIVERY_WRITE"
    """The LogDelivery group gets WRITE and READ_ACP permissions on the bucket.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html
    """
    BUCKET_OWNER_READ = "BUCKET_OWNER_READ"
    """Object owner gets FULL_CONTROL.

    Bucket owner gets READ access.
    If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.
    """
    BUCKET_OWNER_FULL_CONTROL = "BUCKET_OWNER_FULL_CONTROL"
    """Both the object owner and the bucket owner get FULL_CONTROL over the object.

    If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.
    """
    AWS_EXEC_READ = "AWS_EXEC_READ"
    """Owner gets FULL_CONTROL.

    Amazon EC2 gets READ access to GET an Amazon Machine Image (AMI) bundle from Amazon S3.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketAttributes", jsii_struct_bases=[], name_mapping={'bucket_arn': 'bucketArn', 'bucket_domain_name': 'bucketDomainName', 'bucket_dual_stack_domain_name': 'bucketDualStackDomainName', 'bucket_name': 'bucketName', 'bucket_regional_domain_name': 'bucketRegionalDomainName', 'bucket_website_new_url_format': 'bucketWebsiteNewUrlFormat', 'bucket_website_url': 'bucketWebsiteUrl', 'encryption_key': 'encryptionKey'})
class BucketAttributes():
    def __init__(self, *, bucket_arn: typing.Optional[str]=None, bucket_domain_name: typing.Optional[str]=None, bucket_dual_stack_domain_name: typing.Optional[str]=None, bucket_name: typing.Optional[str]=None, bucket_regional_domain_name: typing.Optional[str]=None, bucket_website_new_url_format: typing.Optional[bool]=None, bucket_website_url: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None):
        """A reference to a bucket.

        The easiest way to instantiate is to call
        ``bucket.export()``. Then, the consumer can use ``Bucket.import(this, ref)`` and
        get a ``Bucket``.

        :param bucket_arn: The ARN of the bucket. At least one of bucketArn or bucketName must be defined in order to initialize a bucket ref.
        :param bucket_domain_name: The domain name of the bucket. Default: Inferred from bucket name
        :param bucket_dual_stack_domain_name: The IPv6 DNS name of the specified bucket.
        :param bucket_name: The name of the bucket. If the underlying value of ARN is a string, the name will be parsed from the ARN. Otherwise, the name is optional, but some features that require the bucket name such as auto-creating a bucket policy, won't work.
        :param bucket_regional_domain_name: The regional domain name of the specified bucket.
        :param bucket_website_new_url_format: The format of the website URL of the bucket. This should be true for regions launched since 2014. Default: false
        :param bucket_website_url: The website URL of the bucket (if static web hosting is enabled). Default: Inferred from bucket name
        :param encryption_key: 
        """
        self._values = {
        }
        if bucket_arn is not None: self._values["bucket_arn"] = bucket_arn
        if bucket_domain_name is not None: self._values["bucket_domain_name"] = bucket_domain_name
        if bucket_dual_stack_domain_name is not None: self._values["bucket_dual_stack_domain_name"] = bucket_dual_stack_domain_name
        if bucket_name is not None: self._values["bucket_name"] = bucket_name
        if bucket_regional_domain_name is not None: self._values["bucket_regional_domain_name"] = bucket_regional_domain_name
        if bucket_website_new_url_format is not None: self._values["bucket_website_new_url_format"] = bucket_website_new_url_format
        if bucket_website_url is not None: self._values["bucket_website_url"] = bucket_website_url
        if encryption_key is not None: self._values["encryption_key"] = encryption_key

    @builtins.property
    def bucket_arn(self) -> typing.Optional[str]:
        """The ARN of the bucket.

        At least one of bucketArn or bucketName must be
        defined in order to initialize a bucket ref.
        """
        return self._values.get('bucket_arn')

    @builtins.property
    def bucket_domain_name(self) -> typing.Optional[str]:
        """The domain name of the bucket.

        default
        :default: Inferred from bucket name
        """
        return self._values.get('bucket_domain_name')

    @builtins.property
    def bucket_dual_stack_domain_name(self) -> typing.Optional[str]:
        """The IPv6 DNS name of the specified bucket."""
        return self._values.get('bucket_dual_stack_domain_name')

    @builtins.property
    def bucket_name(self) -> typing.Optional[str]:
        """The name of the bucket.

        If the underlying value of ARN is a string, the
        name will be parsed from the ARN. Otherwise, the name is optional, but
        some features that require the bucket name such as auto-creating a bucket
        policy, won't work.
        """
        return self._values.get('bucket_name')

    @builtins.property
    def bucket_regional_domain_name(self) -> typing.Optional[str]:
        """The regional domain name of the specified bucket."""
        return self._values.get('bucket_regional_domain_name')

    @builtins.property
    def bucket_website_new_url_format(self) -> typing.Optional[bool]:
        """The format of the website URL of the bucket.

        This should be true for
        regions launched since 2014.

        default
        :default: false
        """
        return self._values.get('bucket_website_new_url_format')

    @builtins.property
    def bucket_website_url(self) -> typing.Optional[str]:
        """The website URL of the bucket (if static web hosting is enabled).

        default
        :default: Inferred from bucket name
        """
        return self._values.get('bucket_website_url')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        return self._values.get('encryption_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-s3.BucketEncryption")
class BucketEncryption(enum.Enum):
    """What kind of server-side encryption to apply to this bucket."""
    UNENCRYPTED = "UNENCRYPTED"
    """Objects in the bucket are not encrypted."""
    KMS_MANAGED = "KMS_MANAGED"
    """Server-side KMS encryption with a master key managed by KMS."""
    S3_MANAGED = "S3_MANAGED"
    """Server-side encryption with a master key managed by S3."""
    KMS = "KMS"
    """Server-side encryption with a KMS key managed by the user.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketMetrics", jsii_struct_bases=[], name_mapping={'id': 'id', 'prefix': 'prefix', 'tag_filters': 'tagFilters'})
class BucketMetrics():
    def __init__(self, *, id: str, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Mapping[str,typing.Any]]=None):
        """Specifies a metrics configuration for the CloudWatch request metrics from an Amazon S3 bucket.

        :param id: The ID used to identify the metrics configuration.
        :param prefix: The prefix that an object must have to be included in the metrics results.
        :param tag_filters: Specifies a list of tag filters to use as a metrics configuration filter. The metrics configuration includes only objects that meet the filter's criteria.
        """
        self._values = {
            'id': id,
        }
        if prefix is not None: self._values["prefix"] = prefix
        if tag_filters is not None: self._values["tag_filters"] = tag_filters

    @builtins.property
    def id(self) -> str:
        """The ID used to identify the metrics configuration."""
        return self._values.get('id')

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """The prefix that an object must have to be included in the metrics results."""
        return self._values.get('prefix')

    @builtins.property
    def tag_filters(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Specifies a list of tag filters to use as a metrics configuration filter.

        The metrics configuration includes only objects that meet the filter's criteria.
        """
        return self._values.get('tag_filters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketMetrics(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketNotificationDestinationConfig", jsii_struct_bases=[], name_mapping={'arn': 'arn', 'type': 'type', 'dependencies': 'dependencies'})
class BucketNotificationDestinationConfig():
    def __init__(self, *, arn: str, type: "BucketNotificationDestinationType", dependencies: typing.Optional[typing.List[aws_cdk.core.IDependable]]=None):
        """Represents the properties of a notification destination.

        :param arn: The ARN of the destination (i.e. Lambda, SNS, SQS).
        :param type: The notification type.
        :param dependencies: Any additional dependencies that should be resolved before the bucket notification can be configured (for example, the SNS Topic Policy resource).
        """
        self._values = {
            'arn': arn,
            'type': type,
        }
        if dependencies is not None: self._values["dependencies"] = dependencies

    @builtins.property
    def arn(self) -> str:
        """The ARN of the destination (i.e. Lambda, SNS, SQS)."""
        return self._values.get('arn')

    @builtins.property
    def type(self) -> "BucketNotificationDestinationType":
        """The notification type."""
        return self._values.get('type')

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[aws_cdk.core.IDependable]]:
        """Any additional dependencies that should be resolved before the bucket notification can be configured (for example, the SNS Topic Policy resource)."""
        return self._values.get('dependencies')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketNotificationDestinationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-s3.BucketNotificationDestinationType")
class BucketNotificationDestinationType(enum.Enum):
    """Supported types of notification destinations."""
    LAMBDA = "LAMBDA"
    QUEUE = "QUEUE"
    TOPIC = "TOPIC"

class BucketPolicy(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.BucketPolicy"):
    """Applies an Amazon S3 bucket policy to an Amazon S3 bucket."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bucket: "IBucket") -> None:
        """
        :param scope: -
        :param id: -
        :param bucket: The Amazon S3 bucket that the policy applies to.
        """
        props = BucketPolicyProps(bucket=bucket)

        jsii.create(BucketPolicy, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        """A policy document containing permissions to add to the specified bucket.

        For more information, see Access Policy Language Overview in the Amazon
        Simple Storage Service Developer Guide.
        """
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketPolicyProps", jsii_struct_bases=[], name_mapping={'bucket': 'bucket'})
class BucketPolicyProps():
    def __init__(self, *, bucket: "IBucket"):
        """
        :param bucket: The Amazon S3 bucket that the policy applies to.
        """
        self._values = {
            'bucket': bucket,
        }

    @builtins.property
    def bucket(self) -> "IBucket":
        """The Amazon S3 bucket that the policy applies to."""
        return self._values.get('bucket')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.BucketProps", jsii_struct_bases=[], name_mapping={'access_control': 'accessControl', 'block_public_access': 'blockPublicAccess', 'bucket_name': 'bucketName', 'cors': 'cors', 'encryption': 'encryption', 'encryption_key': 'encryptionKey', 'lifecycle_rules': 'lifecycleRules', 'metrics': 'metrics', 'public_read_access': 'publicReadAccess', 'removal_policy': 'removalPolicy', 'server_access_logs_bucket': 'serverAccessLogsBucket', 'server_access_logs_prefix': 'serverAccessLogsPrefix', 'versioned': 'versioned', 'website_error_document': 'websiteErrorDocument', 'website_index_document': 'websiteIndexDocument', 'website_redirect': 'websiteRedirect', 'website_routing_rules': 'websiteRoutingRules'})
class BucketProps():
    def __init__(self, *, access_control: typing.Optional["BucketAccessControl"]=None, block_public_access: typing.Optional["BlockPublicAccess"]=None, bucket_name: typing.Optional[str]=None, cors: typing.Optional[typing.List["CorsRule"]]=None, encryption: typing.Optional["BucketEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, metrics: typing.Optional[typing.List["BucketMetrics"]]=None, public_read_access: typing.Optional[bool]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, server_access_logs_bucket: typing.Optional["IBucket"]=None, server_access_logs_prefix: typing.Optional[str]=None, versioned: typing.Optional[bool]=None, website_error_document: typing.Optional[str]=None, website_index_document: typing.Optional[str]=None, website_redirect: typing.Optional["RedirectTarget"]=None, website_routing_rules: typing.Optional[typing.List["RoutingRule"]]=None):
        """
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param block_public_access: The block public access configuration of this bucket. Default: false New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access.
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - Access logs are disabled
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. Default: - No log file prefix
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.
        """
        if isinstance(website_redirect, dict): website_redirect = RedirectTarget(**website_redirect)
        self._values = {
        }
        if access_control is not None: self._values["access_control"] = access_control
        if block_public_access is not None: self._values["block_public_access"] = block_public_access
        if bucket_name is not None: self._values["bucket_name"] = bucket_name
        if cors is not None: self._values["cors"] = cors
        if encryption is not None: self._values["encryption"] = encryption
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if lifecycle_rules is not None: self._values["lifecycle_rules"] = lifecycle_rules
        if metrics is not None: self._values["metrics"] = metrics
        if public_read_access is not None: self._values["public_read_access"] = public_read_access
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if server_access_logs_bucket is not None: self._values["server_access_logs_bucket"] = server_access_logs_bucket
        if server_access_logs_prefix is not None: self._values["server_access_logs_prefix"] = server_access_logs_prefix
        if versioned is not None: self._values["versioned"] = versioned
        if website_error_document is not None: self._values["website_error_document"] = website_error_document
        if website_index_document is not None: self._values["website_index_document"] = website_index_document
        if website_redirect is not None: self._values["website_redirect"] = website_redirect
        if website_routing_rules is not None: self._values["website_routing_rules"] = website_routing_rules

    @builtins.property
    def access_control(self) -> typing.Optional["BucketAccessControl"]:
        """Specifies a canned ACL that grants predefined permissions to the bucket.

        default
        :default: BucketAccessControl.PRIVATE
        """
        return self._values.get('access_control')

    @builtins.property
    def block_public_access(self) -> typing.Optional["BlockPublicAccess"]:
        """The block public access configuration of this bucket.

        default
        :default:

        false New buckets and objects don't allow public access, but users can modify bucket
        policies or object permissions to allow public access.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
        """
        return self._values.get('block_public_access')

    @builtins.property
    def bucket_name(self) -> typing.Optional[str]:
        """Physical name of this bucket.

        default
        :default: - Assigned by CloudFormation (recommended).
        """
        return self._values.get('bucket_name')

    @builtins.property
    def cors(self) -> typing.Optional[typing.List["CorsRule"]]:
        """The CORS configuration of this bucket.

        default
        :default: - No CORS configuration.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
        """
        return self._values.get('cors')

    @builtins.property
    def encryption(self) -> typing.Optional["BucketEncryption"]:
        """The kind of server-side encryption to apply to this bucket.

        If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
        encryption key is not specified, a key will automatically be created.

        default
        :default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        """
        return self._values.get('encryption')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """External KMS key to use for bucket encryption.

        The 'encryption' property must be either not specified or set to "Kms".
        An error will be emitted if encryption is set to "Unencrypted" or
        "Managed".

        default
        :default:

        - If encryption is set to "Kms" and this property is undefined,
          a new KMS key will be created and associated with this bucket.
        """
        return self._values.get('encryption_key')

    @builtins.property
    def lifecycle_rules(self) -> typing.Optional[typing.List["LifecycleRule"]]:
        """Rules that define how Amazon S3 manages objects during their lifetime.

        default
        :default: - No lifecycle rules.
        """
        return self._values.get('lifecycle_rules')

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List["BucketMetrics"]]:
        """The metrics configuration of this bucket.

        default
        :default: - No metrics configuration.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html
        """
        return self._values.get('metrics')

    @builtins.property
    def public_read_access(self) -> typing.Optional[bool]:
        """Grants public read access to all objects in the bucket.

        Similar to calling ``bucket.grantPublicAccess()``

        default
        :default: false
        """
        return self._values.get('public_read_access')

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """Policy to apply when the bucket is removed from this stack.

        default
        :default: - The bucket will be orphaned.
        """
        return self._values.get('removal_policy')

    @builtins.property
    def server_access_logs_bucket(self) -> typing.Optional["IBucket"]:
        """Destination bucket for the server access logs.

        default
        :default: - Access logs are disabled
        """
        return self._values.get('server_access_logs_bucket')

    @builtins.property
    def server_access_logs_prefix(self) -> typing.Optional[str]:
        """Optional log file prefix to use for the bucket's access logs.

        default
        :default: - No log file prefix
        """
        return self._values.get('server_access_logs_prefix')

    @builtins.property
    def versioned(self) -> typing.Optional[bool]:
        """Whether this bucket should have versioning turned on or not.

        default
        :default: false
        """
        return self._values.get('versioned')

    @builtins.property
    def website_error_document(self) -> typing.Optional[str]:
        """The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set.

        default
        :default: - No error document.
        """
        return self._values.get('website_error_document')

    @builtins.property
    def website_index_document(self) -> typing.Optional[str]:
        """The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket.

        default
        :default: - No index document.
        """
        return self._values.get('website_index_document')

    @builtins.property
    def website_redirect(self) -> typing.Optional["RedirectTarget"]:
        """Specifies the redirect behavior of all requests to a website endpoint of a bucket.

        If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules".

        default
        :default: - No redirection.
        """
        return self._values.get('website_redirect')

    @builtins.property
    def website_routing_rules(self) -> typing.Optional[typing.List["RoutingRule"]]:
        """Rules that define when a redirect is applied and the redirect behavior.

        default
        :default: - No redirection rules.
        """
        return self._values.get('website_routing_rules')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccessPoint(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.CfnAccessPoint"):
    """A CloudFormation ``AWS::S3::AccessPoint``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html
    cloudformationResource:
    :cloudformationResource:: AWS::S3::AccessPoint
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bucket: str, creation_date: typing.Optional[str]=None, name: typing.Optional[str]=None, network_origin: typing.Optional[str]=None, policy: typing.Any=None, policy_status: typing.Any=None, public_access_block_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PublicAccessBlockConfigurationProperty"]]]=None, vpc_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::S3::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket: ``AWS::S3::AccessPoint.Bucket``.
        :param creation_date: ``AWS::S3::AccessPoint.CreationDate``.
        :param name: ``AWS::S3::AccessPoint.Name``.
        :param network_origin: ``AWS::S3::AccessPoint.NetworkOrigin``.
        :param policy: ``AWS::S3::AccessPoint.Policy``.
        :param policy_status: ``AWS::S3::AccessPoint.PolicyStatus``.
        :param public_access_block_configuration: ``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.
        :param vpc_configuration: ``AWS::S3::AccessPoint.VpcConfiguration``.
        """
        props = CfnAccessPointProps(bucket=bucket, creation_date=creation_date, name=name, network_origin=network_origin, policy=policy, policy_status=policy_status, public_access_block_configuration=public_access_block_configuration, vpc_configuration=vpc_configuration)

        jsii.create(CfnAccessPoint, self, [scope, id, props])

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
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> str:
        """``AWS::S3::AccessPoint.Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-bucket
        """
        return jsii.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: str):
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        """``AWS::S3::AccessPoint.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policy
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Any):
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="policyStatus")
    def policy_status(self) -> typing.Any:
        """``AWS::S3::AccessPoint.PolicyStatus``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policystatus
        """
        return jsii.get(self, "policyStatus")

    @policy_status.setter
    def policy_status(self, value: typing.Any):
        jsii.set(self, "policyStatus", value)

    @builtins.property
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> typing.Optional[str]:
        """``AWS::S3::AccessPoint.CreationDate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-creationdate
        """
        return jsii.get(self, "creationDate")

    @creation_date.setter
    def creation_date(self, value: typing.Optional[str]):
        jsii.set(self, "creationDate", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::S3::AccessPoint.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkOrigin")
    def network_origin(self) -> typing.Optional[str]:
        """``AWS::S3::AccessPoint.NetworkOrigin``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-networkorigin
        """
        return jsii.get(self, "networkOrigin")

    @network_origin.setter
    def network_origin(self, value: typing.Optional[str]):
        jsii.set(self, "networkOrigin", value)

    @builtins.property
    @jsii.member(jsii_name="publicAccessBlockConfiguration")
    def public_access_block_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PublicAccessBlockConfigurationProperty"]]]:
        """``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-publicaccessblockconfiguration
        """
        return jsii.get(self, "publicAccessBlockConfiguration")

    @public_access_block_configuration.setter
    def public_access_block_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PublicAccessBlockConfigurationProperty"]]]):
        jsii.set(self, "publicAccessBlockConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfiguration")
    def vpc_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigurationProperty"]]]:
        """``AWS::S3::AccessPoint.VpcConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-vpcconfiguration
        """
        return jsii.get(self, "vpcConfiguration")

    @vpc_configuration.setter
    def vpc_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigurationProperty"]]]):
        jsii.set(self, "vpcConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnAccessPoint.PublicAccessBlockConfigurationProperty", jsii_struct_bases=[], name_mapping={'block_public_acls': 'blockPublicAcls', 'block_public_policy': 'blockPublicPolicy', 'ignore_public_acls': 'ignorePublicAcls', 'restrict_public_buckets': 'restrictPublicBuckets'})
    class PublicAccessBlockConfigurationProperty():
        def __init__(self, *, block_public_acls: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, block_public_policy: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ignore_public_acls: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, restrict_public_buckets: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param block_public_acls: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.
            :param block_public_policy: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.
            :param ignore_public_acls: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.
            :param restrict_public_buckets: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html
            """
            self._values = {
            }
            if block_public_acls is not None: self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None: self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None: self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None: self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-blockpublicacls
            """
            return self._values.get('block_public_acls')

        @builtins.property
        def block_public_policy(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-blockpublicpolicy
            """
            return self._values.get('block_public_policy')

        @builtins.property
        def ignore_public_acls(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnAccessPoint.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-ignorepublicacls
            """
            return self._values.get('ignore_public_acls')

        @builtins.property
        def restrict_public_buckets(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnAccessPoint.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-restrictpublicbuckets
            """
            return self._values.get('restrict_public_buckets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PublicAccessBlockConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnAccessPoint.VpcConfigurationProperty", jsii_struct_bases=[], name_mapping={'vpc_id': 'vpcId'})
    class VpcConfigurationProperty():
        def __init__(self, *, vpc_id: typing.Optional[str]=None):
            """
            :param vpc_id: ``CfnAccessPoint.VpcConfigurationProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-vpcconfiguration.html
            """
            self._values = {
            }
            if vpc_id is not None: self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[str]:
            """``CfnAccessPoint.VpcConfigurationProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-vpcconfiguration.html#cfn-s3-accesspoint-vpcconfiguration-vpcid
            """
            return self._values.get('vpc_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VpcConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnAccessPointProps", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'creation_date': 'creationDate', 'name': 'name', 'network_origin': 'networkOrigin', 'policy': 'policy', 'policy_status': 'policyStatus', 'public_access_block_configuration': 'publicAccessBlockConfiguration', 'vpc_configuration': 'vpcConfiguration'})
class CfnAccessPointProps():
    def __init__(self, *, bucket: str, creation_date: typing.Optional[str]=None, name: typing.Optional[str]=None, network_origin: typing.Optional[str]=None, policy: typing.Any=None, policy_status: typing.Any=None, public_access_block_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAccessPoint.PublicAccessBlockConfigurationProperty"]]]=None, vpc_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAccessPoint.VpcConfigurationProperty"]]]=None):
        """Properties for defining a ``AWS::S3::AccessPoint``.

        :param bucket: ``AWS::S3::AccessPoint.Bucket``.
        :param creation_date: ``AWS::S3::AccessPoint.CreationDate``.
        :param name: ``AWS::S3::AccessPoint.Name``.
        :param network_origin: ``AWS::S3::AccessPoint.NetworkOrigin``.
        :param policy: ``AWS::S3::AccessPoint.Policy``.
        :param policy_status: ``AWS::S3::AccessPoint.PolicyStatus``.
        :param public_access_block_configuration: ``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.
        :param vpc_configuration: ``AWS::S3::AccessPoint.VpcConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html
        """
        self._values = {
            'bucket': bucket,
        }
        if creation_date is not None: self._values["creation_date"] = creation_date
        if name is not None: self._values["name"] = name
        if network_origin is not None: self._values["network_origin"] = network_origin
        if policy is not None: self._values["policy"] = policy
        if policy_status is not None: self._values["policy_status"] = policy_status
        if public_access_block_configuration is not None: self._values["public_access_block_configuration"] = public_access_block_configuration
        if vpc_configuration is not None: self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def bucket(self) -> str:
        """``AWS::S3::AccessPoint.Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-bucket
        """
        return self._values.get('bucket')

    @builtins.property
    def creation_date(self) -> typing.Optional[str]:
        """``AWS::S3::AccessPoint.CreationDate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-creationdate
        """
        return self._values.get('creation_date')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::S3::AccessPoint.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-name
        """
        return self._values.get('name')

    @builtins.property
    def network_origin(self) -> typing.Optional[str]:
        """``AWS::S3::AccessPoint.NetworkOrigin``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-networkorigin
        """
        return self._values.get('network_origin')

    @builtins.property
    def policy(self) -> typing.Any:
        """``AWS::S3::AccessPoint.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policy
        """
        return self._values.get('policy')

    @builtins.property
    def policy_status(self) -> typing.Any:
        """``AWS::S3::AccessPoint.PolicyStatus``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policystatus
        """
        return self._values.get('policy_status')

    @builtins.property
    def public_access_block_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAccessPoint.PublicAccessBlockConfigurationProperty"]]]:
        """``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-publicaccessblockconfiguration
        """
        return self._values.get('public_access_block_configuration')

    @builtins.property
    def vpc_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAccessPoint.VpcConfigurationProperty"]]]:
        """``AWS::S3::AccessPoint.VpcConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-vpcconfiguration
        """
        return self._values.get('vpc_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAccessPointProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnBucket(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.CfnBucket"):
    """A CloudFormation ``AWS::S3::Bucket``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html
    cloudformationResource:
    :cloudformationResource:: AWS::S3::Bucket
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, accelerate_configuration: typing.Optional[typing.Union[typing.Optional["AccelerateConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, access_control: typing.Optional[str]=None, analytics_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AnalyticsConfigurationProperty"]]]]]=None, bucket_encryption: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["BucketEncryptionProperty"]]]=None, bucket_name: typing.Optional[str]=None, cors_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CorsConfigurationProperty"]]]=None, inventory_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "InventoryConfigurationProperty"]]]]]=None, lifecycle_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LifecycleConfigurationProperty"]]]=None, logging_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoggingConfigurationProperty"]]]=None, metrics_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricsConfigurationProperty"]]]]]=None, notification_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationConfigurationProperty"]]]=None, object_lock_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ObjectLockConfigurationProperty"]]]=None, object_lock_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, public_access_block_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PublicAccessBlockConfigurationProperty"]]]=None, replication_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ReplicationConfigurationProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, versioning_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VersioningConfigurationProperty"]]]=None, website_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["WebsiteConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::S3::Bucket``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accelerate_configuration: ``AWS::S3::Bucket.AccelerateConfiguration``.
        :param access_control: ``AWS::S3::Bucket.AccessControl``.
        :param analytics_configurations: ``AWS::S3::Bucket.AnalyticsConfigurations``.
        :param bucket_encryption: ``AWS::S3::Bucket.BucketEncryption``.
        :param bucket_name: ``AWS::S3::Bucket.BucketName``.
        :param cors_configuration: ``AWS::S3::Bucket.CorsConfiguration``.
        :param inventory_configurations: ``AWS::S3::Bucket.InventoryConfigurations``.
        :param lifecycle_configuration: ``AWS::S3::Bucket.LifecycleConfiguration``.
        :param logging_configuration: ``AWS::S3::Bucket.LoggingConfiguration``.
        :param metrics_configurations: ``AWS::S3::Bucket.MetricsConfigurations``.
        :param notification_configuration: ``AWS::S3::Bucket.NotificationConfiguration``.
        :param object_lock_configuration: ``AWS::S3::Bucket.ObjectLockConfiguration``.
        :param object_lock_enabled: ``AWS::S3::Bucket.ObjectLockEnabled``.
        :param public_access_block_configuration: ``AWS::S3::Bucket.PublicAccessBlockConfiguration``.
        :param replication_configuration: ``AWS::S3::Bucket.ReplicationConfiguration``.
        :param tags: ``AWS::S3::Bucket.Tags``.
        :param versioning_configuration: ``AWS::S3::Bucket.VersioningConfiguration``.
        :param website_configuration: ``AWS::S3::Bucket.WebsiteConfiguration``.
        """
        props = CfnBucketProps(accelerate_configuration=accelerate_configuration, access_control=access_control, analytics_configurations=analytics_configurations, bucket_encryption=bucket_encryption, bucket_name=bucket_name, cors_configuration=cors_configuration, inventory_configurations=inventory_configurations, lifecycle_configuration=lifecycle_configuration, logging_configuration=logging_configuration, metrics_configurations=metrics_configurations, notification_configuration=notification_configuration, object_lock_configuration=object_lock_configuration, object_lock_enabled=object_lock_enabled, public_access_block_configuration=public_access_block_configuration, replication_configuration=replication_configuration, tags=tags, versioning_configuration=versioning_configuration, website_configuration=website_configuration)

        jsii.create(CfnBucket, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DomainName
        """
        return jsii.get(self, "attrDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrDualStackDomainName")
    def attr_dual_stack_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DualStackDomainName
        """
        return jsii.get(self, "attrDualStackDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalDomainName
        """
        return jsii.get(self, "attrRegionalDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrWebsiteUrl")
    def attr_website_url(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: WebsiteURL
        """
        return jsii.get(self, "attrWebsiteUrl")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::S3::Bucket.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="accelerateConfiguration")
    def accelerate_configuration(self) -> typing.Optional[typing.Union[typing.Optional["AccelerateConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::S3::Bucket.AccelerateConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accelerateconfiguration
        """
        return jsii.get(self, "accelerateConfiguration")

    @accelerate_configuration.setter
    def accelerate_configuration(self, value: typing.Optional[typing.Union[typing.Optional["AccelerateConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "accelerateConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="accessControl")
    def access_control(self) -> typing.Optional[str]:
        """``AWS::S3::Bucket.AccessControl``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accesscontrol
        """
        return jsii.get(self, "accessControl")

    @access_control.setter
    def access_control(self, value: typing.Optional[str]):
        jsii.set(self, "accessControl", value)

    @builtins.property
    @jsii.member(jsii_name="analyticsConfigurations")
    def analytics_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AnalyticsConfigurationProperty"]]]]]:
        """``AWS::S3::Bucket.AnalyticsConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-analyticsconfigurations
        """
        return jsii.get(self, "analyticsConfigurations")

    @analytics_configurations.setter
    def analytics_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AnalyticsConfigurationProperty"]]]]]):
        jsii.set(self, "analyticsConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="bucketEncryption")
    def bucket_encryption(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["BucketEncryptionProperty"]]]:
        """``AWS::S3::Bucket.BucketEncryption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-bucketencryption
        """
        return jsii.get(self, "bucketEncryption")

    @bucket_encryption.setter
    def bucket_encryption(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["BucketEncryptionProperty"]]]):
        jsii.set(self, "bucketEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> typing.Optional[str]:
        """``AWS::S3::Bucket.BucketName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-name
        """
        return jsii.get(self, "bucketName")

    @bucket_name.setter
    def bucket_name(self, value: typing.Optional[str]):
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CorsConfigurationProperty"]]]:
        """``AWS::S3::Bucket.CorsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-crossoriginconfig
        """
        return jsii.get(self, "corsConfiguration")

    @cors_configuration.setter
    def cors_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CorsConfigurationProperty"]]]):
        jsii.set(self, "corsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="inventoryConfigurations")
    def inventory_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "InventoryConfigurationProperty"]]]]]:
        """``AWS::S3::Bucket.InventoryConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-inventoryconfigurations
        """
        return jsii.get(self, "inventoryConfigurations")

    @inventory_configurations.setter
    def inventory_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "InventoryConfigurationProperty"]]]]]):
        jsii.set(self, "inventoryConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfiguration")
    def lifecycle_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LifecycleConfigurationProperty"]]]:
        """``AWS::S3::Bucket.LifecycleConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-lifecycleconfig
        """
        return jsii.get(self, "lifecycleConfiguration")

    @lifecycle_configuration.setter
    def lifecycle_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LifecycleConfigurationProperty"]]]):
        jsii.set(self, "lifecycleConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoggingConfigurationProperty"]]]:
        """``AWS::S3::Bucket.LoggingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-loggingconfig
        """
        return jsii.get(self, "loggingConfiguration")

    @logging_configuration.setter
    def logging_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoggingConfigurationProperty"]]]):
        jsii.set(self, "loggingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="metricsConfigurations")
    def metrics_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricsConfigurationProperty"]]]]]:
        """``AWS::S3::Bucket.MetricsConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-metricsconfigurations
        """
        return jsii.get(self, "metricsConfigurations")

    @metrics_configurations.setter
    def metrics_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricsConfigurationProperty"]]]]]):
        jsii.set(self, "metricsConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="notificationConfiguration")
    def notification_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationConfigurationProperty"]]]:
        """``AWS::S3::Bucket.NotificationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-notification
        """
        return jsii.get(self, "notificationConfiguration")

    @notification_configuration.setter
    def notification_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationConfigurationProperty"]]]):
        jsii.set(self, "notificationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="objectLockConfiguration")
    def object_lock_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ObjectLockConfigurationProperty"]]]:
        """``AWS::S3::Bucket.ObjectLockConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockconfiguration
        """
        return jsii.get(self, "objectLockConfiguration")

    @object_lock_configuration.setter
    def object_lock_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ObjectLockConfigurationProperty"]]]):
        jsii.set(self, "objectLockConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="objectLockEnabled")
    def object_lock_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::S3::Bucket.ObjectLockEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockenabled
        """
        return jsii.get(self, "objectLockEnabled")

    @object_lock_enabled.setter
    def object_lock_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "objectLockEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="publicAccessBlockConfiguration")
    def public_access_block_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PublicAccessBlockConfigurationProperty"]]]:
        """``AWS::S3::Bucket.PublicAccessBlockConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-publicaccessblockconfiguration
        """
        return jsii.get(self, "publicAccessBlockConfiguration")

    @public_access_block_configuration.setter
    def public_access_block_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PublicAccessBlockConfigurationProperty"]]]):
        jsii.set(self, "publicAccessBlockConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="replicationConfiguration")
    def replication_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ReplicationConfigurationProperty"]]]:
        """``AWS::S3::Bucket.ReplicationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-replicationconfiguration
        """
        return jsii.get(self, "replicationConfiguration")

    @replication_configuration.setter
    def replication_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ReplicationConfigurationProperty"]]]):
        jsii.set(self, "replicationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="versioningConfiguration")
    def versioning_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VersioningConfigurationProperty"]]]:
        """``AWS::S3::Bucket.VersioningConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-versioning
        """
        return jsii.get(self, "versioningConfiguration")

    @versioning_configuration.setter
    def versioning_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VersioningConfigurationProperty"]]]):
        jsii.set(self, "versioningConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="websiteConfiguration")
    def website_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["WebsiteConfigurationProperty"]]]:
        """``AWS::S3::Bucket.WebsiteConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-websiteconfiguration
        """
        return jsii.get(self, "websiteConfiguration")

    @website_configuration.setter
    def website_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["WebsiteConfigurationProperty"]]]):
        jsii.set(self, "websiteConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AbortIncompleteMultipartUploadProperty", jsii_struct_bases=[], name_mapping={'days_after_initiation': 'daysAfterInitiation'})
    class AbortIncompleteMultipartUploadProperty():
        def __init__(self, *, days_after_initiation: jsii.Number):
            """
            :param days_after_initiation: ``CfnBucket.AbortIncompleteMultipartUploadProperty.DaysAfterInitiation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-abortincompletemultipartupload.html
            """
            self._values = {
                'days_after_initiation': days_after_initiation,
            }

        @builtins.property
        def days_after_initiation(self) -> jsii.Number:
            """``CfnBucket.AbortIncompleteMultipartUploadProperty.DaysAfterInitiation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-abortincompletemultipartupload.html#cfn-s3-bucket-abortincompletemultipartupload-daysafterinitiation
            """
            return self._values.get('days_after_initiation')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AbortIncompleteMultipartUploadProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AccelerateConfigurationProperty", jsii_struct_bases=[], name_mapping={'acceleration_status': 'accelerationStatus'})
    class AccelerateConfigurationProperty():
        def __init__(self, *, acceleration_status: str):
            """
            :param acceleration_status: ``CfnBucket.AccelerateConfigurationProperty.AccelerationStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accelerateconfiguration.html
            """
            self._values = {
                'acceleration_status': acceleration_status,
            }

        @builtins.property
        def acceleration_status(self) -> str:
            """``CfnBucket.AccelerateConfigurationProperty.AccelerationStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accelerateconfiguration.html#cfn-s3-bucket-accelerateconfiguration-accelerationstatus
            """
            return self._values.get('acceleration_status')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccelerateConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AccessControlTranslationProperty", jsii_struct_bases=[], name_mapping={'owner': 'owner'})
    class AccessControlTranslationProperty():
        def __init__(self, *, owner: str):
            """
            :param owner: ``CfnBucket.AccessControlTranslationProperty.Owner``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accesscontroltranslation.html
            """
            self._values = {
                'owner': owner,
            }

        @builtins.property
        def owner(self) -> str:
            """``CfnBucket.AccessControlTranslationProperty.Owner``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accesscontroltranslation.html#cfn-s3-bucket-accesscontroltranslation-owner
            """
            return self._values.get('owner')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessControlTranslationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.AnalyticsConfigurationProperty", jsii_struct_bases=[], name_mapping={'id': 'id', 'storage_class_analysis': 'storageClassAnalysis', 'prefix': 'prefix', 'tag_filters': 'tagFilters'})
    class AnalyticsConfigurationProperty():
        def __init__(self, *, id: str, storage_class_analysis: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.StorageClassAnalysisProperty"], prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TagFilterProperty"]]]]]=None):
            """
            :param id: ``CfnBucket.AnalyticsConfigurationProperty.Id``.
            :param storage_class_analysis: ``CfnBucket.AnalyticsConfigurationProperty.StorageClassAnalysis``.
            :param prefix: ``CfnBucket.AnalyticsConfigurationProperty.Prefix``.
            :param tag_filters: ``CfnBucket.AnalyticsConfigurationProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html
            """
            self._values = {
                'id': id,
                'storage_class_analysis': storage_class_analysis,
            }
            if prefix is not None: self._values["prefix"] = prefix
            if tag_filters is not None: self._values["tag_filters"] = tag_filters

        @builtins.property
        def id(self) -> str:
            """``CfnBucket.AnalyticsConfigurationProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-id
            """
            return self._values.get('id')

        @builtins.property
        def storage_class_analysis(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.StorageClassAnalysisProperty"]:
            """``CfnBucket.AnalyticsConfigurationProperty.StorageClassAnalysis``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-storageclassanalysis
            """
            return self._values.get('storage_class_analysis')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnBucket.AnalyticsConfigurationProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TagFilterProperty"]]]]]:
            """``CfnBucket.AnalyticsConfigurationProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-tagfilters
            """
            return self._values.get('tag_filters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AnalyticsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.BucketEncryptionProperty", jsii_struct_bases=[], name_mapping={'server_side_encryption_configuration': 'serverSideEncryptionConfiguration'})
    class BucketEncryptionProperty():
        def __init__(self, *, server_side_encryption_configuration: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.ServerSideEncryptionRuleProperty"]]]):
            """
            :param server_side_encryption_configuration: ``CfnBucket.BucketEncryptionProperty.ServerSideEncryptionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-bucketencryption.html
            """
            self._values = {
                'server_side_encryption_configuration': server_side_encryption_configuration,
            }

        @builtins.property
        def server_side_encryption_configuration(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.ServerSideEncryptionRuleProperty"]]]:
            """``CfnBucket.BucketEncryptionProperty.ServerSideEncryptionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-bucketencryption.html#cfn-s3-bucket-bucketencryption-serversideencryptionconfiguration
            """
            return self._values.get('server_side_encryption_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BucketEncryptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.CorsConfigurationProperty", jsii_struct_bases=[], name_mapping={'cors_rules': 'corsRules'})
    class CorsConfigurationProperty():
        def __init__(self, *, cors_rules: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.CorsRuleProperty"]]]):
            """
            :param cors_rules: ``CfnBucket.CorsConfigurationProperty.CorsRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
            """
            self._values = {
                'cors_rules': cors_rules,
            }

        @builtins.property
        def cors_rules(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.CorsRuleProperty"]]]:
            """``CfnBucket.CorsConfigurationProperty.CorsRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html#cfn-s3-bucket-cors-corsrule
            """
            return self._values.get('cors_rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CorsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.CorsRuleProperty", jsii_struct_bases=[], name_mapping={'allowed_methods': 'allowedMethods', 'allowed_origins': 'allowedOrigins', 'allowed_headers': 'allowedHeaders', 'exposed_headers': 'exposedHeaders', 'id': 'id', 'max_age': 'maxAge'})
    class CorsRuleProperty():
        def __init__(self, *, allowed_methods: typing.List[str], allowed_origins: typing.List[str], allowed_headers: typing.Optional[typing.List[str]]=None, exposed_headers: typing.Optional[typing.List[str]]=None, id: typing.Optional[str]=None, max_age: typing.Optional[jsii.Number]=None):
            """
            :param allowed_methods: ``CfnBucket.CorsRuleProperty.AllowedMethods``.
            :param allowed_origins: ``CfnBucket.CorsRuleProperty.AllowedOrigins``.
            :param allowed_headers: ``CfnBucket.CorsRuleProperty.AllowedHeaders``.
            :param exposed_headers: ``CfnBucket.CorsRuleProperty.ExposedHeaders``.
            :param id: ``CfnBucket.CorsRuleProperty.Id``.
            :param max_age: ``CfnBucket.CorsRuleProperty.MaxAge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html
            """
            self._values = {
                'allowed_methods': allowed_methods,
                'allowed_origins': allowed_origins,
            }
            if allowed_headers is not None: self._values["allowed_headers"] = allowed_headers
            if exposed_headers is not None: self._values["exposed_headers"] = exposed_headers
            if id is not None: self._values["id"] = id
            if max_age is not None: self._values["max_age"] = max_age

        @builtins.property
        def allowed_methods(self) -> typing.List[str]:
            """``CfnBucket.CorsRuleProperty.AllowedMethods``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-allowedmethods
            """
            return self._values.get('allowed_methods')

        @builtins.property
        def allowed_origins(self) -> typing.List[str]:
            """``CfnBucket.CorsRuleProperty.AllowedOrigins``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-allowedorigins
            """
            return self._values.get('allowed_origins')

        @builtins.property
        def allowed_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnBucket.CorsRuleProperty.AllowedHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-allowedheaders
            """
            return self._values.get('allowed_headers')

        @builtins.property
        def exposed_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnBucket.CorsRuleProperty.ExposedHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-exposedheaders
            """
            return self._values.get('exposed_headers')

        @builtins.property
        def id(self) -> typing.Optional[str]:
            """``CfnBucket.CorsRuleProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-id
            """
            return self._values.get('id')

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            """``CfnBucket.CorsRuleProperty.MaxAge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-maxage
            """
            return self._values.get('max_age')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CorsRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.DataExportProperty", jsii_struct_bases=[], name_mapping={'destination': 'destination', 'output_schema_version': 'outputSchemaVersion'})
    class DataExportProperty():
        def __init__(self, *, destination: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.DestinationProperty"], output_schema_version: str):
            """
            :param destination: ``CfnBucket.DataExportProperty.Destination``.
            :param output_schema_version: ``CfnBucket.DataExportProperty.OutputSchemaVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html
            """
            self._values = {
                'destination': destination,
                'output_schema_version': output_schema_version,
            }

        @builtins.property
        def destination(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.DestinationProperty"]:
            """``CfnBucket.DataExportProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html#cfn-s3-bucket-dataexport-destination
            """
            return self._values.get('destination')

        @builtins.property
        def output_schema_version(self) -> str:
            """``CfnBucket.DataExportProperty.OutputSchemaVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html#cfn-s3-bucket-dataexport-outputschemaversion
            """
            return self._values.get('output_schema_version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DataExportProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.DefaultRetentionProperty", jsii_struct_bases=[], name_mapping={'days': 'days', 'mode': 'mode', 'years': 'years'})
    class DefaultRetentionProperty():
        def __init__(self, *, days: typing.Optional[jsii.Number]=None, mode: typing.Optional[str]=None, years: typing.Optional[jsii.Number]=None):
            """
            :param days: ``CfnBucket.DefaultRetentionProperty.Days``.
            :param mode: ``CfnBucket.DefaultRetentionProperty.Mode``.
            :param years: ``CfnBucket.DefaultRetentionProperty.Years``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html
            """
            self._values = {
            }
            if days is not None: self._values["days"] = days
            if mode is not None: self._values["mode"] = mode
            if years is not None: self._values["years"] = years

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            """``CfnBucket.DefaultRetentionProperty.Days``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-days
            """
            return self._values.get('days')

        @builtins.property
        def mode(self) -> typing.Optional[str]:
            """``CfnBucket.DefaultRetentionProperty.Mode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-mode
            """
            return self._values.get('mode')

        @builtins.property
        def years(self) -> typing.Optional[jsii.Number]:
            """``CfnBucket.DefaultRetentionProperty.Years``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-years
            """
            return self._values.get('years')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DefaultRetentionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.DestinationProperty", jsii_struct_bases=[], name_mapping={'bucket_arn': 'bucketArn', 'format': 'format', 'bucket_account_id': 'bucketAccountId', 'prefix': 'prefix'})
    class DestinationProperty():
        def __init__(self, *, bucket_arn: str, format: str, bucket_account_id: typing.Optional[str]=None, prefix: typing.Optional[str]=None):
            """
            :param bucket_arn: ``CfnBucket.DestinationProperty.BucketArn``.
            :param format: ``CfnBucket.DestinationProperty.Format``.
            :param bucket_account_id: ``CfnBucket.DestinationProperty.BucketAccountId``.
            :param prefix: ``CfnBucket.DestinationProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html
            """
            self._values = {
                'bucket_arn': bucket_arn,
                'format': format,
            }
            if bucket_account_id is not None: self._values["bucket_account_id"] = bucket_account_id
            if prefix is not None: self._values["prefix"] = prefix

        @builtins.property
        def bucket_arn(self) -> str:
            """``CfnBucket.DestinationProperty.BucketArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-bucketarn
            """
            return self._values.get('bucket_arn')

        @builtins.property
        def format(self) -> str:
            """``CfnBucket.DestinationProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-format
            """
            return self._values.get('format')

        @builtins.property
        def bucket_account_id(self) -> typing.Optional[str]:
            """``CfnBucket.DestinationProperty.BucketAccountId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-bucketaccountid
            """
            return self._values.get('bucket_account_id')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnBucket.DestinationProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-prefix
            """
            return self._values.get('prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DestinationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.EncryptionConfigurationProperty", jsii_struct_bases=[], name_mapping={'replica_kms_key_id': 'replicaKmsKeyId'})
    class EncryptionConfigurationProperty():
        def __init__(self, *, replica_kms_key_id: str):
            """
            :param replica_kms_key_id: ``CfnBucket.EncryptionConfigurationProperty.ReplicaKmsKeyID``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-encryptionconfiguration.html
            """
            self._values = {
                'replica_kms_key_id': replica_kms_key_id,
            }

        @builtins.property
        def replica_kms_key_id(self) -> str:
            """``CfnBucket.EncryptionConfigurationProperty.ReplicaKmsKeyID``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-encryptionconfiguration.html#cfn-s3-bucket-encryptionconfiguration-replicakmskeyid
            """
            return self._values.get('replica_kms_key_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.FilterRuleProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class FilterRuleProperty():
        def __init__(self, *, name: str, value: str):
            """
            :param name: ``CfnBucket.FilterRuleProperty.Name``.
            :param value: ``CfnBucket.FilterRuleProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnBucket.FilterRuleProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key-rules-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> str:
            """``CfnBucket.FilterRuleProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key-rules-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FilterRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.InventoryConfigurationProperty", jsii_struct_bases=[], name_mapping={'destination': 'destination', 'enabled': 'enabled', 'id': 'id', 'included_object_versions': 'includedObjectVersions', 'schedule_frequency': 'scheduleFrequency', 'optional_fields': 'optionalFields', 'prefix': 'prefix'})
    class InventoryConfigurationProperty():
        def __init__(self, *, destination: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.DestinationProperty"], enabled: typing.Union[bool, aws_cdk.core.IResolvable], id: str, included_object_versions: str, schedule_frequency: str, optional_fields: typing.Optional[typing.List[str]]=None, prefix: typing.Optional[str]=None):
            """
            :param destination: ``CfnBucket.InventoryConfigurationProperty.Destination``.
            :param enabled: ``CfnBucket.InventoryConfigurationProperty.Enabled``.
            :param id: ``CfnBucket.InventoryConfigurationProperty.Id``.
            :param included_object_versions: ``CfnBucket.InventoryConfigurationProperty.IncludedObjectVersions``.
            :param schedule_frequency: ``CfnBucket.InventoryConfigurationProperty.ScheduleFrequency``.
            :param optional_fields: ``CfnBucket.InventoryConfigurationProperty.OptionalFields``.
            :param prefix: ``CfnBucket.InventoryConfigurationProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html
            """
            self._values = {
                'destination': destination,
                'enabled': enabled,
                'id': id,
                'included_object_versions': included_object_versions,
                'schedule_frequency': schedule_frequency,
            }
            if optional_fields is not None: self._values["optional_fields"] = optional_fields
            if prefix is not None: self._values["prefix"] = prefix

        @builtins.property
        def destination(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.DestinationProperty"]:
            """``CfnBucket.InventoryConfigurationProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-destination
            """
            return self._values.get('destination')

        @builtins.property
        def enabled(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnBucket.InventoryConfigurationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-enabled
            """
            return self._values.get('enabled')

        @builtins.property
        def id(self) -> str:
            """``CfnBucket.InventoryConfigurationProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-id
            """
            return self._values.get('id')

        @builtins.property
        def included_object_versions(self) -> str:
            """``CfnBucket.InventoryConfigurationProperty.IncludedObjectVersions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-includedobjectversions
            """
            return self._values.get('included_object_versions')

        @builtins.property
        def schedule_frequency(self) -> str:
            """``CfnBucket.InventoryConfigurationProperty.ScheduleFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-schedulefrequency
            """
            return self._values.get('schedule_frequency')

        @builtins.property
        def optional_fields(self) -> typing.Optional[typing.List[str]]:
            """``CfnBucket.InventoryConfigurationProperty.OptionalFields``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-optionalfields
            """
            return self._values.get('optional_fields')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnBucket.InventoryConfigurationProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-prefix
            """
            return self._values.get('prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InventoryConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.LambdaConfigurationProperty", jsii_struct_bases=[], name_mapping={'event': 'event', 'function': 'function', 'filter': 'filter'})
    class LambdaConfigurationProperty():
        def __init__(self, *, event: str, function: str, filter: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationFilterProperty"]]]=None):
            """
            :param event: ``CfnBucket.LambdaConfigurationProperty.Event``.
            :param function: ``CfnBucket.LambdaConfigurationProperty.Function``.
            :param filter: ``CfnBucket.LambdaConfigurationProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html
            """
            self._values = {
                'event': event,
                'function': function,
            }
            if filter is not None: self._values["filter"] = filter

        @builtins.property
        def event(self) -> str:
            """``CfnBucket.LambdaConfigurationProperty.Event``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig-event
            """
            return self._values.get('event')

        @builtins.property
        def function(self) -> str:
            """``CfnBucket.LambdaConfigurationProperty.Function``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig-function
            """
            return self._values.get('function')

        @builtins.property
        def filter(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationFilterProperty"]]]:
            """``CfnBucket.LambdaConfigurationProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig-filter
            """
            return self._values.get('filter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LambdaConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.LifecycleConfigurationProperty", jsii_struct_bases=[], name_mapping={'rules': 'rules'})
    class LifecycleConfigurationProperty():
        def __init__(self, *, rules: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.RuleProperty"]]]):
            """
            :param rules: ``CfnBucket.LifecycleConfigurationProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig.html
            """
            self._values = {
                'rules': rules,
            }

        @builtins.property
        def rules(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.RuleProperty"]]]:
            """``CfnBucket.LifecycleConfigurationProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig.html#cfn-s3-bucket-lifecycleconfig-rules
            """
            return self._values.get('rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LifecycleConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.LoggingConfigurationProperty", jsii_struct_bases=[], name_mapping={'destination_bucket_name': 'destinationBucketName', 'log_file_prefix': 'logFilePrefix'})
    class LoggingConfigurationProperty():
        def __init__(self, *, destination_bucket_name: typing.Optional[str]=None, log_file_prefix: typing.Optional[str]=None):
            """
            :param destination_bucket_name: ``CfnBucket.LoggingConfigurationProperty.DestinationBucketName``.
            :param log_file_prefix: ``CfnBucket.LoggingConfigurationProperty.LogFilePrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfig.html
            """
            self._values = {
            }
            if destination_bucket_name is not None: self._values["destination_bucket_name"] = destination_bucket_name
            if log_file_prefix is not None: self._values["log_file_prefix"] = log_file_prefix

        @builtins.property
        def destination_bucket_name(self) -> typing.Optional[str]:
            """``CfnBucket.LoggingConfigurationProperty.DestinationBucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfig.html#cfn-s3-bucket-loggingconfig-destinationbucketname
            """
            return self._values.get('destination_bucket_name')

        @builtins.property
        def log_file_prefix(self) -> typing.Optional[str]:
            """``CfnBucket.LoggingConfigurationProperty.LogFilePrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfig.html#cfn-s3-bucket-loggingconfig-logfileprefix
            """
            return self._values.get('log_file_prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoggingConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.MetricsConfigurationProperty", jsii_struct_bases=[], name_mapping={'id': 'id', 'prefix': 'prefix', 'tag_filters': 'tagFilters'})
    class MetricsConfigurationProperty():
        def __init__(self, *, id: str, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TagFilterProperty"]]]]]=None):
            """
            :param id: ``CfnBucket.MetricsConfigurationProperty.Id``.
            :param prefix: ``CfnBucket.MetricsConfigurationProperty.Prefix``.
            :param tag_filters: ``CfnBucket.MetricsConfigurationProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html
            """
            self._values = {
                'id': id,
            }
            if prefix is not None: self._values["prefix"] = prefix
            if tag_filters is not None: self._values["tag_filters"] = tag_filters

        @builtins.property
        def id(self) -> str:
            """``CfnBucket.MetricsConfigurationProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-id
            """
            return self._values.get('id')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnBucket.MetricsConfigurationProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TagFilterProperty"]]]]]:
            """``CfnBucket.MetricsConfigurationProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-tagfilters
            """
            return self._values.get('tag_filters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.NoncurrentVersionTransitionProperty", jsii_struct_bases=[], name_mapping={'storage_class': 'storageClass', 'transition_in_days': 'transitionInDays'})
    class NoncurrentVersionTransitionProperty():
        def __init__(self, *, storage_class: str, transition_in_days: jsii.Number):
            """
            :param storage_class: ``CfnBucket.NoncurrentVersionTransitionProperty.StorageClass``.
            :param transition_in_days: ``CfnBucket.NoncurrentVersionTransitionProperty.TransitionInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition.html
            """
            self._values = {
                'storage_class': storage_class,
                'transition_in_days': transition_in_days,
            }

        @builtins.property
        def storage_class(self) -> str:
            """``CfnBucket.NoncurrentVersionTransitionProperty.StorageClass``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition-storageclass
            """
            return self._values.get('storage_class')

        @builtins.property
        def transition_in_days(self) -> jsii.Number:
            """``CfnBucket.NoncurrentVersionTransitionProperty.TransitionInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition-transitionindays
            """
            return self._values.get('transition_in_days')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NoncurrentVersionTransitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.NotificationConfigurationProperty", jsii_struct_bases=[], name_mapping={'lambda_configurations': 'lambdaConfigurations', 'queue_configurations': 'queueConfigurations', 'topic_configurations': 'topicConfigurations'})
    class NotificationConfigurationProperty():
        def __init__(self, *, lambda_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.LambdaConfigurationProperty"]]]]]=None, queue_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.QueueConfigurationProperty"]]]]]=None, topic_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TopicConfigurationProperty"]]]]]=None):
            """
            :param lambda_configurations: ``CfnBucket.NotificationConfigurationProperty.LambdaConfigurations``.
            :param queue_configurations: ``CfnBucket.NotificationConfigurationProperty.QueueConfigurations``.
            :param topic_configurations: ``CfnBucket.NotificationConfigurationProperty.TopicConfigurations``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html
            """
            self._values = {
            }
            if lambda_configurations is not None: self._values["lambda_configurations"] = lambda_configurations
            if queue_configurations is not None: self._values["queue_configurations"] = queue_configurations
            if topic_configurations is not None: self._values["topic_configurations"] = topic_configurations

        @builtins.property
        def lambda_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.LambdaConfigurationProperty"]]]]]:
            """``CfnBucket.NotificationConfigurationProperty.LambdaConfigurations``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig
            """
            return self._values.get('lambda_configurations')

        @builtins.property
        def queue_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.QueueConfigurationProperty"]]]]]:
            """``CfnBucket.NotificationConfigurationProperty.QueueConfigurations``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#cfn-s3-bucket-notificationconfig-queueconfig
            """
            return self._values.get('queue_configurations')

        @builtins.property
        def topic_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TopicConfigurationProperty"]]]]]:
            """``CfnBucket.NotificationConfigurationProperty.TopicConfigurations``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#cfn-s3-bucket-notificationconfig-topicconfig
            """
            return self._values.get('topic_configurations')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.NotificationFilterProperty", jsii_struct_bases=[], name_mapping={'s3_key': 's3Key'})
    class NotificationFilterProperty():
        def __init__(self, *, s3_key: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.S3KeyFilterProperty"]):
            """
            :param s3_key: ``CfnBucket.NotificationFilterProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            """
            self._values = {
                's3_key': s3_key,
            }

        @builtins.property
        def s3_key(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.S3KeyFilterProperty"]:
            """``CfnBucket.NotificationFilterProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key
            """
            return self._values.get('s3_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ObjectLockConfigurationProperty", jsii_struct_bases=[], name_mapping={'object_lock_enabled': 'objectLockEnabled', 'rule': 'rule'})
    class ObjectLockConfigurationProperty():
        def __init__(self, *, object_lock_enabled: typing.Optional[str]=None, rule: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ObjectLockRuleProperty"]]]=None):
            """
            :param object_lock_enabled: ``CfnBucket.ObjectLockConfigurationProperty.ObjectLockEnabled``.
            :param rule: ``CfnBucket.ObjectLockConfigurationProperty.Rule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html
            """
            self._values = {
            }
            if object_lock_enabled is not None: self._values["object_lock_enabled"] = object_lock_enabled
            if rule is not None: self._values["rule"] = rule

        @builtins.property
        def object_lock_enabled(self) -> typing.Optional[str]:
            """``CfnBucket.ObjectLockConfigurationProperty.ObjectLockEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html#cfn-s3-bucket-objectlockconfiguration-objectlockenabled
            """
            return self._values.get('object_lock_enabled')

        @builtins.property
        def rule(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ObjectLockRuleProperty"]]]:
            """``CfnBucket.ObjectLockConfigurationProperty.Rule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html#cfn-s3-bucket-objectlockconfiguration-rule
            """
            return self._values.get('rule')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ObjectLockConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ObjectLockRuleProperty", jsii_struct_bases=[], name_mapping={'default_retention': 'defaultRetention'})
    class ObjectLockRuleProperty():
        def __init__(self, *, default_retention: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.DefaultRetentionProperty"]]]=None):
            """
            :param default_retention: ``CfnBucket.ObjectLockRuleProperty.DefaultRetention``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html
            """
            self._values = {
            }
            if default_retention is not None: self._values["default_retention"] = default_retention

        @builtins.property
        def default_retention(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.DefaultRetentionProperty"]]]:
            """``CfnBucket.ObjectLockRuleProperty.DefaultRetention``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html#cfn-s3-bucket-objectlockrule-defaultretention
            """
            return self._values.get('default_retention')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ObjectLockRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.PublicAccessBlockConfigurationProperty", jsii_struct_bases=[], name_mapping={'block_public_acls': 'blockPublicAcls', 'block_public_policy': 'blockPublicPolicy', 'ignore_public_acls': 'ignorePublicAcls', 'restrict_public_buckets': 'restrictPublicBuckets'})
    class PublicAccessBlockConfigurationProperty():
        def __init__(self, *, block_public_acls: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, block_public_policy: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ignore_public_acls: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, restrict_public_buckets: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param block_public_acls: ``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.
            :param block_public_policy: ``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.
            :param ignore_public_acls: ``CfnBucket.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.
            :param restrict_public_buckets: ``CfnBucket.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html
            """
            self._values = {
            }
            if block_public_acls is not None: self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None: self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None: self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None: self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-blockpublicacls
            """
            return self._values.get('block_public_acls')

        @builtins.property
        def block_public_policy(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-blockpublicpolicy
            """
            return self._values.get('block_public_policy')

        @builtins.property
        def ignore_public_acls(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnBucket.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-ignorepublicacls
            """
            return self._values.get('ignore_public_acls')

        @builtins.property
        def restrict_public_buckets(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnBucket.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-restrictpublicbuckets
            """
            return self._values.get('restrict_public_buckets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PublicAccessBlockConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.QueueConfigurationProperty", jsii_struct_bases=[], name_mapping={'event': 'event', 'queue': 'queue', 'filter': 'filter'})
    class QueueConfigurationProperty():
        def __init__(self, *, event: str, queue: str, filter: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationFilterProperty"]]]=None):
            """
            :param event: ``CfnBucket.QueueConfigurationProperty.Event``.
            :param queue: ``CfnBucket.QueueConfigurationProperty.Queue``.
            :param filter: ``CfnBucket.QueueConfigurationProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html
            """
            self._values = {
                'event': event,
                'queue': queue,
            }
            if filter is not None: self._values["filter"] = filter

        @builtins.property
        def event(self) -> str:
            """``CfnBucket.QueueConfigurationProperty.Event``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html#cfn-s3-bucket-notificationconfig-queueconfig-event
            """
            return self._values.get('event')

        @builtins.property
        def queue(self) -> str:
            """``CfnBucket.QueueConfigurationProperty.Queue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html#cfn-s3-bucket-notificationconfig-queueconfig-queue
            """
            return self._values.get('queue')

        @builtins.property
        def filter(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationFilterProperty"]]]:
            """``CfnBucket.QueueConfigurationProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html#cfn-s3-bucket-notificationconfig-queueconfig-filter
            """
            return self._values.get('filter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'QueueConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RedirectAllRequestsToProperty", jsii_struct_bases=[], name_mapping={'host_name': 'hostName', 'protocol': 'protocol'})
    class RedirectAllRequestsToProperty():
        def __init__(self, *, host_name: str, protocol: typing.Optional[str]=None):
            """
            :param host_name: ``CfnBucket.RedirectAllRequestsToProperty.HostName``.
            :param protocol: ``CfnBucket.RedirectAllRequestsToProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-redirectallrequeststo.html
            """
            self._values = {
                'host_name': host_name,
            }
            if protocol is not None: self._values["protocol"] = protocol

        @builtins.property
        def host_name(self) -> str:
            """``CfnBucket.RedirectAllRequestsToProperty.HostName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-redirectallrequeststo.html#cfn-s3-websiteconfiguration-redirectallrequeststo-hostname
            """
            return self._values.get('host_name')

        @builtins.property
        def protocol(self) -> typing.Optional[str]:
            """``CfnBucket.RedirectAllRequestsToProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-redirectallrequeststo.html#cfn-s3-websiteconfiguration-redirectallrequeststo-protocol
            """
            return self._values.get('protocol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RedirectAllRequestsToProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RedirectRuleProperty", jsii_struct_bases=[], name_mapping={'host_name': 'hostName', 'http_redirect_code': 'httpRedirectCode', 'protocol': 'protocol', 'replace_key_prefix_with': 'replaceKeyPrefixWith', 'replace_key_with': 'replaceKeyWith'})
    class RedirectRuleProperty():
        def __init__(self, *, host_name: typing.Optional[str]=None, http_redirect_code: typing.Optional[str]=None, protocol: typing.Optional[str]=None, replace_key_prefix_with: typing.Optional[str]=None, replace_key_with: typing.Optional[str]=None):
            """
            :param host_name: ``CfnBucket.RedirectRuleProperty.HostName``.
            :param http_redirect_code: ``CfnBucket.RedirectRuleProperty.HttpRedirectCode``.
            :param protocol: ``CfnBucket.RedirectRuleProperty.Protocol``.
            :param replace_key_prefix_with: ``CfnBucket.RedirectRuleProperty.ReplaceKeyPrefixWith``.
            :param replace_key_with: ``CfnBucket.RedirectRuleProperty.ReplaceKeyWith``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html
            """
            self._values = {
            }
            if host_name is not None: self._values["host_name"] = host_name
            if http_redirect_code is not None: self._values["http_redirect_code"] = http_redirect_code
            if protocol is not None: self._values["protocol"] = protocol
            if replace_key_prefix_with is not None: self._values["replace_key_prefix_with"] = replace_key_prefix_with
            if replace_key_with is not None: self._values["replace_key_with"] = replace_key_with

        @builtins.property
        def host_name(self) -> typing.Optional[str]:
            """``CfnBucket.RedirectRuleProperty.HostName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-hostname
            """
            return self._values.get('host_name')

        @builtins.property
        def http_redirect_code(self) -> typing.Optional[str]:
            """``CfnBucket.RedirectRuleProperty.HttpRedirectCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-httpredirectcode
            """
            return self._values.get('http_redirect_code')

        @builtins.property
        def protocol(self) -> typing.Optional[str]:
            """``CfnBucket.RedirectRuleProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-protocol
            """
            return self._values.get('protocol')

        @builtins.property
        def replace_key_prefix_with(self) -> typing.Optional[str]:
            """``CfnBucket.RedirectRuleProperty.ReplaceKeyPrefixWith``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-replacekeyprefixwith
            """
            return self._values.get('replace_key_prefix_with')

        @builtins.property
        def replace_key_with(self) -> typing.Optional[str]:
            """``CfnBucket.RedirectRuleProperty.ReplaceKeyWith``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-replacekeywith
            """
            return self._values.get('replace_key_with')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RedirectRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ReplicationConfigurationProperty", jsii_struct_bases=[], name_mapping={'role': 'role', 'rules': 'rules'})
    class ReplicationConfigurationProperty():
        def __init__(self, *, role: str, rules: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.ReplicationRuleProperty"]]]):
            """
            :param role: ``CfnBucket.ReplicationConfigurationProperty.Role``.
            :param rules: ``CfnBucket.ReplicationConfigurationProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html
            """
            self._values = {
                'role': role,
                'rules': rules,
            }

        @builtins.property
        def role(self) -> str:
            """``CfnBucket.ReplicationConfigurationProperty.Role``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html#cfn-s3-bucket-replicationconfiguration-role
            """
            return self._values.get('role')

        @builtins.property
        def rules(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.ReplicationRuleProperty"]]]:
            """``CfnBucket.ReplicationConfigurationProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html#cfn-s3-bucket-replicationconfiguration-rules
            """
            return self._values.get('rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ReplicationConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ReplicationDestinationProperty", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'access_control_translation': 'accessControlTranslation', 'account': 'account', 'encryption_configuration': 'encryptionConfiguration', 'storage_class': 'storageClass'})
    class ReplicationDestinationProperty():
        def __init__(self, *, bucket: str, access_control_translation: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.AccessControlTranslationProperty"]]]=None, account: typing.Optional[str]=None, encryption_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.EncryptionConfigurationProperty"]]]=None, storage_class: typing.Optional[str]=None):
            """
            :param bucket: ``CfnBucket.ReplicationDestinationProperty.Bucket``.
            :param access_control_translation: ``CfnBucket.ReplicationDestinationProperty.AccessControlTranslation``.
            :param account: ``CfnBucket.ReplicationDestinationProperty.Account``.
            :param encryption_configuration: ``CfnBucket.ReplicationDestinationProperty.EncryptionConfiguration``.
            :param storage_class: ``CfnBucket.ReplicationDestinationProperty.StorageClass``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html
            """
            self._values = {
                'bucket': bucket,
            }
            if access_control_translation is not None: self._values["access_control_translation"] = access_control_translation
            if account is not None: self._values["account"] = account
            if encryption_configuration is not None: self._values["encryption_configuration"] = encryption_configuration
            if storage_class is not None: self._values["storage_class"] = storage_class

        @builtins.property
        def bucket(self) -> str:
            """``CfnBucket.ReplicationDestinationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationconfiguration-rules-destination-bucket
            """
            return self._values.get('bucket')

        @builtins.property
        def access_control_translation(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.AccessControlTranslationProperty"]]]:
            """``CfnBucket.ReplicationDestinationProperty.AccessControlTranslation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-accesscontroltranslation
            """
            return self._values.get('access_control_translation')

        @builtins.property
        def account(self) -> typing.Optional[str]:
            """``CfnBucket.ReplicationDestinationProperty.Account``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-account
            """
            return self._values.get('account')

        @builtins.property
        def encryption_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.EncryptionConfigurationProperty"]]]:
            """``CfnBucket.ReplicationDestinationProperty.EncryptionConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-encryptionconfiguration
            """
            return self._values.get('encryption_configuration')

        @builtins.property
        def storage_class(self) -> typing.Optional[str]:
            """``CfnBucket.ReplicationDestinationProperty.StorageClass``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationconfiguration-rules-destination-storageclass
            """
            return self._values.get('storage_class')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ReplicationDestinationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ReplicationRuleProperty", jsii_struct_bases=[], name_mapping={'destination': 'destination', 'prefix': 'prefix', 'status': 'status', 'id': 'id', 'source_selection_criteria': 'sourceSelectionCriteria'})
    class ReplicationRuleProperty():
        def __init__(self, *, destination: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.ReplicationDestinationProperty"], prefix: str, status: str, id: typing.Optional[str]=None, source_selection_criteria: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.SourceSelectionCriteriaProperty"]]]=None):
            """
            :param destination: ``CfnBucket.ReplicationRuleProperty.Destination``.
            :param prefix: ``CfnBucket.ReplicationRuleProperty.Prefix``.
            :param status: ``CfnBucket.ReplicationRuleProperty.Status``.
            :param id: ``CfnBucket.ReplicationRuleProperty.Id``.
            :param source_selection_criteria: ``CfnBucket.ReplicationRuleProperty.SourceSelectionCriteria``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html
            """
            self._values = {
                'destination': destination,
                'prefix': prefix,
                'status': status,
            }
            if id is not None: self._values["id"] = id
            if source_selection_criteria is not None: self._values["source_selection_criteria"] = source_selection_criteria

        @builtins.property
        def destination(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.ReplicationDestinationProperty"]:
            """``CfnBucket.ReplicationRuleProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-destination
            """
            return self._values.get('destination')

        @builtins.property
        def prefix(self) -> str:
            """``CfnBucket.ReplicationRuleProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def status(self) -> str:
            """``CfnBucket.ReplicationRuleProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-status
            """
            return self._values.get('status')

        @builtins.property
        def id(self) -> typing.Optional[str]:
            """``CfnBucket.ReplicationRuleProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-id
            """
            return self._values.get('id')

        @builtins.property
        def source_selection_criteria(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.SourceSelectionCriteriaProperty"]]]:
            """``CfnBucket.ReplicationRuleProperty.SourceSelectionCriteria``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationrule-sourceselectioncriteria
            """
            return self._values.get('source_selection_criteria')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ReplicationRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RoutingRuleConditionProperty", jsii_struct_bases=[], name_mapping={'http_error_code_returned_equals': 'httpErrorCodeReturnedEquals', 'key_prefix_equals': 'keyPrefixEquals'})
    class RoutingRuleConditionProperty():
        def __init__(self, *, http_error_code_returned_equals: typing.Optional[str]=None, key_prefix_equals: typing.Optional[str]=None):
            """
            :param http_error_code_returned_equals: ``CfnBucket.RoutingRuleConditionProperty.HttpErrorCodeReturnedEquals``.
            :param key_prefix_equals: ``CfnBucket.RoutingRuleConditionProperty.KeyPrefixEquals``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-routingrulecondition.html
            """
            self._values = {
            }
            if http_error_code_returned_equals is not None: self._values["http_error_code_returned_equals"] = http_error_code_returned_equals
            if key_prefix_equals is not None: self._values["key_prefix_equals"] = key_prefix_equals

        @builtins.property
        def http_error_code_returned_equals(self) -> typing.Optional[str]:
            """``CfnBucket.RoutingRuleConditionProperty.HttpErrorCodeReturnedEquals``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-routingrulecondition.html#cfn-s3-websiteconfiguration-routingrules-routingrulecondition-httperrorcodereturnedequals
            """
            return self._values.get('http_error_code_returned_equals')

        @builtins.property
        def key_prefix_equals(self) -> typing.Optional[str]:
            """``CfnBucket.RoutingRuleConditionProperty.KeyPrefixEquals``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-routingrulecondition.html#cfn-s3-websiteconfiguration-routingrules-routingrulecondition-keyprefixequals
            """
            return self._values.get('key_prefix_equals')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RoutingRuleConditionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RoutingRuleProperty", jsii_struct_bases=[], name_mapping={'redirect_rule': 'redirectRule', 'routing_rule_condition': 'routingRuleCondition'})
    class RoutingRuleProperty():
        def __init__(self, *, redirect_rule: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.RedirectRuleProperty"], routing_rule_condition: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.RoutingRuleConditionProperty"]]]=None):
            """
            :param redirect_rule: ``CfnBucket.RoutingRuleProperty.RedirectRule``.
            :param routing_rule_condition: ``CfnBucket.RoutingRuleProperty.RoutingRuleCondition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html
            """
            self._values = {
                'redirect_rule': redirect_rule,
            }
            if routing_rule_condition is not None: self._values["routing_rule_condition"] = routing_rule_condition

        @builtins.property
        def redirect_rule(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.RedirectRuleProperty"]:
            """``CfnBucket.RoutingRuleProperty.RedirectRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html#cfn-s3-websiteconfiguration-routingrules-redirectrule
            """
            return self._values.get('redirect_rule')

        @builtins.property
        def routing_rule_condition(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.RoutingRuleConditionProperty"]]]:
            """``CfnBucket.RoutingRuleProperty.RoutingRuleCondition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html#cfn-s3-websiteconfiguration-routingrules-routingrulecondition
            """
            return self._values.get('routing_rule_condition')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RoutingRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.RuleProperty", jsii_struct_bases=[], name_mapping={'status': 'status', 'abort_incomplete_multipart_upload': 'abortIncompleteMultipartUpload', 'expiration_date': 'expirationDate', 'expiration_in_days': 'expirationInDays', 'id': 'id', 'noncurrent_version_expiration_in_days': 'noncurrentVersionExpirationInDays', 'noncurrent_version_transition': 'noncurrentVersionTransition', 'noncurrent_version_transitions': 'noncurrentVersionTransitions', 'prefix': 'prefix', 'tag_filters': 'tagFilters', 'transition': 'transition', 'transitions': 'transitions'})
    class RuleProperty():
        def __init__(self, *, status: str, abort_incomplete_multipart_upload: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.AbortIncompleteMultipartUploadProperty"]]]=None, expiration_date: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]=None, expiration_in_days: typing.Optional[jsii.Number]=None, id: typing.Optional[str]=None, noncurrent_version_expiration_in_days: typing.Optional[jsii.Number]=None, noncurrent_version_transition: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NoncurrentVersionTransitionProperty"]]]=None, noncurrent_version_transitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.NoncurrentVersionTransitionProperty"]]]]]=None, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TagFilterProperty"]]]]]=None, transition: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.TransitionProperty"]]]=None, transitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TransitionProperty"]]]]]=None):
            """
            :param status: ``CfnBucket.RuleProperty.Status``.
            :param abort_incomplete_multipart_upload: ``CfnBucket.RuleProperty.AbortIncompleteMultipartUpload``.
            :param expiration_date: ``CfnBucket.RuleProperty.ExpirationDate``.
            :param expiration_in_days: ``CfnBucket.RuleProperty.ExpirationInDays``.
            :param id: ``CfnBucket.RuleProperty.Id``.
            :param noncurrent_version_expiration_in_days: ``CfnBucket.RuleProperty.NoncurrentVersionExpirationInDays``.
            :param noncurrent_version_transition: ``CfnBucket.RuleProperty.NoncurrentVersionTransition``.
            :param noncurrent_version_transitions: ``CfnBucket.RuleProperty.NoncurrentVersionTransitions``.
            :param prefix: ``CfnBucket.RuleProperty.Prefix``.
            :param tag_filters: ``CfnBucket.RuleProperty.TagFilters``.
            :param transition: ``CfnBucket.RuleProperty.Transition``.
            :param transitions: ``CfnBucket.RuleProperty.Transitions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html
            """
            self._values = {
                'status': status,
            }
            if abort_incomplete_multipart_upload is not None: self._values["abort_incomplete_multipart_upload"] = abort_incomplete_multipart_upload
            if expiration_date is not None: self._values["expiration_date"] = expiration_date
            if expiration_in_days is not None: self._values["expiration_in_days"] = expiration_in_days
            if id is not None: self._values["id"] = id
            if noncurrent_version_expiration_in_days is not None: self._values["noncurrent_version_expiration_in_days"] = noncurrent_version_expiration_in_days
            if noncurrent_version_transition is not None: self._values["noncurrent_version_transition"] = noncurrent_version_transition
            if noncurrent_version_transitions is not None: self._values["noncurrent_version_transitions"] = noncurrent_version_transitions
            if prefix is not None: self._values["prefix"] = prefix
            if tag_filters is not None: self._values["tag_filters"] = tag_filters
            if transition is not None: self._values["transition"] = transition
            if transitions is not None: self._values["transitions"] = transitions

        @builtins.property
        def status(self) -> str:
            """``CfnBucket.RuleProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-status
            """
            return self._values.get('status')

        @builtins.property
        def abort_incomplete_multipart_upload(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.AbortIncompleteMultipartUploadProperty"]]]:
            """``CfnBucket.RuleProperty.AbortIncompleteMultipartUpload``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-rule-abortincompletemultipartupload
            """
            return self._values.get('abort_incomplete_multipart_upload')

        @builtins.property
        def expiration_date(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]:
            """``CfnBucket.RuleProperty.ExpirationDate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-expirationdate
            """
            return self._values.get('expiration_date')

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnBucket.RuleProperty.ExpirationInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-expirationindays
            """
            return self._values.get('expiration_in_days')

        @builtins.property
        def id(self) -> typing.Optional[str]:
            """``CfnBucket.RuleProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-id
            """
            return self._values.get('id')

        @builtins.property
        def noncurrent_version_expiration_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnBucket.RuleProperty.NoncurrentVersionExpirationInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversionexpirationindays
            """
            return self._values.get('noncurrent_version_expiration_in_days')

        @builtins.property
        def noncurrent_version_transition(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NoncurrentVersionTransitionProperty"]]]:
            """``CfnBucket.RuleProperty.NoncurrentVersionTransition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition
            """
            return self._values.get('noncurrent_version_transition')

        @builtins.property
        def noncurrent_version_transitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.NoncurrentVersionTransitionProperty"]]]]]:
            """``CfnBucket.RuleProperty.NoncurrentVersionTransitions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransitions
            """
            return self._values.get('noncurrent_version_transitions')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnBucket.RuleProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TagFilterProperty"]]]]]:
            """``CfnBucket.RuleProperty.TagFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-rule-tagfilters
            """
            return self._values.get('tag_filters')

        @builtins.property
        def transition(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.TransitionProperty"]]]:
            """``CfnBucket.RuleProperty.Transition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-transition
            """
            return self._values.get('transition')

        @builtins.property
        def transitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.TransitionProperty"]]]]]:
            """``CfnBucket.RuleProperty.Transitions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-transitions
            """
            return self._values.get('transitions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.S3KeyFilterProperty", jsii_struct_bases=[], name_mapping={'rules': 'rules'})
    class S3KeyFilterProperty():
        def __init__(self, *, rules: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.FilterRuleProperty"]]]):
            """
            :param rules: ``CfnBucket.S3KeyFilterProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key.html
            """
            self._values = {
                'rules': rules,
            }

        @builtins.property
        def rules(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.FilterRuleProperty"]]]:
            """``CfnBucket.S3KeyFilterProperty.Rules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key-rules
            """
            return self._values.get('rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3KeyFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ServerSideEncryptionByDefaultProperty", jsii_struct_bases=[], name_mapping={'sse_algorithm': 'sseAlgorithm', 'kms_master_key_id': 'kmsMasterKeyId'})
    class ServerSideEncryptionByDefaultProperty():
        def __init__(self, *, sse_algorithm: str, kms_master_key_id: typing.Optional[str]=None):
            """
            :param sse_algorithm: ``CfnBucket.ServerSideEncryptionByDefaultProperty.SSEAlgorithm``.
            :param kms_master_key_id: ``CfnBucket.ServerSideEncryptionByDefaultProperty.KMSMasterKeyID``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html
            """
            self._values = {
                'sse_algorithm': sse_algorithm,
            }
            if kms_master_key_id is not None: self._values["kms_master_key_id"] = kms_master_key_id

        @builtins.property
        def sse_algorithm(self) -> str:
            """``CfnBucket.ServerSideEncryptionByDefaultProperty.SSEAlgorithm``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html#cfn-s3-bucket-serversideencryptionbydefault-ssealgorithm
            """
            return self._values.get('sse_algorithm')

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[str]:
            """``CfnBucket.ServerSideEncryptionByDefaultProperty.KMSMasterKeyID``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html#cfn-s3-bucket-serversideencryptionbydefault-kmsmasterkeyid
            """
            return self._values.get('kms_master_key_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ServerSideEncryptionByDefaultProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.ServerSideEncryptionRuleProperty", jsii_struct_bases=[], name_mapping={'server_side_encryption_by_default': 'serverSideEncryptionByDefault'})
    class ServerSideEncryptionRuleProperty():
        def __init__(self, *, server_side_encryption_by_default: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ServerSideEncryptionByDefaultProperty"]]]=None):
            """
            :param server_side_encryption_by_default: ``CfnBucket.ServerSideEncryptionRuleProperty.ServerSideEncryptionByDefault``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html
            """
            self._values = {
            }
            if server_side_encryption_by_default is not None: self._values["server_side_encryption_by_default"] = server_side_encryption_by_default

        @builtins.property
        def server_side_encryption_by_default(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ServerSideEncryptionByDefaultProperty"]]]:
            """``CfnBucket.ServerSideEncryptionRuleProperty.ServerSideEncryptionByDefault``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html#cfn-s3-bucket-serversideencryptionrule-serversideencryptionbydefault
            """
            return self._values.get('server_side_encryption_by_default')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ServerSideEncryptionRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.SourceSelectionCriteriaProperty", jsii_struct_bases=[], name_mapping={'sse_kms_encrypted_objects': 'sseKmsEncryptedObjects'})
    class SourceSelectionCriteriaProperty():
        def __init__(self, *, sse_kms_encrypted_objects: typing.Union[aws_cdk.core.IResolvable, "CfnBucket.SseKmsEncryptedObjectsProperty"]):
            """
            :param sse_kms_encrypted_objects: ``CfnBucket.SourceSelectionCriteriaProperty.SseKmsEncryptedObjects``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html
            """
            self._values = {
                'sse_kms_encrypted_objects': sse_kms_encrypted_objects,
            }

        @builtins.property
        def sse_kms_encrypted_objects(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnBucket.SseKmsEncryptedObjectsProperty"]:
            """``CfnBucket.SourceSelectionCriteriaProperty.SseKmsEncryptedObjects``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html#cfn-s3-bucket-sourceselectioncriteria-ssekmsencryptedobjects
            """
            return self._values.get('sse_kms_encrypted_objects')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SourceSelectionCriteriaProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.SseKmsEncryptedObjectsProperty", jsii_struct_bases=[], name_mapping={'status': 'status'})
    class SseKmsEncryptedObjectsProperty():
        def __init__(self, *, status: str):
            """
            :param status: ``CfnBucket.SseKmsEncryptedObjectsProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ssekmsencryptedobjects.html
            """
            self._values = {
                'status': status,
            }

        @builtins.property
        def status(self) -> str:
            """``CfnBucket.SseKmsEncryptedObjectsProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ssekmsencryptedobjects.html#cfn-s3-bucket-ssekmsencryptedobjects-status
            """
            return self._values.get('status')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SseKmsEncryptedObjectsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.StorageClassAnalysisProperty", jsii_struct_bases=[], name_mapping={'data_export': 'dataExport'})
    class StorageClassAnalysisProperty():
        def __init__(self, *, data_export: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.DataExportProperty"]]]=None):
            """
            :param data_export: ``CfnBucket.StorageClassAnalysisProperty.DataExport``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-storageclassanalysis.html
            """
            self._values = {
            }
            if data_export is not None: self._values["data_export"] = data_export

        @builtins.property
        def data_export(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.DataExportProperty"]]]:
            """``CfnBucket.StorageClassAnalysisProperty.DataExport``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-storageclassanalysis.html#cfn-s3-bucket-storageclassanalysis-dataexport
            """
            return self._values.get('data_export')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StorageClassAnalysisProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.TagFilterProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagFilterProperty():
        def __init__(self, *, key: str, value: str):
            """
            :param key: ``CfnBucket.TagFilterProperty.Key``.
            :param value: ``CfnBucket.TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnBucket.TagFilterProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html#cfn-s3-bucket-tagfilter-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnBucket.TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html#cfn-s3-bucket-tagfilter-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.TopicConfigurationProperty", jsii_struct_bases=[], name_mapping={'event': 'event', 'topic': 'topic', 'filter': 'filter'})
    class TopicConfigurationProperty():
        def __init__(self, *, event: str, topic: str, filter: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationFilterProperty"]]]=None):
            """
            :param event: ``CfnBucket.TopicConfigurationProperty.Event``.
            :param topic: ``CfnBucket.TopicConfigurationProperty.Topic``.
            :param filter: ``CfnBucket.TopicConfigurationProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html
            """
            self._values = {
                'event': event,
                'topic': topic,
            }
            if filter is not None: self._values["filter"] = filter

        @builtins.property
        def event(self) -> str:
            """``CfnBucket.TopicConfigurationProperty.Event``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html#cfn-s3-bucket-notificationconfig-topicconfig-event
            """
            return self._values.get('event')

        @builtins.property
        def topic(self) -> str:
            """``CfnBucket.TopicConfigurationProperty.Topic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html#cfn-s3-bucket-notificationconfig-topicconfig-topic
            """
            return self._values.get('topic')

        @builtins.property
        def filter(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationFilterProperty"]]]:
            """``CfnBucket.TopicConfigurationProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html#cfn-s3-bucket-notificationconfig-topicconfig-filter
            """
            return self._values.get('filter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TopicConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.TransitionProperty", jsii_struct_bases=[], name_mapping={'storage_class': 'storageClass', 'transition_date': 'transitionDate', 'transition_in_days': 'transitionInDays'})
    class TransitionProperty():
        def __init__(self, *, storage_class: str, transition_date: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]=None, transition_in_days: typing.Optional[jsii.Number]=None):
            """
            :param storage_class: ``CfnBucket.TransitionProperty.StorageClass``.
            :param transition_date: ``CfnBucket.TransitionProperty.TransitionDate``.
            :param transition_in_days: ``CfnBucket.TransitionProperty.TransitionInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html
            """
            self._values = {
                'storage_class': storage_class,
            }
            if transition_date is not None: self._values["transition_date"] = transition_date
            if transition_in_days is not None: self._values["transition_in_days"] = transition_in_days

        @builtins.property
        def storage_class(self) -> str:
            """``CfnBucket.TransitionProperty.StorageClass``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html#cfn-s3-bucket-lifecycleconfig-rule-transition-storageclass
            """
            return self._values.get('storage_class')

        @builtins.property
        def transition_date(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]:
            """``CfnBucket.TransitionProperty.TransitionDate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html#cfn-s3-bucket-lifecycleconfig-rule-transition-transitiondate
            """
            return self._values.get('transition_date')

        @builtins.property
        def transition_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnBucket.TransitionProperty.TransitionInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html#cfn-s3-bucket-lifecycleconfig-rule-transition-transitionindays
            """
            return self._values.get('transition_in_days')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TransitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.VersioningConfigurationProperty", jsii_struct_bases=[], name_mapping={'status': 'status'})
    class VersioningConfigurationProperty():
        def __init__(self, *, status: str):
            """
            :param status: ``CfnBucket.VersioningConfigurationProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html
            """
            self._values = {
                'status': status,
            }

        @builtins.property
        def status(self) -> str:
            """``CfnBucket.VersioningConfigurationProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html#cfn-s3-bucket-versioningconfig-status
            """
            return self._values.get('status')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VersioningConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucket.WebsiteConfigurationProperty", jsii_struct_bases=[], name_mapping={'error_document': 'errorDocument', 'index_document': 'indexDocument', 'redirect_all_requests_to': 'redirectAllRequestsTo', 'routing_rules': 'routingRules'})
    class WebsiteConfigurationProperty():
        def __init__(self, *, error_document: typing.Optional[str]=None, index_document: typing.Optional[str]=None, redirect_all_requests_to: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.RedirectAllRequestsToProperty"]]]=None, routing_rules: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.RoutingRuleProperty"]]]]]=None):
            """
            :param error_document: ``CfnBucket.WebsiteConfigurationProperty.ErrorDocument``.
            :param index_document: ``CfnBucket.WebsiteConfigurationProperty.IndexDocument``.
            :param redirect_all_requests_to: ``CfnBucket.WebsiteConfigurationProperty.RedirectAllRequestsTo``.
            :param routing_rules: ``CfnBucket.WebsiteConfigurationProperty.RoutingRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html
            """
            self._values = {
            }
            if error_document is not None: self._values["error_document"] = error_document
            if index_document is not None: self._values["index_document"] = index_document
            if redirect_all_requests_to is not None: self._values["redirect_all_requests_to"] = redirect_all_requests_to
            if routing_rules is not None: self._values["routing_rules"] = routing_rules

        @builtins.property
        def error_document(self) -> typing.Optional[str]:
            """``CfnBucket.WebsiteConfigurationProperty.ErrorDocument``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-errordocument
            """
            return self._values.get('error_document')

        @builtins.property
        def index_document(self) -> typing.Optional[str]:
            """``CfnBucket.WebsiteConfigurationProperty.IndexDocument``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-indexdocument
            """
            return self._values.get('index_document')

        @builtins.property
        def redirect_all_requests_to(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.RedirectAllRequestsToProperty"]]]:
            """``CfnBucket.WebsiteConfigurationProperty.RedirectAllRequestsTo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-redirectallrequeststo
            """
            return self._values.get('redirect_all_requests_to')

        @builtins.property
        def routing_rules(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.RoutingRuleProperty"]]]]]:
            """``CfnBucket.WebsiteConfigurationProperty.RoutingRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-routingrules
            """
            return self._values.get('routing_rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WebsiteConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnBucketPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.CfnBucketPolicy"):
    """A CloudFormation ``AWS::S3::BucketPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::S3::BucketPolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bucket: str, policy_document: typing.Any) -> None:
        """Create a new ``AWS::S3::BucketPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket: ``AWS::S3::BucketPolicy.Bucket``.
        :param policy_document: ``AWS::S3::BucketPolicy.PolicyDocument``.
        """
        props = CfnBucketPolicyProps(bucket=bucket, policy_document=policy_document)

        jsii.create(CfnBucketPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> str:
        """``AWS::S3::BucketPolicy.Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-bucket
        """
        return jsii.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: str):
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        """``AWS::S3::BucketPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-policydocument
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter
    def policy_document(self, value: typing.Any):
        jsii.set(self, "policyDocument", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucketPolicyProps", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'policy_document': 'policyDocument'})
class CfnBucketPolicyProps():
    def __init__(self, *, bucket: str, policy_document: typing.Any):
        """Properties for defining a ``AWS::S3::BucketPolicy``.

        :param bucket: ``AWS::S3::BucketPolicy.Bucket``.
        :param policy_document: ``AWS::S3::BucketPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html
        """
        self._values = {
            'bucket': bucket,
            'policy_document': policy_document,
        }

    @builtins.property
    def bucket(self) -> str:
        """``AWS::S3::BucketPolicy.Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-bucket
        """
        return self._values.get('bucket')

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::S3::BucketPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-policydocument
        """
        return self._values.get('policy_document')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBucketPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.CfnBucketProps", jsii_struct_bases=[], name_mapping={'accelerate_configuration': 'accelerateConfiguration', 'access_control': 'accessControl', 'analytics_configurations': 'analyticsConfigurations', 'bucket_encryption': 'bucketEncryption', 'bucket_name': 'bucketName', 'cors_configuration': 'corsConfiguration', 'inventory_configurations': 'inventoryConfigurations', 'lifecycle_configuration': 'lifecycleConfiguration', 'logging_configuration': 'loggingConfiguration', 'metrics_configurations': 'metricsConfigurations', 'notification_configuration': 'notificationConfiguration', 'object_lock_configuration': 'objectLockConfiguration', 'object_lock_enabled': 'objectLockEnabled', 'public_access_block_configuration': 'publicAccessBlockConfiguration', 'replication_configuration': 'replicationConfiguration', 'tags': 'tags', 'versioning_configuration': 'versioningConfiguration', 'website_configuration': 'websiteConfiguration'})
class CfnBucketProps():
    def __init__(self, *, accelerate_configuration: typing.Optional[typing.Union[typing.Optional["CfnBucket.AccelerateConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, access_control: typing.Optional[str]=None, analytics_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.AnalyticsConfigurationProperty"]]]]]=None, bucket_encryption: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.BucketEncryptionProperty"]]]=None, bucket_name: typing.Optional[str]=None, cors_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.CorsConfigurationProperty"]]]=None, inventory_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.InventoryConfigurationProperty"]]]]]=None, lifecycle_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.LifecycleConfigurationProperty"]]]=None, logging_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.LoggingConfigurationProperty"]]]=None, metrics_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.MetricsConfigurationProperty"]]]]]=None, notification_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationConfigurationProperty"]]]=None, object_lock_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ObjectLockConfigurationProperty"]]]=None, object_lock_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, public_access_block_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.PublicAccessBlockConfigurationProperty"]]]=None, replication_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ReplicationConfigurationProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, versioning_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.VersioningConfigurationProperty"]]]=None, website_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.WebsiteConfigurationProperty"]]]=None):
        """Properties for defining a ``AWS::S3::Bucket``.

        :param accelerate_configuration: ``AWS::S3::Bucket.AccelerateConfiguration``.
        :param access_control: ``AWS::S3::Bucket.AccessControl``.
        :param analytics_configurations: ``AWS::S3::Bucket.AnalyticsConfigurations``.
        :param bucket_encryption: ``AWS::S3::Bucket.BucketEncryption``.
        :param bucket_name: ``AWS::S3::Bucket.BucketName``.
        :param cors_configuration: ``AWS::S3::Bucket.CorsConfiguration``.
        :param inventory_configurations: ``AWS::S3::Bucket.InventoryConfigurations``.
        :param lifecycle_configuration: ``AWS::S3::Bucket.LifecycleConfiguration``.
        :param logging_configuration: ``AWS::S3::Bucket.LoggingConfiguration``.
        :param metrics_configurations: ``AWS::S3::Bucket.MetricsConfigurations``.
        :param notification_configuration: ``AWS::S3::Bucket.NotificationConfiguration``.
        :param object_lock_configuration: ``AWS::S3::Bucket.ObjectLockConfiguration``.
        :param object_lock_enabled: ``AWS::S3::Bucket.ObjectLockEnabled``.
        :param public_access_block_configuration: ``AWS::S3::Bucket.PublicAccessBlockConfiguration``.
        :param replication_configuration: ``AWS::S3::Bucket.ReplicationConfiguration``.
        :param tags: ``AWS::S3::Bucket.Tags``.
        :param versioning_configuration: ``AWS::S3::Bucket.VersioningConfiguration``.
        :param website_configuration: ``AWS::S3::Bucket.WebsiteConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html
        """
        self._values = {
        }
        if accelerate_configuration is not None: self._values["accelerate_configuration"] = accelerate_configuration
        if access_control is not None: self._values["access_control"] = access_control
        if analytics_configurations is not None: self._values["analytics_configurations"] = analytics_configurations
        if bucket_encryption is not None: self._values["bucket_encryption"] = bucket_encryption
        if bucket_name is not None: self._values["bucket_name"] = bucket_name
        if cors_configuration is not None: self._values["cors_configuration"] = cors_configuration
        if inventory_configurations is not None: self._values["inventory_configurations"] = inventory_configurations
        if lifecycle_configuration is not None: self._values["lifecycle_configuration"] = lifecycle_configuration
        if logging_configuration is not None: self._values["logging_configuration"] = logging_configuration
        if metrics_configurations is not None: self._values["metrics_configurations"] = metrics_configurations
        if notification_configuration is not None: self._values["notification_configuration"] = notification_configuration
        if object_lock_configuration is not None: self._values["object_lock_configuration"] = object_lock_configuration
        if object_lock_enabled is not None: self._values["object_lock_enabled"] = object_lock_enabled
        if public_access_block_configuration is not None: self._values["public_access_block_configuration"] = public_access_block_configuration
        if replication_configuration is not None: self._values["replication_configuration"] = replication_configuration
        if tags is not None: self._values["tags"] = tags
        if versioning_configuration is not None: self._values["versioning_configuration"] = versioning_configuration
        if website_configuration is not None: self._values["website_configuration"] = website_configuration

    @builtins.property
    def accelerate_configuration(self) -> typing.Optional[typing.Union[typing.Optional["CfnBucket.AccelerateConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::S3::Bucket.AccelerateConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accelerateconfiguration
        """
        return self._values.get('accelerate_configuration')

    @builtins.property
    def access_control(self) -> typing.Optional[str]:
        """``AWS::S3::Bucket.AccessControl``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accesscontrol
        """
        return self._values.get('access_control')

    @builtins.property
    def analytics_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.AnalyticsConfigurationProperty"]]]]]:
        """``AWS::S3::Bucket.AnalyticsConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-analyticsconfigurations
        """
        return self._values.get('analytics_configurations')

    @builtins.property
    def bucket_encryption(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.BucketEncryptionProperty"]]]:
        """``AWS::S3::Bucket.BucketEncryption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-bucketencryption
        """
        return self._values.get('bucket_encryption')

    @builtins.property
    def bucket_name(self) -> typing.Optional[str]:
        """``AWS::S3::Bucket.BucketName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-name
        """
        return self._values.get('bucket_name')

    @builtins.property
    def cors_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.CorsConfigurationProperty"]]]:
        """``AWS::S3::Bucket.CorsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-crossoriginconfig
        """
        return self._values.get('cors_configuration')

    @builtins.property
    def inventory_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.InventoryConfigurationProperty"]]]]]:
        """``AWS::S3::Bucket.InventoryConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-inventoryconfigurations
        """
        return self._values.get('inventory_configurations')

    @builtins.property
    def lifecycle_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.LifecycleConfigurationProperty"]]]:
        """``AWS::S3::Bucket.LifecycleConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-lifecycleconfig
        """
        return self._values.get('lifecycle_configuration')

    @builtins.property
    def logging_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.LoggingConfigurationProperty"]]]:
        """``AWS::S3::Bucket.LoggingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-loggingconfig
        """
        return self._values.get('logging_configuration')

    @builtins.property
    def metrics_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnBucket.MetricsConfigurationProperty"]]]]]:
        """``AWS::S3::Bucket.MetricsConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-metricsconfigurations
        """
        return self._values.get('metrics_configurations')

    @builtins.property
    def notification_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.NotificationConfigurationProperty"]]]:
        """``AWS::S3::Bucket.NotificationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-notification
        """
        return self._values.get('notification_configuration')

    @builtins.property
    def object_lock_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ObjectLockConfigurationProperty"]]]:
        """``AWS::S3::Bucket.ObjectLockConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockconfiguration
        """
        return self._values.get('object_lock_configuration')

    @builtins.property
    def object_lock_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::S3::Bucket.ObjectLockEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockenabled
        """
        return self._values.get('object_lock_enabled')

    @builtins.property
    def public_access_block_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.PublicAccessBlockConfigurationProperty"]]]:
        """``AWS::S3::Bucket.PublicAccessBlockConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-publicaccessblockconfiguration
        """
        return self._values.get('public_access_block_configuration')

    @builtins.property
    def replication_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.ReplicationConfigurationProperty"]]]:
        """``AWS::S3::Bucket.ReplicationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-replicationconfiguration
        """
        return self._values.get('replication_configuration')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::S3::Bucket.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-tags
        """
        return self._values.get('tags')

    @builtins.property
    def versioning_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.VersioningConfigurationProperty"]]]:
        """``AWS::S3::Bucket.VersioningConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-versioning
        """
        return self._values.get('versioning_configuration')

    @builtins.property
    def website_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnBucket.WebsiteConfigurationProperty"]]]:
        """``AWS::S3::Bucket.WebsiteConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-websiteconfiguration
        """
        return self._values.get('website_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBucketProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.CorsRule", jsii_struct_bases=[], name_mapping={'allowed_methods': 'allowedMethods', 'allowed_origins': 'allowedOrigins', 'allowed_headers': 'allowedHeaders', 'exposed_headers': 'exposedHeaders', 'id': 'id', 'max_age': 'maxAge'})
class CorsRule():
    def __init__(self, *, allowed_methods: typing.List["HttpMethods"], allowed_origins: typing.List[str], allowed_headers: typing.Optional[typing.List[str]]=None, exposed_headers: typing.Optional[typing.List[str]]=None, id: typing.Optional[str]=None, max_age: typing.Optional[jsii.Number]=None):
        """Specifies a cross-origin access rule for an Amazon S3 bucket.

        :param allowed_methods: An HTTP method that you allow the origin to execute.
        :param allowed_origins: One or more origins you want customers to be able to access the bucket from.
        :param allowed_headers: Headers that are specified in the Access-Control-Request-Headers header. Default: - No headers allowed.
        :param exposed_headers: One or more headers in the response that you want customers to be able to access from their applications. Default: - No headers exposed.
        :param id: A unique identifier for this rule. Default: - No id specified.
        :param max_age: The time in seconds that your browser is to cache the preflight response for the specified resource. Default: - No caching.
        """
        self._values = {
            'allowed_methods': allowed_methods,
            'allowed_origins': allowed_origins,
        }
        if allowed_headers is not None: self._values["allowed_headers"] = allowed_headers
        if exposed_headers is not None: self._values["exposed_headers"] = exposed_headers
        if id is not None: self._values["id"] = id
        if max_age is not None: self._values["max_age"] = max_age

    @builtins.property
    def allowed_methods(self) -> typing.List["HttpMethods"]:
        """An HTTP method that you allow the origin to execute."""
        return self._values.get('allowed_methods')

    @builtins.property
    def allowed_origins(self) -> typing.List[str]:
        """One or more origins you want customers to be able to access the bucket from."""
        return self._values.get('allowed_origins')

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[str]]:
        """Headers that are specified in the Access-Control-Request-Headers header.

        default
        :default: - No headers allowed.
        """
        return self._values.get('allowed_headers')

    @builtins.property
    def exposed_headers(self) -> typing.Optional[typing.List[str]]:
        """One or more headers in the response that you want customers to be able to access from their applications.

        default
        :default: - No headers exposed.
        """
        return self._values.get('exposed_headers')

    @builtins.property
    def id(self) -> typing.Optional[str]:
        """A unique identifier for this rule.

        default
        :default: - No id specified.
        """
        return self._values.get('id')

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        """The time in seconds that your browser is to cache the preflight response for the specified resource.

        default
        :default: - No caching.
        """
        return self._values.get('max_age')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CorsRule(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-s3.EventType")
class EventType(enum.Enum):
    """Notification event types."""
    OBJECT_CREATED = "OBJECT_CREATED"
    """Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.
    """
    OBJECT_CREATED_PUT = "OBJECT_CREATED_PUT"
    """Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.
    """
    OBJECT_CREATED_POST = "OBJECT_CREATED_POST"
    """Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.
    """
    OBJECT_CREATED_COPY = "OBJECT_CREATED_COPY"
    """Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.
    """
    OBJECT_CREATED_COMPLETE_MULTIPART_UPLOAD = "OBJECT_CREATED_COMPLETE_MULTIPART_UPLOAD"
    """Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.
    """
    OBJECT_REMOVED = "OBJECT_REMOVED"
    """By using the ObjectRemoved event types, you can enable notification when an object or a batch of objects is removed from a bucket.

    You can request notification when an object is deleted or a versioned
    object is permanently deleted by using the s3:ObjectRemoved:Delete event
    type. Or you can request notification when a delete marker is created for
    a versioned object by using s3:ObjectRemoved:DeleteMarkerCreated. For
    information about deleting versioned objects, see Deleting Object
    Versions. You can also use a wildcard s3:ObjectRemoved:* to request
    notification anytime an object is deleted.

    You will not receive event notifications from automatic deletes from
    lifecycle policies or from failed operations.
    """
    OBJECT_REMOVED_DELETE = "OBJECT_REMOVED_DELETE"
    """By using the ObjectRemoved event types, you can enable notification when an object or a batch of objects is removed from a bucket.

    You can request notification when an object is deleted or a versioned
    object is permanently deleted by using the s3:ObjectRemoved:Delete event
    type. Or you can request notification when a delete marker is created for
    a versioned object by using s3:ObjectRemoved:DeleteMarkerCreated. For
    information about deleting versioned objects, see Deleting Object
    Versions. You can also use a wildcard s3:ObjectRemoved:* to request
    notification anytime an object is deleted.

    You will not receive event notifications from automatic deletes from
    lifecycle policies or from failed operations.
    """
    OBJECT_REMOVED_DELETE_MARKER_CREATED = "OBJECT_REMOVED_DELETE_MARKER_CREATED"
    """By using the ObjectRemoved event types, you can enable notification when an object or a batch of objects is removed from a bucket.

    You can request notification when an object is deleted or a versioned
    object is permanently deleted by using the s3:ObjectRemoved:Delete event
    type. Or you can request notification when a delete marker is created for
    a versioned object by using s3:ObjectRemoved:DeleteMarkerCreated. For
    information about deleting versioned objects, see Deleting Object
    Versions. You can also use a wildcard s3:ObjectRemoved:* to request
    notification anytime an object is deleted.

    You will not receive event notifications from automatic deletes from
    lifecycle policies or from failed operations.
    """
    REDUCED_REDUNDANCY_LOST_OBJECT = "REDUCED_REDUNDANCY_LOST_OBJECT"
    """You can use this event type to request Amazon S3 to send a notification message when Amazon S3 detects that an object of the RRS storage class is lost."""

@jsii.enum(jsii_type="@aws-cdk/aws-s3.HttpMethods")
class HttpMethods(enum.Enum):
    """All http request methods."""
    GET = "GET"
    """The GET method requests a representation of the specified resource."""
    PUT = "PUT"
    """The PUT method replaces all current representations of the target resource with the request payload."""
    HEAD = "HEAD"
    """The HEAD method asks for a response identical to that of a GET request, but without the response body."""
    POST = "POST"
    """The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server."""
    DELETE = "DELETE"
    """The DELETE method deletes the specified resource."""

@jsii.interface(jsii_type="@aws-cdk/aws-s3.IBucket")
class IBucket(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBucketProxy

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        """The ARN of the bucket.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> str:
        """The IPv4 DNS name of the specified bucket.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> str:
        """The IPv6 DNS name of the specified bucket.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        """The name of the bucket.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> str:
        """The regional domain name of the specified bucket.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> str:
        """The Domain name of the static website.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> str:
        """The URL of the static website.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this bucket."""
        ...

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        """The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).
        """
        ...

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, permission: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or it's contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        :param permission: -
        """
        ...

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, key_pattern: str) -> str:
        """Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        :param key_pattern: -
        """
        ...

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants s3:DeleteObject* permission to an IAM pricipal for objects in this bucket.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        ...

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(self, key_prefix: typing.Optional[str]=None, *allowed_actions: str) -> aws_cdk.aws_iam.Grant:
        """Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param key_prefix: the prefix of S3 object keys (e.g. ``home/*``). Default is "*".
        :param allowed_actions: the set of S3 actions to allow. Default is "s3:GetObject".

        return
        :return: The ``iam.PolicyStatement`` object, which can be used to apply e.g. conditions.
        """
        ...

    @jsii.member(jsii_name="grantPut")
    def grant_put(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event that triggers when something happens to this bucket.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[str]=None) -> str:
        """The https URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.

        return
        :return: an ObjectS3Url token

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        ...


class _IBucketProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-s3.IBucket"
    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        """The ARN of the bucket.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketArn")

    @builtins.property
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> str:
        """The IPv4 DNS name of the specified bucket.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> str:
        """The IPv6 DNS name of the specified bucket.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketDualStackDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        """The name of the bucket.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketName")

    @builtins.property
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> str:
        """The regional domain name of the specified bucket.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketRegionalDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> str:
        """The Domain name of the static website.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketWebsiteDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> str:
        """The URL of the static website.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "bucketWebsiteUrl")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this bucket."""
        return jsii.get(self, "encryptionKey")

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        """The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        jsii.set(self, "policy", value)

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, permission: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or it's contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        :param permission: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [permission])

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, key_pattern: str) -> str:
        """Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        :param key_pattern: -
        """
        return jsii.invoke(self, "arnForObjects", [key_pattern])

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants s3:DeleteObject* permission to an IAM pricipal for objects in this bucket.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantDelete", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(self, key_prefix: typing.Optional[str]=None, *allowed_actions: str) -> aws_cdk.aws_iam.Grant:
        """Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param key_prefix: the prefix of S3 object keys (e.g. ``home/*``). Default is "*".
        :param allowed_actions: the set of S3 actions to allow. Default is "s3:GetObject".

        return
        :return: The ``iam.PolicyStatement`` object, which can be used to apply e.g. conditions.
        """
        return jsii.invoke(self, "grantPublicAccess", [key_prefix, *allowed_actions])

    @jsii.member(jsii_name="grantPut")
    def grant_put(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantPut", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantRead", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantReadWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event that triggers when something happens to this bucket.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailBucketEventOptions(paths=paths, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailBucketEventOptions(paths=paths, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailPutObject", [id, options])

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailBucketEventOptions(paths=paths, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailWriteObject", [id, options])

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[str]=None) -> str:
        """The https URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.

        return
        :return: an ObjectS3Url token

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.invoke(self, "urlForObject", [key])


@jsii.implements(IBucket)
class Bucket(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.Bucket"):
    """An S3 bucket with associated policy objects.

    This bucket does not yet have all features that exposed by the underlying
    BucketResource.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, access_control: typing.Optional["BucketAccessControl"]=None, block_public_access: typing.Optional["BlockPublicAccess"]=None, bucket_name: typing.Optional[str]=None, cors: typing.Optional[typing.List["CorsRule"]]=None, encryption: typing.Optional["BucketEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, metrics: typing.Optional[typing.List["BucketMetrics"]]=None, public_read_access: typing.Optional[bool]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, server_access_logs_bucket: typing.Optional["IBucket"]=None, server_access_logs_prefix: typing.Optional[str]=None, versioned: typing.Optional[bool]=None, website_error_document: typing.Optional[str]=None, website_index_document: typing.Optional[str]=None, website_redirect: typing.Optional["RedirectTarget"]=None, website_routing_rules: typing.Optional[typing.List["RoutingRule"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param block_public_access: The block public access configuration of this bucket. Default: false New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access.
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - Access logs are disabled
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. Default: - No log file prefix
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.
        """
        props = BucketProps(access_control=access_control, block_public_access=block_public_access, bucket_name=bucket_name, cors=cors, encryption=encryption, encryption_key=encryption_key, lifecycle_rules=lifecycle_rules, metrics=metrics, public_read_access=public_read_access, removal_policy=removal_policy, server_access_logs_bucket=server_access_logs_bucket, server_access_logs_prefix=server_access_logs_prefix, versioned=versioned, website_error_document=website_error_document, website_index_document=website_index_document, website_redirect=website_redirect, website_routing_rules=website_routing_rules)

        jsii.create(Bucket, self, [scope, id, props])

    @jsii.member(jsii_name="fromBucketArn")
    @builtins.classmethod
    def from_bucket_arn(cls, scope: aws_cdk.core.Construct, id: str, bucket_arn: str) -> "IBucket":
        """
        :param scope: -
        :param id: -
        :param bucket_arn: -
        """
        return jsii.sinvoke(cls, "fromBucketArn", [scope, id, bucket_arn])

    @jsii.member(jsii_name="fromBucketAttributes")
    @builtins.classmethod
    def from_bucket_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, bucket_arn: typing.Optional[str]=None, bucket_domain_name: typing.Optional[str]=None, bucket_dual_stack_domain_name: typing.Optional[str]=None, bucket_name: typing.Optional[str]=None, bucket_regional_domain_name: typing.Optional[str]=None, bucket_website_new_url_format: typing.Optional[bool]=None, bucket_website_url: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> "IBucket":
        """Creates a Bucket construct that represents an external bucket.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param bucket_arn: The ARN of the bucket. At least one of bucketArn or bucketName must be defined in order to initialize a bucket ref.
        :param bucket_domain_name: The domain name of the bucket. Default: Inferred from bucket name
        :param bucket_dual_stack_domain_name: The IPv6 DNS name of the specified bucket.
        :param bucket_name: The name of the bucket. If the underlying value of ARN is a string, the name will be parsed from the ARN. Otherwise, the name is optional, but some features that require the bucket name such as auto-creating a bucket policy, won't work.
        :param bucket_regional_domain_name: The regional domain name of the specified bucket.
        :param bucket_website_new_url_format: The format of the website URL of the bucket. This should be true for regions launched since 2014. Default: false
        :param bucket_website_url: The website URL of the bucket (if static web hosting is enabled). Default: Inferred from bucket name
        :param encryption_key: 
        """
        attrs = BucketAttributes(bucket_arn=bucket_arn, bucket_domain_name=bucket_domain_name, bucket_dual_stack_domain_name=bucket_dual_stack_domain_name, bucket_name=bucket_name, bucket_regional_domain_name=bucket_regional_domain_name, bucket_website_new_url_format=bucket_website_new_url_format, bucket_website_url=bucket_website_url, encryption_key=encryption_key)

        return jsii.sinvoke(cls, "fromBucketAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromBucketName")
    @builtins.classmethod
    def from_bucket_name(cls, scope: aws_cdk.core.Construct, id: str, bucket_name: str) -> "IBucket":
        """
        :param scope: -
        :param id: -
        :param bucket_name: -
        """
        return jsii.sinvoke(cls, "fromBucketName", [scope, id, bucket_name])

    @jsii.member(jsii_name="addCorsRule")
    def add_cors_rule(self, *, allowed_methods: typing.List["HttpMethods"], allowed_origins: typing.List[str], allowed_headers: typing.Optional[typing.List[str]]=None, exposed_headers: typing.Optional[typing.List[str]]=None, id: typing.Optional[str]=None, max_age: typing.Optional[jsii.Number]=None) -> None:
        """Adds a cross-origin access configuration for objects in an Amazon S3 bucket.

        :param allowed_methods: An HTTP method that you allow the origin to execute.
        :param allowed_origins: One or more origins you want customers to be able to access the bucket from.
        :param allowed_headers: Headers that are specified in the Access-Control-Request-Headers header. Default: - No headers allowed.
        :param exposed_headers: One or more headers in the response that you want customers to be able to access from their applications. Default: - No headers exposed.
        :param id: A unique identifier for this rule. Default: - No id specified.
        :param max_age: The time in seconds that your browser is to cache the preflight response for the specified resource. Default: - No caching.
        """
        rule = CorsRule(allowed_methods=allowed_methods, allowed_origins=allowed_origins, allowed_headers=allowed_headers, exposed_headers=exposed_headers, id=id, max_age=max_age)

        return jsii.invoke(self, "addCorsRule", [rule])

    @jsii.member(jsii_name="addEventNotification")
    def add_event_notification(self, event: "EventType", dest: "IBucketNotificationDestination", *filters: "NotificationKeyFilter") -> None:
        """Adds a bucket notification event destination.

        :param event: The event to trigger the notification.
        :param dest: The notification destination (Lambda, SNS Topic or SQS Queue).
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            bucket.add_event_notification(EventType.OnObjectCreated, my_lambda, "home/myusername/*")
        """
        return jsii.invoke(self, "addEventNotification", [event, dest, *filters])

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(self, *, abort_incomplete_multipart_upload_after: typing.Optional[aws_cdk.core.Duration]=None, enabled: typing.Optional[bool]=None, expiration: typing.Optional[aws_cdk.core.Duration]=None, expiration_date: typing.Optional[datetime.datetime]=None, id: typing.Optional[str]=None, noncurrent_version_expiration: typing.Optional[aws_cdk.core.Duration]=None, noncurrent_version_transitions: typing.Optional[typing.List["NoncurrentVersionTransition"]]=None, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Mapping[str,typing.Any]]=None, transitions: typing.Optional[typing.List["Transition"]]=None) -> None:
        """Add a lifecycle rule to the bucket.

        :param abort_incomplete_multipart_upload_after: Specifies a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. The AbortIncompleteMultipartUpload property type creates a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. When Amazon S3 aborts a multipart upload, it deletes all parts associated with the multipart upload. Default: Incomplete uploads are never aborted
        :param enabled: Whether this rule is enabled. Default: true
        :param expiration: Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon Glacier. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration timeout
        :param expiration_date: Indicates when objects are deleted from Amazon S3 and Amazon Glacier. The date value must be in ISO 8601 format. The time is always midnight UTC. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration date
        :param id: A unique identifier for this rule. The value cannot be more than 255 characters.
        :param noncurrent_version_expiration: Time between when a new version of the object is uploaded to the bucket and when old versions of the object expire. For buckets with versioning enabled (or suspended), specifies the time, in days, between when a new version of the object is uploaded to the bucket and when old versions of the object expire. When object versions expire, Amazon S3 permanently deletes them. If you specify a transition and expiration time, the expiration time must be later than the transition time. Default: No noncurrent version expiration
        :param noncurrent_version_transitions: One or more transition rules that specify when non-current objects transition to a specified storage class. Only for for buckets with versioning enabled (or suspended). If you specify a transition and expiration time, the expiration time must be later than the transition time.
        :param prefix: Object key prefix that identifies one or more objects to which this rule applies. Default: Rule applies to all objects
        :param tag_filters: The TagFilter property type specifies tags to use to identify a subset of objects for an Amazon S3 bucket. Default: Rule applies to all objects
        :param transitions: One or more transition rules that specify when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No transition rules
        """
        rule = LifecycleRule(abort_incomplete_multipart_upload_after=abort_incomplete_multipart_upload_after, enabled=enabled, expiration=expiration, expiration_date=expiration_date, id=id, noncurrent_version_expiration=noncurrent_version_expiration, noncurrent_version_transitions=noncurrent_version_transitions, prefix=prefix, tag_filters=tag_filters, transitions=transitions)

        return jsii.invoke(self, "addLifecycleRule", [rule])

    @jsii.member(jsii_name="addMetric")
    def add_metric(self, *, id: str, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """Adds a metrics configuration for the CloudWatch request metrics from the bucket.

        :param id: The ID used to identify the metrics configuration.
        :param prefix: The prefix that an object must have to be included in the metrics results.
        :param tag_filters: Specifies a list of tag filters to use as a metrics configuration filter. The metrics configuration includes only objects that meet the filter's criteria.
        """
        metric = BucketMetrics(id=id, prefix=prefix, tag_filters=tag_filters)

        return jsii.invoke(self, "addMetric", [metric])

    @jsii.member(jsii_name="addObjectCreatedNotification")
    def add_object_created_notification(self, dest: "IBucketNotificationDestination", *filters: "NotificationKeyFilter") -> None:
        """Subscribes a destination to receive notificatins when an object is created in the bucket.

        This is identical to calling
        ``onEvent(EventType.ObjectCreated)``.

        :param dest: The notification destination (see onEvent).
        :param filters: Filters (see onEvent).
        """
        return jsii.invoke(self, "addObjectCreatedNotification", [dest, *filters])

    @jsii.member(jsii_name="addObjectRemovedNotification")
    def add_object_removed_notification(self, dest: "IBucketNotificationDestination", *filters: "NotificationKeyFilter") -> None:
        """Subscribes a destination to receive notificatins when an object is removed from the bucket.

        This is identical to calling
        ``onEvent(EventType.ObjectRemoved)``.

        :param dest: The notification destination (see onEvent).
        :param filters: Filters (see onEvent).
        """
        return jsii.invoke(self, "addObjectRemovedNotification", [dest, *filters])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, permission: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or it's contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        :param permission: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [permission])

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, key_pattern: str) -> str:
        """Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        If you specify multiple components for keyPattern, they will be concatenated::

        arnForObjects('home/', team, '/', user, '/*')

        :param key_pattern: -
        """
        return jsii.invoke(self, "arnForObjects", [key_pattern])

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants s3:DeleteObject* permission to an IAM pricipal for objects in this bucket.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantDelete", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(self, key_prefix: typing.Optional[str]=None, *allowed_actions: str) -> aws_cdk.aws_iam.Grant:
        """Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param key_prefix: the prefix of S3 object keys (e.g. ``home/*``). Default is "*".
        :param allowed_actions: the set of S3 actions to allow. Default is "s3:GetObject".
        """
        return jsii.invoke(self, "grantPublicAccess", [key_prefix, *allowed_actions])

    @jsii.member(jsii_name="grantPut")
    def grant_put(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantPut", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantRead", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantReadWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: aws_cdk.aws_iam.IGrantable, objects_key_pattern: typing.Any=None) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').
        """
        return jsii.invoke(self, "grantWrite", [identity, objects_key_pattern])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailBucketEventOptions(paths=paths, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailBucketEventOptions(paths=paths, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailPutObject", [id, options])

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(self, id: str, *, paths: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailBucketEventOptions(paths=paths, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailWriteObject", [id, options])

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[str]=None) -> str:
        """The https URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.

        return
        :return: an ObjectS3Url token

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.invoke(self, "urlForObject", [key])

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> str:
        """The ARN of the bucket."""
        return jsii.get(self, "bucketArn")

    @builtins.property
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> str:
        """The IPv4 DNS name of the specified bucket."""
        return jsii.get(self, "bucketDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> str:
        """The IPv6 DNS name of the specified bucket."""
        return jsii.get(self, "bucketDualStackDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        """The name of the bucket."""
        return jsii.get(self, "bucketName")

    @builtins.property
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> str:
        """The regional domain name of the specified bucket."""
        return jsii.get(self, "bucketRegionalDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> str:
        """The Domain name of the static website."""
        return jsii.get(self, "bucketWebsiteDomainName")

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> str:
        """The URL of the static website."""
        return jsii.get(self, "bucketWebsiteUrl")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this bucket."""
        return jsii.get(self, "encryptionKey")

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Indicates if a bucket resource policy should automatically created upon the first call to ``addToResourcePolicy``."""
        return jsii.get(self, "autoCreatePolicy")

    @_auto_create_policy.setter
    def _auto_create_policy(self, value: bool):
        jsii.set(self, "autoCreatePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="disallowPublicAccess")
    def _disallow_public_access(self) -> typing.Optional[bool]:
        """Whether to disallow public access."""
        return jsii.get(self, "disallowPublicAccess")

    @_disallow_public_access.setter
    def _disallow_public_access(self, value: typing.Optional[bool]):
        jsii.set(self, "disallowPublicAccess", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional["BucketPolicy"]:
        """The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional["BucketPolicy"]):
        jsii.set(self, "policy", value)


@jsii.interface(jsii_type="@aws-cdk/aws-s3.IBucketNotificationDestination")
class IBucketNotificationDestination(jsii.compat.Protocol):
    """Implemented by constructs that can be used as bucket notification destinations."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBucketNotificationDestinationProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, bucket: "IBucket") -> "BucketNotificationDestinationConfig":
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param scope: -
        :param bucket: The bucket object to bind to.
        """
        ...


class _IBucketNotificationDestinationProxy():
    """Implemented by constructs that can be used as bucket notification destinations."""
    __jsii_type__ = "@aws-cdk/aws-s3.IBucketNotificationDestination"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, bucket: "IBucket") -> "BucketNotificationDestinationConfig":
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param scope: -
        :param bucket: The bucket object to bind to.
        """
        return jsii.invoke(self, "bind", [scope, bucket])


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.LifecycleRule", jsii_struct_bases=[], name_mapping={'abort_incomplete_multipart_upload_after': 'abortIncompleteMultipartUploadAfter', 'enabled': 'enabled', 'expiration': 'expiration', 'expiration_date': 'expirationDate', 'id': 'id', 'noncurrent_version_expiration': 'noncurrentVersionExpiration', 'noncurrent_version_transitions': 'noncurrentVersionTransitions', 'prefix': 'prefix', 'tag_filters': 'tagFilters', 'transitions': 'transitions'})
class LifecycleRule():
    def __init__(self, *, abort_incomplete_multipart_upload_after: typing.Optional[aws_cdk.core.Duration]=None, enabled: typing.Optional[bool]=None, expiration: typing.Optional[aws_cdk.core.Duration]=None, expiration_date: typing.Optional[datetime.datetime]=None, id: typing.Optional[str]=None, noncurrent_version_expiration: typing.Optional[aws_cdk.core.Duration]=None, noncurrent_version_transitions: typing.Optional[typing.List["NoncurrentVersionTransition"]]=None, prefix: typing.Optional[str]=None, tag_filters: typing.Optional[typing.Mapping[str,typing.Any]]=None, transitions: typing.Optional[typing.List["Transition"]]=None):
        """Declaration of a Life cycle rule.

        :param abort_incomplete_multipart_upload_after: Specifies a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. The AbortIncompleteMultipartUpload property type creates a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. When Amazon S3 aborts a multipart upload, it deletes all parts associated with the multipart upload. Default: Incomplete uploads are never aborted
        :param enabled: Whether this rule is enabled. Default: true
        :param expiration: Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon Glacier. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration timeout
        :param expiration_date: Indicates when objects are deleted from Amazon S3 and Amazon Glacier. The date value must be in ISO 8601 format. The time is always midnight UTC. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration date
        :param id: A unique identifier for this rule. The value cannot be more than 255 characters.
        :param noncurrent_version_expiration: Time between when a new version of the object is uploaded to the bucket and when old versions of the object expire. For buckets with versioning enabled (or suspended), specifies the time, in days, between when a new version of the object is uploaded to the bucket and when old versions of the object expire. When object versions expire, Amazon S3 permanently deletes them. If you specify a transition and expiration time, the expiration time must be later than the transition time. Default: No noncurrent version expiration
        :param noncurrent_version_transitions: One or more transition rules that specify when non-current objects transition to a specified storage class. Only for for buckets with versioning enabled (or suspended). If you specify a transition and expiration time, the expiration time must be later than the transition time.
        :param prefix: Object key prefix that identifies one or more objects to which this rule applies. Default: Rule applies to all objects
        :param tag_filters: The TagFilter property type specifies tags to use to identify a subset of objects for an Amazon S3 bucket. Default: Rule applies to all objects
        :param transitions: One or more transition rules that specify when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No transition rules
        """
        self._values = {
        }
        if abort_incomplete_multipart_upload_after is not None: self._values["abort_incomplete_multipart_upload_after"] = abort_incomplete_multipart_upload_after
        if enabled is not None: self._values["enabled"] = enabled
        if expiration is not None: self._values["expiration"] = expiration
        if expiration_date is not None: self._values["expiration_date"] = expiration_date
        if id is not None: self._values["id"] = id
        if noncurrent_version_expiration is not None: self._values["noncurrent_version_expiration"] = noncurrent_version_expiration
        if noncurrent_version_transitions is not None: self._values["noncurrent_version_transitions"] = noncurrent_version_transitions
        if prefix is not None: self._values["prefix"] = prefix
        if tag_filters is not None: self._values["tag_filters"] = tag_filters
        if transitions is not None: self._values["transitions"] = transitions

    @builtins.property
    def abort_incomplete_multipart_upload_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket.

        The AbortIncompleteMultipartUpload property type creates a lifecycle
        rule that aborts incomplete multipart uploads to an Amazon S3 bucket.
        When Amazon S3 aborts a multipart upload, it deletes all parts
        associated with the multipart upload.

        default
        :default: Incomplete uploads are never aborted
        """
        return self._values.get('abort_incomplete_multipart_upload_after')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """Whether this rule is enabled.

        default
        :default: true
        """
        return self._values.get('enabled')

    @builtins.property
    def expiration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon Glacier.

        If you specify an expiration and transition time, you must use the same
        time unit for both properties (either in days or by date). The
        expiration time must also be later than the transition time.

        default
        :default: No expiration timeout
        """
        return self._values.get('expiration')

    @builtins.property
    def expiration_date(self) -> typing.Optional[datetime.datetime]:
        """Indicates when objects are deleted from Amazon S3 and Amazon Glacier.

        The date value must be in ISO 8601 format. The time is always midnight UTC.

        If you specify an expiration and transition time, you must use the same
        time unit for both properties (either in days or by date). The
        expiration time must also be later than the transition time.

        default
        :default: No expiration date
        """
        return self._values.get('expiration_date')

    @builtins.property
    def id(self) -> typing.Optional[str]:
        """A unique identifier for this rule.

        The value cannot be more than 255 characters.
        """
        return self._values.get('id')

    @builtins.property
    def noncurrent_version_expiration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time between when a new version of the object is uploaded to the bucket and when old versions of the object expire.

        For buckets with versioning enabled (or suspended), specifies the time,
        in days, between when a new version of the object is uploaded to the
        bucket and when old versions of the object expire. When object versions
        expire, Amazon S3 permanently deletes them. If you specify a transition
        and expiration time, the expiration time must be later than the
        transition time.

        default
        :default: No noncurrent version expiration
        """
        return self._values.get('noncurrent_version_expiration')

    @builtins.property
    def noncurrent_version_transitions(self) -> typing.Optional[typing.List["NoncurrentVersionTransition"]]:
        """One or more transition rules that specify when non-current objects transition to a specified storage class.

        Only for for buckets with versioning enabled (or suspended).

        If you specify a transition and expiration time, the expiration time
        must be later than the transition time.
        """
        return self._values.get('noncurrent_version_transitions')

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """Object key prefix that identifies one or more objects to which this rule applies.

        default
        :default: Rule applies to all objects
        """
        return self._values.get('prefix')

    @builtins.property
    def tag_filters(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """The TagFilter property type specifies tags to use to identify a subset of objects for an Amazon S3 bucket.

        default
        :default: Rule applies to all objects
        """
        return self._values.get('tag_filters')

    @builtins.property
    def transitions(self) -> typing.Optional[typing.List["Transition"]]:
        """One or more transition rules that specify when an object transitions to a specified storage class.

        If you specify an expiration and transition time, you must use the same
        time unit for both properties (either in days or by date). The
        expiration time must also be later than the transition time.

        default
        :default: No transition rules
        """
        return self._values.get('transitions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LifecycleRule(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.Location", jsii_struct_bases=[], name_mapping={'bucket_name': 'bucketName', 'object_key': 'objectKey', 'object_version': 'objectVersion'})
class Location():
    def __init__(self, *, bucket_name: str, object_key: str, object_version: typing.Optional[str]=None):
        """An interface that represents the location of a specific object in an S3 Bucket.

        :param bucket_name: The name of the S3 Bucket the object is in.
        :param object_key: The path inside the Bucket where the object is located at.
        :param object_version: The S3 object version.
        """
        self._values = {
            'bucket_name': bucket_name,
            'object_key': object_key,
        }
        if object_version is not None: self._values["object_version"] = object_version

    @builtins.property
    def bucket_name(self) -> str:
        """The name of the S3 Bucket the object is in."""
        return self._values.get('bucket_name')

    @builtins.property
    def object_key(self) -> str:
        """The path inside the Bucket where the object is located at."""
        return self._values.get('object_key')

    @builtins.property
    def object_version(self) -> typing.Optional[str]:
        """The S3 object version."""
        return self._values.get('object_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Location(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.NoncurrentVersionTransition", jsii_struct_bases=[], name_mapping={'storage_class': 'storageClass', 'transition_after': 'transitionAfter'})
class NoncurrentVersionTransition():
    def __init__(self, *, storage_class: "StorageClass", transition_after: aws_cdk.core.Duration):
        """Describes when noncurrent versions transition to a specified storage class.

        :param storage_class: The storage class to which you want the object to transition.
        :param transition_after: Indicates the number of days after creation when objects are transitioned to the specified storage class. Default: No transition count.
        """
        self._values = {
            'storage_class': storage_class,
            'transition_after': transition_after,
        }

    @builtins.property
    def storage_class(self) -> "StorageClass":
        """The storage class to which you want the object to transition."""
        return self._values.get('storage_class')

    @builtins.property
    def transition_after(self) -> aws_cdk.core.Duration:
        """Indicates the number of days after creation when objects are transitioned to the specified storage class.

        default
        :default: No transition count.
        """
        return self._values.get('transition_after')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NoncurrentVersionTransition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.NotificationKeyFilter", jsii_struct_bases=[], name_mapping={'prefix': 'prefix', 'suffix': 'suffix'})
class NotificationKeyFilter():
    def __init__(self, *, prefix: typing.Optional[str]=None, suffix: typing.Optional[str]=None):
        """
        :param prefix: S3 keys must have the specified prefix.
        :param suffix: S3 keys must have the specified suffix.
        """
        self._values = {
        }
        if prefix is not None: self._values["prefix"] = prefix
        if suffix is not None: self._values["suffix"] = suffix

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """S3 keys must have the specified prefix."""
        return self._values.get('prefix')

    @builtins.property
    def suffix(self) -> typing.Optional[str]:
        """S3 keys must have the specified suffix."""
        return self._values.get('suffix')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NotificationKeyFilter(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.OnCloudTrailBucketEventOptions", jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions], name_mapping={'description': 'description', 'event_pattern': 'eventPattern', 'rule_name': 'ruleName', 'target': 'target', 'paths': 'paths'})
class OnCloudTrailBucketEventOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(self, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, paths: typing.Optional[typing.List[str]]=None):
        """Options for the onCloudTrailPutObject method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        """
        if isinstance(event_pattern, dict): event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if rule_name is not None: self._values["rule_name"] = rule_name
        if target is not None: self._values["target"] = target
        if paths is not None: self._values["paths"] = paths

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the rule's purpose.

        default
        :default: - No description
        """
        return self._values.get('description')

    @builtins.property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        default
        :default: - No additional filtering based on an event pattern.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CloudWatchEventsandEventPatterns.html
        """
        return self._values.get('event_pattern')

    @builtins.property
    def rule_name(self) -> typing.Optional[str]:
        """A name for the rule.

        default
        :default: AWS CloudFormation generates a unique physical ID.
        """
        return self._values.get('rule_name')

    @builtins.property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        """The target to register for the event.

        default
        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        return self._values.get('target')

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[str]]:
        """Only watch changes to these object paths.

        default
        :default: - Watch changes to all objects
        """
        return self._values.get('paths')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OnCloudTrailBucketEventOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-s3.RedirectProtocol")
class RedirectProtocol(enum.Enum):
    """All http request methods."""
    HTTP = "HTTP"
    HTTPS = "HTTPS"

@jsii.data_type(jsii_type="@aws-cdk/aws-s3.RedirectTarget", jsii_struct_bases=[], name_mapping={'host_name': 'hostName', 'protocol': 'protocol'})
class RedirectTarget():
    def __init__(self, *, host_name: str, protocol: typing.Optional["RedirectProtocol"]=None):
        """Specifies a redirect behavior of all requests to a website endpoint of a bucket.

        :param host_name: Name of the host where requests are redirected.
        :param protocol: Protocol to use when redirecting requests. Default: - The protocol used in the original request.
        """
        self._values = {
            'host_name': host_name,
        }
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def host_name(self) -> str:
        """Name of the host where requests are redirected."""
        return self._values.get('host_name')

    @builtins.property
    def protocol(self) -> typing.Optional["RedirectProtocol"]:
        """Protocol to use when redirecting requests.

        default
        :default: - The protocol used in the original request.
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RedirectTarget(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ReplaceKey(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.ReplaceKey"):
    @jsii.member(jsii_name="prefixWith")
    @builtins.classmethod
    def prefix_with(cls, key_replacement: str) -> "ReplaceKey":
        """The object key prefix to use in the redirect request.

        :param key_replacement: -
        """
        return jsii.sinvoke(cls, "prefixWith", [key_replacement])

    @jsii.member(jsii_name="with")
    @builtins.classmethod
    def with_(cls, key_replacement: str) -> "ReplaceKey":
        """The specific object key to use in the redirect request.

        :param key_replacement: -
        """
        return jsii.sinvoke(cls, "with", [key_replacement])

    @builtins.property
    @jsii.member(jsii_name="prefixWithKey")
    def prefix_with_key(self) -> typing.Optional[str]:
        return jsii.get(self, "prefixWithKey")

    @builtins.property
    @jsii.member(jsii_name="withKey")
    def with_key(self) -> typing.Optional[str]:
        return jsii.get(self, "withKey")


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.RoutingRule", jsii_struct_bases=[], name_mapping={'condition': 'condition', 'host_name': 'hostName', 'http_redirect_code': 'httpRedirectCode', 'protocol': 'protocol', 'replace_key': 'replaceKey'})
class RoutingRule():
    def __init__(self, *, condition: typing.Optional["RoutingRuleCondition"]=None, host_name: typing.Optional[str]=None, http_redirect_code: typing.Optional[str]=None, protocol: typing.Optional["RedirectProtocol"]=None, replace_key: typing.Optional["ReplaceKey"]=None):
        """Rule that define when a redirect is applied and the redirect behavior.

        :param condition: Specifies a condition that must be met for the specified redirect to apply. Default: - No condition
        :param host_name: The host name to use in the redirect request. Default: - The host name used in the original request.
        :param http_redirect_code: The HTTP redirect code to use on the response. Default: "301" - Moved Permanently
        :param protocol: Protocol to use when redirecting requests. Default: - The protocol used in the original request.
        :param replace_key: Specifies the object key prefix to use in the redirect request. Default: - The key will not be replaced

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html
        """
        if isinstance(condition, dict): condition = RoutingRuleCondition(**condition)
        self._values = {
        }
        if condition is not None: self._values["condition"] = condition
        if host_name is not None: self._values["host_name"] = host_name
        if http_redirect_code is not None: self._values["http_redirect_code"] = http_redirect_code
        if protocol is not None: self._values["protocol"] = protocol
        if replace_key is not None: self._values["replace_key"] = replace_key

    @builtins.property
    def condition(self) -> typing.Optional["RoutingRuleCondition"]:
        """Specifies a condition that must be met for the specified redirect to apply.

        default
        :default: - No condition
        """
        return self._values.get('condition')

    @builtins.property
    def host_name(self) -> typing.Optional[str]:
        """The host name to use in the redirect request.

        default
        :default: - The host name used in the original request.
        """
        return self._values.get('host_name')

    @builtins.property
    def http_redirect_code(self) -> typing.Optional[str]:
        """The HTTP redirect code to use on the response.

        default
        :default: "301" - Moved Permanently
        """
        return self._values.get('http_redirect_code')

    @builtins.property
    def protocol(self) -> typing.Optional["RedirectProtocol"]:
        """Protocol to use when redirecting requests.

        default
        :default: - The protocol used in the original request.
        """
        return self._values.get('protocol')

    @builtins.property
    def replace_key(self) -> typing.Optional["ReplaceKey"]:
        """Specifies the object key prefix to use in the redirect request.

        default
        :default: - The key will not be replaced
        """
        return self._values.get('replace_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RoutingRule(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.RoutingRuleCondition", jsii_struct_bases=[], name_mapping={'http_error_code_returned_equals': 'httpErrorCodeReturnedEquals', 'key_prefix_equals': 'keyPrefixEquals'})
class RoutingRuleCondition():
    def __init__(self, *, http_error_code_returned_equals: typing.Optional[str]=None, key_prefix_equals: typing.Optional[str]=None):
        """
        :param http_error_code_returned_equals: The HTTP error code when the redirect is applied. In the event of an error, if the error code equals this value, then the specified redirect is applied. If both condition properties are specified, both must be true for the redirect to be applied. Default: - The HTTP error code will not be verified
        :param key_prefix_equals: The object key name prefix when the redirect is applied. If both condition properties are specified, both must be true for the redirect to be applied. Default: - The object key name will not be verified
        """
        self._values = {
        }
        if http_error_code_returned_equals is not None: self._values["http_error_code_returned_equals"] = http_error_code_returned_equals
        if key_prefix_equals is not None: self._values["key_prefix_equals"] = key_prefix_equals

    @builtins.property
    def http_error_code_returned_equals(self) -> typing.Optional[str]:
        """The HTTP error code when the redirect is applied.

        In the event of an error, if the error code equals this value, then the specified redirect is applied.

        If both condition properties are specified, both must be true for the redirect to be applied.

        default
        :default: - The HTTP error code will not be verified
        """
        return self._values.get('http_error_code_returned_equals')

    @builtins.property
    def key_prefix_equals(self) -> typing.Optional[str]:
        """The object key name prefix when the redirect is applied.

        If both condition properties are specified, both must be true for the redirect to be applied.

        default
        :default: - The object key name will not be verified
        """
        return self._values.get('key_prefix_equals')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RoutingRuleCondition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class StorageClass(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3.StorageClass"):
    """Storage class to move an object to."""
    def __init__(self, value: str) -> None:
        """
        :param value: -
        """
        jsii.create(StorageClass, self, [value])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEEP_ARCHIVE")
    def DEEP_ARCHIVE(cls) -> "StorageClass":
        """Use for archiving data that rarely needs to be accessed.

        Data stored in the
        DEEP_ARCHIVE storage class has a minimum storage duration period of 180
        days and a default retrieval time of 12 hours. If you delete an object
        before the 180-day minimum, you are charged for 180 days. For pricing
        information, see Amazon S3 Pricing.
        """
        return jsii.sget(cls, "DEEP_ARCHIVE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="GLACIER")
    def GLACIER(cls) -> "StorageClass":
        """Storage class for long-term archival that can take between minutes and hours to access.

        Use for archives where portions of the data might need to be retrieved in
        minutes. Data stored in the GLACIER storage class has a minimum storage
        duration period of 90 days and can be accessed in as little as 1-5 minutes
        using expedited retrieval. If you delete an object before the 90-day
        minimum, you are charged for 90 days.
        """
        return jsii.sget(cls, "GLACIER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="INFREQUENT_ACCESS")
    def INFREQUENT_ACCESS(cls) -> "StorageClass":
        """Storage class for data that is accessed less frequently, but requires rapid access when needed.

        Has lower availability than Standard storage.
        """
        return jsii.sget(cls, "INFREQUENT_ACCESS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="INTELLIGENT_TIERING")
    def INTELLIGENT_TIERING(cls) -> "StorageClass":
        """The INTELLIGENT_TIERING storage class is designed to optimize storage costs by automatically moving data to the most cost-effective storage access tier, without performance impact or operational overhead.

        INTELLIGENT_TIERING delivers automatic cost savings by moving data on a
        granular object level between two access tiers, a frequent access tier and
        a lower-cost infrequent access tier, when access patterns change. The
        INTELLIGENT_TIERING storage class is ideal if you want to optimize storage
        costs automatically for long-lived data when access patterns are unknown or
        unpredictable.
        """
        return jsii.sget(cls, "INTELLIGENT_TIERING")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ONE_ZONE_INFREQUENT_ACCESS")
    def ONE_ZONE_INFREQUENT_ACCESS(cls) -> "StorageClass":
        """Infrequent Access that's only stored in one availability zone.

        Has lower availability than standard InfrequentAccess.
        """
        return jsii.sget(cls, "ONE_ZONE_INFREQUENT_ACCESS")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        return jsii.get(self, "value")


@jsii.data_type(jsii_type="@aws-cdk/aws-s3.Transition", jsii_struct_bases=[], name_mapping={'storage_class': 'storageClass', 'transition_after': 'transitionAfter', 'transition_date': 'transitionDate'})
class Transition():
    def __init__(self, *, storage_class: "StorageClass", transition_after: typing.Optional[aws_cdk.core.Duration]=None, transition_date: typing.Optional[datetime.datetime]=None):
        """Describes when an object transitions to a specified storage class.

        :param storage_class: The storage class to which you want the object to transition.
        :param transition_after: Indicates the number of days after creation when objects are transitioned to the specified storage class. Default: No transition count.
        :param transition_date: Indicates when objects are transitioned to the specified storage class. The date value must be in ISO 8601 format. The time is always midnight UTC. Default: No transition date.
        """
        self._values = {
            'storage_class': storage_class,
        }
        if transition_after is not None: self._values["transition_after"] = transition_after
        if transition_date is not None: self._values["transition_date"] = transition_date

    @builtins.property
    def storage_class(self) -> "StorageClass":
        """The storage class to which you want the object to transition."""
        return self._values.get('storage_class')

    @builtins.property
    def transition_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Indicates the number of days after creation when objects are transitioned to the specified storage class.

        default
        :default: No transition count.
        """
        return self._values.get('transition_after')

    @builtins.property
    def transition_date(self) -> typing.Optional[datetime.datetime]:
        """Indicates when objects are transitioned to the specified storage class.

        The date value must be in ISO 8601 format. The time is always midnight UTC.

        default
        :default: No transition date.
        """
        return self._values.get('transition_date')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Transition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["BlockPublicAccess", "BlockPublicAccessOptions", "Bucket", "BucketAccessControl", "BucketAttributes", "BucketEncryption", "BucketMetrics", "BucketNotificationDestinationConfig", "BucketNotificationDestinationType", "BucketPolicy", "BucketPolicyProps", "BucketProps", "CfnAccessPoint", "CfnAccessPointProps", "CfnBucket", "CfnBucketPolicy", "CfnBucketPolicyProps", "CfnBucketProps", "CorsRule", "EventType", "HttpMethods", "IBucket", "IBucketNotificationDestination", "LifecycleRule", "Location", "NoncurrentVersionTransition", "NotificationKeyFilter", "OnCloudTrailBucketEventOptions", "RedirectProtocol", "RedirectTarget", "ReplaceKey", "RoutingRule", "RoutingRuleCondition", "StorageClass", "Transition", "__jsii_assembly__"]

publication.publish()
