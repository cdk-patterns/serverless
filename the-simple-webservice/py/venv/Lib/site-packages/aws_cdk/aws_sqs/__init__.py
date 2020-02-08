"""
## Amazon Simple Queue Service Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Amazon Simple Queue Service (SQS) is a fully managed message queuing service that
enables you to decouple and scale microservices, distributed systems, and serverless
applications. SQS eliminates the complexity and overhead associated with managing and
operating message oriented middleware, and empowers developers to focus on differentiating work.
Using SQS, you can send, store, and receive messages between software components at any volume,
without losing messages or requiring other services to be available.

### Installation

Import to your project:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sqs as sqs
```

### Basic usage

Here's how to add a basic queue to your application:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sqs.Queue(self, "Queue")
```

### Encryption

If you want to encrypt the queue contents, set the `encryption` property. You can have
the messages encrypted with a key that SQS manages for you, or a key that you
can manage yourself.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Use managed key
sqs.Queue(self, "Queue",
    encryption=QueueEncryption.KMS_MANAGED
)

# Use custom key
my_key = kms.Key(self, "Key")

sqs.Queue(self, "Queue",
    encryption=QueueEncryption.KMS,
    encryption_master_key=my_key
)
```

### First-In-First-Out (FIFO) queues

FIFO queues give guarantees on the order in which messages are dequeued, and have additional
features in order to help guarantee exactly-once processing. For more information, see
the SQS manual. Note that FIFO queues are not available in all AWS regions.

A queue can be made a FIFO queue by either setting `fifo: true`, giving it a name which ends
in `".fifo"`, or enabling content-based deduplication (which requires FIFO queues).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sqs", "1.23.0", __name__, "aws-sqs@1.23.0.jsii.tgz")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnQueue(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.CfnQueue"):
    """A CloudFormation ``AWS::SQS::Queue``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html
    cloudformationResource:
    :cloudformationResource:: AWS::SQS::Queue
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, content_based_deduplication: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, delay_seconds: typing.Optional[jsii.Number]=None, fifo_queue: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number]=None, kms_master_key_id: typing.Optional[str]=None, maximum_message_size: typing.Optional[jsii.Number]=None, message_retention_period: typing.Optional[jsii.Number]=None, queue_name: typing.Optional[str]=None, receive_message_wait_time_seconds: typing.Optional[jsii.Number]=None, redrive_policy: typing.Any=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, visibility_timeout: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::SQS::Queue``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content_based_deduplication: ``AWS::SQS::Queue.ContentBasedDeduplication``.
        :param delay_seconds: ``AWS::SQS::Queue.DelaySeconds``.
        :param fifo_queue: ``AWS::SQS::Queue.FifoQueue``.
        :param kms_data_key_reuse_period_seconds: ``AWS::SQS::Queue.KmsDataKeyReusePeriodSeconds``.
        :param kms_master_key_id: ``AWS::SQS::Queue.KmsMasterKeyId``.
        :param maximum_message_size: ``AWS::SQS::Queue.MaximumMessageSize``.
        :param message_retention_period: ``AWS::SQS::Queue.MessageRetentionPeriod``.
        :param queue_name: ``AWS::SQS::Queue.QueueName``.
        :param receive_message_wait_time_seconds: ``AWS::SQS::Queue.ReceiveMessageWaitTimeSeconds``.
        :param redrive_policy: ``AWS::SQS::Queue.RedrivePolicy``.
        :param tags: ``AWS::SQS::Queue.Tags``.
        :param visibility_timeout: ``AWS::SQS::Queue.VisibilityTimeout``.
        """
        props = CfnQueueProps(content_based_deduplication=content_based_deduplication, delay_seconds=delay_seconds, fifo_queue=fifo_queue, kms_data_key_reuse_period_seconds=kms_data_key_reuse_period_seconds, kms_master_key_id=kms_master_key_id, maximum_message_size=maximum_message_size, message_retention_period=message_retention_period, queue_name=queue_name, receive_message_wait_time_seconds=receive_message_wait_time_seconds, redrive_policy=redrive_policy, tags=tags, visibility_timeout=visibility_timeout)

        jsii.create(CfnQueue, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrQueueName")
    def attr_queue_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: QueueName
        """
        return jsii.get(self, "attrQueueName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SQS::Queue.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#cfn-sqs-queue-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="redrivePolicy")
    def redrive_policy(self) -> typing.Any:
        """``AWS::SQS::Queue.RedrivePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-redrive
        """
        return jsii.get(self, "redrivePolicy")

    @redrive_policy.setter
    def redrive_policy(self, value: typing.Any):
        jsii.set(self, "redrivePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="contentBasedDeduplication")
    def content_based_deduplication(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::SQS::Queue.ContentBasedDeduplication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-contentbaseddeduplication
        """
        return jsii.get(self, "contentBasedDeduplication")

    @content_based_deduplication.setter
    def content_based_deduplication(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "contentBasedDeduplication", value)

    @builtins.property
    @jsii.member(jsii_name="delaySeconds")
    def delay_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.DelaySeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-delayseconds
        """
        return jsii.get(self, "delaySeconds")

    @delay_seconds.setter
    def delay_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "delaySeconds", value)

    @builtins.property
    @jsii.member(jsii_name="fifoQueue")
    def fifo_queue(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::SQS::Queue.FifoQueue``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-fifoqueue
        """
        return jsii.get(self, "fifoQueue")

    @fifo_queue.setter
    def fifo_queue(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "fifoQueue", value)

    @builtins.property
    @jsii.member(jsii_name="kmsDataKeyReusePeriodSeconds")
    def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.KmsDataKeyReusePeriodSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-kmsdatakeyreuseperiodseconds
        """
        return jsii.get(self, "kmsDataKeyReusePeriodSeconds")

    @kms_data_key_reuse_period_seconds.setter
    def kms_data_key_reuse_period_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "kmsDataKeyReusePeriodSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="kmsMasterKeyId")
    def kms_master_key_id(self) -> typing.Optional[str]:
        """``AWS::SQS::Queue.KmsMasterKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-kmsmasterkeyid
        """
        return jsii.get(self, "kmsMasterKeyId")

    @kms_master_key_id.setter
    def kms_master_key_id(self, value: typing.Optional[str]):
        jsii.set(self, "kmsMasterKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="maximumMessageSize")
    def maximum_message_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.MaximumMessageSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-maxmesgsize
        """
        return jsii.get(self, "maximumMessageSize")

    @maximum_message_size.setter
    def maximum_message_size(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "maximumMessageSize", value)

    @builtins.property
    @jsii.member(jsii_name="messageRetentionPeriod")
    def message_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.MessageRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-msgretentionperiod
        """
        return jsii.get(self, "messageRetentionPeriod")

    @message_retention_period.setter
    def message_retention_period(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "messageRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> typing.Optional[str]:
        """``AWS::SQS::Queue.QueueName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-name
        """
        return jsii.get(self, "queueName")

    @queue_name.setter
    def queue_name(self, value: typing.Optional[str]):
        jsii.set(self, "queueName", value)

    @builtins.property
    @jsii.member(jsii_name="receiveMessageWaitTimeSeconds")
    def receive_message_wait_time_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.ReceiveMessageWaitTimeSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-receivemsgwaittime
        """
        return jsii.get(self, "receiveMessageWaitTimeSeconds")

    @receive_message_wait_time_seconds.setter
    def receive_message_wait_time_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "receiveMessageWaitTimeSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="visibilityTimeout")
    def visibility_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.VisibilityTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-visiblitytimeout
        """
        return jsii.get(self, "visibilityTimeout")

    @visibility_timeout.setter
    def visibility_timeout(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "visibilityTimeout", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnQueuePolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.CfnQueuePolicy"):
    """A CloudFormation ``AWS::SQS::QueuePolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::SQS::QueuePolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_document: typing.Any, queues: typing.List[str]) -> None:
        """Create a new ``AWS::SQS::QueuePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: ``AWS::SQS::QueuePolicy.PolicyDocument``.
        :param queues: ``AWS::SQS::QueuePolicy.Queues``.
        """
        props = CfnQueuePolicyProps(policy_document=policy_document, queues=queues)

        jsii.create(CfnQueuePolicy, self, [scope, id, props])

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
        """``AWS::SQS::QueuePolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-policydoc
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter
    def policy_document(self, value: typing.Any):
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="queues")
    def queues(self) -> typing.List[str]:
        """``AWS::SQS::QueuePolicy.Queues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-queues
        """
        return jsii.get(self, "queues")

    @queues.setter
    def queues(self, value: typing.List[str]):
        jsii.set(self, "queues", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.CfnQueuePolicyProps", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'queues': 'queues'})
class CfnQueuePolicyProps():
    def __init__(self, *, policy_document: typing.Any, queues: typing.List[str]):
        """Properties for defining a ``AWS::SQS::QueuePolicy``.

        :param policy_document: ``AWS::SQS::QueuePolicy.PolicyDocument``.
        :param queues: ``AWS::SQS::QueuePolicy.Queues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html
        """
        self._values = {
            'policy_document': policy_document,
            'queues': queues,
        }

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::SQS::QueuePolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-policydoc
        """
        return self._values.get('policy_document')

    @builtins.property
    def queues(self) -> typing.List[str]:
        """``AWS::SQS::QueuePolicy.Queues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-policy.html#cfn-sqs-queuepolicy-queues
        """
        return self._values.get('queues')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnQueuePolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.CfnQueueProps", jsii_struct_bases=[], name_mapping={'content_based_deduplication': 'contentBasedDeduplication', 'delay_seconds': 'delaySeconds', 'fifo_queue': 'fifoQueue', 'kms_data_key_reuse_period_seconds': 'kmsDataKeyReusePeriodSeconds', 'kms_master_key_id': 'kmsMasterKeyId', 'maximum_message_size': 'maximumMessageSize', 'message_retention_period': 'messageRetentionPeriod', 'queue_name': 'queueName', 'receive_message_wait_time_seconds': 'receiveMessageWaitTimeSeconds', 'redrive_policy': 'redrivePolicy', 'tags': 'tags', 'visibility_timeout': 'visibilityTimeout'})
class CfnQueueProps():
    def __init__(self, *, content_based_deduplication: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, delay_seconds: typing.Optional[jsii.Number]=None, fifo_queue: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number]=None, kms_master_key_id: typing.Optional[str]=None, maximum_message_size: typing.Optional[jsii.Number]=None, message_retention_period: typing.Optional[jsii.Number]=None, queue_name: typing.Optional[str]=None, receive_message_wait_time_seconds: typing.Optional[jsii.Number]=None, redrive_policy: typing.Any=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, visibility_timeout: typing.Optional[jsii.Number]=None):
        """Properties for defining a ``AWS::SQS::Queue``.

        :param content_based_deduplication: ``AWS::SQS::Queue.ContentBasedDeduplication``.
        :param delay_seconds: ``AWS::SQS::Queue.DelaySeconds``.
        :param fifo_queue: ``AWS::SQS::Queue.FifoQueue``.
        :param kms_data_key_reuse_period_seconds: ``AWS::SQS::Queue.KmsDataKeyReusePeriodSeconds``.
        :param kms_master_key_id: ``AWS::SQS::Queue.KmsMasterKeyId``.
        :param maximum_message_size: ``AWS::SQS::Queue.MaximumMessageSize``.
        :param message_retention_period: ``AWS::SQS::Queue.MessageRetentionPeriod``.
        :param queue_name: ``AWS::SQS::Queue.QueueName``.
        :param receive_message_wait_time_seconds: ``AWS::SQS::Queue.ReceiveMessageWaitTimeSeconds``.
        :param redrive_policy: ``AWS::SQS::Queue.RedrivePolicy``.
        :param tags: ``AWS::SQS::Queue.Tags``.
        :param visibility_timeout: ``AWS::SQS::Queue.VisibilityTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html
        """
        self._values = {
        }
        if content_based_deduplication is not None: self._values["content_based_deduplication"] = content_based_deduplication
        if delay_seconds is not None: self._values["delay_seconds"] = delay_seconds
        if fifo_queue is not None: self._values["fifo_queue"] = fifo_queue
        if kms_data_key_reuse_period_seconds is not None: self._values["kms_data_key_reuse_period_seconds"] = kms_data_key_reuse_period_seconds
        if kms_master_key_id is not None: self._values["kms_master_key_id"] = kms_master_key_id
        if maximum_message_size is not None: self._values["maximum_message_size"] = maximum_message_size
        if message_retention_period is not None: self._values["message_retention_period"] = message_retention_period
        if queue_name is not None: self._values["queue_name"] = queue_name
        if receive_message_wait_time_seconds is not None: self._values["receive_message_wait_time_seconds"] = receive_message_wait_time_seconds
        if redrive_policy is not None: self._values["redrive_policy"] = redrive_policy
        if tags is not None: self._values["tags"] = tags
        if visibility_timeout is not None: self._values["visibility_timeout"] = visibility_timeout

    @builtins.property
    def content_based_deduplication(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::SQS::Queue.ContentBasedDeduplication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-contentbaseddeduplication
        """
        return self._values.get('content_based_deduplication')

    @builtins.property
    def delay_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.DelaySeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-delayseconds
        """
        return self._values.get('delay_seconds')

    @builtins.property
    def fifo_queue(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::SQS::Queue.FifoQueue``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-fifoqueue
        """
        return self._values.get('fifo_queue')

    @builtins.property
    def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.KmsDataKeyReusePeriodSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-kmsdatakeyreuseperiodseconds
        """
        return self._values.get('kms_data_key_reuse_period_seconds')

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[str]:
        """``AWS::SQS::Queue.KmsMasterKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-kmsmasterkeyid
        """
        return self._values.get('kms_master_key_id')

    @builtins.property
    def maximum_message_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.MaximumMessageSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-maxmesgsize
        """
        return self._values.get('maximum_message_size')

    @builtins.property
    def message_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.MessageRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-msgretentionperiod
        """
        return self._values.get('message_retention_period')

    @builtins.property
    def queue_name(self) -> typing.Optional[str]:
        """``AWS::SQS::Queue.QueueName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-name
        """
        return self._values.get('queue_name')

    @builtins.property
    def receive_message_wait_time_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.ReceiveMessageWaitTimeSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-receivemsgwaittime
        """
        return self._values.get('receive_message_wait_time_seconds')

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        """``AWS::SQS::Queue.RedrivePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-redrive
        """
        return self._values.get('redrive_policy')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SQS::Queue.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#cfn-sqs-queue-tags
        """
        return self._values.get('tags')

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::SQS::Queue.VisibilityTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html#aws-sqs-queue-visiblitytimeout
        """
        return self._values.get('visibility_timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.DeadLetterQueue", jsii_struct_bases=[], name_mapping={'max_receive_count': 'maxReceiveCount', 'queue': 'queue'})
class DeadLetterQueue():
    def __init__(self, *, max_receive_count: jsii.Number, queue: "IQueue"):
        """Dead letter queue settings.

        :param max_receive_count: The number of times a message can be unsuccesfully dequeued before being moved to the dead-letter queue.
        :param queue: The dead-letter queue to which Amazon SQS moves messages after the value of maxReceiveCount is exceeded.
        """
        self._values = {
            'max_receive_count': max_receive_count,
            'queue': queue,
        }

    @builtins.property
    def max_receive_count(self) -> jsii.Number:
        """The number of times a message can be unsuccesfully dequeued before being moved to the dead-letter queue."""
        return self._values.get('max_receive_count')

    @builtins.property
    def queue(self) -> "IQueue":
        """The dead-letter queue to which Amazon SQS moves messages after the value of maxReceiveCount is exceeded."""
        return self._values.get('queue')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DeadLetterQueue(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-sqs.IQueue")
class IQueue(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IQueueProxy

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> bool:
        """Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        """The ARN of this queue.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        """The name of this queue.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        """The URL of this queue.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """If this queue is server-side encrypted, this is the KMS encryption key."""
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this queue.

        If this queue was created in this stack (``new Queue``), a queue policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the queue is improted (``Queue.import``), then this is a no-op.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *queue_actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the actions defined in queueActions to the identity Principal given on this SQS queue resource.

        :param grantee: Principal to grant right to.
        :param queue_actions: The actions to grant.
        """
        ...

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant permissions to consume messages from a queue.

        This will grant the following permissions:

        - sqs:ChangeMessageVisibility
        - sqs:DeleteMessage
        - sqs:ReceiveMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant consume rights to.
        """
        ...

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant an IAM principal permissions to purge all messages from the queue.

        This will grant the following permissions:

        - sqs:PurgeQueue
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.
        """
        ...

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to send messages to a queue to the given identity.

        This will grant the following permissions:

        - sqs:SendMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Queue.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The approximate age of the oldest non-deleted message in the queue.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages in the queue that are delayed and not available for reading immediately.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that are in flight.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages available for retrieval from the queue.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of ReceiveMessage API calls that did not return a message.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages deleted from the queue.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages returned by calls to the ReceiveMessage action.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages added to a queue.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The size of messages added to a queue.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        ...


class _IQueueProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-sqs.IQueue"
    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> bool:
        """Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.
        """
        return jsii.get(self, "fifo")

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        """The ARN of this queue.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "queueArn")

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        """The name of this queue.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "queueName")

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        """The URL of this queue.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "queueUrl")

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """If this queue is server-side encrypted, this is the KMS encryption key."""
        return jsii.get(self, "encryptionMasterKey")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this queue.

        If this queue was created in this stack (``new Queue``), a queue policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the queue is improted (``Queue.import``), then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *queue_actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the actions defined in queueActions to the identity Principal given on this SQS queue resource.

        :param grantee: Principal to grant right to.
        :param queue_actions: The actions to grant.
        """
        return jsii.invoke(self, "grant", [grantee, *queue_actions])

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant permissions to consume messages from a queue.

        This will grant the following permissions:

        - sqs:ChangeMessageVisibility
        - sqs:DeleteMessage
        - sqs:ReceiveMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant consume rights to.
        """
        return jsii.invoke(self, "grantConsumeMessages", [grantee])

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant an IAM principal permissions to purge all messages from the queue.

        This will grant the following permissions:

        - sqs:PurgeQueue
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.
        """
        return jsii.invoke(self, "grantPurge", [grantee])

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to send messages to a queue to the given identity.

        This will grant the following permissions:

        - sqs:SendMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.
        """
        return jsii.invoke(self, "grantSendMessages", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Queue.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The approximate age of the oldest non-deleted message in the queue.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateAgeOfOldestMessage", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages in the queue that are delayed and not available for reading immediately.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateNumberOfMessagesDelayed", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that are in flight.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateNumberOfMessagesNotVisible", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages available for retrieval from the queue.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateNumberOfMessagesVisible", [props])

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of ReceiveMessage API calls that did not return a message.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfEmptyReceives", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages deleted from the queue.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfMessagesDeleted", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages returned by calls to the ReceiveMessage action.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfMessagesReceived", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages added to a queue.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfMessagesSent", [props])

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The size of messages added to a queue.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSentMessageSize", [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.QueueAttributes", jsii_struct_bases=[], name_mapping={'queue_arn': 'queueArn', 'key_arn': 'keyArn', 'queue_name': 'queueName', 'queue_url': 'queueUrl'})
class QueueAttributes():
    def __init__(self, *, queue_arn: str, key_arn: typing.Optional[str]=None, queue_name: typing.Optional[str]=None, queue_url: typing.Optional[str]=None):
        """Reference to a queue.

        :param queue_arn: The ARN of the queue.
        :param key_arn: KMS encryption key, if this queue is server-side encrypted by a KMS key.
        :param queue_name: The name of the queue. Default: if queue name is not specified, the name will be derived from the queue ARN
        :param queue_url: The URL of the queue.
        """
        self._values = {
            'queue_arn': queue_arn,
        }
        if key_arn is not None: self._values["key_arn"] = key_arn
        if queue_name is not None: self._values["queue_name"] = queue_name
        if queue_url is not None: self._values["queue_url"] = queue_url

    @builtins.property
    def queue_arn(self) -> str:
        """The ARN of the queue."""
        return self._values.get('queue_arn')

    @builtins.property
    def key_arn(self) -> typing.Optional[str]:
        """KMS encryption key, if this queue is server-side encrypted by a KMS key."""
        return self._values.get('key_arn')

    @builtins.property
    def queue_name(self) -> typing.Optional[str]:
        """The name of the queue.

        default
        :default: if queue name is not specified, the name will be derived from the queue ARN
        """
        return self._values.get('queue_name')

    @builtins.property
    def queue_url(self) -> typing.Optional[str]:
        """The URL of the queue."""
        return self._values.get('queue_url')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IQueue)
class QueueBase(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-sqs.QueueBase"):
    """Reference to a new or existing Amazon SQS queue."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _QueueBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = aws_cdk.core.ResourceProps(physical_name=physical_name)

        jsii.create(QueueBase, self, [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this queue.

        If this queue was created in this stack (``new Queue``), a queue policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the queue is improted (``Queue.import``), then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the actions defined in queueActions to the identity Principal given on this SQS queue resource.

        :param grantee: Principal to grant right to.
        :param actions: The actions to grant.
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant permissions to consume messages from a queue.

        This will grant the following permissions:

        - sqs:ChangeMessageVisibility
        - sqs:DeleteMessage
        - sqs:ReceiveMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant consume rights to.
        """
        return jsii.invoke(self, "grantConsumeMessages", [grantee])

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant an IAM principal permissions to purge all messages from the queue.

        This will grant the following permissions:

        - sqs:PurgeQueue
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.
        """
        return jsii.invoke(self, "grantPurge", [grantee])

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant access to send messages to a queue to the given identity.

        This will grant the following permissions:

        - sqs:SendMessage
        - sqs:GetQueueAttributes
        - sqs:GetQueueUrl

        :param grantee: Principal to grant send rights to.
        """
        return jsii.invoke(self, "grantSendMessages", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Queue.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The approximate age of the oldest non-deleted message in the queue.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateAgeOfOldestMessage", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages in the queue that are delayed and not available for reading immediately.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateNumberOfMessagesDelayed", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that are in flight.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateNumberOfMessagesNotVisible", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages available for retrieval from the queue.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricApproximateNumberOfMessagesVisible", [props])

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of ReceiveMessage API calls that did not return a message.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfEmptyReceives", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages deleted from the queue.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfMessagesDeleted", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages returned by calls to the ReceiveMessage action.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfMessagesReceived", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages added to a queue.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNumberOfMessagesSent", [props])

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The size of messages added to a queue.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSentMessageSize", [props])

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="fifo")
    @abc.abstractmethod
    def fifo(self) -> bool:
        """Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    @abc.abstractmethod
    def queue_arn(self) -> str:
        """The ARN of this queue."""
        ...

    @builtins.property
    @jsii.member(jsii_name="queueName")
    @abc.abstractmethod
    def queue_name(self) -> str:
        """The name of this queue."""
        ...

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    @abc.abstractmethod
    def queue_url(self) -> str:
        """The URL of this queue."""
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    @abc.abstractmethod
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """If this queue is server-side encrypted, this is the KMS encryption key."""
        ...


class _QueueBaseProxy(QueueBase, jsii.proxy_for(aws_cdk.core.Resource)):
    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> bool:
        """Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.
        """
        return jsii.get(self, "fifo")

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        """The ARN of this queue."""
        return jsii.get(self, "queueArn")

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        """The name of this queue."""
        return jsii.get(self, "queueName")

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        """The URL of this queue."""
        return jsii.get(self, "queueUrl")

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """If this queue is server-side encrypted, this is the KMS encryption key."""
        return jsii.get(self, "encryptionMasterKey")


class Queue(QueueBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.Queue"):
    """A new Amazon SQS queue."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, content_based_deduplication: typing.Optional[bool]=None, data_key_reuse: typing.Optional[aws_cdk.core.Duration]=None, dead_letter_queue: typing.Optional["DeadLetterQueue"]=None, delivery_delay: typing.Optional[aws_cdk.core.Duration]=None, encryption: typing.Optional["QueueEncryption"]=None, encryption_master_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, fifo: typing.Optional[bool]=None, max_message_size_bytes: typing.Optional[jsii.Number]=None, queue_name: typing.Optional[str]=None, receive_message_wait_time: typing.Optional[aws_cdk.core.Duration]=None, retention_period: typing.Optional[aws_cdk.core.Duration]=None, visibility_timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param content_based_deduplication: Specifies whether to enable content-based deduplication. During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with identical content (excluding attributes) as duplicates and delivers only one copy of the message. If you don't enable content-based deduplication and you want to deduplicate messages, provide an explicit deduplication ID in your SendMessage() call. (Only applies to FIFO queues.) Default: false
        :param data_key_reuse: The length of time that Amazon SQS reuses a data key before calling KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). Default: Duration.minutes(5)
        :param dead_letter_queue: Send messages to this queue if they were unsuccessfully dequeued a number of times. Default: no dead-letter queue
        :param delivery_delay: The time in seconds that the delivery of all messages in the queue is delayed. You can specify an integer value of 0 to 900 (15 minutes). The default value is 0. Default: 0
        :param encryption: Whether the contents of the queue are encrypted, and by what type of key. Be aware that encryption is not available in all regions, please see the docs for current availability details. Default: Unencrypted
        :param encryption_master_key: External KMS master key to use for queue encryption. Individual messages will be encrypted using data keys. The data keys in turn will be encrypted using this key, and reused for a maximum of ``dataKeyReuseSecs`` seconds. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "KmsManaged". Default: If encryption is set to KMS and not specified, a key will be created.
        :param fifo: Whether this a first-in-first-out (FIFO) queue. Default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.
        :param max_message_size_bytes: The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes (256 KiB). The default value is 262144 (256 KiB). Default: 256KiB
        :param queue_name: A name for the queue. If specified and this is a FIFO queue, must end in the string '.fifo'. Default: CloudFormation-generated name
        :param receive_message_wait_time: Default wait time for ReceiveMessage calls. Does not wait if set to 0, otherwise waits this amount of seconds by default for messages to arrive. For more information, see Amazon SQS Long Poll. Default: 0
        :param retention_period: The number of seconds that Amazon SQS retains a message. You can specify an integer value from 60 seconds (1 minute) to 1209600 seconds (14 days). The default value is 345600 seconds (4 days). Default: Duration.days(4)
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be from 0 to 43200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. Default: Duration.seconds(30)
        """
        props = QueueProps(content_based_deduplication=content_based_deduplication, data_key_reuse=data_key_reuse, dead_letter_queue=dead_letter_queue, delivery_delay=delivery_delay, encryption=encryption, encryption_master_key=encryption_master_key, fifo=fifo, max_message_size_bytes=max_message_size_bytes, queue_name=queue_name, receive_message_wait_time=receive_message_wait_time, retention_period=retention_period, visibility_timeout=visibility_timeout)

        jsii.create(Queue, self, [scope, id, props])

    @jsii.member(jsii_name="fromQueueArn")
    @builtins.classmethod
    def from_queue_arn(cls, scope: aws_cdk.core.Construct, id: str, queue_arn: str) -> "IQueue":
        """
        :param scope: -
        :param id: -
        :param queue_arn: -
        """
        return jsii.sinvoke(cls, "fromQueueArn", [scope, id, queue_arn])

    @jsii.member(jsii_name="fromQueueAttributes")
    @builtins.classmethod
    def from_queue_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, queue_arn: str, key_arn: typing.Optional[str]=None, queue_name: typing.Optional[str]=None, queue_url: typing.Optional[str]=None) -> "IQueue":
        """Import an existing queue.

        :param scope: -
        :param id: -
        :param queue_arn: The ARN of the queue.
        :param key_arn: KMS encryption key, if this queue is server-side encrypted by a KMS key.
        :param queue_name: The name of the queue. Default: if queue name is not specified, the name will be derived from the queue ARN
        :param queue_url: The URL of the queue.
        """
        attrs = QueueAttributes(queue_arn=queue_arn, key_arn=key_arn, queue_name=queue_name, queue_url=queue_url)

        return jsii.sinvoke(cls, "fromQueueAttributes", [scope, id, attrs])

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> bool:
        """Whether this queue is an Amazon SQS FIFO queue.

        If false, this is a standard queue.
        """
        return jsii.get(self, "fifo")

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        """The ARN of this queue."""
        return jsii.get(self, "queueArn")

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        """The name of this queue."""
        return jsii.get(self, "queueName")

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        """The URL of this queue."""
        return jsii.get(self, "queueUrl")

    @builtins.property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """If this queue is encrypted, this is the KMS key."""
        return jsii.get(self, "encryptionMasterKey")


@jsii.enum(jsii_type="@aws-cdk/aws-sqs.QueueEncryption")
class QueueEncryption(enum.Enum):
    """What kind of encryption to apply to this queue."""
    UNENCRYPTED = "UNENCRYPTED"
    """Messages in the queue are not encrypted."""
    KMS_MANAGED = "KMS_MANAGED"
    """Server-side KMS encryption with a master key managed by SQS."""
    KMS = "KMS"
    """Server-side encryption with a KMS key managed by the user.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.
    """

class QueuePolicy(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.QueuePolicy"):
    """Applies a policy to SQS queues."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, queues: typing.List["IQueue"]) -> None:
        """
        :param scope: -
        :param id: -
        :param queues: The set of queues this policy applies to.
        """
        props = QueuePolicyProps(queues=queues)

        jsii.create(QueuePolicy, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        """The IAM policy document for this policy."""
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.QueuePolicyProps", jsii_struct_bases=[], name_mapping={'queues': 'queues'})
class QueuePolicyProps():
    def __init__(self, *, queues: typing.List["IQueue"]):
        """
        :param queues: The set of queues this policy applies to.
        """
        self._values = {
            'queues': queues,
        }

    @builtins.property
    def queues(self) -> typing.List["IQueue"]:
        """The set of queues this policy applies to."""
        return self._values.get('queues')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueuePolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.QueueProps", jsii_struct_bases=[], name_mapping={'content_based_deduplication': 'contentBasedDeduplication', 'data_key_reuse': 'dataKeyReuse', 'dead_letter_queue': 'deadLetterQueue', 'delivery_delay': 'deliveryDelay', 'encryption': 'encryption', 'encryption_master_key': 'encryptionMasterKey', 'fifo': 'fifo', 'max_message_size_bytes': 'maxMessageSizeBytes', 'queue_name': 'queueName', 'receive_message_wait_time': 'receiveMessageWaitTime', 'retention_period': 'retentionPeriod', 'visibility_timeout': 'visibilityTimeout'})
class QueueProps():
    def __init__(self, *, content_based_deduplication: typing.Optional[bool]=None, data_key_reuse: typing.Optional[aws_cdk.core.Duration]=None, dead_letter_queue: typing.Optional["DeadLetterQueue"]=None, delivery_delay: typing.Optional[aws_cdk.core.Duration]=None, encryption: typing.Optional["QueueEncryption"]=None, encryption_master_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, fifo: typing.Optional[bool]=None, max_message_size_bytes: typing.Optional[jsii.Number]=None, queue_name: typing.Optional[str]=None, receive_message_wait_time: typing.Optional[aws_cdk.core.Duration]=None, retention_period: typing.Optional[aws_cdk.core.Duration]=None, visibility_timeout: typing.Optional[aws_cdk.core.Duration]=None):
        """Properties for creating a new Queue.

        :param content_based_deduplication: Specifies whether to enable content-based deduplication. During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with identical content (excluding attributes) as duplicates and delivers only one copy of the message. If you don't enable content-based deduplication and you want to deduplicate messages, provide an explicit deduplication ID in your SendMessage() call. (Only applies to FIFO queues.) Default: false
        :param data_key_reuse: The length of time that Amazon SQS reuses a data key before calling KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). Default: Duration.minutes(5)
        :param dead_letter_queue: Send messages to this queue if they were unsuccessfully dequeued a number of times. Default: no dead-letter queue
        :param delivery_delay: The time in seconds that the delivery of all messages in the queue is delayed. You can specify an integer value of 0 to 900 (15 minutes). The default value is 0. Default: 0
        :param encryption: Whether the contents of the queue are encrypted, and by what type of key. Be aware that encryption is not available in all regions, please see the docs for current availability details. Default: Unencrypted
        :param encryption_master_key: External KMS master key to use for queue encryption. Individual messages will be encrypted using data keys. The data keys in turn will be encrypted using this key, and reused for a maximum of ``dataKeyReuseSecs`` seconds. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "KmsManaged". Default: If encryption is set to KMS and not specified, a key will be created.
        :param fifo: Whether this a first-in-first-out (FIFO) queue. Default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.
        :param max_message_size_bytes: The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes (256 KiB). The default value is 262144 (256 KiB). Default: 256KiB
        :param queue_name: A name for the queue. If specified and this is a FIFO queue, must end in the string '.fifo'. Default: CloudFormation-generated name
        :param receive_message_wait_time: Default wait time for ReceiveMessage calls. Does not wait if set to 0, otherwise waits this amount of seconds by default for messages to arrive. For more information, see Amazon SQS Long Poll. Default: 0
        :param retention_period: The number of seconds that Amazon SQS retains a message. You can specify an integer value from 60 seconds (1 minute) to 1209600 seconds (14 days). The default value is 345600 seconds (4 days). Default: Duration.days(4)
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be from 0 to 43200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. Default: Duration.seconds(30)
        """
        if isinstance(dead_letter_queue, dict): dead_letter_queue = DeadLetterQueue(**dead_letter_queue)
        self._values = {
        }
        if content_based_deduplication is not None: self._values["content_based_deduplication"] = content_based_deduplication
        if data_key_reuse is not None: self._values["data_key_reuse"] = data_key_reuse
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if delivery_delay is not None: self._values["delivery_delay"] = delivery_delay
        if encryption is not None: self._values["encryption"] = encryption
        if encryption_master_key is not None: self._values["encryption_master_key"] = encryption_master_key
        if fifo is not None: self._values["fifo"] = fifo
        if max_message_size_bytes is not None: self._values["max_message_size_bytes"] = max_message_size_bytes
        if queue_name is not None: self._values["queue_name"] = queue_name
        if receive_message_wait_time is not None: self._values["receive_message_wait_time"] = receive_message_wait_time
        if retention_period is not None: self._values["retention_period"] = retention_period
        if visibility_timeout is not None: self._values["visibility_timeout"] = visibility_timeout

    @builtins.property
    def content_based_deduplication(self) -> typing.Optional[bool]:
        """Specifies whether to enable content-based deduplication.

        During the deduplication interval (5 minutes), Amazon SQS treats
        messages that are sent with identical content (excluding attributes) as
        duplicates and delivers only one copy of the message.

        If you don't enable content-based deduplication and you want to deduplicate
        messages, provide an explicit deduplication ID in your SendMessage() call.

        (Only applies to FIFO queues.)

        default
        :default: false
        """
        return self._values.get('content_based_deduplication')

    @builtins.property
    def data_key_reuse(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time that Amazon SQS reuses a data key before calling KMS again.

        The value must be an integer between 60 (1 minute) and 86,400 (24
        hours). The default is 300 (5 minutes).

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('data_key_reuse')

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional["DeadLetterQueue"]:
        """Send messages to this queue if they were unsuccessfully dequeued a number of times.

        default
        :default: no dead-letter queue
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def delivery_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time in seconds that the delivery of all messages in the queue is delayed.

        You can specify an integer value of 0 to 900 (15 minutes). The default
        value is 0.

        default
        :default: 0
        """
        return self._values.get('delivery_delay')

    @builtins.property
    def encryption(self) -> typing.Optional["QueueEncryption"]:
        """Whether the contents of the queue are encrypted, and by what type of key.

        Be aware that encryption is not available in all regions, please see the docs
        for current availability details.

        default
        :default: Unencrypted
        """
        return self._values.get('encryption')

    @builtins.property
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """External KMS master key to use for queue encryption.

        Individual messages will be encrypted using data keys. The data keys in
        turn will be encrypted using this key, and reused for a maximum of
        ``dataKeyReuseSecs`` seconds.

        The 'encryption' property must be either not specified or set to "Kms".
        An error will be emitted if encryption is set to "Unencrypted" or
        "KmsManaged".

        default
        :default: If encryption is set to KMS and not specified, a key will be created.
        """
        return self._values.get('encryption_master_key')

    @builtins.property
    def fifo(self) -> typing.Optional[bool]:
        """Whether this a first-in-first-out (FIFO) queue.

        default
        :default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.
        """
        return self._values.get('fifo')

    @builtins.property
    def max_message_size_bytes(self) -> typing.Optional[jsii.Number]:
        """The limit of how many bytes that a message can contain before Amazon SQS rejects it.

        You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes
        (256 KiB). The default value is 262144 (256 KiB).

        default
        :default: 256KiB
        """
        return self._values.get('max_message_size_bytes')

    @builtins.property
    def queue_name(self) -> typing.Optional[str]:
        """A name for the queue.

        If specified and this is a FIFO queue, must end in the string '.fifo'.

        default
        :default: CloudFormation-generated name
        """
        return self._values.get('queue_name')

    @builtins.property
    def receive_message_wait_time(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Default wait time for ReceiveMessage calls.

        Does not wait if set to 0, otherwise waits this amount of seconds
        by default for messages to arrive.

        For more information, see Amazon SQS Long Poll.

        default
        :default: 0
        """
        return self._values.get('receive_message_wait_time')

    @builtins.property
    def retention_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of seconds that Amazon SQS retains a message.

        You can specify an integer value from 60 seconds (1 minute) to 1209600
        seconds (14 days). The default value is 345600 seconds (4 days).

        default
        :default: Duration.days(4)
        """
        return self._values.get('retention_period')

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout of processing a single message.

        After dequeuing, the processor has this much time to handle the message
        and delete it from the queue before it becomes visible again for dequeueing
        by another processor.

        Values must be from 0 to 43200 seconds (12 hours). If you don't specify
        a value, AWS CloudFormation uses the default value of 30 seconds.

        default
        :default: Duration.seconds(30)
        """
        return self._values.get('visibility_timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CfnQueue", "CfnQueuePolicy", "CfnQueuePolicyProps", "CfnQueueProps", "DeadLetterQueue", "IQueue", "Queue", "QueueAttributes", "QueueBase", "QueueEncryption", "QueuePolicy", "QueuePolicyProps", "QueueProps", "__jsii_assembly__"]

publication.publish()
