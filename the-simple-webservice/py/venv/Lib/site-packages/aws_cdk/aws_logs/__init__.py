"""
## Amazon CloudWatch Logs Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library supplies constructs for working with CloudWatch Logs.

### Log Groups/Streams

The basic unit of CloudWatch is a *Log Group*. Every log group typically has the
same kind of data logged to it, in the same format. If there are multiple
applications or services logging into the Log Group, each of them creates a new
*Log Stream*.

Every log operation creates a "log event", which can consist of a simple string
or a single-line JSON object. JSON objects have the advantage that they afford
more filtering abilities (see below).

The only configurable attribute for log streams is the retention period, which
configures after how much time the events in the log stream expire and are
deleted.

The default retention period if not supplied is 2 years, but it can be set to
one of the values in the `RetentionDays` enum to configure a different
retention period (including infinite retention).

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Configure log group for short retention
log_group = LogGroup(stack, "LogGroup",
    retention=RetentionDays.ONE_WEEK
)
# Configure log group for infinite retention
log_group = LogGroup(stack, "LogGroup",
    retention=Infinity
)
```

### Subscriptions and Destinations

Log events matching a particular filter can be sent to either a Lambda function
or a Kinesis stream.

If the Kinesis stream lives in a different account, a `CrossAccountDestination`
object needs to be added in the destination account which will act as a proxy
for the remote Kinesis stream. This object is automatically created for you
if you use the CDK Kinesis library.

Create a `SubscriptionFilter`, initialize it with an appropriate `Pattern` (see
below) and supply the intended destination:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn = lambda.Function(self, "Lambda", ...)
log_group = LogGroup(self, "LogGroup", ...)

SubscriptionFilter(self, "Subscription",
    log_group=log_group,
    destination=LogsDestinations.LambdaDestination(fn),
    filter_pattern=FilterPattern.all_terms("ERROR", "MainThread")
)
```

### Metric Filters

CloudWatch Logs can extract and emit metrics based on a textual log stream.
Depending on your needs, this may be a more convenient way of generating metrics
for you application than making calls to CloudWatch Metrics yourself.

A `MetricFilter` either emits a fixed number every time it sees a log event
matching a particular pattern (see below), or extracts a number from the log
event and uses that as the metric value.

Example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
MetricFilter(self, "MetricFilter",
    log_group=log_group,
    metric_namespace="MyApp",
    metric_name="Latency",
    filter_pattern=FilterPattern.exists("$.latency"),
    metric_value="$.latency"
)
```

Remember that if you want to use a value from the log event as the metric value,
you must mention it in your pattern somewhere.

A very simple MetricFilter can be created by using the `logGroup.extractMetric()`
helper function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
log_group.extract_metric("$.jsonField", "Namespace", "MetricName")
```

Will extract the value of `jsonField` wherever it occurs in JSON-structed
log records in the LogGroup, and emit them to CloudWatch Metrics under
the name `Namespace/MetricName`.

### Patterns

Patterns describe which log events match a subscription or metric filter. There
are three types of patterns:

* Text patterns
* JSON patterns
* Space-delimited table patterns

All patterns are constructed by using static functions on the `FilterPattern`
class.

In addition to the patterns above, the following special patterns exist:

* `FilterPattern.allEvents()`: matches all log events.
* `FilterPattern.literal(string)`: if you already know what pattern expression to
  use, this function takes a string and will use that as the log pattern. For
  more information, see the [Filter and Pattern
  Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).

#### Text Patterns

Text patterns match if the literal strings appear in the text form of the log
line.

* `FilterPattern.allTerms(term, term, ...)`: matches if all of the given terms
  (substrings) appear in the log event.
* `FilterPattern.anyTerm(term, term, ...)`: matches if all of the given terms
  (substrings) appear in the log event.
* `FilterPattern.anyGroup([term, term, ...], [term, term, ...], ...)`: matches if
  all of the terms in any of the groups (specified as arrays) matches. This is
  an OR match.

Examples:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Search for lines that contain both "ERROR" and "MainThread"
pattern1 = FilterPattern.all_terms("ERROR", "MainThread")

# Search for lines that either contain both "ERROR" and "MainThread", or
# both "WARN" and "Deadlock".
pattern2 = FilterPattern.any_group(["ERROR", "MainThread"], ["WARN", "Deadlock"])
```

### JSON Patterns

JSON patterns apply if the log event is the JSON representation of an object
(without any other characters, so it cannot include a prefix such as timestamp
or log level). JSON patterns can make comparisons on the values inside the
fields.

* **Strings**: the comparison operators allowed for strings are `=` and `!=`.
  String values can start or end with a `*` wildcard.
* **Numbers**: the comparison operators allowed for numbers are `=`, `!=`,
  `<`, `<=`, `>`, `>=`.

Fields in the JSON structure are identified by identifier the complete object as `$`
and then descending into it, such as `$.field` or `$.list[0].field`.

* `FilterPattern.stringValue(field, comparison, string)`: matches if the given
  field compares as indicated with the given string value.
* `FilterPattern.numberValue(field, comparison, number)`: matches if the given
  field compares as indicated with the given numerical value.
* `FilterPattern.isNull(field)`: matches if the given field exists and has the
  value `null`.
* `FilterPattern.notExists(field)`: matches if the given field is not in the JSON
  structure.
* `FilterPattern.exists(field)`: matches if the given field is in the JSON
  structure.
* `FilterPattern.booleanValue(field, boolean)`: matches if the given field
  is exactly the given boolean value.
* `FilterPattern.all(jsonPattern, jsonPattern, ...)`: matches if all of the
  given JSON patterns match. This makes an AND combination of the given
  patterns.
* `FilterPattern.any(jsonPattern, jsonPattern, ...)`: matches if any of the
  given JSON patterns match. This makes an OR combination of the given
  patterns.

Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Search for all events where the component field is equal to
# "HttpServer" and either error is true or the latency is higher
# than 1000.
pattern = FilterPattern.all(
    FilterPattern.string_value("$.component", "=", "HttpServer"),
    FilterPattern.any(
        FilterPattern.boolean_value("$.error", True),
        FilterPattern.number_value("$.latency", ">", 1000)))
```

### Space-delimited table patterns

If the log events are rows of a space-delimited table, this pattern can be used
to identify the columns in that structure and add conditions on any of them. The
canonical example where you would apply this type of pattern is Apache server
logs.

Text that is surrounded by `"..."` quotes or `[...]` square brackets will
be treated as one column.

* `FilterPattern.spaceDelimited(column, column, ...)`: construct a
  `SpaceDelimitedTextPattern` object with the indicated columns. The columns
  map one-by-one the columns found in the log event. The string `"..."` may
  be used to specify an arbitrary number of unnamed columns anywhere in the
  name list (but may only be specified once).

After constructing a `SpaceDelimitedTextPattern`, you can use the following
two members to add restrictions:

* `pattern.whereString(field, comparison, string)`: add a string condition.
  The rules are the same as for JSON patterns.
* `pattern.whereNumber(field, comparison, number)`: add a numerical condition.
  The rules are the same as for JSON patterns.

Multiple restrictions can be added on the same column; they must all apply.

Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Search for all events where the component is "HttpServer" and the
# result code is not equal to 200.
pattern = FilterPattern.space_delimited("time", "component", "...", "result_code", "latency").where_string("component", "=", "HttpServer").where_number("result_code", "!=", 200)
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

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-logs", "1.23.0", __name__, "aws-logs@1.23.0.jsii.tgz")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDestination(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnDestination"):
    """A CloudFormation ``AWS::Logs::Destination``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::Destination
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, destination_name: str, destination_policy: str, role_arn: str, target_arn: str) -> None:
        """Create a new ``AWS::Logs::Destination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_name: ``AWS::Logs::Destination.DestinationName``.
        :param destination_policy: ``AWS::Logs::Destination.DestinationPolicy``.
        :param role_arn: ``AWS::Logs::Destination.RoleArn``.
        :param target_arn: ``AWS::Logs::Destination.TargetArn``.
        """
        props = CfnDestinationProps(destination_name=destination_name, destination_policy=destination_policy, role_arn=role_arn, target_arn=target_arn)

        jsii.create(CfnDestination, self, [scope, id, props])

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
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> str:
        """``AWS::Logs::Destination.DestinationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        """
        return jsii.get(self, "destinationName")

    @destination_name.setter
    def destination_name(self, value: str):
        jsii.set(self, "destinationName", value)

    @builtins.property
    @jsii.member(jsii_name="destinationPolicy")
    def destination_policy(self) -> str:
        """``AWS::Logs::Destination.DestinationPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        """
        return jsii.get(self, "destinationPolicy")

    @destination_policy.setter
    def destination_policy(self, value: str):
        jsii.set(self, "destinationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::Logs::Destination.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str):
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> str:
        """``AWS::Logs::Destination.TargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        """
        return jsii.get(self, "targetArn")

    @target_arn.setter
    def target_arn(self, value: str):
        jsii.set(self, "targetArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnDestinationProps", jsii_struct_bases=[], name_mapping={'destination_name': 'destinationName', 'destination_policy': 'destinationPolicy', 'role_arn': 'roleArn', 'target_arn': 'targetArn'})
class CfnDestinationProps():
    def __init__(self, *, destination_name: str, destination_policy: str, role_arn: str, target_arn: str):
        """Properties for defining a ``AWS::Logs::Destination``.

        :param destination_name: ``AWS::Logs::Destination.DestinationName``.
        :param destination_policy: ``AWS::Logs::Destination.DestinationPolicy``.
        :param role_arn: ``AWS::Logs::Destination.RoleArn``.
        :param target_arn: ``AWS::Logs::Destination.TargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
        """
        self._values = {
            'destination_name': destination_name,
            'destination_policy': destination_policy,
            'role_arn': role_arn,
            'target_arn': target_arn,
        }

    @builtins.property
    def destination_name(self) -> str:
        """``AWS::Logs::Destination.DestinationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        """
        return self._values.get('destination_name')

    @builtins.property
    def destination_policy(self) -> str:
        """``AWS::Logs::Destination.DestinationPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        """
        return self._values.get('destination_policy')

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::Logs::Destination.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def target_arn(self) -> str:
        """``AWS::Logs::Destination.TargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        """
        return self._values.get('target_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDestinationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLogGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnLogGroup"):
    """A CloudFormation ``AWS::Logs::LogGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::LogGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, log_group_name: typing.Optional[str]=None, retention_in_days: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::Logs::LogGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: ``AWS::Logs::LogGroup.LogGroupName``.
        :param retention_in_days: ``AWS::Logs::LogGroup.RetentionInDays``.
        """
        props = CfnLogGroupProps(log_group_name=log_group_name, retention_in_days=retention_in_days)

        jsii.create(CfnLogGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogGroup.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="retentionInDays")
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::Logs::LogGroup.RetentionInDays``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-retentionindays
        """
        return jsii.get(self, "retentionInDays")

    @retention_in_days.setter
    def retention_in_days(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "retentionInDays", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnLogGroupProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'retention_in_days': 'retentionInDays'})
class CfnLogGroupProps():
    def __init__(self, *, log_group_name: typing.Optional[str]=None, retention_in_days: typing.Optional[jsii.Number]=None):
        """Properties for defining a ``AWS::Logs::LogGroup``.

        :param log_group_name: ``AWS::Logs::LogGroup.LogGroupName``.
        :param retention_in_days: ``AWS::Logs::LogGroup.RetentionInDays``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
        """
        self._values = {
        }
        if log_group_name is not None: self._values["log_group_name"] = log_group_name
        if retention_in_days is not None: self._values["retention_in_days"] = retention_in_days

    @builtins.property
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogGroup.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::Logs::LogGroup.RetentionInDays``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-retentionindays
        """
        return self._values.get('retention_in_days')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLogGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLogStream(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnLogStream"):
    """A CloudFormation ``AWS::Logs::LogStream``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::LogStream
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, log_group_name: str, log_stream_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Logs::LogStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: ``AWS::Logs::LogStream.LogGroupName``.
        :param log_stream_name: ``AWS::Logs::LogStream.LogStreamName``.
        """
        props = CfnLogStreamProps(log_group_name=log_group_name, log_stream_name=log_stream_name)

        jsii.create(CfnLogStream, self, [scope, id, props])

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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """``AWS::Logs::LogStream.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: str):
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogStream.LogStreamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        """
        return jsii.get(self, "logStreamName")

    @log_stream_name.setter
    def log_stream_name(self, value: typing.Optional[str]):
        jsii.set(self, "logStreamName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnLogStreamProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'log_stream_name': 'logStreamName'})
class CfnLogStreamProps():
    def __init__(self, *, log_group_name: str, log_stream_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Logs::LogStream``.

        :param log_group_name: ``AWS::Logs::LogStream.LogGroupName``.
        :param log_stream_name: ``AWS::Logs::LogStream.LogStreamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
        """
        self._values = {
            'log_group_name': log_group_name,
        }
        if log_stream_name is not None: self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_group_name(self) -> str:
        """``AWS::Logs::LogStream.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def log_stream_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogStream.LogStreamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        """
        return self._values.get('log_stream_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLogStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMetricFilter(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnMetricFilter"):
    """A CloudFormation ``AWS::Logs::MetricFilter``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::MetricFilter
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, filter_pattern: str, log_group_name: str, metric_transformations: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["MetricTransformationProperty", aws_cdk.core.IResolvable]]]) -> None:
        """Create a new ``AWS::Logs::MetricFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter_pattern: ``AWS::Logs::MetricFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::MetricFilter.LogGroupName``.
        :param metric_transformations: ``AWS::Logs::MetricFilter.MetricTransformations``.
        """
        props = CfnMetricFilterProps(filter_pattern=filter_pattern, log_group_name=log_group_name, metric_transformations=metric_transformations)

        jsii.create(CfnMetricFilter, self, [scope, id, props])

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
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> str:
        """``AWS::Logs::MetricFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-filterpattern
        """
        return jsii.get(self, "filterPattern")

    @filter_pattern.setter
    def filter_pattern(self, value: str):
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """``AWS::Logs::MetricFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: str):
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="metricTransformations")
    def metric_transformations(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["MetricTransformationProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Logs::MetricFilter.MetricTransformations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-metrictransformations
        """
        return jsii.get(self, "metricTransformations")

    @metric_transformations.setter
    def metric_transformations(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["MetricTransformationProperty", aws_cdk.core.IResolvable]]]):
        jsii.set(self, "metricTransformations", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnMetricFilter.MetricTransformationProperty", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'metric_value': 'metricValue', 'default_value': 'defaultValue'})
    class MetricTransformationProperty():
        def __init__(self, *, metric_name: str, metric_namespace: str, metric_value: str, default_value: typing.Optional[jsii.Number]=None):
            """
            :param metric_name: ``CfnMetricFilter.MetricTransformationProperty.MetricName``.
            :param metric_namespace: ``CfnMetricFilter.MetricTransformationProperty.MetricNamespace``.
            :param metric_value: ``CfnMetricFilter.MetricTransformationProperty.MetricValue``.
            :param default_value: ``CfnMetricFilter.MetricTransformationProperty.DefaultValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html
            """
            self._values = {
                'metric_name': metric_name,
                'metric_namespace': metric_namespace,
                'metric_value': metric_value,
            }
            if default_value is not None: self._values["default_value"] = default_value

        @builtins.property
        def metric_name(self) -> str:
            """``CfnMetricFilter.MetricTransformationProperty.MetricName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricname
            """
            return self._values.get('metric_name')

        @builtins.property
        def metric_namespace(self) -> str:
            """``CfnMetricFilter.MetricTransformationProperty.MetricNamespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricnamespace
            """
            return self._values.get('metric_namespace')

        @builtins.property
        def metric_value(self) -> str:
            """``CfnMetricFilter.MetricTransformationProperty.MetricValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricvalue
            """
            return self._values.get('metric_value')

        @builtins.property
        def default_value(self) -> typing.Optional[jsii.Number]:
            """``CfnMetricFilter.MetricTransformationProperty.DefaultValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-defaultvalue
            """
            return self._values.get('default_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricTransformationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnMetricFilterProps", jsii_struct_bases=[], name_mapping={'filter_pattern': 'filterPattern', 'log_group_name': 'logGroupName', 'metric_transformations': 'metricTransformations'})
class CfnMetricFilterProps():
    def __init__(self, *, filter_pattern: str, log_group_name: str, metric_transformations: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", aws_cdk.core.IResolvable]]]):
        """Properties for defining a ``AWS::Logs::MetricFilter``.

        :param filter_pattern: ``AWS::Logs::MetricFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::MetricFilter.LogGroupName``.
        :param metric_transformations: ``AWS::Logs::MetricFilter.MetricTransformations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
        """
        self._values = {
            'filter_pattern': filter_pattern,
            'log_group_name': log_group_name,
            'metric_transformations': metric_transformations,
        }

    @builtins.property
    def filter_pattern(self) -> str:
        """``AWS::Logs::MetricFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-filterpattern
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def log_group_name(self) -> str:
        """``AWS::Logs::MetricFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def metric_transformations(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Logs::MetricFilter.MetricTransformations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-metrictransformations
        """
        return self._values.get('metric_transformations')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMetricFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSubscriptionFilter(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnSubscriptionFilter"):
    """A CloudFormation ``AWS::Logs::SubscriptionFilter``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::SubscriptionFilter
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, destination_arn: str, filter_pattern: str, log_group_name: str, role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Logs::SubscriptionFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: ``AWS::Logs::SubscriptionFilter.DestinationArn``.
        :param filter_pattern: ``AWS::Logs::SubscriptionFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::SubscriptionFilter.LogGroupName``.
        :param role_arn: ``AWS::Logs::SubscriptionFilter.RoleArn``.
        """
        props = CfnSubscriptionFilterProps(destination_arn=destination_arn, filter_pattern=filter_pattern, log_group_name=log_group_name, role_arn=role_arn)

        jsii.create(CfnSubscriptionFilter, self, [scope, id, props])

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
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> str:
        """``AWS::Logs::SubscriptionFilter.DestinationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-destinationarn
        """
        return jsii.get(self, "destinationArn")

    @destination_arn.setter
    def destination_arn(self, value: str):
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> str:
        """``AWS::Logs::SubscriptionFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-filterpattern
        """
        return jsii.get(self, "filterPattern")

    @filter_pattern.setter
    def filter_pattern(self, value: str):
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """``AWS::Logs::SubscriptionFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: str):
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Logs::SubscriptionFilter.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]):
        jsii.set(self, "roleArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnSubscriptionFilterProps", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'filter_pattern': 'filterPattern', 'log_group_name': 'logGroupName', 'role_arn': 'roleArn'})
class CfnSubscriptionFilterProps():
    def __init__(self, *, destination_arn: str, filter_pattern: str, log_group_name: str, role_arn: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Logs::SubscriptionFilter``.

        :param destination_arn: ``AWS::Logs::SubscriptionFilter.DestinationArn``.
        :param filter_pattern: ``AWS::Logs::SubscriptionFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::SubscriptionFilter.LogGroupName``.
        :param role_arn: ``AWS::Logs::SubscriptionFilter.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
        """
        self._values = {
            'destination_arn': destination_arn,
            'filter_pattern': filter_pattern,
            'log_group_name': log_group_name,
        }
        if role_arn is not None: self._values["role_arn"] = role_arn

    @builtins.property
    def destination_arn(self) -> str:
        """``AWS::Logs::SubscriptionFilter.DestinationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-destinationarn
        """
        return self._values.get('destination_arn')

    @builtins.property
    def filter_pattern(self) -> str:
        """``AWS::Logs::SubscriptionFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-filterpattern
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def log_group_name(self) -> str:
        """``AWS::Logs::SubscriptionFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Logs::SubscriptionFilter.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-rolearn
        """
        return self._values.get('role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSubscriptionFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.ColumnRestriction", jsii_struct_bases=[], name_mapping={'comparison': 'comparison', 'number_value': 'numberValue', 'string_value': 'stringValue'})
class ColumnRestriction():
    def __init__(self, *, comparison: str, number_value: typing.Optional[jsii.Number]=None, string_value: typing.Optional[str]=None):
        """
        :param comparison: Comparison operator to use.
        :param number_value: Number value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.
        :param string_value: String value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.
        """
        self._values = {
            'comparison': comparison,
        }
        if number_value is not None: self._values["number_value"] = number_value
        if string_value is not None: self._values["string_value"] = string_value

    @builtins.property
    def comparison(self) -> str:
        """Comparison operator to use."""
        return self._values.get('comparison')

    @builtins.property
    def number_value(self) -> typing.Optional[jsii.Number]:
        """Number value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.
        """
        return self._values.get('number_value')

    @builtins.property
    def string_value(self) -> typing.Optional[str]:
        """String value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.
        """
        return self._values.get('string_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ColumnRestriction(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CrossAccountDestinationProps", jsii_struct_bases=[], name_mapping={'role': 'role', 'target_arn': 'targetArn', 'destination_name': 'destinationName'})
class CrossAccountDestinationProps():
    def __init__(self, *, role: aws_cdk.aws_iam.IRole, target_arn: str, destination_name: typing.Optional[str]=None):
        """Properties for a CrossAccountDestination.

        :param role: The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: The log destination target's ARN.
        :param destination_name: The name of the log destination. Default: Automatically generated
        """
        self._values = {
            'role': role,
            'target_arn': target_arn,
        }
        if destination_name is not None: self._values["destination_name"] = destination_name

    @builtins.property
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role to assume that grants permissions to write to 'target'.

        The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        """
        return self._values.get('role')

    @builtins.property
    def target_arn(self) -> str:
        """The log destination target's ARN."""
        return self._values.get('target_arn')

    @builtins.property
    def destination_name(self) -> typing.Optional[str]:
        """The name of the log destination.

        default
        :default: Automatically generated
        """
        return self._values.get('destination_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CrossAccountDestinationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class FilterPattern(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.FilterPattern"):
    """A collection of static methods to generate appropriate ILogPatterns."""
    def __init__(self) -> None:
        jsii.create(FilterPattern, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls, *patterns: "JsonPattern") -> "JsonPattern":
        """A JSON log pattern that matches if all given JSON log patterns match.

        :param patterns: -
        """
        return jsii.sinvoke(cls, "all", [*patterns])

    @jsii.member(jsii_name="allEvents")
    @builtins.classmethod
    def all_events(cls) -> "IFilterPattern":
        """A log pattern that matches all events."""
        return jsii.sinvoke(cls, "allEvents", [])

    @jsii.member(jsii_name="allTerms")
    @builtins.classmethod
    def all_terms(cls, *terms: str) -> "IFilterPattern":
        """A log pattern that matches if all the strings given appear in the event.

        :param terms: The words to search for. All terms must match.
        """
        return jsii.sinvoke(cls, "allTerms", [*terms])

    @jsii.member(jsii_name="any")
    @builtins.classmethod
    def any(cls, *patterns: "JsonPattern") -> "JsonPattern":
        """A JSON log pattern that matches if any of the given JSON log patterns match.

        :param patterns: -
        """
        return jsii.sinvoke(cls, "any", [*patterns])

    @jsii.member(jsii_name="anyTerm")
    @builtins.classmethod
    def any_term(cls, *terms: str) -> "IFilterPattern":
        """A log pattern that matches if any of the strings given appear in the event.

        :param terms: The words to search for. Any terms must match.
        """
        return jsii.sinvoke(cls, "anyTerm", [*terms])

    @jsii.member(jsii_name="anyTermGroup")
    @builtins.classmethod
    def any_term_group(cls, *term_groups: typing.List[str]) -> "IFilterPattern":
        """A log pattern that matches if any of the given term groups matches the event.

        A term group matches an event if all the terms in it appear in the event string.

        :param term_groups: A list of term groups to search for. Any one of the clauses must match.
        """
        return jsii.sinvoke(cls, "anyTermGroup", [*term_groups])

    @jsii.member(jsii_name="booleanValue")
    @builtins.classmethod
    def boolean_value(cls, json_field: str, value: bool) -> "JsonPattern":
        """A JSON log pattern that matches if the field exists and equals the boolean value.

        :param json_field: Field inside JSON. Example: "$.myField"
        :param value: The value to match.
        """
        return jsii.sinvoke(cls, "booleanValue", [json_field, value])

    @jsii.member(jsii_name="exists")
    @builtins.classmethod
    def exists(cls, json_field: str) -> "JsonPattern":
        """A JSON log patter that matches if the field exists.

        This is a readable convenience wrapper over 'field = *'

        :param json_field: Field inside JSON. Example: "$.myField"
        """
        return jsii.sinvoke(cls, "exists", [json_field])

    @jsii.member(jsii_name="isNull")
    @builtins.classmethod
    def is_null(cls, json_field: str) -> "JsonPattern":
        """A JSON log pattern that matches if the field exists and has the special value 'null'.

        :param json_field: Field inside JSON. Example: "$.myField"
        """
        return jsii.sinvoke(cls, "isNull", [json_field])

    @jsii.member(jsii_name="literal")
    @builtins.classmethod
    def literal(cls, log_pattern_string: str) -> "IFilterPattern":
        """Use the given string as log pattern.

        See https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
        for information on writing log patterns.

        :param log_pattern_string: The pattern string to use.
        """
        return jsii.sinvoke(cls, "literal", [log_pattern_string])

    @jsii.member(jsii_name="notExists")
    @builtins.classmethod
    def not_exists(cls, json_field: str) -> "JsonPattern":
        """A JSON log pattern that matches if the field does not exist.

        :param json_field: Field inside JSON. Example: "$.myField"
        """
        return jsii.sinvoke(cls, "notExists", [json_field])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, json_field: str, comparison: str, value: jsii.Number) -> "JsonPattern":
        """A JSON log pattern that compares numerical values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the value in the indicated way.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. One of =, !=, <, <=, >, >=.
        :param value: The numerical value to compare to.
        """
        return jsii.sinvoke(cls, "numberValue", [json_field, comparison, value])

    @jsii.member(jsii_name="spaceDelimited")
    @builtins.classmethod
    def space_delimited(cls, *columns: str) -> "SpaceDelimitedTextPattern":
        """A space delimited log pattern matcher.

        The log event is divided into space-delimited columns (optionally
        enclosed by "" or [] to capture spaces into column values), and names
        are given to each column.

        '...' may be specified once to match any number of columns.

        Afterwards, conditions may be added to individual columns.

        :param columns: The columns in the space-delimited log stream.
        """
        return jsii.sinvoke(cls, "spaceDelimited", [*columns])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(cls, json_field: str, comparison: str, value: str) -> "JsonPattern":
        """A JSON log pattern that compares string values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the string value.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. Either = or !=.
        :param value: The string value to compare to. May use '*' as wildcard at start or end of string.
        """
        return jsii.sinvoke(cls, "stringValue", [json_field, comparison, value])


@jsii.interface(jsii_type="@aws-cdk/aws-logs.IFilterPattern")
class IFilterPattern(jsii.compat.Protocol):
    """Interface for objects that can render themselves to log patterns."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFilterPatternProxy

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        ...


class _IFilterPatternProxy():
    """Interface for objects that can render themselves to log patterns."""
    __jsii_type__ = "@aws-cdk/aws-logs.IFilterPattern"
    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        return jsii.get(self, "logPatternString")


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogGroup")
class ILogGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILogGroupProxy

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of this log group.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """The name of this log group.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(self, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        """Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        """
        ...

    @jsii.member(jsii_name="addStream")
    def add_stream(self, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        """Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        """
        ...

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(self, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        """Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        """
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> aws_cdk.aws_cloudwatch.Metric:
        """Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        return
        :return: A Metric object representing the extracted metric
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Give permissions to write to create and write to streams in this log group.

        :param grantee: -
        """
        ...


class _ILogGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-logs.ILogGroup"
    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of this log group.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "logGroupArn")

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """The name of this log group.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "logGroupName")

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(self, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        """Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        """
        props = MetricFilterOptions(filter_pattern=filter_pattern, metric_name=metric_name, metric_namespace=metric_namespace, default_value=default_value, metric_value=metric_value)

        return jsii.invoke(self, "addMetricFilter", [id, props])

    @jsii.member(jsii_name="addStream")
    def add_stream(self, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        """Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        """
        props = StreamOptions(log_stream_name=log_stream_name)

        return jsii.invoke(self, "addStream", [id, props])

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(self, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        """Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        """
        props = SubscriptionFilterOptions(destination=destination, filter_pattern=filter_pattern)

        return jsii.invoke(self, "addSubscriptionFilter", [id, props])

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> aws_cdk.aws_cloudwatch.Metric:
        """Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        return
        :return: A Metric object representing the extracted metric
        """
        return jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Give permissions to write to create and write to streams in this log group.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogStream")
class ILogStream(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILogStreamProxy

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        """The name of this log stream.

        attribute:
        :attribute:: true
        """
        ...


class _ILogStreamProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-logs.ILogStream"
    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        """The name of this log stream.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "logStreamName")


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogSubscriptionDestination")
class ILogSubscriptionDestination(jsii.compat.Protocol):
    """Interface for classes that can be the destination of a log Subscription."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILogSubscriptionDestinationProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, source_log_group: "ILogGroup") -> "LogSubscriptionDestinationConfig":
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -
        """
        ...


class _ILogSubscriptionDestinationProxy():
    """Interface for classes that can be the destination of a log Subscription."""
    __jsii_type__ = "@aws-cdk/aws-logs.ILogSubscriptionDestination"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, source_log_group: "ILogGroup") -> "LogSubscriptionDestinationConfig":
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -
        """
        return jsii.invoke(self, "bind", [scope, source_log_group])


@jsii.implements(ILogSubscriptionDestination)
class CrossAccountDestination(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CrossAccountDestination"):
    """A new CloudWatch Logs Destination for use in cross-account scenarios.

    CrossAccountDestinations are used to subscribe a Kinesis stream in a
    different account to a CloudWatch Subscription.

    Consumers will hardly ever need to use this class. Instead, directly
    subscribe a Kinesis stream using the integration class in the
    ``@aws-cdk/aws-logs-destinations`` package; if necessary, a
    ``CrossAccountDestination`` will be created automatically.

    resource:
    :resource:: AWS::Logs::Destination
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, role: aws_cdk.aws_iam.IRole, target_arn: str, destination_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param role: The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: The log destination target's ARN.
        :param destination_name: The name of the log destination. Default: Automatically generated
        """
        props = CrossAccountDestinationProps(role=role, target_arn=target_arn, destination_name=destination_name)

        jsii.create(CrossAccountDestination, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """
        :param statement: -
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _source_log_group: "ILogGroup") -> "LogSubscriptionDestinationConfig":
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param _scope: -
        :param _source_log_group: -
        """
        return jsii.invoke(self, "bind", [_scope, _source_log_group])

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> str:
        """The ARN of this CrossAccountDestination object.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "destinationArn")

    @builtins.property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> str:
        """The name of this CrossAccountDestination object.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "destinationName")

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> aws_cdk.aws_iam.PolicyDocument:
        """Policy object of this CrossAccountDestination object."""
        return jsii.get(self, "policyDocument")


@jsii.implements(IFilterPattern)
class JsonPattern(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-logs.JsonPattern"):
    """Base class for patterns that only match JSON log events."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _JsonPatternProxy

    def __init__(self, json_pattern_string: str) -> None:
        """
        :param json_pattern_string: -
        """
        jsii.create(JsonPattern, self, [json_pattern_string])

    @builtins.property
    @jsii.member(jsii_name="jsonPatternString")
    def json_pattern_string(self) -> str:
        return jsii.get(self, "jsonPatternString")

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        return jsii.get(self, "logPatternString")


class _JsonPatternProxy(JsonPattern):
    pass

@jsii.implements(ILogGroup)
class LogGroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.LogGroup"):
    """Define a CloudWatch Log Group."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, log_group_name: typing.Optional[str]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, retention: typing.Optional["RetentionDays"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group_name: Name of the log group. Default: Automatically generated
        :param removal_policy: Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS
        """
        props = LogGroupProps(log_group_name=log_group_name, removal_policy=removal_policy, retention=retention)

        jsii.create(LogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogGroupArn")
    @builtins.classmethod
    def from_log_group_arn(cls, scope: aws_cdk.core.Construct, id: str, log_group_arn: str) -> "ILogGroup":
        """Import an existing LogGroup given its ARN.

        :param scope: -
        :param id: -
        :param log_group_arn: -
        """
        return jsii.sinvoke(cls, "fromLogGroupArn", [scope, id, log_group_arn])

    @jsii.member(jsii_name="fromLogGroupName")
    @builtins.classmethod
    def from_log_group_name(cls, scope: aws_cdk.core.Construct, id: str, log_group_name: str) -> "ILogGroup":
        """Import an existing LogGroup given its name.

        :param scope: -
        :param id: -
        :param log_group_name: -
        """
        return jsii.sinvoke(cls, "fromLogGroupName", [scope, id, log_group_name])

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(self, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        """Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        """
        props = MetricFilterOptions(filter_pattern=filter_pattern, metric_name=metric_name, metric_namespace=metric_namespace, default_value=default_value, metric_value=metric_value)

        return jsii.invoke(self, "addMetricFilter", [id, props])

    @jsii.member(jsii_name="addStream")
    def add_stream(self, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        """Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        """
        props = StreamOptions(log_stream_name=log_stream_name)

        return jsii.invoke(self, "addStream", [id, props])

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(self, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        """Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        """
        props = SubscriptionFilterOptions(destination=destination, filter_pattern=filter_pattern)

        return jsii.invoke(self, "addSubscriptionFilter", [id, props])

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> aws_cdk.aws_cloudwatch.Metric:
        """Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        return
        :return: A Metric object representing the extracted metric
        """
        return jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Give permissions to write to create and write to streams in this log group.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of this log group."""
        return jsii.get(self, "logGroupArn")

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """The name of this log group."""
        return jsii.get(self, "logGroupName")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogGroupProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'removal_policy': 'removalPolicy', 'retention': 'retention'})
class LogGroupProps():
    def __init__(self, *, log_group_name: typing.Optional[str]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, retention: typing.Optional["RetentionDays"]=None):
        """Properties for a LogGroup.

        :param log_group_name: Name of the log group. Default: Automatically generated
        :param removal_policy: Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS
        """
        self._values = {
        }
        if log_group_name is not None: self._values["log_group_name"] = log_group_name
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if retention is not None: self._values["retention"] = retention

    @builtins.property
    def log_group_name(self) -> typing.Optional[str]:
        """Name of the log group.

        default
        :default: Automatically generated
        """
        return self._values.get('log_group_name')

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """Determine the removal policy of this log group.

        Normally you want to retain the log group so you can diagnose issues
        from logs even after a deployment that no longer includes the log group.
        In that case, use the normal date-based retention policy to age out your
        logs.

        default
        :default: RemovalPolicy.Retain
        """
        return self._values.get('removal_policy')

    @builtins.property
    def retention(self) -> typing.Optional["RetentionDays"]:
        """How long, in days, the log contents will be retained.

        To retain all logs, set this value to RetentionDays.INFINITE.

        default
        :default: RetentionDays.TWO_YEARS
        """
        return self._values.get('retention')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ILogStream)
class LogStream(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.LogStream"):
    """Define a Log Stream in a Log Group."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, log_group: "ILogGroup", log_stream_name: typing.Optional[str]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group: The log group to create a log stream for.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain
        """
        props = LogStreamProps(log_group=log_group, log_stream_name=log_stream_name, removal_policy=removal_policy)

        jsii.create(LogStream, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogStreamName")
    @builtins.classmethod
    def from_log_stream_name(cls, scope: aws_cdk.core.Construct, id: str, log_stream_name: str) -> "ILogStream":
        """Import an existing LogGroup.

        :param scope: -
        :param id: -
        :param log_stream_name: -
        """
        return jsii.sinvoke(cls, "fromLogStreamName", [scope, id, log_stream_name])

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        """The name of this log stream."""
        return jsii.get(self, "logStreamName")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogStreamProps", jsii_struct_bases=[], name_mapping={'log_group': 'logGroup', 'log_stream_name': 'logStreamName', 'removal_policy': 'removalPolicy'})
class LogStreamProps():
    def __init__(self, *, log_group: "ILogGroup", log_stream_name: typing.Optional[str]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None):
        """Properties for a LogStream.

        :param log_group: The log group to create a log stream for.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain
        """
        self._values = {
            'log_group': log_group,
        }
        if log_stream_name is not None: self._values["log_stream_name"] = log_stream_name
        if removal_policy is not None: self._values["removal_policy"] = removal_policy

    @builtins.property
    def log_group(self) -> "ILogGroup":
        """The log group to create a log stream for."""
        return self._values.get('log_group')

    @builtins.property
    def log_stream_name(self) -> typing.Optional[str]:
        """The name of the log stream to create.

        The name must be unique within the log group.

        default
        :default: Automatically generated
        """
        return self._values.get('log_stream_name')

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """Determine what happens when the log stream resource is removed from the app.

        Normally you want to retain the log stream so you can diagnose issues from
        logs even after a deployment that no longer includes the log stream.

        The date-based retention policy of your log group will age out the logs
        after a certain time.

        default
        :default: RemovalPolicy.Retain
        """
        return self._values.get('removal_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogSubscriptionDestinationConfig", jsii_struct_bases=[], name_mapping={'arn': 'arn', 'role': 'role'})
class LogSubscriptionDestinationConfig():
    def __init__(self, *, arn: str, role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Properties returned by a Subscription destination.

        :param arn: The ARN of the subscription's destination.
        :param role: The role to assume to write log events to the destination. Default: No role assumed
        """
        self._values = {
            'arn': arn,
        }
        if role is not None: self._values["role"] = role

    @builtins.property
    def arn(self) -> str:
        """The ARN of the subscription's destination."""
        return self._values.get('arn')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role to assume to write log events to the destination.

        default
        :default: No role assumed
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogSubscriptionDestinationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class MetricFilter(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.MetricFilter"):
    """A filter that extracts information from CloudWatch Logs and emits to CloudWatch Metrics."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, log_group: "ILogGroup", filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group: The log group to create the filter on.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        """
        props = MetricFilterProps(log_group=log_group, filter_pattern=filter_pattern, metric_name=metric_name, metric_namespace=metric_namespace, default_value=default_value, metric_value=metric_value)

        jsii.create(MetricFilter, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.MetricFilterOptions", jsii_struct_bases=[], name_mapping={'filter_pattern': 'filterPattern', 'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'default_value': 'defaultValue', 'metric_value': 'metricValue'})
class MetricFilterOptions():
    def __init__(self, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None):
        """Properties for a MetricFilter created from a LogGroup.

        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        """
        self._values = {
            'filter_pattern': filter_pattern,
            'metric_name': metric_name,
            'metric_namespace': metric_namespace,
        }
        if default_value is not None: self._values["default_value"] = default_value
        if metric_value is not None: self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Pattern to search for log events."""
        return self._values.get('filter_pattern')

    @builtins.property
    def metric_name(self) -> str:
        """The name of the metric to emit."""
        return self._values.get('metric_name')

    @builtins.property
    def metric_namespace(self) -> str:
        """The namespace of the metric to emit."""
        return self._values.get('metric_namespace')

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        """The value to emit if the pattern does not match a particular event.

        default
        :default: No metric emitted.
        """
        return self._values.get('default_value')

    @builtins.property
    def metric_value(self) -> typing.Optional[str]:
        """The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        default
        :default: "1"
        """
        return self._values.get('metric_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricFilterOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.MetricFilterProps", jsii_struct_bases=[MetricFilterOptions], name_mapping={'filter_pattern': 'filterPattern', 'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'default_value': 'defaultValue', 'metric_value': 'metricValue', 'log_group': 'logGroup'})
class MetricFilterProps(MetricFilterOptions):
    def __init__(self, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None, log_group: "ILogGroup"):
        """Properties for a MetricFilter.

        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        :param log_group: The log group to create the filter on.
        """
        self._values = {
            'filter_pattern': filter_pattern,
            'metric_name': metric_name,
            'metric_namespace': metric_namespace,
            'log_group': log_group,
        }
        if default_value is not None: self._values["default_value"] = default_value
        if metric_value is not None: self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Pattern to search for log events."""
        return self._values.get('filter_pattern')

    @builtins.property
    def metric_name(self) -> str:
        """The name of the metric to emit."""
        return self._values.get('metric_name')

    @builtins.property
    def metric_namespace(self) -> str:
        """The namespace of the metric to emit."""
        return self._values.get('metric_namespace')

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        """The value to emit if the pattern does not match a particular event.

        default
        :default: No metric emitted.
        """
        return self._values.get('default_value')

    @builtins.property
    def metric_value(self) -> typing.Optional[str]:
        """The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        default
        :default: "1"
        """
        return self._values.get('metric_value')

    @builtins.property
    def log_group(self) -> "ILogGroup":
        """The log group to create the filter on."""
        return self._values.get('log_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-logs.RetentionDays")
class RetentionDays(enum.Enum):
    """How long, in days, the log contents will be retained."""
    ONE_DAY = "ONE_DAY"
    """1 day."""
    THREE_DAYS = "THREE_DAYS"
    """3 days."""
    FIVE_DAYS = "FIVE_DAYS"
    """5 days."""
    ONE_WEEK = "ONE_WEEK"
    """1 week."""
    TWO_WEEKS = "TWO_WEEKS"
    """2 weeks."""
    ONE_MONTH = "ONE_MONTH"
    """1 month."""
    TWO_MONTHS = "TWO_MONTHS"
    """2 months."""
    THREE_MONTHS = "THREE_MONTHS"
    """3 months."""
    FOUR_MONTHS = "FOUR_MONTHS"
    """4 months."""
    FIVE_MONTHS = "FIVE_MONTHS"
    """5 months."""
    SIX_MONTHS = "SIX_MONTHS"
    """6 months."""
    ONE_YEAR = "ONE_YEAR"
    """1 year."""
    THIRTEEN_MONTHS = "THIRTEEN_MONTHS"
    """13 months."""
    EIGHTEEN_MONTHS = "EIGHTEEN_MONTHS"
    """18 months."""
    TWO_YEARS = "TWO_YEARS"
    """2 years."""
    FIVE_YEARS = "FIVE_YEARS"
    """5 years."""
    TEN_YEARS = "TEN_YEARS"
    """10 years."""
    INFINITE = "INFINITE"
    """Retain logs forever."""

@jsii.implements(IFilterPattern)
class SpaceDelimitedTextPattern(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.SpaceDelimitedTextPattern"):
    """Space delimited text pattern."""
    def __init__(self, columns: typing.List[str], restrictions: typing.Mapping[str,typing.List["ColumnRestriction"]]) -> None:
        """
        :param columns: -
        :param restrictions: -
        """
        jsii.create(SpaceDelimitedTextPattern, self, [columns, restrictions])

    @jsii.member(jsii_name="construct")
    @builtins.classmethod
    def construct(cls, columns: typing.List[str]) -> "SpaceDelimitedTextPattern":
        """Construct a new instance of a space delimited text pattern.

        Since this class must be public, we can't rely on the user only creating it through
        the ``LogPattern.spaceDelimited()`` factory function. We must therefore validate the
        argument in the constructor. Since we're returning a copy on every mutation, and we
        don't want to re-validate the same things on every construction, we provide a limited
        set of mutator functions and only validate the new data every time.

        :param columns: -
        """
        return jsii.sinvoke(cls, "construct", [columns])

    @jsii.member(jsii_name="whereNumber")
    def where_number(self, column_name: str, comparison: str, value: jsii.Number) -> "SpaceDelimitedTextPattern":
        """Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -
        """
        return jsii.invoke(self, "whereNumber", [column_name, comparison, value])

    @jsii.member(jsii_name="whereString")
    def where_string(self, column_name: str, comparison: str, value: str) -> "SpaceDelimitedTextPattern":
        """Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -
        """
        return jsii.invoke(self, "whereString", [column_name, comparison, value])

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        return jsii.get(self, "logPatternString")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.StreamOptions", jsii_struct_bases=[], name_mapping={'log_stream_name': 'logStreamName'})
class StreamOptions():
    def __init__(self, *, log_stream_name: typing.Optional[str]=None):
        """Properties for a new LogStream created from a LogGroup.

        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        """
        self._values = {
        }
        if log_stream_name is not None: self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_stream_name(self) -> typing.Optional[str]:
        """The name of the log stream to create.

        The name must be unique within the log group.

        default
        :default: Automatically generated
        """
        return self._values.get('log_stream_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StreamOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class SubscriptionFilter(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.SubscriptionFilter"):
    """A new Subscription on a CloudWatch log group."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, log_group: "ILogGroup", destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> None:
        """
        :param scope: -
        :param id: -
        :param log_group: The log group to create the subscription on.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        """
        props = SubscriptionFilterProps(log_group=log_group, destination=destination, filter_pattern=filter_pattern)

        jsii.create(SubscriptionFilter, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.SubscriptionFilterOptions", jsii_struct_bases=[], name_mapping={'destination': 'destination', 'filter_pattern': 'filterPattern'})
class SubscriptionFilterOptions():
    def __init__(self, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern"):
        """Properties for a new SubscriptionFilter created from a LogGroup.

        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        """
        self._values = {
            'destination': destination,
            'filter_pattern': filter_pattern,
        }

    @builtins.property
    def destination(self) -> "ILogSubscriptionDestination":
        """The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.
        """
        return self._values.get('destination')

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Log events matching this pattern will be sent to the destination."""
        return self._values.get('filter_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionFilterOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.SubscriptionFilterProps", jsii_struct_bases=[SubscriptionFilterOptions], name_mapping={'destination': 'destination', 'filter_pattern': 'filterPattern', 'log_group': 'logGroup'})
class SubscriptionFilterProps(SubscriptionFilterOptions):
    def __init__(self, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern", log_group: "ILogGroup"):
        """Properties for a SubscriptionFilter.

        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        :param log_group: The log group to create the subscription on.
        """
        self._values = {
            'destination': destination,
            'filter_pattern': filter_pattern,
            'log_group': log_group,
        }

    @builtins.property
    def destination(self) -> "ILogSubscriptionDestination":
        """The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.
        """
        return self._values.get('destination')

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Log events matching this pattern will be sent to the destination."""
        return self._values.get('filter_pattern')

    @builtins.property
    def log_group(self) -> "ILogGroup":
        """The log group to create the subscription on."""
        return self._values.get('log_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CfnDestination", "CfnDestinationProps", "CfnLogGroup", "CfnLogGroupProps", "CfnLogStream", "CfnLogStreamProps", "CfnMetricFilter", "CfnMetricFilterProps", "CfnSubscriptionFilter", "CfnSubscriptionFilterProps", "ColumnRestriction", "CrossAccountDestination", "CrossAccountDestinationProps", "FilterPattern", "IFilterPattern", "ILogGroup", "ILogStream", "ILogSubscriptionDestination", "JsonPattern", "LogGroup", "LogGroupProps", "LogStream", "LogStreamProps", "LogSubscriptionDestinationConfig", "MetricFilter", "MetricFilterOptions", "MetricFilterProps", "RetentionDays", "SpaceDelimitedTextPattern", "StreamOptions", "SubscriptionFilter", "SubscriptionFilterOptions", "SubscriptionFilterProps", "__jsii_assembly__"]

publication.publish()
