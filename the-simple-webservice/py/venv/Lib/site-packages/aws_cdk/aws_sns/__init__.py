"""
## Amazon Simple Notification Service Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Add an SNS Topic to your stack:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns as sns

topic = sns.Topic(self, "Topic",
    display_name="Customer subscription topic"
)
```

### Subscriptions

Various subscriptions can be added to the topic by calling the
`.addSubscription(...)` method on the topic. It accepts a *subscription* object,
default implementations of which can be found in the
`@aws-cdk/aws-sns-subscriptions` package:

Add an HTTPS Subscription to your topic:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns_subscriptions as subs

my_topic = sns.Topic(self, "MyTopic")

my_topic.add_subscription(subs.UrlSubscription("https://foobar.com/"))
```

Subscribe a queue to the topic:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_topic.add_subscription(subs.SqsSubscription(queue))
```

Note that subscriptions of queues in different accounts need to be manually confirmed by
reading the initial message from the queue and visiting the link found in it.

#### Filter policy

A filter policy can be specified when subscribing an endpoint to a topic.

Example with a Lambda subscription:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_topic = sns.Topic(self, "MyTopic")
fn = lambda.Function(self, "Function", ...)

# Lambda should receive only message matching the following conditions on attributes:
# color: 'red' or 'orange' or begins with 'bl'
# size: anything but 'small' or 'medium'
# price: between 100 and 200 or greater than 300
# store: attribute must be present
topic.add_subscription(subs.LambdaSubscription(fn,
    filter_policy={
        "color": sns.SubscriptionFilter.string_filter(
            whitelist=["red", "orange"],
            match_prefixes=["bl"]
        ),
        "size": sns.SubscriptionFilter.string_filter(
            blacklist=["small", "medium"]
        ),
        "price": sns.SubscriptionFilter.numeric_filter(
            between={"start": 100, "stop": 200},
            greater_than=300
        ),
        "store": sns.SubscriptionFilter.exists_filter()
    }
))
```

### CloudWatch Event Rule Target

SNS topics can be used as targets for CloudWatch event rules.

Use the `@aws-cdk/aws-events-targets.SnsTopicTarget`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_events_targets as targets

code_commit_repository.on_commit(targets.SnsTopicTarget(my_topic))
```

This will result in adding a target to the event rule and will also modify the
topic resource policy to allow CloudWatch events to publish to the topic.
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
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sns", "1.23.0", __name__, "aws-sns@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.BetweenCondition", jsii_struct_bases=[], name_mapping={'start': 'start', 'stop': 'stop'})
class BetweenCondition():
    def __init__(self, *, start: jsii.Number, stop: jsii.Number):
        """Between condition for a numeric attribute.

        :param start: The start value.
        :param stop: The stop value.
        """
        self._values = {
            'start': start,
            'stop': stop,
        }

    @builtins.property
    def start(self) -> jsii.Number:
        """The start value."""
        return self._values.get('start')

    @builtins.property
    def stop(self) -> jsii.Number:
        """The stop value."""
        return self._values.get('stop')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BetweenCondition(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSubscription(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnSubscription"):
    """A CloudFormation ``AWS::SNS::Subscription``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
    cloudformationResource:
    :cloudformationResource:: AWS::SNS::Subscription
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, protocol: str, topic_arn: str, delivery_policy: typing.Any=None, endpoint: typing.Optional[str]=None, filter_policy: typing.Any=None, raw_message_delivery: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, redrive_policy: typing.Any=None, region: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SNS::Subscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param protocol: ``AWS::SNS::Subscription.Protocol``.
        :param topic_arn: ``AWS::SNS::Subscription.TopicArn``.
        :param delivery_policy: ``AWS::SNS::Subscription.DeliveryPolicy``.
        :param endpoint: ``AWS::SNS::Subscription.Endpoint``.
        :param filter_policy: ``AWS::SNS::Subscription.FilterPolicy``.
        :param raw_message_delivery: ``AWS::SNS::Subscription.RawMessageDelivery``.
        :param redrive_policy: ``AWS::SNS::Subscription.RedrivePolicy``.
        :param region: ``AWS::SNS::Subscription.Region``.
        """
        props = CfnSubscriptionProps(protocol=protocol, topic_arn=topic_arn, delivery_policy=delivery_policy, endpoint=endpoint, filter_policy=filter_policy, raw_message_delivery=raw_message_delivery, redrive_policy=redrive_policy, region=region)

        jsii.create(CfnSubscription, self, [scope, id, props])

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
    @jsii.member(jsii_name="deliveryPolicy")
    def delivery_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.DeliveryPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        """
        return jsii.get(self, "deliveryPolicy")

    @delivery_policy.setter
    def delivery_policy(self, value: typing.Any):
        jsii.set(self, "deliveryPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="filterPolicy")
    def filter_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.FilterPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        """
        return jsii.get(self, "filterPolicy")

    @filter_policy.setter
    def filter_policy(self, value: typing.Any):
        jsii.set(self, "filterPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> str:
        """``AWS::SNS::Subscription.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: str):
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="redrivePolicy")
    def redrive_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.RedrivePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        """
        return jsii.get(self, "redrivePolicy")

    @redrive_policy.setter
    def redrive_policy(self, value: typing.Any):
        jsii.set(self, "redrivePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        """``AWS::SNS::Subscription.TopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
        """
        return jsii.get(self, "topicArn")

    @topic_arn.setter
    def topic_arn(self, value: str):
        jsii.set(self, "topicArn", value)

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[str]:
        """``AWS::SNS::Subscription.Endpoint``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
        """
        return jsii.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: typing.Optional[str]):
        jsii.set(self, "endpoint", value)

    @builtins.property
    @jsii.member(jsii_name="rawMessageDelivery")
    def raw_message_delivery(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::SNS::Subscription.RawMessageDelivery``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        """
        return jsii.get(self, "rawMessageDelivery")

    @raw_message_delivery.setter
    def raw_message_delivery(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "rawMessageDelivery", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[str]:
        """``AWS::SNS::Subscription.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        return jsii.get(self, "region")

    @region.setter
    def region(self, value: typing.Optional[str]):
        jsii.set(self, "region", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnSubscriptionProps", jsii_struct_bases=[], name_mapping={'protocol': 'protocol', 'topic_arn': 'topicArn', 'delivery_policy': 'deliveryPolicy', 'endpoint': 'endpoint', 'filter_policy': 'filterPolicy', 'raw_message_delivery': 'rawMessageDelivery', 'redrive_policy': 'redrivePolicy', 'region': 'region'})
class CfnSubscriptionProps():
    def __init__(self, *, protocol: str, topic_arn: str, delivery_policy: typing.Any=None, endpoint: typing.Optional[str]=None, filter_policy: typing.Any=None, raw_message_delivery: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, redrive_policy: typing.Any=None, region: typing.Optional[str]=None):
        """Properties for defining a ``AWS::SNS::Subscription``.

        :param protocol: ``AWS::SNS::Subscription.Protocol``.
        :param topic_arn: ``AWS::SNS::Subscription.TopicArn``.
        :param delivery_policy: ``AWS::SNS::Subscription.DeliveryPolicy``.
        :param endpoint: ``AWS::SNS::Subscription.Endpoint``.
        :param filter_policy: ``AWS::SNS::Subscription.FilterPolicy``.
        :param raw_message_delivery: ``AWS::SNS::Subscription.RawMessageDelivery``.
        :param redrive_policy: ``AWS::SNS::Subscription.RedrivePolicy``.
        :param region: ``AWS::SNS::Subscription.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
        """
        self._values = {
            'protocol': protocol,
            'topic_arn': topic_arn,
        }
        if delivery_policy is not None: self._values["delivery_policy"] = delivery_policy
        if endpoint is not None: self._values["endpoint"] = endpoint
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery
        if redrive_policy is not None: self._values["redrive_policy"] = redrive_policy
        if region is not None: self._values["region"] = region

    @builtins.property
    def protocol(self) -> str:
        """``AWS::SNS::Subscription.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
        """
        return self._values.get('protocol')

    @builtins.property
    def topic_arn(self) -> str:
        """``AWS::SNS::Subscription.TopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
        """
        return self._values.get('topic_arn')

    @builtins.property
    def delivery_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.DeliveryPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        """
        return self._values.get('delivery_policy')

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """``AWS::SNS::Subscription.Endpoint``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
        """
        return self._values.get('endpoint')

    @builtins.property
    def filter_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.FilterPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        """
        return self._values.get('filter_policy')

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::SNS::Subscription.RawMessageDelivery``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        """
        return self._values.get('raw_message_delivery')

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.RedrivePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        """
        return self._values.get('redrive_policy')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """``AWS::SNS::Subscription.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTopic(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnTopic"):
    """A CloudFormation ``AWS::SNS::Topic``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
    cloudformationResource:
    :cloudformationResource:: AWS::SNS::Topic
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, display_name: typing.Optional[str]=None, kms_master_key_id: typing.Optional[str]=None, subscription: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SubscriptionProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, topic_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SNS::Topic``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param display_name: ``AWS::SNS::Topic.DisplayName``.
        :param kms_master_key_id: ``AWS::SNS::Topic.KmsMasterKeyId``.
        :param subscription: ``AWS::SNS::Topic.Subscription``.
        :param tags: ``AWS::SNS::Topic.Tags``.
        :param topic_name: ``AWS::SNS::Topic.TopicName``.
        """
        props = CfnTopicProps(display_name=display_name, kms_master_key_id=kms_master_key_id, subscription=subscription, tags=tags, topic_name=topic_name)

        jsii.create(CfnTopic, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrTopicName")
    def attr_topic_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: TopicName
        """
        return jsii.get(self, "attrTopicName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SNS::Topic.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[str]:
        """``AWS::SNS::Topic.DisplayName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-displayname
        """
        return jsii.get(self, "displayName")

    @display_name.setter
    def display_name(self, value: typing.Optional[str]):
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="kmsMasterKeyId")
    def kms_master_key_id(self) -> typing.Optional[str]:
        """``AWS::SNS::Topic.KmsMasterKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        """
        return jsii.get(self, "kmsMasterKeyId")

    @kms_master_key_id.setter
    def kms_master_key_id(self, value: typing.Optional[str]):
        jsii.set(self, "kmsMasterKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="subscription")
    def subscription(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SubscriptionProperty"]]]]]:
        """``AWS::SNS::Topic.Subscription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-subscription
        """
        return jsii.get(self, "subscription")

    @subscription.setter
    def subscription(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SubscriptionProperty"]]]]]):
        jsii.set(self, "subscription", value)

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> typing.Optional[str]:
        """``AWS::SNS::Topic.TopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-topicname
        """
        return jsii.get(self, "topicName")

    @topic_name.setter
    def topic_name(self, value: typing.Optional[str]):
        jsii.set(self, "topicName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopic.SubscriptionProperty", jsii_struct_bases=[], name_mapping={'endpoint': 'endpoint', 'protocol': 'protocol'})
    class SubscriptionProperty():
        def __init__(self, *, endpoint: str, protocol: str):
            """
            :param endpoint: ``CfnTopic.SubscriptionProperty.Endpoint``.
            :param protocol: ``CfnTopic.SubscriptionProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html
            """
            self._values = {
                'endpoint': endpoint,
                'protocol': protocol,
            }

        @builtins.property
        def endpoint(self) -> str:
            """``CfnTopic.SubscriptionProperty.Endpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html#cfn-sns-topic-subscription-endpoint
            """
            return self._values.get('endpoint')

        @builtins.property
        def protocol(self) -> str:
            """``CfnTopic.SubscriptionProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html#cfn-sns-topic-subscription-protocol
            """
            return self._values.get('protocol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SubscriptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnTopicPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnTopicPolicy"):
    """A CloudFormation ``AWS::SNS::TopicPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::SNS::TopicPolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_document: typing.Any, topics: typing.List[str]) -> None:
        """Create a new ``AWS::SNS::TopicPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: ``AWS::SNS::TopicPolicy.PolicyDocument``.
        :param topics: ``AWS::SNS::TopicPolicy.Topics``.
        """
        props = CfnTopicPolicyProps(policy_document=policy_document, topics=topics)

        jsii.create(CfnTopicPolicy, self, [scope, id, props])

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
        """``AWS::SNS::TopicPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter
    def policy_document(self, value: typing.Any):
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[str]:
        """``AWS::SNS::TopicPolicy.Topics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
        """
        return jsii.get(self, "topics")

    @topics.setter
    def topics(self, value: typing.List[str]):
        jsii.set(self, "topics", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopicPolicyProps", jsii_struct_bases=[], name_mapping={'policy_document': 'policyDocument', 'topics': 'topics'})
class CfnTopicPolicyProps():
    def __init__(self, *, policy_document: typing.Any, topics: typing.List[str]):
        """Properties for defining a ``AWS::SNS::TopicPolicy``.

        :param policy_document: ``AWS::SNS::TopicPolicy.PolicyDocument``.
        :param topics: ``AWS::SNS::TopicPolicy.Topics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
        """
        self._values = {
            'policy_document': policy_document,
            'topics': topics,
        }

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::SNS::TopicPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
        """
        return self._values.get('policy_document')

    @builtins.property
    def topics(self) -> typing.List[str]:
        """``AWS::SNS::TopicPolicy.Topics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
        """
        return self._values.get('topics')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTopicPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopicProps", jsii_struct_bases=[], name_mapping={'display_name': 'displayName', 'kms_master_key_id': 'kmsMasterKeyId', 'subscription': 'subscription', 'tags': 'tags', 'topic_name': 'topicName'})
class CfnTopicProps():
    def __init__(self, *, display_name: typing.Optional[str]=None, kms_master_key_id: typing.Optional[str]=None, subscription: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopic.SubscriptionProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, topic_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::SNS::Topic``.

        :param display_name: ``AWS::SNS::Topic.DisplayName``.
        :param kms_master_key_id: ``AWS::SNS::Topic.KmsMasterKeyId``.
        :param subscription: ``AWS::SNS::Topic.Subscription``.
        :param tags: ``AWS::SNS::Topic.Tags``.
        :param topic_name: ``AWS::SNS::Topic.TopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
        """
        self._values = {
        }
        if display_name is not None: self._values["display_name"] = display_name
        if kms_master_key_id is not None: self._values["kms_master_key_id"] = kms_master_key_id
        if subscription is not None: self._values["subscription"] = subscription
        if tags is not None: self._values["tags"] = tags
        if topic_name is not None: self._values["topic_name"] = topic_name

    @builtins.property
    def display_name(self) -> typing.Optional[str]:
        """``AWS::SNS::Topic.DisplayName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-displayname
        """
        return self._values.get('display_name')

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[str]:
        """``AWS::SNS::Topic.KmsMasterKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        """
        return self._values.get('kms_master_key_id')

    @builtins.property
    def subscription(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTopic.SubscriptionProperty"]]]]]:
        """``AWS::SNS::Topic.Subscription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-subscription
        """
        return self._values.get('subscription')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SNS::Topic.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-tags
        """
        return self._values.get('tags')

    @builtins.property
    def topic_name(self) -> typing.Optional[str]:
        """``AWS::SNS::Topic.TopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-topicname
        """
        return self._values.get('topic_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTopicProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-sns.ITopic")
class ITopic(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITopicProxy

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        """Subscribe some endpoint to this topic.

        :param subscription: -
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is improted (``Topic.import``), then this is a no-op.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant topic publishing permissions to the given identity.

        :param identity: -
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Topic.

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages published to your Amazon SNS topics.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that Amazon SNS failed to deliver.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

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

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the size of messages published through this topic.

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

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

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

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The rate of successful SMS message deliveries.

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


class _ITopicProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-sns.ITopic"
    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "topicArn")

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "topicName")

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        """Subscribe some endpoint to this topic.

        :param subscription: -
        """
        return jsii.invoke(self, "addSubscription", [subscription])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is improted (``Topic.import``), then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant topic publishing permissions to the given identity.

        :param identity: -
        """
        return jsii.invoke(self, "grantPublish", [identity])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Topic.

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages published to your Amazon SNS topics.

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

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

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

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that Amazon SNS failed to deliver.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the size of messages published through this topic.

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

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

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

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The rate of successful SMS message deliveries.

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

        return jsii.invoke(self, "metricSMSSuccessRate", [props])


@jsii.interface(jsii_type="@aws-cdk/aws-sns.ITopicSubscription")
class ITopicSubscription(jsii.compat.Protocol):
    """Topic subscription."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITopicSubscriptionProxy

    @jsii.member(jsii_name="bind")
    def bind(self, topic: "ITopic") -> "TopicSubscriptionConfig":
        """
        :param topic: -
        """
        ...


class _ITopicSubscriptionProxy():
    """Topic subscription."""
    __jsii_type__ = "@aws-cdk/aws-sns.ITopicSubscription"
    @jsii.member(jsii_name="bind")
    def bind(self, topic: "ITopic") -> "TopicSubscriptionConfig":
        """
        :param topic: -
        """
        return jsii.invoke(self, "bind", [topic])


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.NumericConditions", jsii_struct_bases=[], name_mapping={'between': 'between', 'between_strict': 'betweenStrict', 'greater_than': 'greaterThan', 'greater_than_or_equal_to': 'greaterThanOrEqualTo', 'less_than': 'lessThan', 'less_than_or_equal_to': 'lessThanOrEqualTo', 'whitelist': 'whitelist'})
class NumericConditions():
    def __init__(self, *, between: typing.Optional["BetweenCondition"]=None, between_strict: typing.Optional["BetweenCondition"]=None, greater_than: typing.Optional[jsii.Number]=None, greater_than_or_equal_to: typing.Optional[jsii.Number]=None, less_than: typing.Optional[jsii.Number]=None, less_than_or_equal_to: typing.Optional[jsii.Number]=None, whitelist: typing.Optional[typing.List[jsii.Number]]=None):
        """Conditions that can be applied to numeric attributes.

        :param between: Match values that are between the specified values.
        :param between_strict: Match values that are strictly between the specified values.
        :param greater_than: Match values that are greater than the specified value.
        :param greater_than_or_equal_to: Match values that are greater than or equal to the specified value.
        :param less_than: Match values that are less than the specified value.
        :param less_than_or_equal_to: Match values that are less than or equal to the specified value.
        :param whitelist: Match one or more values.
        """
        if isinstance(between, dict): between = BetweenCondition(**between)
        if isinstance(between_strict, dict): between_strict = BetweenCondition(**between_strict)
        self._values = {
        }
        if between is not None: self._values["between"] = between
        if between_strict is not None: self._values["between_strict"] = between_strict
        if greater_than is not None: self._values["greater_than"] = greater_than
        if greater_than_or_equal_to is not None: self._values["greater_than_or_equal_to"] = greater_than_or_equal_to
        if less_than is not None: self._values["less_than"] = less_than
        if less_than_or_equal_to is not None: self._values["less_than_or_equal_to"] = less_than_or_equal_to
        if whitelist is not None: self._values["whitelist"] = whitelist

    @builtins.property
    def between(self) -> typing.Optional["BetweenCondition"]:
        """Match values that are between the specified values."""
        return self._values.get('between')

    @builtins.property
    def between_strict(self) -> typing.Optional["BetweenCondition"]:
        """Match values that are strictly between the specified values."""
        return self._values.get('between_strict')

    @builtins.property
    def greater_than(self) -> typing.Optional[jsii.Number]:
        """Match values that are greater than the specified value."""
        return self._values.get('greater_than')

    @builtins.property
    def greater_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        """Match values that are greater than or equal to the specified value."""
        return self._values.get('greater_than_or_equal_to')

    @builtins.property
    def less_than(self) -> typing.Optional[jsii.Number]:
        """Match values that are less than the specified value."""
        return self._values.get('less_than')

    @builtins.property
    def less_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        """Match values that are less than or equal to the specified value."""
        return self._values.get('less_than_or_equal_to')

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[jsii.Number]]:
        """Match one or more values."""
        return self._values.get('whitelist')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NumericConditions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.StringConditions", jsii_struct_bases=[], name_mapping={'blacklist': 'blacklist', 'match_prefixes': 'matchPrefixes', 'whitelist': 'whitelist'})
class StringConditions():
    def __init__(self, *, blacklist: typing.Optional[typing.List[str]]=None, match_prefixes: typing.Optional[typing.List[str]]=None, whitelist: typing.Optional[typing.List[str]]=None):
        """Conditions that can be applied to string attributes.

        :param blacklist: Match any value that doesn't include any of the specified values.
        :param match_prefixes: Matches values that begins with the specified prefixes.
        :param whitelist: Match one or more values.
        """
        self._values = {
        }
        if blacklist is not None: self._values["blacklist"] = blacklist
        if match_prefixes is not None: self._values["match_prefixes"] = match_prefixes
        if whitelist is not None: self._values["whitelist"] = whitelist

    @builtins.property
    def blacklist(self) -> typing.Optional[typing.List[str]]:
        """Match any value that doesn't include any of the specified values."""
        return self._values.get('blacklist')

    @builtins.property
    def match_prefixes(self) -> typing.Optional[typing.List[str]]:
        """Matches values that begins with the specified prefixes."""
        return self._values.get('match_prefixes')

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[str]]:
        """Match one or more values."""
        return self._values.get('whitelist')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StringConditions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Subscription(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.Subscription"):
    """A new subscription.

    Prefer to use the ``ITopic.addSubscription()`` methods to create instances of
    this class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, topic: "ITopic", endpoint: str, protocol: "SubscriptionProtocol", filter_policy: typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]=None, raw_message_delivery: typing.Optional[bool]=None, region: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param topic: The topic to subscribe to.
        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        """
        props = SubscriptionProps(topic=topic, endpoint=endpoint, protocol=protocol, filter_policy=filter_policy, raw_message_delivery=raw_message_delivery, region=region)

        jsii.create(Subscription, self, [scope, id, props])


class SubscriptionFilter(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.SubscriptionFilter"):
    """A subscription filter for an attribute."""
    def __init__(self, conditions: typing.Optional[typing.List[typing.Any]]=None) -> None:
        """
        :param conditions: -
        """
        jsii.create(SubscriptionFilter, self, [conditions])

    @jsii.member(jsii_name="existsFilter")
    @builtins.classmethod
    def exists_filter(cls) -> "SubscriptionFilter":
        """Returns a subscription filter for attribute key matching."""
        return jsii.sinvoke(cls, "existsFilter", [])

    @jsii.member(jsii_name="numericFilter")
    @builtins.classmethod
    def numeric_filter(cls, *, between: typing.Optional["BetweenCondition"]=None, between_strict: typing.Optional["BetweenCondition"]=None, greater_than: typing.Optional[jsii.Number]=None, greater_than_or_equal_to: typing.Optional[jsii.Number]=None, less_than: typing.Optional[jsii.Number]=None, less_than_or_equal_to: typing.Optional[jsii.Number]=None, whitelist: typing.Optional[typing.List[jsii.Number]]=None) -> "SubscriptionFilter":
        """Returns a subscription filter for a numeric attribute.

        :param between: Match values that are between the specified values.
        :param between_strict: Match values that are strictly between the specified values.
        :param greater_than: Match values that are greater than the specified value.
        :param greater_than_or_equal_to: Match values that are greater than or equal to the specified value.
        :param less_than: Match values that are less than the specified value.
        :param less_than_or_equal_to: Match values that are less than or equal to the specified value.
        :param whitelist: Match one or more values.
        """
        numeric_conditions = NumericConditions(between=between, between_strict=between_strict, greater_than=greater_than, greater_than_or_equal_to=greater_than_or_equal_to, less_than=less_than, less_than_or_equal_to=less_than_or_equal_to, whitelist=whitelist)

        return jsii.sinvoke(cls, "numericFilter", [numeric_conditions])

    @jsii.member(jsii_name="stringFilter")
    @builtins.classmethod
    def string_filter(cls, *, blacklist: typing.Optional[typing.List[str]]=None, match_prefixes: typing.Optional[typing.List[str]]=None, whitelist: typing.Optional[typing.List[str]]=None) -> "SubscriptionFilter":
        """Returns a subscription filter for a string attribute.

        :param blacklist: Match any value that doesn't include any of the specified values.
        :param match_prefixes: Matches values that begins with the specified prefixes.
        :param whitelist: Match one or more values.
        """
        string_conditions = StringConditions(blacklist=blacklist, match_prefixes=match_prefixes, whitelist=whitelist)

        return jsii.sinvoke(cls, "stringFilter", [string_conditions])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.List[typing.Any]:
        return jsii.get(self, "conditions")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.SubscriptionOptions", jsii_struct_bases=[], name_mapping={'endpoint': 'endpoint', 'protocol': 'protocol', 'filter_policy': 'filterPolicy', 'raw_message_delivery': 'rawMessageDelivery', 'region': 'region'})
class SubscriptionOptions():
    def __init__(self, *, endpoint: str, protocol: "SubscriptionProtocol", filter_policy: typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]=None, raw_message_delivery: typing.Optional[bool]=None, region: typing.Optional[str]=None):
        """Options for creating a new subscription.

        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        """
        self._values = {
            'endpoint': endpoint,
            'protocol': protocol,
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None: self._values["region"] = region

    @builtins.property
    def endpoint(self) -> str:
        """The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.
        """
        return self._values.get('endpoint')

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        """What type of subscription to add."""
        return self._values.get('protocol')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        default
        :default: false
        """
        return self._values.get('raw_message_delivery')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where the topic resides, in the case of cross-region subscriptions.

        default
        :default: - the region where the CloudFormation stack is being deployed.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.SubscriptionProps", jsii_struct_bases=[SubscriptionOptions], name_mapping={'endpoint': 'endpoint', 'protocol': 'protocol', 'filter_policy': 'filterPolicy', 'raw_message_delivery': 'rawMessageDelivery', 'region': 'region', 'topic': 'topic'})
class SubscriptionProps(SubscriptionOptions):
    def __init__(self, *, endpoint: str, protocol: "SubscriptionProtocol", filter_policy: typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]=None, raw_message_delivery: typing.Optional[bool]=None, region: typing.Optional[str]=None, topic: "ITopic"):
        """Properties for creating a new subscription.

        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param topic: The topic to subscribe to.
        """
        self._values = {
            'endpoint': endpoint,
            'protocol': protocol,
            'topic': topic,
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None: self._values["region"] = region

    @builtins.property
    def endpoint(self) -> str:
        """The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.
        """
        return self._values.get('endpoint')

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        """What type of subscription to add."""
        return self._values.get('protocol')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        default
        :default: false
        """
        return self._values.get('raw_message_delivery')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where the topic resides, in the case of cross-region subscriptions.

        default
        :default: - the region where the CloudFormation stack is being deployed.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        return self._values.get('region')

    @builtins.property
    def topic(self) -> "ITopic":
        """The topic to subscribe to."""
        return self._values.get('topic')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-sns.SubscriptionProtocol")
class SubscriptionProtocol(enum.Enum):
    """The type of subscription, controlling the type of the endpoint parameter."""
    HTTP = "HTTP"
    """JSON-encoded message is POSTED to an HTTP url."""
    HTTPS = "HTTPS"
    """JSON-encoded message is POSTed to an HTTPS url."""
    EMAIL = "EMAIL"
    """Notifications are sent via email."""
    EMAIL_JSON = "EMAIL_JSON"
    """Notifications are JSON-encoded and sent via mail."""
    SMS = "SMS"
    """Notification is delivered by SMS."""
    SQS = "SQS"
    """Notifications are enqueued into an SQS queue."""
    APPLICATION = "APPLICATION"
    """JSON-encoded notifications are sent to a mobile app endpoint."""
    LAMBDA = "LAMBDA"
    """Notifications trigger a Lambda function."""

@jsii.implements(ITopic)
class TopicBase(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-sns.TopicBase"):
    """Either a new or imported Topic."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TopicBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = aws_cdk.core.ResourceProps(physical_name=physical_name)

        jsii.create(TopicBase, self, [scope, id, props])

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        """Subscribe some endpoint to this topic.

        :param subscription: -
        """
        return jsii.invoke(self, "addSubscription", [subscription])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is improted (``Topic.import``), then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant topic publishing permissions to the given identity.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Topic.

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages published to your Amazon SNS topics.

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

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

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

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that Amazon SNS failed to deliver.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the size of messages published through this topic.

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

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

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

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The rate of successful SMS message deliveries.

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

        return jsii.invoke(self, "metricSMSSuccessRate", [props])

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    @abc.abstractmethod
    def topic_arn(self) -> str:
        ...

    @builtins.property
    @jsii.member(jsii_name="topicName")
    @abc.abstractmethod
    def topic_name(self) -> str:
        ...


class _TopicBaseProxy(TopicBase, jsii.proxy_for(aws_cdk.core.Resource)):
    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")


class Topic(TopicBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.Topic"):
    """A new SNS topic."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, display_name: typing.Optional[str]=None, master_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, topic_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param display_name: A developer-defined string that can be used to identify this SNS topic. Default: None
        :param master_key: A KMS Key, either managed by this CDK app, or imported. Default: None
        :param topic_name: A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name
        """
        props = TopicProps(display_name=display_name, master_key=master_key, topic_name=topic_name)

        jsii.create(Topic, self, [scope, id, props])

    @jsii.member(jsii_name="fromTopicArn")
    @builtins.classmethod
    def from_topic_arn(cls, scope: aws_cdk.core.Construct, id: str, topic_arn: str) -> "ITopic":
        """
        :param scope: -
        :param id: -
        :param topic_arn: -
        """
        return jsii.sinvoke(cls, "fromTopicArn", [scope, id, topic_arn])

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")


class TopicPolicy(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.TopicPolicy"):
    """Applies a policy to SNS topics."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, topics: typing.List["ITopic"]) -> None:
        """
        :param scope: -
        :param id: -
        :param topics: The set of topics this policy applies to.
        """
        props = TopicPolicyProps(topics=topics)

        jsii.create(TopicPolicy, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        """The IAM policy document for this policy."""
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicPolicyProps", jsii_struct_bases=[], name_mapping={'topics': 'topics'})
class TopicPolicyProps():
    def __init__(self, *, topics: typing.List["ITopic"]):
        """
        :param topics: The set of topics this policy applies to.
        """
        self._values = {
            'topics': topics,
        }

    @builtins.property
    def topics(self) -> typing.List["ITopic"]:
        """The set of topics this policy applies to."""
        return self._values.get('topics')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TopicPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicProps", jsii_struct_bases=[], name_mapping={'display_name': 'displayName', 'master_key': 'masterKey', 'topic_name': 'topicName'})
class TopicProps():
    def __init__(self, *, display_name: typing.Optional[str]=None, master_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, topic_name: typing.Optional[str]=None):
        """Properties for a new SNS topic.

        :param display_name: A developer-defined string that can be used to identify this SNS topic. Default: None
        :param master_key: A KMS Key, either managed by this CDK app, or imported. Default: None
        :param topic_name: A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name
        """
        self._values = {
        }
        if display_name is not None: self._values["display_name"] = display_name
        if master_key is not None: self._values["master_key"] = master_key
        if topic_name is not None: self._values["topic_name"] = topic_name

    @builtins.property
    def display_name(self) -> typing.Optional[str]:
        """A developer-defined string that can be used to identify this SNS topic.

        default
        :default: None
        """
        return self._values.get('display_name')

    @builtins.property
    def master_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """A KMS Key, either managed by this CDK app, or imported.

        default
        :default: None
        """
        return self._values.get('master_key')

    @builtins.property
    def topic_name(self) -> typing.Optional[str]:
        """A name for the topic.

        If you don't specify a name, AWS CloudFormation generates a unique
        physical ID and uses that ID for the topic name. For more information,
        see Name Type.

        default
        :default: Generated name
        """
        return self._values.get('topic_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TopicProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicSubscriptionConfig", jsii_struct_bases=[SubscriptionOptions], name_mapping={'endpoint': 'endpoint', 'protocol': 'protocol', 'filter_policy': 'filterPolicy', 'raw_message_delivery': 'rawMessageDelivery', 'region': 'region', 'subscriber_id': 'subscriberId', 'subscriber_scope': 'subscriberScope'})
class TopicSubscriptionConfig(SubscriptionOptions):
    def __init__(self, *, endpoint: str, protocol: "SubscriptionProtocol", filter_policy: typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]=None, raw_message_delivery: typing.Optional[bool]=None, region: typing.Optional[str]=None, subscriber_id: str, subscriber_scope: typing.Optional[aws_cdk.core.Construct]=None):
        """Subscription configuration.

        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param subscriber_id: The id of the SNS subscription resource created under ``scope``. In most cases, it is recommended to use the ``uniqueId`` of the topic you are subscribing to.
        :param subscriber_scope: The scope in which to create the SNS subscription resource. Normally you'd want the subscription to be created on the consuming stack because the topic is usually referenced by the consumer's resource policy (e.g. SQS queue policy). Otherwise, it will cause a cyclic reference. If this is undefined, the subscription will be created on the topic's stack. Default: - use the topic as the scope of the subscription, in which case ``subscriberId`` must be defined.
        """
        self._values = {
            'endpoint': endpoint,
            'protocol': protocol,
            'subscriber_id': subscriber_id,
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None: self._values["region"] = region
        if subscriber_scope is not None: self._values["subscriber_scope"] = subscriber_scope

    @builtins.property
    def endpoint(self) -> str:
        """The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.
        """
        return self._values.get('endpoint')

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        """What type of subscription to add."""
        return self._values.get('protocol')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,"SubscriptionFilter"]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        default
        :default: false
        """
        return self._values.get('raw_message_delivery')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where the topic resides, in the case of cross-region subscriptions.

        default
        :default: - the region where the CloudFormation stack is being deployed.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        return self._values.get('region')

    @builtins.property
    def subscriber_id(self) -> str:
        """The id of the SNS subscription resource created under ``scope``.

        In most
        cases, it is recommended to use the ``uniqueId`` of the topic you are
        subscribing to.
        """
        return self._values.get('subscriber_id')

    @builtins.property
    def subscriber_scope(self) -> typing.Optional[aws_cdk.core.Construct]:
        """The scope in which to create the SNS subscription resource.

        Normally you'd
        want the subscription to be created on the consuming stack because the
        topic is usually referenced by the consumer's resource policy (e.g. SQS
        queue policy). Otherwise, it will cause a cyclic reference.

        If this is undefined, the subscription will be created on the topic's stack.

        default
        :default: - use the topic as the scope of the subscription, in which case ``subscriberId`` must be defined.
        """
        return self._values.get('subscriber_scope')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TopicSubscriptionConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["BetweenCondition", "CfnSubscription", "CfnSubscriptionProps", "CfnTopic", "CfnTopicPolicy", "CfnTopicPolicyProps", "CfnTopicProps", "ITopic", "ITopicSubscription", "NumericConditions", "StringConditions", "Subscription", "SubscriptionFilter", "SubscriptionOptions", "SubscriptionProps", "SubscriptionProtocol", "Topic", "TopicBase", "TopicPolicy", "TopicPolicyProps", "TopicProps", "TopicSubscriptionConfig", "__jsii_assembly__"]

publication.publish()
