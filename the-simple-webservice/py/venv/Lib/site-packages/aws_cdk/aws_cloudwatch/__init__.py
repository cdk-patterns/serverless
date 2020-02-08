"""
## Amazon CloudWatch Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

## Metric objects

Metric objects represent a metric that is emitted by AWS services or your own
application, such as `CPUUsage`, `FailureCount` or `Bandwidth`.

Metric objects can be constructed directly or are exposed by resources as
attributes. Resources that expose metrics will have functions that look
like `metricXxx()` which will return a Metric object, initialized with defaults
that make sense.

For example, `lambda.Function` objects have the `fn.metricErrors()` method, which
represents the amount of errors reported by that Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
errors = fn.metric_errors()
```

### Instantiating a new Metric object

If you want to reference a metric that is not yet exposed by an existing construct,
you can instantiate a `Metric` object to represent it. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
metric = Metric(
    namespace="MyNamespace",
    metric_name="MyMetric",
    dimensions={
        "ProcessingStep": "Download"
    }
)
```

### Metric Math

Math expressions are supported by instantiating the `MathExpression` class.
For example, a math expression that sums two other metrics looks like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
all_problems = MathExpression(
    expression="errors + faults",
    using_metrics={
        "errors": my_construct.metric_errors(),
        "faults": my_construct.metric_faults()
    }
)
```

You can use `MathExpression` objects like any other metric, including using
them in other math expressions:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
problem_percentage = MathExpression(
    expression="(problems / invocations) * 100",
    using_metrics={
        "problems": all_problems,
        "invocations": my_construct.metric_invocations()
    }
)
```

### Aggregation

To graph or alarm on metrics you must aggregate them first, using a function
like `Average` or a percentile function like `P99`. By default, most Metric objects
returned by CDK libraries will be configured as `Average` over `300 seconds` (5 minutes).
The exception is if the metric represents a count of discrete events, such as
failures. In that case, the Metric object will be configured as `Sum` over `300 seconds`, i.e. it represents the number of times that event occurred over the
time period.

If you want to change the default aggregation of the Metric object (for example,
the function or the period), you can do so by passing additional parameters
to the metric function call:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
minute_error_rate = fn.metric_errors(
    statistic="avg",
    period=Duration.minutes(1),
    label="Lambda failure rate"
)
```

This function also allows changing the metric label or color (which will be
useful when embedding them in graphs, see below).

> Rates versus Sums
>
> The reason for using `Sum` to count discrete events is that *some* events are
> emitted as either `0` or `1` (for example `Errors` for a Lambda) and some are
> only emitted as `1` (for example `NumberOfMessagesPublished` for an SNS
> topic).
>
> In case `0`-metrics are emitted, it makes sense to take the `Average` of this
> metric: the result will be the fraction of errors over all executions.
>
> If `0`-metrics are not emitted, the `Average` will always be equal to `1`,
> and not be very useful.
>
> In order to simplify the mental model of `Metric` objects, we default to
> aggregating using `Sum`, which will be the same for both metrics types. If you
> happen to know the Metric you want to alarm on makes sense as a rate
> (`Average`) you can always choose to change the statistic.

## Alarms

Alarms can be created on metrics in one of two ways. Either create an `Alarm`
object, passing the `Metric` object to set the alarm on:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Alarm(self, "Alarm",
    metric=fn.metric_errors(),
    threshold=100,
    evaluation_periods=2
)
```

Alternatively, you can call `metric.createAlarm()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn.metric_errors().create_alarm(self, "Alarm",
    threshold=100,
    evaluation_periods=2
)
```

The most important properties to set while creating an Alarms are:

* `threshold`: the value to compare the metric against.
* `comparisonOperator`: the comparison operation to use, defaults to `metric >= threshold`.
* `evaluationPeriods`: how many consecutive periods the metric has to be
  breaching the the threshold for the alarm to trigger.

### A note on units

In CloudWatch, Metrics datums are emitted with units, such as `seconds` or
`bytes`. When `Metric` objects are given a `unit` attribute, it will be used to
*filter* the stream of metric datums for datums emitted using the same `unit`
attribute.

In particular, the `unit` field is *not* used to rescale datums or alarm threshold
values (for example, it cannot be used to specify an alarm threshold in
*Megabytes* if the metric stream is being emitted as *bytes*).

You almost certainly don't want to specify the `unit` property when creating
`Metric` objects (which will retrieve all datums regardless of their unit),
unless you have very specific requirements. Note that in any case, CloudWatch
only supports filtering by `unit` for Alarms, not in Dashboard graphs.

Please see the following GitHub issue for a discussion on real unit
calculations in CDK: https://github.com/aws/aws-cdk/issues/5595

## Dashboards

Dashboards are set of Widgets stored server-side which can be accessed quickly
from the AWS console. Available widgets are graphs of a metric over time, the
current value of a metric, or a static piece of Markdown which explains what the
graphs mean.

The following widgets are available:

* `GraphWidget` -- shows any number of metrics on both the left and right
  vertical axes.
* `AlarmWidget` -- shows the graph and alarm line for a single alarm.
* `SingleValueWidget` -- shows the current value of a set of metrics.
* `TextWidget` -- shows some static Markdown.

### Graph widget

A graph widget can display any number of metrics on either the `left` or
`right` vertical axis:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(GraphWidget(
    title="Executions vs error rate",

    left=[execution_count_metric],

    right=[error_count_metric.with(
        statistic="average",
        label="Error rate",
        color="00FF00"
    )]
))
```

### Alarm widget

An alarm widget shows the graph and the alarm line of a single alarm:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(AlarmWidget(
    title="Errors",
    alarm=error_alarm
))
```

### Single value widget

A single-value widget shows the latest value of a set of metrics (as opposed
to a graph of the value over time):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(SingleValueWidget(
    metrics=[visitor_count, purchase_count]
))
```

### Text widget

A text widget shows an arbitrary piece of MarkDown. Use this to add explanations
to your dashboard:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(TextWidget(
    markdown="# Key Performance Indicators"
))
```

### Dashboard Layout

The widgets on a dashboard are visually laid out in a grid that is 24 columns
wide. Normally you specify X and Y coordinates for the widgets on a Dashboard,
but because this is inconvenient to do manually, the library contains a simple
layout system to help you lay out your dashboards the way you want them to.

Widgets have a `width` and `height` property, and they will be automatically
laid out either horizontally or vertically stacked to fill out the available
space.

Widgets are added to a Dashboard by calling `add(widget1, widget2, ...)`.
Widgets given in the same call will be laid out horizontally. Widgets given
in different calls will be laid out vertically. To make more complex layouts,
you can use the following widgets to pack widgets together in different ways:

* `Column`: stack two or more widgets vertically.
* `Row`: lay out two or more widgets horizontally.
* `Spacer`: take up empty space
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_iam
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudwatch", "1.23.0", __name__, "aws-cloudwatch@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmActionConfig", jsii_struct_bases=[], name_mapping={'alarm_action_arn': 'alarmActionArn'})
class AlarmActionConfig():
    def __init__(self, *, alarm_action_arn: str):
        """Properties for an alarm action.

        :param alarm_action_arn: Return the ARN that should be used for a CloudWatch Alarm action.
        """
        self._values = {
            'alarm_action_arn': alarm_action_arn,
        }

    @builtins.property
    def alarm_action_arn(self) -> str:
        """Return the ARN that should be used for a CloudWatch Alarm action."""
        return self._values.get('alarm_action_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlarmActionConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAlarm(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm"):
    """A CloudFormation ``AWS::CloudWatch::Alarm``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudWatch::Alarm
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comparison_operator: str, evaluation_periods: jsii.Number, actions_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, alarm_actions: typing.Optional[typing.List[str]]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DimensionProperty"]]]]]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, extended_statistic: typing.Optional[str]=None, insufficient_data_actions: typing.Optional[typing.List[str]]=None, metric_name: typing.Optional[str]=None, metrics: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricDataQueryProperty"]]]]]=None, namespace: typing.Optional[str]=None, ok_actions: typing.Optional[typing.List[str]]=None, period: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, threshold: typing.Optional[jsii.Number]=None, threshold_metric_id: typing.Optional[str]=None, treat_missing_data: typing.Optional[str]=None, unit: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudWatch::Alarm``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param comparison_operator: ``AWS::CloudWatch::Alarm.ComparisonOperator``.
        :param evaluation_periods: ``AWS::CloudWatch::Alarm.EvaluationPeriods``.
        :param actions_enabled: ``AWS::CloudWatch::Alarm.ActionsEnabled``.
        :param alarm_actions: ``AWS::CloudWatch::Alarm.AlarmActions``.
        :param alarm_description: ``AWS::CloudWatch::Alarm.AlarmDescription``.
        :param alarm_name: ``AWS::CloudWatch::Alarm.AlarmName``.
        :param datapoints_to_alarm: ``AWS::CloudWatch::Alarm.DatapointsToAlarm``.
        :param dimensions: ``AWS::CloudWatch::Alarm.Dimensions``.
        :param evaluate_low_sample_count_percentile: ``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.
        :param extended_statistic: ``AWS::CloudWatch::Alarm.ExtendedStatistic``.
        :param insufficient_data_actions: ``AWS::CloudWatch::Alarm.InsufficientDataActions``.
        :param metric_name: ``AWS::CloudWatch::Alarm.MetricName``.
        :param metrics: ``AWS::CloudWatch::Alarm.Metrics``.
        :param namespace: ``AWS::CloudWatch::Alarm.Namespace``.
        :param ok_actions: ``AWS::CloudWatch::Alarm.OKActions``.
        :param period: ``AWS::CloudWatch::Alarm.Period``.
        :param statistic: ``AWS::CloudWatch::Alarm.Statistic``.
        :param threshold: ``AWS::CloudWatch::Alarm.Threshold``.
        :param threshold_metric_id: ``AWS::CloudWatch::Alarm.ThresholdMetricId``.
        :param treat_missing_data: ``AWS::CloudWatch::Alarm.TreatMissingData``.
        :param unit: ``AWS::CloudWatch::Alarm.Unit``.
        """
        props = CfnAlarmProps(comparison_operator=comparison_operator, evaluation_periods=evaluation_periods, actions_enabled=actions_enabled, alarm_actions=alarm_actions, alarm_description=alarm_description, alarm_name=alarm_name, datapoints_to_alarm=datapoints_to_alarm, dimensions=dimensions, evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile, extended_statistic=extended_statistic, insufficient_data_actions=insufficient_data_actions, metric_name=metric_name, metrics=metrics, namespace=namespace, ok_actions=ok_actions, period=period, statistic=statistic, threshold=threshold, threshold_metric_id=threshold_metric_id, treat_missing_data=treat_missing_data, unit=unit)

        jsii.create(CfnAlarm, self, [scope, id, props])

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
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> str:
        """``AWS::CloudWatch::Alarm.ComparisonOperator``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
        """
        return jsii.get(self, "comparisonOperator")

    @comparison_operator.setter
    def comparison_operator(self, value: str):
        jsii.set(self, "comparisonOperator", value)

    @builtins.property
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        """``AWS::CloudWatch::Alarm.EvaluationPeriods``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
        """
        return jsii.get(self, "evaluationPeriods")

    @evaluation_periods.setter
    def evaluation_periods(self, value: jsii.Number):
        jsii.set(self, "evaluationPeriods", value)

    @builtins.property
    @jsii.member(jsii_name="actionsEnabled")
    def actions_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CloudWatch::Alarm.ActionsEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-actionsenabled
        """
        return jsii.get(self, "actionsEnabled")

    @actions_enabled.setter
    def actions_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "actionsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="alarmActions")
    def alarm_actions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudWatch::Alarm.AlarmActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmactions
        """
        return jsii.get(self, "alarmActions")

    @alarm_actions.setter
    def alarm_actions(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "alarmActions", value)

    @builtins.property
    @jsii.member(jsii_name="alarmDescription")
    def alarm_description(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.AlarmDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmdescription
        """
        return jsii.get(self, "alarmDescription")

    @alarm_description.setter
    def alarm_description(self, value: typing.Optional[str]):
        jsii.set(self, "alarmDescription", value)

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.AlarmName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmname
        """
        return jsii.get(self, "alarmName")

    @alarm_name.setter
    def alarm_name(self, value: typing.Optional[str]):
        jsii.set(self, "alarmName", value)

    @builtins.property
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.DatapointsToAlarm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        """
        return jsii.get(self, "datapointsToAlarm")

    @datapoints_to_alarm.setter
    def datapoints_to_alarm(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "datapointsToAlarm", value)

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DimensionProperty"]]]]]:
        """``AWS::CloudWatch::Alarm.Dimensions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dimension
        """
        return jsii.get(self, "dimensions")

    @dimensions.setter
    def dimensions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DimensionProperty"]]]]]):
        jsii.set(self, "dimensions", value)

    @builtins.property
    @jsii.member(jsii_name="evaluateLowSampleCountPercentile")
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
        """
        return jsii.get(self, "evaluateLowSampleCountPercentile")

    @evaluate_low_sample_count_percentile.setter
    def evaluate_low_sample_count_percentile(self, value: typing.Optional[str]):
        jsii.set(self, "evaluateLowSampleCountPercentile", value)

    @builtins.property
    @jsii.member(jsii_name="extendedStatistic")
    def extended_statistic(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.ExtendedStatistic``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
        """
        return jsii.get(self, "extendedStatistic")

    @extended_statistic.setter
    def extended_statistic(self, value: typing.Optional[str]):
        jsii.set(self, "extendedStatistic", value)

    @builtins.property
    @jsii.member(jsii_name="insufficientDataActions")
    def insufficient_data_actions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudWatch::Alarm.InsufficientDataActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
        """
        return jsii.get(self, "insufficientDataActions")

    @insufficient_data_actions.setter
    def insufficient_data_actions(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "insufficientDataActions", value)

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-metricname
        """
        return jsii.get(self, "metricName")

    @metric_name.setter
    def metric_name(self, value: typing.Optional[str]):
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricDataQueryProperty"]]]]]:
        """``AWS::CloudWatch::Alarm.Metrics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-metrics
        """
        return jsii.get(self, "metrics")

    @metrics.setter
    def metrics(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricDataQueryProperty"]]]]]):
        jsii.set(self, "metrics", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.Namespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-namespace
        """
        return jsii.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: typing.Optional[str]):
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="okActions")
    def ok_actions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudWatch::Alarm.OKActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-okactions
        """
        return jsii.get(self, "okActions")

    @ok_actions.setter
    def ok_actions(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "okActions", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Period``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-period
        """
        return jsii.get(self, "period")

    @period.setter
    def period(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.Statistic``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-statistic
        """
        return jsii.get(self, "statistic")

    @statistic.setter
    def statistic(self, value: typing.Optional[str]):
        jsii.set(self, "statistic", value)

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Threshold``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-threshold
        """
        return jsii.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "threshold", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdMetricId")
    def threshold_metric_id(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.ThresholdMetricId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dynamic-threshold
        """
        return jsii.get(self, "thresholdMetricId")

    @threshold_metric_id.setter
    def threshold_metric_id(self, value: typing.Optional[str]):
        jsii.set(self, "thresholdMetricId", value)

    @builtins.property
    @jsii.member(jsii_name="treatMissingData")
    def treat_missing_data(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.TreatMissingData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
        """
        return jsii.get(self, "treatMissingData")

    @treat_missing_data.setter
    def treat_missing_data(self, value: typing.Optional[str]):
        jsii.set(self, "treatMissingData", value)

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.Unit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-unit
        """
        return jsii.get(self, "unit")

    @unit.setter
    def unit(self, value: typing.Optional[str]):
        jsii.set(self, "unit", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.DimensionProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class DimensionProperty():
        def __init__(self, *, name: str, value: str):
            """
            :param name: ``CfnAlarm.DimensionProperty.Name``.
            :param value: ``CfnAlarm.DimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnAlarm.DimensionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> str:
            """``CfnAlarm.DimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DimensionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricDataQueryProperty", jsii_struct_bases=[], name_mapping={'id': 'id', 'expression': 'expression', 'label': 'label', 'metric_stat': 'metricStat', 'return_data': 'returnData'})
    class MetricDataQueryProperty():
        def __init__(self, *, id: str, expression: typing.Optional[str]=None, label: typing.Optional[str]=None, metric_stat: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAlarm.MetricStatProperty"]]]=None, return_data: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param id: ``CfnAlarm.MetricDataQueryProperty.Id``.
            :param expression: ``CfnAlarm.MetricDataQueryProperty.Expression``.
            :param label: ``CfnAlarm.MetricDataQueryProperty.Label``.
            :param metric_stat: ``CfnAlarm.MetricDataQueryProperty.MetricStat``.
            :param return_data: ``CfnAlarm.MetricDataQueryProperty.ReturnData``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html
            """
            self._values = {
                'id': id,
            }
            if expression is not None: self._values["expression"] = expression
            if label is not None: self._values["label"] = label
            if metric_stat is not None: self._values["metric_stat"] = metric_stat
            if return_data is not None: self._values["return_data"] = return_data

        @builtins.property
        def id(self) -> str:
            """``CfnAlarm.MetricDataQueryProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-id
            """
            return self._values.get('id')

        @builtins.property
        def expression(self) -> typing.Optional[str]:
            """``CfnAlarm.MetricDataQueryProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-expression
            """
            return self._values.get('expression')

        @builtins.property
        def label(self) -> typing.Optional[str]:
            """``CfnAlarm.MetricDataQueryProperty.Label``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-label
            """
            return self._values.get('label')

        @builtins.property
        def metric_stat(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAlarm.MetricStatProperty"]]]:
            """``CfnAlarm.MetricDataQueryProperty.MetricStat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-metricstat
            """
            return self._values.get('metric_stat')

        @builtins.property
        def return_data(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnAlarm.MetricDataQueryProperty.ReturnData``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-returndata
            """
            return self._values.get('return_data')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricDataQueryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricProperty", jsii_struct_bases=[], name_mapping={'dimensions': 'dimensions', 'metric_name': 'metricName', 'namespace': 'namespace'})
    class MetricProperty():
        def __init__(self, *, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]]]=None, metric_name: typing.Optional[str]=None, namespace: typing.Optional[str]=None):
            """
            :param dimensions: ``CfnAlarm.MetricProperty.Dimensions``.
            :param metric_name: ``CfnAlarm.MetricProperty.MetricName``.
            :param namespace: ``CfnAlarm.MetricProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html
            """
            self._values = {
            }
            if dimensions is not None: self._values["dimensions"] = dimensions
            if metric_name is not None: self._values["metric_name"] = metric_name
            if namespace is not None: self._values["namespace"] = namespace

        @builtins.property
        def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]]]:
            """``CfnAlarm.MetricProperty.Dimensions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-dimensions
            """
            return self._values.get('dimensions')

        @builtins.property
        def metric_name(self) -> typing.Optional[str]:
            """``CfnAlarm.MetricProperty.MetricName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-metricname
            """
            return self._values.get('metric_name')

        @builtins.property
        def namespace(self) -> typing.Optional[str]:
            """``CfnAlarm.MetricProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-namespace
            """
            return self._values.get('namespace')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricStatProperty", jsii_struct_bases=[], name_mapping={'metric': 'metric', 'period': 'period', 'stat': 'stat', 'unit': 'unit'})
    class MetricStatProperty():
        def __init__(self, *, metric: typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricProperty"], period: jsii.Number, stat: str, unit: typing.Optional[str]=None):
            """
            :param metric: ``CfnAlarm.MetricStatProperty.Metric``.
            :param period: ``CfnAlarm.MetricStatProperty.Period``.
            :param stat: ``CfnAlarm.MetricStatProperty.Stat``.
            :param unit: ``CfnAlarm.MetricStatProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html
            """
            self._values = {
                'metric': metric,
                'period': period,
                'stat': stat,
            }
            if unit is not None: self._values["unit"] = unit

        @builtins.property
        def metric(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricProperty"]:
            """``CfnAlarm.MetricStatProperty.Metric``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-metric
            """
            return self._values.get('metric')

        @builtins.property
        def period(self) -> jsii.Number:
            """``CfnAlarm.MetricStatProperty.Period``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-period
            """
            return self._values.get('period')

        @builtins.property
        def stat(self) -> str:
            """``CfnAlarm.MetricStatProperty.Stat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-stat
            """
            return self._values.get('stat')

        @builtins.property
        def unit(self) -> typing.Optional[str]:
            """``CfnAlarm.MetricStatProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-unit
            """
            return self._values.get('unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricStatProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarmProps", jsii_struct_bases=[], name_mapping={'comparison_operator': 'comparisonOperator', 'evaluation_periods': 'evaluationPeriods', 'actions_enabled': 'actionsEnabled', 'alarm_actions': 'alarmActions', 'alarm_description': 'alarmDescription', 'alarm_name': 'alarmName', 'datapoints_to_alarm': 'datapointsToAlarm', 'dimensions': 'dimensions', 'evaluate_low_sample_count_percentile': 'evaluateLowSampleCountPercentile', 'extended_statistic': 'extendedStatistic', 'insufficient_data_actions': 'insufficientDataActions', 'metric_name': 'metricName', 'metrics': 'metrics', 'namespace': 'namespace', 'ok_actions': 'okActions', 'period': 'period', 'statistic': 'statistic', 'threshold': 'threshold', 'threshold_metric_id': 'thresholdMetricId', 'treat_missing_data': 'treatMissingData', 'unit': 'unit'})
class CfnAlarmProps():
    def __init__(self, *, comparison_operator: str, evaluation_periods: jsii.Number, actions_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, alarm_actions: typing.Optional[typing.List[str]]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]]]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, extended_statistic: typing.Optional[str]=None, insufficient_data_actions: typing.Optional[typing.List[str]]=None, metric_name: typing.Optional[str]=None, metrics: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricDataQueryProperty"]]]]]=None, namespace: typing.Optional[str]=None, ok_actions: typing.Optional[typing.List[str]]=None, period: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, threshold: typing.Optional[jsii.Number]=None, threshold_metric_id: typing.Optional[str]=None, treat_missing_data: typing.Optional[str]=None, unit: typing.Optional[str]=None):
        """Properties for defining a ``AWS::CloudWatch::Alarm``.

        :param comparison_operator: ``AWS::CloudWatch::Alarm.ComparisonOperator``.
        :param evaluation_periods: ``AWS::CloudWatch::Alarm.EvaluationPeriods``.
        :param actions_enabled: ``AWS::CloudWatch::Alarm.ActionsEnabled``.
        :param alarm_actions: ``AWS::CloudWatch::Alarm.AlarmActions``.
        :param alarm_description: ``AWS::CloudWatch::Alarm.AlarmDescription``.
        :param alarm_name: ``AWS::CloudWatch::Alarm.AlarmName``.
        :param datapoints_to_alarm: ``AWS::CloudWatch::Alarm.DatapointsToAlarm``.
        :param dimensions: ``AWS::CloudWatch::Alarm.Dimensions``.
        :param evaluate_low_sample_count_percentile: ``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.
        :param extended_statistic: ``AWS::CloudWatch::Alarm.ExtendedStatistic``.
        :param insufficient_data_actions: ``AWS::CloudWatch::Alarm.InsufficientDataActions``.
        :param metric_name: ``AWS::CloudWatch::Alarm.MetricName``.
        :param metrics: ``AWS::CloudWatch::Alarm.Metrics``.
        :param namespace: ``AWS::CloudWatch::Alarm.Namespace``.
        :param ok_actions: ``AWS::CloudWatch::Alarm.OKActions``.
        :param period: ``AWS::CloudWatch::Alarm.Period``.
        :param statistic: ``AWS::CloudWatch::Alarm.Statistic``.
        :param threshold: ``AWS::CloudWatch::Alarm.Threshold``.
        :param threshold_metric_id: ``AWS::CloudWatch::Alarm.ThresholdMetricId``.
        :param treat_missing_data: ``AWS::CloudWatch::Alarm.TreatMissingData``.
        :param unit: ``AWS::CloudWatch::Alarm.Unit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
        """
        self._values = {
            'comparison_operator': comparison_operator,
            'evaluation_periods': evaluation_periods,
        }
        if actions_enabled is not None: self._values["actions_enabled"] = actions_enabled
        if alarm_actions is not None: self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None: self._values["alarm_description"] = alarm_description
        if alarm_name is not None: self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None: self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if dimensions is not None: self._values["dimensions"] = dimensions
        if evaluate_low_sample_count_percentile is not None: self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if extended_statistic is not None: self._values["extended_statistic"] = extended_statistic
        if insufficient_data_actions is not None: self._values["insufficient_data_actions"] = insufficient_data_actions
        if metric_name is not None: self._values["metric_name"] = metric_name
        if metrics is not None: self._values["metrics"] = metrics
        if namespace is not None: self._values["namespace"] = namespace
        if ok_actions is not None: self._values["ok_actions"] = ok_actions
        if period is not None: self._values["period"] = period
        if statistic is not None: self._values["statistic"] = statistic
        if threshold is not None: self._values["threshold"] = threshold
        if threshold_metric_id is not None: self._values["threshold_metric_id"] = threshold_metric_id
        if treat_missing_data is not None: self._values["treat_missing_data"] = treat_missing_data
        if unit is not None: self._values["unit"] = unit

    @builtins.property
    def comparison_operator(self) -> str:
        """``AWS::CloudWatch::Alarm.ComparisonOperator``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
        """
        return self._values.get('comparison_operator')

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        """``AWS::CloudWatch::Alarm.EvaluationPeriods``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
        """
        return self._values.get('evaluation_periods')

    @builtins.property
    def actions_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CloudWatch::Alarm.ActionsEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-actionsenabled
        """
        return self._values.get('actions_enabled')

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudWatch::Alarm.AlarmActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmactions
        """
        return self._values.get('alarm_actions')

    @builtins.property
    def alarm_description(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.AlarmDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmdescription
        """
        return self._values.get('alarm_description')

    @builtins.property
    def alarm_name(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.AlarmName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmname
        """
        return self._values.get('alarm_name')

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.DatapointsToAlarm``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        """
        return self._values.get('datapoints_to_alarm')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]]]:
        """``AWS::CloudWatch::Alarm.Dimensions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dimension
        """
        return self._values.get('dimensions')

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
        """
        return self._values.get('evaluate_low_sample_count_percentile')

    @builtins.property
    def extended_statistic(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.ExtendedStatistic``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
        """
        return self._values.get('extended_statistic')

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudWatch::Alarm.InsufficientDataActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
        """
        return self._values.get('insufficient_data_actions')

    @builtins.property
    def metric_name(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-metricname
        """
        return self._values.get('metric_name')

    @builtins.property
    def metrics(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricDataQueryProperty"]]]]]:
        """``AWS::CloudWatch::Alarm.Metrics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-metrics
        """
        return self._values.get('metrics')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.Namespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-namespace
        """
        return self._values.get('namespace')

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CloudWatch::Alarm.OKActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-okactions
        """
        return self._values.get('ok_actions')

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Period``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-period
        """
        return self._values.get('period')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.Statistic``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-statistic
        """
        return self._values.get('statistic')

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Threshold``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-threshold
        """
        return self._values.get('threshold')

    @builtins.property
    def threshold_metric_id(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.ThresholdMetricId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dynamic-threshold
        """
        return self._values.get('threshold_metric_id')

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.TreatMissingData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
        """
        return self._values.get('treat_missing_data')

    @builtins.property
    def unit(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Alarm.Unit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-unit
        """
        return self._values.get('unit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAlarmProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAnomalyDetector(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector"):
    """A CloudFormation ``AWS::CloudWatch::AnomalyDetector``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudWatch::AnomalyDetector
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, metric_name: str, namespace: str, stat: str, configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConfigurationProperty"]]]=None, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DimensionProperty"]]]]]=None) -> None:
        """Create a new ``AWS::CloudWatch::AnomalyDetector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param metric_name: ``AWS::CloudWatch::AnomalyDetector.MetricName``.
        :param namespace: ``AWS::CloudWatch::AnomalyDetector.Namespace``.
        :param stat: ``AWS::CloudWatch::AnomalyDetector.Stat``.
        :param configuration: ``AWS::CloudWatch::AnomalyDetector.Configuration``.
        :param dimensions: ``AWS::CloudWatch::AnomalyDetector.Dimensions``.
        """
        props = CfnAnomalyDetectorProps(metric_name=metric_name, namespace=namespace, stat=stat, configuration=configuration, dimensions=dimensions)

        jsii.create(CfnAnomalyDetector, self, [scope, id, props])

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
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> str:
        """``AWS::CloudWatch::AnomalyDetector.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        """
        return jsii.get(self, "metricName")

    @metric_name.setter
    def metric_name(self, value: str):
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> str:
        """``AWS::CloudWatch::AnomalyDetector.Namespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        """
        return jsii.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: str):
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="stat")
    def stat(self) -> str:
        """``AWS::CloudWatch::AnomalyDetector.Stat``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        """
        return jsii.get(self, "stat")

    @stat.setter
    def stat(self, value: str):
        jsii.set(self, "stat", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConfigurationProperty"]]]:
        """``AWS::CloudWatch::AnomalyDetector.Configuration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        """
        return jsii.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConfigurationProperty"]]]):
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DimensionProperty"]]]]]:
        """``AWS::CloudWatch::AnomalyDetector.Dimensions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        """
        return jsii.get(self, "dimensions")

    @dimensions.setter
    def dimensions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DimensionProperty"]]]]]):
        jsii.set(self, "dimensions", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector.ConfigurationProperty", jsii_struct_bases=[], name_mapping={'excluded_time_ranges': 'excludedTimeRanges', 'metric_time_zone': 'metricTimeZone'})
    class ConfigurationProperty():
        def __init__(self, *, excluded_time_ranges: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.RangeProperty"]]]]]=None, metric_time_zone: typing.Optional[str]=None):
            """
            :param excluded_time_ranges: ``CfnAnomalyDetector.ConfigurationProperty.ExcludedTimeRanges``.
            :param metric_time_zone: ``CfnAnomalyDetector.ConfigurationProperty.MetricTimeZone``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html
            """
            self._values = {
            }
            if excluded_time_ranges is not None: self._values["excluded_time_ranges"] = excluded_time_ranges
            if metric_time_zone is not None: self._values["metric_time_zone"] = metric_time_zone

        @builtins.property
        def excluded_time_ranges(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.RangeProperty"]]]]]:
            """``CfnAnomalyDetector.ConfigurationProperty.ExcludedTimeRanges``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-excludedtimeranges
            """
            return self._values.get('excluded_time_ranges')

        @builtins.property
        def metric_time_zone(self) -> typing.Optional[str]:
            """``CfnAnomalyDetector.ConfigurationProperty.MetricTimeZone``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-metrictimezone
            """
            return self._values.get('metric_time_zone')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector.DimensionProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class DimensionProperty():
        def __init__(self, *, name: str, value: str):
            """
            :param name: ``CfnAnomalyDetector.DimensionProperty.Name``.
            :param value: ``CfnAnomalyDetector.DimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnAnomalyDetector.DimensionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> str:
            """``CfnAnomalyDetector.DimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DimensionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector.RangeProperty", jsii_struct_bases=[], name_mapping={'end_time': 'endTime', 'start_time': 'startTime'})
    class RangeProperty():
        def __init__(self, *, end_time: str, start_time: str):
            """
            :param end_time: ``CfnAnomalyDetector.RangeProperty.EndTime``.
            :param start_time: ``CfnAnomalyDetector.RangeProperty.StartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html
            """
            self._values = {
                'end_time': end_time,
                'start_time': start_time,
            }

        @builtins.property
        def end_time(self) -> str:
            """``CfnAnomalyDetector.RangeProperty.EndTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-endtime
            """
            return self._values.get('end_time')

        @builtins.property
        def start_time(self) -> str:
            """``CfnAnomalyDetector.RangeProperty.StartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-starttime
            """
            return self._values.get('start_time')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RangeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetectorProps", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'namespace': 'namespace', 'stat': 'stat', 'configuration': 'configuration', 'dimensions': 'dimensions'})
class CfnAnomalyDetectorProps():
    def __init__(self, *, metric_name: str, namespace: str, stat: str, configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAnomalyDetector.ConfigurationProperty"]]]=None, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.DimensionProperty"]]]]]=None):
        """Properties for defining a ``AWS::CloudWatch::AnomalyDetector``.

        :param metric_name: ``AWS::CloudWatch::AnomalyDetector.MetricName``.
        :param namespace: ``AWS::CloudWatch::AnomalyDetector.Namespace``.
        :param stat: ``AWS::CloudWatch::AnomalyDetector.Stat``.
        :param configuration: ``AWS::CloudWatch::AnomalyDetector.Configuration``.
        :param dimensions: ``AWS::CloudWatch::AnomalyDetector.Dimensions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
        """
        self._values = {
            'metric_name': metric_name,
            'namespace': namespace,
            'stat': stat,
        }
        if configuration is not None: self._values["configuration"] = configuration
        if dimensions is not None: self._values["dimensions"] = dimensions

    @builtins.property
    def metric_name(self) -> str:
        """``AWS::CloudWatch::AnomalyDetector.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        """
        return self._values.get('metric_name')

    @builtins.property
    def namespace(self) -> str:
        """``AWS::CloudWatch::AnomalyDetector.Namespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        """
        return self._values.get('namespace')

    @builtins.property
    def stat(self) -> str:
        """``AWS::CloudWatch::AnomalyDetector.Stat``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        """
        return self._values.get('stat')

    @builtins.property
    def configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAnomalyDetector.ConfigurationProperty"]]]:
        """``AWS::CloudWatch::AnomalyDetector.Configuration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        """
        return self._values.get('configuration')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.DimensionProperty"]]]]]:
        """``AWS::CloudWatch::AnomalyDetector.Dimensions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        """
        return self._values.get('dimensions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAnomalyDetectorProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDashboard(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboard"):
    """A CloudFormation ``AWS::CloudWatch::Dashboard``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudWatch::Dashboard
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, dashboard_body: str, dashboard_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudWatch::Dashboard``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dashboard_body: ``AWS::CloudWatch::Dashboard.DashboardBody``.
        :param dashboard_name: ``AWS::CloudWatch::Dashboard.DashboardName``.
        """
        props = CfnDashboardProps(dashboard_body=dashboard_body, dashboard_name=dashboard_name)

        jsii.create(CfnDashboard, self, [scope, id, props])

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
    @jsii.member(jsii_name="dashboardBody")
    def dashboard_body(self) -> str:
        """``AWS::CloudWatch::Dashboard.DashboardBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        """
        return jsii.get(self, "dashboardBody")

    @dashboard_body.setter
    def dashboard_body(self, value: str):
        jsii.set(self, "dashboardBody", value)

    @builtins.property
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Dashboard.DashboardName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        """
        return jsii.get(self, "dashboardName")

    @dashboard_name.setter
    def dashboard_name(self, value: typing.Optional[str]):
        jsii.set(self, "dashboardName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboardProps", jsii_struct_bases=[], name_mapping={'dashboard_body': 'dashboardBody', 'dashboard_name': 'dashboardName'})
class CfnDashboardProps():
    def __init__(self, *, dashboard_body: str, dashboard_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::CloudWatch::Dashboard``.

        :param dashboard_body: ``AWS::CloudWatch::Dashboard.DashboardBody``.
        :param dashboard_name: ``AWS::CloudWatch::Dashboard.DashboardName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
        """
        self._values = {
            'dashboard_body': dashboard_body,
        }
        if dashboard_name is not None: self._values["dashboard_name"] = dashboard_name

    @builtins.property
    def dashboard_body(self) -> str:
        """``AWS::CloudWatch::Dashboard.DashboardBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        """
        return self._values.get('dashboard_body')

    @builtins.property
    def dashboard_name(self) -> typing.Optional[str]:
        """``AWS::CloudWatch::Dashboard.DashboardName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        """
        return self._values.get('dashboard_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDashboardProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnInsightRule(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnInsightRule"):
    """A CloudFormation ``AWS::CloudWatch::InsightRule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
    cloudformationResource:
    :cloudformationResource:: AWS::CloudWatch::InsightRule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rule_body: str, rule_name: str, rule_state: str) -> None:
        """Create a new ``AWS::CloudWatch::InsightRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule_body: ``AWS::CloudWatch::InsightRule.RuleBody``.
        :param rule_name: ``AWS::CloudWatch::InsightRule.RuleName``.
        :param rule_state: ``AWS::CloudWatch::InsightRule.RuleState``.
        """
        props = CfnInsightRuleProps(rule_body=rule_body, rule_name=rule_name, rule_state=rule_state)

        jsii.create(CfnInsightRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrRuleName")
    def attr_rule_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RuleName
        """
        return jsii.get(self, "attrRuleName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="ruleBody")
    def rule_body(self) -> str:
        """``AWS::CloudWatch::InsightRule.RuleBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        """
        return jsii.get(self, "ruleBody")

    @rule_body.setter
    def rule_body(self, value: str):
        jsii.set(self, "ruleBody", value)

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> str:
        """``AWS::CloudWatch::InsightRule.RuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        """
        return jsii.get(self, "ruleName")

    @rule_name.setter
    def rule_name(self, value: str):
        jsii.set(self, "ruleName", value)

    @builtins.property
    @jsii.member(jsii_name="ruleState")
    def rule_state(self) -> str:
        """``AWS::CloudWatch::InsightRule.RuleState``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        """
        return jsii.get(self, "ruleState")

    @rule_state.setter
    def rule_state(self, value: str):
        jsii.set(self, "ruleState", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnInsightRuleProps", jsii_struct_bases=[], name_mapping={'rule_body': 'ruleBody', 'rule_name': 'ruleName', 'rule_state': 'ruleState'})
class CfnInsightRuleProps():
    def __init__(self, *, rule_body: str, rule_name: str, rule_state: str):
        """Properties for defining a ``AWS::CloudWatch::InsightRule``.

        :param rule_body: ``AWS::CloudWatch::InsightRule.RuleBody``.
        :param rule_name: ``AWS::CloudWatch::InsightRule.RuleName``.
        :param rule_state: ``AWS::CloudWatch::InsightRule.RuleState``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
        """
        self._values = {
            'rule_body': rule_body,
            'rule_name': rule_name,
            'rule_state': rule_state,
        }

    @builtins.property
    def rule_body(self) -> str:
        """``AWS::CloudWatch::InsightRule.RuleBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        """
        return self._values.get('rule_body')

    @builtins.property
    def rule_name(self) -> str:
        """``AWS::CloudWatch::InsightRule.RuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        """
        return self._values.get('rule_name')

    @builtins.property
    def rule_state(self) -> str:
        """``AWS::CloudWatch::InsightRule.RuleState``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        """
        return self._values.get('rule_state')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnInsightRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CommonMetricOptions", jsii_struct_bases=[], name_mapping={'account': 'account', 'color': 'color', 'dimensions': 'dimensions', 'label': 'label', 'period': 'period', 'region': 'region', 'statistic': 'statistic', 'unit': 'unit'})
class CommonMetricOptions():
    def __init__(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None):
        """Options shared by most methods accepting metric options.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if color is not None: self._values["color"] = color
        if dimensions is not None: self._values["dimensions"] = dimensions
        if label is not None: self._values["label"] = label
        if period is not None: self._values["period"] = period
        if region is not None: self._values["region"] = region
        if statistic is not None: self._values["statistic"] = statistic
        if unit is not None: self._values["unit"] = unit

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Account which this metric comes from.

        default
        :default: Deployment account.
        """
        return self._values.get('account')

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for this metric when added to a Graph in a Dashboard."""
        return self._values.get('color')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Dimensions of the metric.

        default
        :default: - No dimensions.
        """
        return self._values.get('dimensions')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for this metric when added to a Graph in a Dashboard."""
        return self._values.get('label')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('period')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Region which this metric comes from.

        default
        :default: Deployment region.
        """
        return self._values.get('region')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        default
        :default: Average
        """
        return self._values.get('statistic')

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        default
        :default: All metric datums in the given metric stream
        """
        return self._values.get('unit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonMetricOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.ComparisonOperator")
class ComparisonOperator(enum.Enum):
    """Comparison operator for evaluating alarms."""
    GREATER_THAN_OR_EQUAL_TO_THRESHOLD = "GREATER_THAN_OR_EQUAL_TO_THRESHOLD"
    GREATER_THAN_THRESHOLD = "GREATER_THAN_THRESHOLD"
    LESS_THAN_THRESHOLD = "LESS_THAN_THRESHOLD"
    LESS_THAN_OR_EQUAL_TO_THRESHOLD = "LESS_THAN_OR_EQUAL_TO_THRESHOLD"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CreateAlarmOptions", jsii_struct_bases=[], name_mapping={'evaluation_periods': 'evaluationPeriods', 'threshold': 'threshold', 'actions_enabled': 'actionsEnabled', 'alarm_description': 'alarmDescription', 'alarm_name': 'alarmName', 'comparison_operator': 'comparisonOperator', 'datapoints_to_alarm': 'datapointsToAlarm', 'evaluate_low_sample_count_percentile': 'evaluateLowSampleCountPercentile', 'period': 'period', 'statistic': 'statistic', 'treat_missing_data': 'treatMissingData'})
class CreateAlarmOptions():
    def __init__(self, *, evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None):
        """Properties needed to make an alarm from a metric.

        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        self._values = {
            'evaluation_periods': evaluation_periods,
            'threshold': threshold,
        }
        if actions_enabled is not None: self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None: self._values["alarm_description"] = alarm_description
        if alarm_name is not None: self._values["alarm_name"] = alarm_name
        if comparison_operator is not None: self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None: self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluate_low_sample_count_percentile is not None: self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if period is not None: self._values["period"] = period
        if statistic is not None: self._values["statistic"] = statistic
        if treat_missing_data is not None: self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        """The number of periods over which data is compared to the specified threshold."""
        return self._values.get('evaluation_periods')

    @builtins.property
    def threshold(self) -> jsii.Number:
        """The value against which the specified statistic is compared."""
        return self._values.get('threshold')

    @builtins.property
    def actions_enabled(self) -> typing.Optional[bool]:
        """Whether the actions for this alarm are enabled.

        default
        :default: true
        """
        return self._values.get('actions_enabled')

    @builtins.property
    def alarm_description(self) -> typing.Optional[str]:
        """Description for the alarm.

        default
        :default: No description
        """
        return self._values.get('alarm_description')

    @builtins.property
    def alarm_name(self) -> typing.Optional[str]:
        """Name of the alarm.

        default
        :default: Automatically generated name
        """
        return self._values.get('alarm_name')

    @builtins.property
    def comparison_operator(self) -> typing.Optional["ComparisonOperator"]:
        """Comparison to use to check if metric is breaching.

        default
        :default: GreaterThanOrEqualToThreshold
        """
        return self._values.get('comparison_operator')

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M
        out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
        CloudWatch User Guide.

        default
        :default: ``evaluationPeriods``

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
        """
        return self._values.get('datapoints_to_alarm')

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[str]:
        """Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

        Used only for alarms that are based on percentiles.

        default
        :default: - Not configured.
        """
        return self._values.get('evaluate_low_sample_count_percentile')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        Cannot be used with ``MathExpression`` objects.

        default
        :default: - The period from the metric

        deprecated
        :deprecated: Use ``metric.with({ period: ... })`` to encode the period into the Metric object

        stability
        :stability: deprecated
        """
        return self._values.get('period')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        Cannot be used with ``MathExpression`` objects.

        default
        :default: - The statistic from the metric

        deprecated
        :deprecated: Use ``metric.with({ statistic: ... })`` to encode the period into the Metric object

        stability
        :stability: deprecated
        """
        return self._values.get('statistic')

    @builtins.property
    def treat_missing_data(self) -> typing.Optional["TreatMissingData"]:
        """Sets how this alarm is to handle missing data points.

        default
        :default: TreatMissingData.Missing
        """
        return self._values.get('treat_missing_data')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CreateAlarmOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmProps", jsii_struct_bases=[CreateAlarmOptions], name_mapping={'evaluation_periods': 'evaluationPeriods', 'threshold': 'threshold', 'actions_enabled': 'actionsEnabled', 'alarm_description': 'alarmDescription', 'alarm_name': 'alarmName', 'comparison_operator': 'comparisonOperator', 'datapoints_to_alarm': 'datapointsToAlarm', 'evaluate_low_sample_count_percentile': 'evaluateLowSampleCountPercentile', 'period': 'period', 'statistic': 'statistic', 'treat_missing_data': 'treatMissingData', 'metric': 'metric'})
class AlarmProps(CreateAlarmOptions):
    def __init__(self, *, evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None, metric: "IMetric"):
        """Properties for Alarms.

        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        :param metric: The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.
        """
        self._values = {
            'evaluation_periods': evaluation_periods,
            'threshold': threshold,
            'metric': metric,
        }
        if actions_enabled is not None: self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None: self._values["alarm_description"] = alarm_description
        if alarm_name is not None: self._values["alarm_name"] = alarm_name
        if comparison_operator is not None: self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None: self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluate_low_sample_count_percentile is not None: self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if period is not None: self._values["period"] = period
        if statistic is not None: self._values["statistic"] = statistic
        if treat_missing_data is not None: self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        """The number of periods over which data is compared to the specified threshold."""
        return self._values.get('evaluation_periods')

    @builtins.property
    def threshold(self) -> jsii.Number:
        """The value against which the specified statistic is compared."""
        return self._values.get('threshold')

    @builtins.property
    def actions_enabled(self) -> typing.Optional[bool]:
        """Whether the actions for this alarm are enabled.

        default
        :default: true
        """
        return self._values.get('actions_enabled')

    @builtins.property
    def alarm_description(self) -> typing.Optional[str]:
        """Description for the alarm.

        default
        :default: No description
        """
        return self._values.get('alarm_description')

    @builtins.property
    def alarm_name(self) -> typing.Optional[str]:
        """Name of the alarm.

        default
        :default: Automatically generated name
        """
        return self._values.get('alarm_name')

    @builtins.property
    def comparison_operator(self) -> typing.Optional["ComparisonOperator"]:
        """Comparison to use to check if metric is breaching.

        default
        :default: GreaterThanOrEqualToThreshold
        """
        return self._values.get('comparison_operator')

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M
        out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
        CloudWatch User Guide.

        default
        :default: ``evaluationPeriods``

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
        """
        return self._values.get('datapoints_to_alarm')

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[str]:
        """Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

        Used only for alarms that are based on percentiles.

        default
        :default: - Not configured.
        """
        return self._values.get('evaluate_low_sample_count_percentile')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        Cannot be used with ``MathExpression`` objects.

        default
        :default: - The period from the metric

        deprecated
        :deprecated: Use ``metric.with({ period: ... })`` to encode the period into the Metric object

        stability
        :stability: deprecated
        """
        return self._values.get('period')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        Cannot be used with ``MathExpression`` objects.

        default
        :default: - The statistic from the metric

        deprecated
        :deprecated: Use ``metric.with({ statistic: ... })`` to encode the period into the Metric object

        stability
        :stability: deprecated
        """
        return self._values.get('statistic')

    @builtins.property
    def treat_missing_data(self) -> typing.Optional["TreatMissingData"]:
        """Sets how this alarm is to handle missing data points.

        default
        :default: TreatMissingData.Missing
        """
        return self._values.get('treat_missing_data')

    @builtins.property
    def metric(self) -> "IMetric":
        """The metric to add the alarm on.

        Metric objects can be obtained from most resources, or you can construct
        custom Metric objects by instantiating one.
        """
        return self._values.get('metric')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlarmProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Dashboard(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Dashboard"):
    """A CloudWatch dashboard."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, dashboard_name: typing.Optional[str]=None, end: typing.Optional[str]=None, period_override: typing.Optional["PeriodOverride"]=None, start: typing.Optional[str]=None, widgets: typing.Optional[typing.List[typing.List["IWidget"]]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param dashboard_name: Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets
        """
        props = DashboardProps(dashboard_name=dashboard_name, end=end, period_override=period_override, start=start, widgets=widgets)

        jsii.create(Dashboard, self, [scope, id, props])

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: "IWidget") -> None:
        """Add a widget to the dashboard.

        Widgets given in multiple calls to add() will be laid out stacked on
        top of each other.

        Multiple widgets added in the same call to add() will be laid out next
        to each other.

        :param widgets: -
        """
        return jsii.invoke(self, "addWidgets", [*widgets])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.DashboardProps", jsii_struct_bases=[], name_mapping={'dashboard_name': 'dashboardName', 'end': 'end', 'period_override': 'periodOverride', 'start': 'start', 'widgets': 'widgets'})
class DashboardProps():
    def __init__(self, *, dashboard_name: typing.Optional[str]=None, end: typing.Optional[str]=None, period_override: typing.Optional["PeriodOverride"]=None, start: typing.Optional[str]=None, widgets: typing.Optional[typing.List[typing.List["IWidget"]]]=None):
        """
        :param dashboard_name: Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets
        """
        self._values = {
        }
        if dashboard_name is not None: self._values["dashboard_name"] = dashboard_name
        if end is not None: self._values["end"] = end
        if period_override is not None: self._values["period_override"] = period_override
        if start is not None: self._values["start"] = start
        if widgets is not None: self._values["widgets"] = widgets

    @builtins.property
    def dashboard_name(self) -> typing.Optional[str]:
        """Name of the dashboard.

        If set, must only contain alphanumerics, dash (-) and underscore (_)

        default
        :default: - automatically generated name
        """
        return self._values.get('dashboard_name')

    @builtins.property
    def end(self) -> typing.Optional[str]:
        """The end of the time range to use for each widget on the dashboard when the dashboard loads.

        If you specify a value for end, you must also specify a value for start.
        Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        default
        :default: When the dashboard loads, the end date will be the current time.
        """
        return self._values.get('end')

    @builtins.property
    def period_override(self) -> typing.Optional["PeriodOverride"]:
        """Use this field to specify the period for the graphs when the dashboard loads.

        Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard.
        Specifying ``Inherit`` ensures that the period set for each graph is always obeyed.

        default
        :default: Auto
        """
        return self._values.get('period_override')

    @builtins.property
    def start(self) -> typing.Optional[str]:
        """The start of the time range to use for each widget on the dashboard.

        You can specify start without specifying end to specify a relative time range that ends with the current time.
        In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for
        minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months.
        You can also use start along with an end field, to specify an absolute time range.
        When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        default
        :default: When the dashboard loads, the start time will be the default time range.
        """
        return self._values.get('start')

    @builtins.property
    def widgets(self) -> typing.Optional[typing.List[typing.List["IWidget"]]]:
        """Initial set of widgets on the dashboard.

        One array represents a row of widgets.

        default
        :default: - No widgets
        """
        return self._values.get('widgets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DashboardProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.Dimension", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
class Dimension():
    def __init__(self, *, name: str, value: typing.Any):
        """Metric dimension.

        :param name: Name of the dimension.
        :param value: Value of the dimension.
        """
        self._values = {
            'name': name,
            'value': value,
        }

    @builtins.property
    def name(self) -> str:
        """Name of the dimension."""
        return self._values.get('name')

    @builtins.property
    def value(self) -> typing.Any:
        """Value of the dimension."""
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Dimension(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.HorizontalAnnotation", jsii_struct_bases=[], name_mapping={'value': 'value', 'color': 'color', 'fill': 'fill', 'label': 'label', 'visible': 'visible'})
class HorizontalAnnotation():
    def __init__(self, *, value: jsii.Number, color: typing.Optional[str]=None, fill: typing.Optional["Shading"]=None, label: typing.Optional[str]=None, visible: typing.Optional[bool]=None):
        """Horizontal annotation to be added to a graph.

        :param value: The value of the annotation.
        :param color: Hex color code to be used for the annotation. Default: Automatic color
        :param fill: Add shading above or below the annotation. Default: No shading
        :param label: Label for the annotation. Default: No label
        :param visible: Whether the annotation is visible. Default: true
        """
        self._values = {
            'value': value,
        }
        if color is not None: self._values["color"] = color
        if fill is not None: self._values["fill"] = fill
        if label is not None: self._values["label"] = label
        if visible is not None: self._values["visible"] = visible

    @builtins.property
    def value(self) -> jsii.Number:
        """The value of the annotation."""
        return self._values.get('value')

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Hex color code to be used for the annotation.

        default
        :default: Automatic color
        """
        return self._values.get('color')

    @builtins.property
    def fill(self) -> typing.Optional["Shading"]:
        """Add shading above or below the annotation.

        default
        :default: No shading
        """
        return self._values.get('fill')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for the annotation.

        default
        :default: No label
        """
        return self._values.get('label')

    @builtins.property
    def visible(self) -> typing.Optional[bool]:
        """Whether the annotation is visible.

        default
        :default: true
        """
        return self._values.get('visible')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HorizontalAnnotation(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarm")
class IAlarm(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAlarmProxy

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _IAlarmProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IAlarm"
    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "alarmArn")

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "alarmName")


@jsii.implements(IAlarm)
class Alarm(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Alarm"):
    """An alarm on a CloudWatch metric."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, metric: "IMetric", evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param metric: The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props = AlarmProps(metric=metric, evaluation_periods=evaluation_periods, threshold=threshold, actions_enabled=actions_enabled, alarm_description=alarm_description, alarm_name=alarm_name, comparison_operator=comparison_operator, datapoints_to_alarm=datapoints_to_alarm, evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile, period=period, statistic=statistic, treat_missing_data=treat_missing_data)

        jsii.create(Alarm, self, [scope, id, props])

    @jsii.member(jsii_name="fromAlarmArn")
    @builtins.classmethod
    def from_alarm_arn(cls, scope: aws_cdk.core.Construct, id: str, alarm_arn: str) -> "IAlarm":
        """
        :param scope: -
        :param id: -
        :param alarm_arn: -
        """
        return jsii.sinvoke(cls, "fromAlarmArn", [scope, id, alarm_arn])

    @jsii.member(jsii_name="addAlarmAction")
    def add_alarm_action(self, *actions: "IAlarmAction") -> None:
        """Trigger this action if the alarm fires.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -
        """
        return jsii.invoke(self, "addAlarmAction", [*actions])

    @jsii.member(jsii_name="addInsufficientDataAction")
    def add_insufficient_data_action(self, *actions: "IAlarmAction") -> None:
        """Trigger this action if there is insufficient data to evaluate the alarm.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -
        """
        return jsii.invoke(self, "addInsufficientDataAction", [*actions])

    @jsii.member(jsii_name="addOkAction")
    def add_ok_action(self, *actions: "IAlarmAction") -> None:
        """Trigger this action if the alarm returns from breaching state into ok state.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -
        """
        return jsii.invoke(self, "addOkAction", [*actions])

    @jsii.member(jsii_name="toAnnotation")
    def to_annotation(self) -> "HorizontalAnnotation":
        """Turn this alarm into a horizontal annotation.

        This is useful if you want to represent an Alarm in a non-AlarmWidget.
        An ``AlarmWidget`` can directly show an alarm, but it can only show a
        single alarm and no other metrics. Instead, you can convert the alarm to
        a HorizontalAnnotation and add it as an annotation to another graph.

        This might be useful if:

        - You want to show multiple alarms inside a single graph, for example if
          you have both a "small margin/long period" alarm as well as a
          "large margin/short period" alarm.
        - You want to show an Alarm line in a graph with multiple metrics in it.
        """
        return jsii.invoke(self, "toAnnotation", [])

    @builtins.property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """ARN of this alarm.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "alarmArn")

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        """Name of this alarm.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "alarmName")

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> "IMetric":
        """The metric object this alarm was based on."""
        return jsii.get(self, "metric")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarmAction")
class IAlarmAction(jsii.compat.Protocol):
    """Interface for objects that can be the targets of CloudWatch alarm actions."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAlarmActionProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, alarm: "IAlarm") -> "AlarmActionConfig":
        """
        :param scope: -
        :param alarm: -
        """
        ...


class _IAlarmActionProxy():
    """Interface for objects that can be the targets of CloudWatch alarm actions."""
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IAlarmAction"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, alarm: "IAlarm") -> "AlarmActionConfig":
        """
        :param scope: -
        :param alarm: -
        """
        return jsii.invoke(self, "bind", [scope, alarm])


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IMetric")
class IMetric(jsii.compat.Protocol):
    """Interface for metrics."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IMetricProxy

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """Turn this metric object into an alarm configuration.

        deprecated
        :deprecated: Use ``toMetricsConfig()`` instead.

        stability
        :stability: deprecated
        """
        ...

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """Turn this metric object into a graph configuration.

        deprecated
        :deprecated: Use ``toMetricsConfig()`` instead.

        stability
        :stability: deprecated
        """
        ...

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        ...


class _IMetricProxy():
    """Interface for metrics."""
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IMetric"
    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """Turn this metric object into an alarm configuration.

        deprecated
        :deprecated: Use ``toMetricsConfig()`` instead.

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "toAlarmConfig", [])

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """Turn this metric object into a graph configuration.

        deprecated
        :deprecated: Use ``toMetricsConfig()`` instead.

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "toGraphConfig", [])

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        return jsii.invoke(self, "toMetricConfig", [])


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IWidget")
class IWidget(jsii.compat.Protocol):
    """A single dashboard widget."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IWidgetProxy

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        ...

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        ...

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        ...

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        ...


class _IWidgetProxy():
    """A single dashboard widget."""
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IWidget"
    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.implements(IWidget)
class Column(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Column"):
    """A widget that contains other widgets in a vertical column.

    Widgets will be laid out next to each other
    """
    def __init__(self, *widgets: "IWidget") -> None:
        """
        :param widgets: -
        """
        jsii.create(Column, self, [*widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.implements(IWidget)
class ConcreteWidget(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-cloudwatch.ConcreteWidget"):
    """A real CloudWatch widget that has its own fixed size and remembers its position.

    This is in contrast to other widgets which exist for layout purposes.
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ConcreteWidgetProxy

    def __init__(self, width: jsii.Number, height: jsii.Number) -> None:
        """
        :param width: -
        :param height: -
        """
        jsii.create(ConcreteWidget, self, [width, height])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    @abc.abstractmethod
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        ...

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")

    @builtins.property
    @jsii.member(jsii_name="x")
    def _x(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "x")

    @_x.setter
    def _x(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "x", value)

    @builtins.property
    @jsii.member(jsii_name="y")
    def _y(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "y")

    @_y.setter
    def _y(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "y", value)


class _ConcreteWidgetProxy(ConcreteWidget):
    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class AlarmWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidget"):
    """Display the metric associated with an alarm, including the alarm line."""
    def __init__(self, *, alarm: "IAlarm", left_y_axis: typing.Optional["YAxisProps"]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        :param alarm: The alarm to show.
        :param left_y_axis: Left Y axis.
        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = AlarmWidgetProps(alarm=alarm, left_y_axis=left_y_axis, height=height, region=region, title=title, width=width)

        jsii.create(AlarmWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class GraphWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.GraphWidget"):
    """A dashboard widget that displays metrics."""
    def __init__(self, *, left: typing.Optional[typing.List["IMetric"]]=None, left_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, left_y_axis: typing.Optional["YAxisProps"]=None, right: typing.Optional[typing.List["IMetric"]]=None, right_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, right_y_axis: typing.Optional["YAxisProps"]=None, stacked: typing.Optional[bool]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        :param left: Metrics to display on left Y axis.
        :param left_annotations: Annotations for the left Y axis.
        :param left_y_axis: Left Y axis.
        :param right: Metrics to display on right Y axis.
        :param right_annotations: Annotations for the right Y axis.
        :param right_y_axis: Right Y axis.
        :param stacked: Whether the graph should be shown as stacked lines.
        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = GraphWidgetProps(left=left, left_annotations=left_annotations, left_y_axis=left_y_axis, right=right, right_annotations=right_annotations, right_y_axis=right_y_axis, stacked=stacked, height=height, region=region, title=title, width=width)

        jsii.create(GraphWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.implements(IMetric)
class MathExpression(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.MathExpression"):
    """A math expression built with metric(s) emitted by a service.

    The math expression is a combination of an expression (x+y) and metrics to apply expression on.
    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    This class does not represent a resource, so hence is not a construct. Instead,
    MathExpression is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.
    """
    def __init__(self, *, expression: str, using_metrics: typing.Mapping[str,"IMetric"], color: typing.Optional[str]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param expression: The expression defining the metric.
        :param using_metrics: The metrics used in the expression, in a map. The key is the identifier that represents the given metric in the expression, and the value is the actual Metric object.
        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        """
        props = MathExpressionProps(expression=expression, using_metrics=using_metrics, color=color, label=label, period=period)

        jsii.create(MathExpression, self, [props])

    @jsii.member(jsii_name="createAlarm")
    def create_alarm(self, scope: aws_cdk.core.Construct, id: str, *, evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> "Alarm":
        """Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        :param scope: -
        :param id: -
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props = CreateAlarmOptions(evaluation_periods=evaluation_periods, threshold=threshold, actions_enabled=actions_enabled, alarm_description=alarm_description, alarm_name=alarm_name, comparison_operator=comparison_operator, datapoints_to_alarm=datapoints_to_alarm, evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile, period=period, statistic=statistic, treat_missing_data=treat_missing_data)

        return jsii.invoke(self, "createAlarm", [scope, id, props])

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """Turn this metric object into an alarm configuration."""
        return jsii.invoke(self, "toAlarmConfig", [])

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """Turn this metric object into a graph configuration."""
        return jsii.invoke(self, "toGraphConfig", [])

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        return jsii.invoke(self, "toMetricConfig", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="with")
    def with_(self, *, color: typing.Optional[str]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None) -> "MathExpression":
        """Return a copy of Metric with properties changed.

        All properties except namespace and metricName can be changed.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        """
        props = MathExpressionOptions(color=color, label=label, period=period)

        return jsii.invoke(self, "with", [props])

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> str:
        """The expression defining the metric."""
        return jsii.get(self, "expression")

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> aws_cdk.core.Duration:
        """Aggregation period of this metric."""
        return jsii.get(self, "period")

    @builtins.property
    @jsii.member(jsii_name="usingMetrics")
    def using_metrics(self) -> typing.Mapping[str,"IMetric"]:
        """The metrics used in the expression as KeyValuePair <id, metric>."""
        return jsii.get(self, "usingMetrics")

    @builtins.property
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[str]:
        """Color for this metric when added to a Graph."""
        return jsii.get(self, "color")

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[str]:
        """Label for this metric when added to a Graph."""
        return jsii.get(self, "label")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MathExpressionOptions", jsii_struct_bases=[], name_mapping={'color': 'color', 'label': 'label', 'period': 'period'})
class MathExpressionOptions():
    def __init__(self, *, color: typing.Optional[str]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None):
        """Configurable options for MathExpressions.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        """
        self._values = {
        }
        if color is not None: self._values["color"] = color
        if label is not None: self._values["label"] = label
        if period is not None: self._values["period"] = period

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for this metric when added to a Graph in a Dashboard.

        default
        :default: - Automatic color
        """
        return self._values.get('color')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for this metric when added to a Graph in a Dashboard.

        default
        :default: - Expression value is used as label
        """
        return self._values.get('label')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the expression's statistics are applied.

        This period overrides all periods in the metrics used in this
        math expression.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('period')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MathExpressionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MathExpressionProps", jsii_struct_bases=[MathExpressionOptions], name_mapping={'color': 'color', 'label': 'label', 'period': 'period', 'expression': 'expression', 'using_metrics': 'usingMetrics'})
class MathExpressionProps(MathExpressionOptions):
    def __init__(self, *, color: typing.Optional[str]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, expression: str, using_metrics: typing.Mapping[str,"IMetric"]):
        """Properties for a MathExpression.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param expression: The expression defining the metric.
        :param using_metrics: The metrics used in the expression, in a map. The key is the identifier that represents the given metric in the expression, and the value is the actual Metric object.
        """
        self._values = {
            'expression': expression,
            'using_metrics': using_metrics,
        }
        if color is not None: self._values["color"] = color
        if label is not None: self._values["label"] = label
        if period is not None: self._values["period"] = period

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for this metric when added to a Graph in a Dashboard.

        default
        :default: - Automatic color
        """
        return self._values.get('color')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for this metric when added to a Graph in a Dashboard.

        default
        :default: - Expression value is used as label
        """
        return self._values.get('label')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the expression's statistics are applied.

        This period overrides all periods in the metrics used in this
        math expression.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('period')

    @builtins.property
    def expression(self) -> str:
        """The expression defining the metric."""
        return self._values.get('expression')

    @builtins.property
    def using_metrics(self) -> typing.Mapping[str,"IMetric"]:
        """The metrics used in the expression, in a map.

        The key is the identifier that represents the given metric in the
        expression, and the value is the actual Metric object.
        """
        return self._values.get('using_metrics')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MathExpressionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IMetric)
class Metric(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Metric"):
    """A metric emitted by a service.

    The metric is a combination of a metric identifier (namespace, name and dimensions)
    and an aggregation function (statistic, period and unit).

    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    This class does not represent a resource, so hence is not a construct. Instead,
    Metric is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.
    """
    def __init__(self, *, metric_name: str, namespace: str, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None) -> None:
        """
        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = MetricProps(metric_name=metric_name, namespace=namespace, account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        jsii.create(Metric, self, [props])

    @jsii.member(jsii_name="grantPutMetricData")
    @builtins.classmethod
    def grant_put_metric_data(cls, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant permissions to the given identity to write metrics.

        :param grantee: The IAM identity to give permissions to.
        """
        return jsii.sinvoke(cls, "grantPutMetricData", [grantee])

    @jsii.member(jsii_name="attachTo")
    def attach_to(self, scope: aws_cdk.core.Construct) -> "Metric":
        """Attach the metric object to the given construct scope.

        Returns a Metric object that uses the account and region from the Stack
        the given construct is defined in. If the metric is subsequently used
        in a Dashboard or Alarm in a different Stack defined in a different
        account or region, the appropriate 'region' and 'account' fields
        will be added to it.

        If the scope we attach to is in an environment-agnostic stack,
        nothing is done and the same Metric object is returned.

        :param scope: -
        """
        return jsii.invoke(self, "attachTo", [scope])

    @jsii.member(jsii_name="createAlarm")
    def create_alarm(self, scope: aws_cdk.core.Construct, id: str, *, evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> "Alarm":
        """Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        :param scope: -
        :param id: -
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props = CreateAlarmOptions(evaluation_periods=evaluation_periods, threshold=threshold, actions_enabled=actions_enabled, alarm_description=alarm_description, alarm_name=alarm_name, comparison_operator=comparison_operator, datapoints_to_alarm=datapoints_to_alarm, evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile, period=period, statistic=statistic, treat_missing_data=treat_missing_data)

        return jsii.invoke(self, "createAlarm", [scope, id, props])

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """Turn this metric object into an alarm configuration."""
        return jsii.invoke(self, "toAlarmConfig", [])

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """Turn this metric object into a graph configuration."""
        return jsii.invoke(self, "toGraphConfig", [])

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        return jsii.invoke(self, "toMetricConfig", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="with")
    def with_(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None) -> "Metric":
        """Return a copy of Metric with properties changed.

        All properties except namespace and metricName can be changed.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        props = MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "with", [props])

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> str:
        return jsii.get(self, "metricName")

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> str:
        return jsii.get(self, "namespace")

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> aws_cdk.core.Duration:
        return jsii.get(self, "period")

    @builtins.property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> str:
        return jsii.get(self, "statistic")

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[str]:
        """Account which this metric comes from.

        default
        :default: Deployment account.
        """
        return jsii.get(self, "account")

    @builtins.property
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[str]:
        return jsii.get(self, "color")

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        return jsii.get(self, "dimensions")

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[str]:
        return jsii.get(self, "label")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[str]:
        """Region which this metric comes from.

        default
        :default: Deployment region.
        """
        return jsii.get(self, "region")

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional["Unit"]:
        """Unit of the metric.

        default
        :default: None
        """
        return jsii.get(self, "unit")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricAlarmConfig", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'namespace': 'namespace', 'period': 'period', 'dimensions': 'dimensions', 'extended_statistic': 'extendedStatistic', 'statistic': 'statistic', 'unit': 'unit'})
class MetricAlarmConfig():
    def __init__(self, *, metric_name: str, namespace: str, period: jsii.Number, dimensions: typing.Optional[typing.List["Dimension"]]=None, extended_statistic: typing.Optional[str]=None, statistic: typing.Optional["Statistic"]=None, unit: typing.Optional["Unit"]=None):
        """Properties used to construct the Metric identifying part of an Alarm.

        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        :param period: How many seconds to aggregate over.
        :param dimensions: The dimensions to apply to the alarm.
        :param extended_statistic: Percentile aggregation function to use.
        :param statistic: Simple aggregation function to use.
        :param unit: The unit of the alarm.

        deprecated
        :deprecated: Replaced by MetricConfig

        stability
        :stability: deprecated
        """
        self._values = {
            'metric_name': metric_name,
            'namespace': namespace,
            'period': period,
        }
        if dimensions is not None: self._values["dimensions"] = dimensions
        if extended_statistic is not None: self._values["extended_statistic"] = extended_statistic
        if statistic is not None: self._values["statistic"] = statistic
        if unit is not None: self._values["unit"] = unit

    @builtins.property
    def metric_name(self) -> str:
        """Name of the metric.

        stability
        :stability: deprecated
        """
        return self._values.get('metric_name')

    @builtins.property
    def namespace(self) -> str:
        """Namespace of the metric.

        stability
        :stability: deprecated
        """
        return self._values.get('namespace')

    @builtins.property
    def period(self) -> jsii.Number:
        """How many seconds to aggregate over.

        stability
        :stability: deprecated
        """
        return self._values.get('period')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List["Dimension"]]:
        """The dimensions to apply to the alarm.

        stability
        :stability: deprecated
        """
        return self._values.get('dimensions')

    @builtins.property
    def extended_statistic(self) -> typing.Optional[str]:
        """Percentile aggregation function to use.

        stability
        :stability: deprecated
        """
        return self._values.get('extended_statistic')

    @builtins.property
    def statistic(self) -> typing.Optional["Statistic"]:
        """Simple aggregation function to use.

        stability
        :stability: deprecated
        """
        return self._values.get('statistic')

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """The unit of the alarm.

        stability
        :stability: deprecated
        """
        return self._values.get('unit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricAlarmConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricConfig", jsii_struct_bases=[], name_mapping={'math_expression': 'mathExpression', 'metric_stat': 'metricStat', 'rendering_properties': 'renderingProperties'})
class MetricConfig():
    def __init__(self, *, math_expression: typing.Optional["MetricExpressionConfig"]=None, metric_stat: typing.Optional["MetricStatConfig"]=None, rendering_properties: typing.Optional[typing.Mapping[str,typing.Any]]=None):
        """Properties of a rendered metric.

        :param math_expression: In case the metric is a math expression, the details of the math expression. Default: - unset
        :param metric_stat: In case the metric represents a query, the details of the query. Default: - unset
        :param rendering_properties: Additional properties which will be rendered if the metric is used in a dashboard. Examples are 'label' and 'color', but any key in here will be added to dashboard graphs. Default: {}
        """
        if isinstance(math_expression, dict): math_expression = MetricExpressionConfig(**math_expression)
        if isinstance(metric_stat, dict): metric_stat = MetricStatConfig(**metric_stat)
        self._values = {
        }
        if math_expression is not None: self._values["math_expression"] = math_expression
        if metric_stat is not None: self._values["metric_stat"] = metric_stat
        if rendering_properties is not None: self._values["rendering_properties"] = rendering_properties

    @builtins.property
    def math_expression(self) -> typing.Optional["MetricExpressionConfig"]:
        """In case the metric is a math expression, the details of the math expression.

        default
        :default: - unset
        """
        return self._values.get('math_expression')

    @builtins.property
    def metric_stat(self) -> typing.Optional["MetricStatConfig"]:
        """In case the metric represents a query, the details of the query.

        default
        :default: - unset
        """
        return self._values.get('metric_stat')

    @builtins.property
    def rendering_properties(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Additional properties which will be rendered if the metric is used in a dashboard.

        Examples are 'label' and 'color', but any key in here will be
        added to dashboard graphs.

        default
        :default: {}
        """
        return self._values.get('rendering_properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricExpressionConfig", jsii_struct_bases=[], name_mapping={'expression': 'expression', 'using_metrics': 'usingMetrics'})
class MetricExpressionConfig():
    def __init__(self, *, expression: str, using_metrics: typing.Mapping[str,"IMetric"]):
        """Properties for a concrete metric.

        :param expression: Math expression for the metric.
        :param using_metrics: Metrics used in the math expression.
        """
        self._values = {
            'expression': expression,
            'using_metrics': using_metrics,
        }

    @builtins.property
    def expression(self) -> str:
        """Math expression for the metric."""
        return self._values.get('expression')

    @builtins.property
    def using_metrics(self) -> typing.Mapping[str,"IMetric"]:
        """Metrics used in the math expression."""
        return self._values.get('using_metrics')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricExpressionConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricGraphConfig", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'namespace': 'namespace', 'period': 'period', 'rendering_properties': 'renderingProperties', 'color': 'color', 'dimensions': 'dimensions', 'label': 'label', 'statistic': 'statistic', 'unit': 'unit'})
class MetricGraphConfig():
    def __init__(self, *, metric_name: str, namespace: str, period: jsii.Number, rendering_properties: "MetricRenderingProperties", color: typing.Optional[str]=None, dimensions: typing.Optional[typing.List["Dimension"]]=None, label: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None):
        """Properties used to construct the Metric identifying part of a Graph.

        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        :param period: How many seconds to aggregate over.
        :param rendering_properties: Rendering properties override yAxis parameter of the widget object.
        :param color: Color for the graph line.
        :param dimensions: The dimensions to apply to the alarm.
        :param label: Label for the metric.
        :param statistic: Aggregation function to use (can be either simple or a percentile).
        :param unit: The unit of the alarm.

        deprecated
        :deprecated: Replaced by MetricConfig

        stability
        :stability: deprecated
        """
        if isinstance(rendering_properties, dict): rendering_properties = MetricRenderingProperties(**rendering_properties)
        self._values = {
            'metric_name': metric_name,
            'namespace': namespace,
            'period': period,
            'rendering_properties': rendering_properties,
        }
        if color is not None: self._values["color"] = color
        if dimensions is not None: self._values["dimensions"] = dimensions
        if label is not None: self._values["label"] = label
        if statistic is not None: self._values["statistic"] = statistic
        if unit is not None: self._values["unit"] = unit

    @builtins.property
    def metric_name(self) -> str:
        """Name of the metric.

        stability
        :stability: deprecated
        """
        return self._values.get('metric_name')

    @builtins.property
    def namespace(self) -> str:
        """Namespace of the metric.

        stability
        :stability: deprecated
        """
        return self._values.get('namespace')

    @builtins.property
    def period(self) -> jsii.Number:
        """How many seconds to aggregate over.

        deprecated
        :deprecated: Use ``period`` in ``renderingProperties``

        stability
        :stability: deprecated
        """
        return self._values.get('period')

    @builtins.property
    def rendering_properties(self) -> "MetricRenderingProperties":
        """Rendering properties override yAxis parameter of the widget object.

        stability
        :stability: deprecated
        """
        return self._values.get('rendering_properties')

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for the graph line.

        deprecated
        :deprecated: Use ``color`` in ``renderingProperties``

        stability
        :stability: deprecated
        """
        return self._values.get('color')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List["Dimension"]]:
        """The dimensions to apply to the alarm.

        stability
        :stability: deprecated
        """
        return self._values.get('dimensions')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for the metric.

        deprecated
        :deprecated: Use ``label`` in ``renderingProperties``

        stability
        :stability: deprecated
        """
        return self._values.get('label')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """Aggregation function to use (can be either simple or a percentile).

        deprecated
        :deprecated: Use ``stat`` in ``renderingProperties``

        stability
        :stability: deprecated
        """
        return self._values.get('statistic')

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """The unit of the alarm.

        deprecated
        :deprecated: not used in dashboard widgets

        stability
        :stability: deprecated
        """
        return self._values.get('unit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricGraphConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricOptions", jsii_struct_bases=[CommonMetricOptions], name_mapping={'account': 'account', 'color': 'color', 'dimensions': 'dimensions', 'label': 'label', 'period': 'period', 'region': 'region', 'statistic': 'statistic', 'unit': 'unit'})
class MetricOptions(CommonMetricOptions):
    def __init__(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None):
        """Properties of a metric that can be changed.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if color is not None: self._values["color"] = color
        if dimensions is not None: self._values["dimensions"] = dimensions
        if label is not None: self._values["label"] = label
        if period is not None: self._values["period"] = period
        if region is not None: self._values["region"] = region
        if statistic is not None: self._values["statistic"] = statistic
        if unit is not None: self._values["unit"] = unit

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Account which this metric comes from.

        default
        :default: Deployment account.
        """
        return self._values.get('account')

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for this metric when added to a Graph in a Dashboard."""
        return self._values.get('color')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Dimensions of the metric.

        default
        :default: - No dimensions.
        """
        return self._values.get('dimensions')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for this metric when added to a Graph in a Dashboard."""
        return self._values.get('label')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('period')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Region which this metric comes from.

        default
        :default: Deployment region.
        """
        return self._values.get('region')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        default
        :default: Average
        """
        return self._values.get('statistic')

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        default
        :default: All metric datums in the given metric stream
        """
        return self._values.get('unit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricProps", jsii_struct_bases=[CommonMetricOptions], name_mapping={'account': 'account', 'color': 'color', 'dimensions': 'dimensions', 'label': 'label', 'period': 'period', 'region': 'region', 'statistic': 'statistic', 'unit': 'unit', 'metric_name': 'metricName', 'namespace': 'namespace'})
class MetricProps(CommonMetricOptions):
    def __init__(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None, metric_name: str, namespace: str):
        """Properties for a metric.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream
        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        """
        self._values = {
            'metric_name': metric_name,
            'namespace': namespace,
        }
        if account is not None: self._values["account"] = account
        if color is not None: self._values["color"] = color
        if dimensions is not None: self._values["dimensions"] = dimensions
        if label is not None: self._values["label"] = label
        if period is not None: self._values["period"] = period
        if region is not None: self._values["region"] = region
        if statistic is not None: self._values["statistic"] = statistic
        if unit is not None: self._values["unit"] = unit

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Account which this metric comes from.

        default
        :default: Deployment account.
        """
        return self._values.get('account')

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for this metric when added to a Graph in a Dashboard."""
        return self._values.get('color')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Dimensions of the metric.

        default
        :default: - No dimensions.
        """
        return self._values.get('dimensions')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for this metric when added to a Graph in a Dashboard."""
        return self._values.get('label')

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('period')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Region which this metric comes from.

        default
        :default: Deployment region.
        """
        return self._values.get('region')

    @builtins.property
    def statistic(self) -> typing.Optional[str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        default
        :default: Average
        """
        return self._values.get('statistic')

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        default
        :default: All metric datums in the given metric stream
        """
        return self._values.get('unit')

    @builtins.property
    def metric_name(self) -> str:
        """Name of the metric."""
        return self._values.get('metric_name')

    @builtins.property
    def namespace(self) -> str:
        """Namespace of the metric."""
        return self._values.get('namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricRenderingProperties", jsii_struct_bases=[], name_mapping={'period': 'period', 'color': 'color', 'label': 'label', 'stat': 'stat'})
class MetricRenderingProperties():
    def __init__(self, *, period: jsii.Number, color: typing.Optional[str]=None, label: typing.Optional[str]=None, stat: typing.Optional[str]=None):
        """Custom rendering properties that override the default rendering properties specified in the yAxis parameter of the widget object.

        :param period: How many seconds to aggregate over.
        :param color: Color for the graph line.
        :param label: Label for the metric.
        :param stat: Aggregation function to use (can be either simple or a percentile).

        deprecated
        :deprecated: Replaced by MetricConfig.

        stability
        :stability: deprecated
        """
        self._values = {
            'period': period,
        }
        if color is not None: self._values["color"] = color
        if label is not None: self._values["label"] = label
        if stat is not None: self._values["stat"] = stat

    @builtins.property
    def period(self) -> jsii.Number:
        """How many seconds to aggregate over.

        stability
        :stability: deprecated
        """
        return self._values.get('period')

    @builtins.property
    def color(self) -> typing.Optional[str]:
        """Color for the graph line.

        stability
        :stability: deprecated
        """
        return self._values.get('color')

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """Label for the metric.

        stability
        :stability: deprecated
        """
        return self._values.get('label')

    @builtins.property
    def stat(self) -> typing.Optional[str]:
        """Aggregation function to use (can be either simple or a percentile).

        stability
        :stability: deprecated
        """
        return self._values.get('stat')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricRenderingProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricStatConfig", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'namespace': 'namespace', 'period': 'period', 'statistic': 'statistic', 'account': 'account', 'dimensions': 'dimensions', 'region': 'region', 'unit_filter': 'unitFilter'})
class MetricStatConfig():
    def __init__(self, *, metric_name: str, namespace: str, period: aws_cdk.core.Duration, statistic: str, account: typing.Optional[str]=None, dimensions: typing.Optional[typing.List["Dimension"]]=None, region: typing.Optional[str]=None, unit_filter: typing.Optional["Unit"]=None):
        """Properties for a concrete metric.

        NOTE: ``unit`` is no longer on this object since it is only used for ``Alarms``, and doesn't mean what one
        would expect it to mean there anyway. It is most likely to be misused.

        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        :param period: How many seconds to aggregate over.
        :param statistic: Aggregation function to use (can be either simple or a percentile).
        :param account: Account which this metric comes from. Default: Deployment account.
        :param dimensions: The dimensions to apply to the alarm. Default: []
        :param region: Region which this metric comes from. Default: Deployment region.
        :param unit_filter: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. This field has been renamed from plain ``unit`` to clearly communicate its purpose. Default: - Refer to all metric datums
        """
        self._values = {
            'metric_name': metric_name,
            'namespace': namespace,
            'period': period,
            'statistic': statistic,
        }
        if account is not None: self._values["account"] = account
        if dimensions is not None: self._values["dimensions"] = dimensions
        if region is not None: self._values["region"] = region
        if unit_filter is not None: self._values["unit_filter"] = unit_filter

    @builtins.property
    def metric_name(self) -> str:
        """Name of the metric."""
        return self._values.get('metric_name')

    @builtins.property
    def namespace(self) -> str:
        """Namespace of the metric."""
        return self._values.get('namespace')

    @builtins.property
    def period(self) -> aws_cdk.core.Duration:
        """How many seconds to aggregate over."""
        return self._values.get('period')

    @builtins.property
    def statistic(self) -> str:
        """Aggregation function to use (can be either simple or a percentile)."""
        return self._values.get('statistic')

    @builtins.property
    def account(self) -> typing.Optional[str]:
        """Account which this metric comes from.

        default
        :default: Deployment account.
        """
        return self._values.get('account')

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List["Dimension"]]:
        """The dimensions to apply to the alarm.

        default
        :default: []
        """
        return self._values.get('dimensions')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Region which this metric comes from.

        default
        :default: Deployment region.
        """
        return self._values.get('region')

    @builtins.property
    def unit_filter(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        This field has been renamed from plain ``unit`` to clearly communicate
        its purpose.

        default
        :default: - Refer to all metric datums
        """
        return self._values.get('unit_filter')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricStatConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricWidgetProps", jsii_struct_bases=[], name_mapping={'height': 'height', 'region': 'region', 'title': 'title', 'width': 'width'})
class MetricWidgetProps():
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None):
        """Basic properties for widgets that display metrics.

        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        self._values = {
        }
        if height is not None: self._values["height"] = height
        if region is not None: self._values["region"] = region
        if title is not None: self._values["title"] = title
        if width is not None: self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        default
        :default: Depends on the type of widget
        """
        return self._values.get('height')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region the metrics of this graph should be taken from.

        default
        :default: Current region
        """
        return self._values.get('region')

    @builtins.property
    def title(self) -> typing.Optional[str]:
        """Title for the graph."""
        return self._values.get('title')

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        default
        :default: 6
        """
        return self._values.get('width')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricWidgetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidgetProps", jsii_struct_bases=[MetricWidgetProps], name_mapping={'height': 'height', 'region': 'region', 'title': 'title', 'width': 'width', 'alarm': 'alarm', 'left_y_axis': 'leftYAxis'})
class AlarmWidgetProps(MetricWidgetProps):
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None, alarm: "IAlarm", left_y_axis: typing.Optional["YAxisProps"]=None):
        """Properties for an AlarmWidget.

        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        :param alarm: The alarm to show.
        :param left_y_axis: Left Y axis.
        """
        if isinstance(left_y_axis, dict): left_y_axis = YAxisProps(**left_y_axis)
        self._values = {
            'alarm': alarm,
        }
        if height is not None: self._values["height"] = height
        if region is not None: self._values["region"] = region
        if title is not None: self._values["title"] = title
        if width is not None: self._values["width"] = width
        if left_y_axis is not None: self._values["left_y_axis"] = left_y_axis

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        default
        :default: Depends on the type of widget
        """
        return self._values.get('height')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region the metrics of this graph should be taken from.

        default
        :default: Current region
        """
        return self._values.get('region')

    @builtins.property
    def title(self) -> typing.Optional[str]:
        """Title for the graph."""
        return self._values.get('title')

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        default
        :default: 6
        """
        return self._values.get('width')

    @builtins.property
    def alarm(self) -> "IAlarm":
        """The alarm to show."""
        return self._values.get('alarm')

    @builtins.property
    def left_y_axis(self) -> typing.Optional["YAxisProps"]:
        """Left Y axis."""
        return self._values.get('left_y_axis')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlarmWidgetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.GraphWidgetProps", jsii_struct_bases=[MetricWidgetProps], name_mapping={'height': 'height', 'region': 'region', 'title': 'title', 'width': 'width', 'left': 'left', 'left_annotations': 'leftAnnotations', 'left_y_axis': 'leftYAxis', 'right': 'right', 'right_annotations': 'rightAnnotations', 'right_y_axis': 'rightYAxis', 'stacked': 'stacked'})
class GraphWidgetProps(MetricWidgetProps):
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None, left: typing.Optional[typing.List["IMetric"]]=None, left_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, left_y_axis: typing.Optional["YAxisProps"]=None, right: typing.Optional[typing.List["IMetric"]]=None, right_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, right_y_axis: typing.Optional["YAxisProps"]=None, stacked: typing.Optional[bool]=None):
        """Properties for a GraphWidget.

        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        :param left: Metrics to display on left Y axis.
        :param left_annotations: Annotations for the left Y axis.
        :param left_y_axis: Left Y axis.
        :param right: Metrics to display on right Y axis.
        :param right_annotations: Annotations for the right Y axis.
        :param right_y_axis: Right Y axis.
        :param stacked: Whether the graph should be shown as stacked lines.
        """
        if isinstance(left_y_axis, dict): left_y_axis = YAxisProps(**left_y_axis)
        if isinstance(right_y_axis, dict): right_y_axis = YAxisProps(**right_y_axis)
        self._values = {
        }
        if height is not None: self._values["height"] = height
        if region is not None: self._values["region"] = region
        if title is not None: self._values["title"] = title
        if width is not None: self._values["width"] = width
        if left is not None: self._values["left"] = left
        if left_annotations is not None: self._values["left_annotations"] = left_annotations
        if left_y_axis is not None: self._values["left_y_axis"] = left_y_axis
        if right is not None: self._values["right"] = right
        if right_annotations is not None: self._values["right_annotations"] = right_annotations
        if right_y_axis is not None: self._values["right_y_axis"] = right_y_axis
        if stacked is not None: self._values["stacked"] = stacked

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        default
        :default: Depends on the type of widget
        """
        return self._values.get('height')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region the metrics of this graph should be taken from.

        default
        :default: Current region
        """
        return self._values.get('region')

    @builtins.property
    def title(self) -> typing.Optional[str]:
        """Title for the graph."""
        return self._values.get('title')

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        default
        :default: 6
        """
        return self._values.get('width')

    @builtins.property
    def left(self) -> typing.Optional[typing.List["IMetric"]]:
        """Metrics to display on left Y axis."""
        return self._values.get('left')

    @builtins.property
    def left_annotations(self) -> typing.Optional[typing.List["HorizontalAnnotation"]]:
        """Annotations for the left Y axis."""
        return self._values.get('left_annotations')

    @builtins.property
    def left_y_axis(self) -> typing.Optional["YAxisProps"]:
        """Left Y axis."""
        return self._values.get('left_y_axis')

    @builtins.property
    def right(self) -> typing.Optional[typing.List["IMetric"]]:
        """Metrics to display on right Y axis."""
        return self._values.get('right')

    @builtins.property
    def right_annotations(self) -> typing.Optional[typing.List["HorizontalAnnotation"]]:
        """Annotations for the right Y axis."""
        return self._values.get('right_annotations')

    @builtins.property
    def right_y_axis(self) -> typing.Optional["YAxisProps"]:
        """Right Y axis."""
        return self._values.get('right_y_axis')

    @builtins.property
    def stacked(self) -> typing.Optional[bool]:
        """Whether the graph should be shown as stacked lines."""
        return self._values.get('stacked')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GraphWidgetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.PeriodOverride")
class PeriodOverride(enum.Enum):
    AUTO = "AUTO"
    INHERIT = "INHERIT"

@jsii.implements(IWidget)
class Row(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Row"):
    """A widget that contains other widgets in a horizontal row.

    Widgets will be laid out next to each other
    """
    def __init__(self, *widgets: "IWidget") -> None:
        """
        :param widgets: -
        """
        jsii.create(Row, self, [*widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Shading")
class Shading(enum.Enum):
    NONE = "NONE"
    """Don't add shading."""
    ABOVE = "ABOVE"
    """Add shading above the annotation."""
    BELOW = "BELOW"
    """Add shading below the annotation."""

class SingleValueWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidget"):
    """A dashboard widget that displays the most recent value for every metric."""
    def __init__(self, *, metrics: typing.List["IMetric"], set_period_to_time_range: typing.Optional[bool]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        :param metrics: Metrics to display.
        :param set_period_to_time_range: Whether to show the value from the entire time range. Default: false
        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = SingleValueWidgetProps(metrics=metrics, set_period_to_time_range=set_period_to_time_range, height=height, region=region, title=title, width=width)

        jsii.create(SingleValueWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidgetProps", jsii_struct_bases=[MetricWidgetProps], name_mapping={'height': 'height', 'region': 'region', 'title': 'title', 'width': 'width', 'metrics': 'metrics', 'set_period_to_time_range': 'setPeriodToTimeRange'})
class SingleValueWidgetProps(MetricWidgetProps):
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None, metrics: typing.List["IMetric"], set_period_to_time_range: typing.Optional[bool]=None):
        """Properties for a SingleValueWidget.

        :param height: Height of the widget. Default: Depends on the type of widget
        :param region: The region the metrics of this graph should be taken from. Default: Current region
        :param title: Title for the graph.
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        :param metrics: Metrics to display.
        :param set_period_to_time_range: Whether to show the value from the entire time range. Default: false
        """
        self._values = {
            'metrics': metrics,
        }
        if height is not None: self._values["height"] = height
        if region is not None: self._values["region"] = region
        if title is not None: self._values["title"] = title
        if width is not None: self._values["width"] = width
        if set_period_to_time_range is not None: self._values["set_period_to_time_range"] = set_period_to_time_range

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        default
        :default: Depends on the type of widget
        """
        return self._values.get('height')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region the metrics of this graph should be taken from.

        default
        :default: Current region
        """
        return self._values.get('region')

    @builtins.property
    def title(self) -> typing.Optional[str]:
        """Title for the graph."""
        return self._values.get('title')

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        default
        :default: 6
        """
        return self._values.get('width')

    @builtins.property
    def metrics(self) -> typing.List["IMetric"]:
        """Metrics to display."""
        return self._values.get('metrics')

    @builtins.property
    def set_period_to_time_range(self) -> typing.Optional[bool]:
        """Whether to show the value from the entire time range.

        default
        :default: false
        """
        return self._values.get('set_period_to_time_range')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SingleValueWidgetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IWidget)
class Spacer(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Spacer"):
    """A widget that doesn't display anything but takes up space."""
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        :param height: Height of the spacer. Default: : 1
        :param width: Width of the spacer. Default: 1
        """
        props = SpacerProps(height=height, width=width)

        jsii.create(Spacer, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, _x: jsii.Number, _y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param _x: -
        :param _y: -
        """
        return jsii.invoke(self, "position", [_x, _y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.SpacerProps", jsii_struct_bases=[], name_mapping={'height': 'height', 'width': 'width'})
class SpacerProps():
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None):
        """Props of the spacer.

        :param height: Height of the spacer. Default: : 1
        :param width: Width of the spacer. Default: 1
        """
        self._values = {
        }
        if height is not None: self._values["height"] = height
        if width is not None: self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the spacer.

        default
        :default: : 1
        """
        return self._values.get('height')

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the spacer.

        default
        :default: 1
        """
        return self._values.get('width')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SpacerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Statistic")
class Statistic(enum.Enum):
    """Statistic to use over the aggregation period."""
    SAMPLE_COUNT = "SAMPLE_COUNT"
    AVERAGE = "AVERAGE"
    SUM = "SUM"
    MINIMUM = "MINIMUM"
    MAXIMUM = "MAXIMUM"

class TextWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.TextWidget"):
    """A dashboard widget that displays MarkDown."""
    def __init__(self, *, markdown: str, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        :param markdown: The text to display, in MarkDown format.
        :param height: Height of the widget. Default: 2
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = TextWidgetProps(markdown=markdown, height=height, width=width)

        jsii.create(TextWidget, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.TextWidgetProps", jsii_struct_bases=[], name_mapping={'markdown': 'markdown', 'height': 'height', 'width': 'width'})
class TextWidgetProps():
    def __init__(self, *, markdown: str, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None):
        """Properties for a Text widget.

        :param markdown: The text to display, in MarkDown format.
        :param height: Height of the widget. Default: 2
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        self._values = {
            'markdown': markdown,
        }
        if height is not None: self._values["height"] = height
        if width is not None: self._values["width"] = width

    @builtins.property
    def markdown(self) -> str:
        """The text to display, in MarkDown format."""
        return self._values.get('markdown')

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        default
        :default: 2
        """
        return self._values.get('height')

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        default
        :default: 6
        """
        return self._values.get('width')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TextWidgetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.TreatMissingData")
class TreatMissingData(enum.Enum):
    """Specify how missing data points are treated during alarm evaluation."""
    BREACHING = "BREACHING"
    """Missing data points are treated as breaching the threshold."""
    NOT_BREACHING = "NOT_BREACHING"
    """Missing data points are treated as being within the threshold."""
    IGNORE = "IGNORE"
    """The current alarm state is maintained."""
    MISSING = "MISSING"
    """The alarm does not consider missing data points when evaluating whether to change state."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Unit")
class Unit(enum.Enum):
    """Unit for metric."""
    SECONDS = "SECONDS"
    MICROSECONDS = "MICROSECONDS"
    MILLISECONDS = "MILLISECONDS"
    BYTES = "BYTES"
    KILOBYTES = "KILOBYTES"
    MEGABYTES = "MEGABYTES"
    GIGABYTES = "GIGABYTES"
    TERABYTES = "TERABYTES"
    BITS = "BITS"
    KILOBITS = "KILOBITS"
    MEGABITS = "MEGABITS"
    GIGABITS = "GIGABITS"
    TERABITS = "TERABITS"
    PERCENT = "PERCENT"
    COUNT = "COUNT"
    BYTES_PER_SECOND = "BYTES_PER_SECOND"
    KILOBYTES_PER_SECOND = "KILOBYTES_PER_SECOND"
    MEGABYTES_PER_SECOND = "MEGABYTES_PER_SECOND"
    GIGABYTES_PER_SECOND = "GIGABYTES_PER_SECOND"
    TERABYTES_PER_SECOND = "TERABYTES_PER_SECOND"
    BITS_PER_SECOND = "BITS_PER_SECOND"
    KILOBITS_PER_SECOND = "KILOBITS_PER_SECOND"
    MEGABITS_PER_SECOND = "MEGABITS_PER_SECOND"
    GIGABITS_PER_SECOND = "GIGABITS_PER_SECOND"
    TERABITS_PER_SECOND = "TERABITS_PER_SECOND"
    COUNT_PER_SECOND = "COUNT_PER_SECOND"
    NONE = "NONE"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.YAxisProps", jsii_struct_bases=[], name_mapping={'label': 'label', 'max': 'max', 'min': 'min', 'show_units': 'showUnits'})
class YAxisProps():
    def __init__(self, *, label: typing.Optional[str]=None, max: typing.Optional[jsii.Number]=None, min: typing.Optional[jsii.Number]=None, show_units: typing.Optional[bool]=None):
        """Properties for a Y-Axis.

        :param label: The label. Default: No label
        :param max: The max value. Default: No maximum value
        :param min: The min value. Default: 0
        :param show_units: Whether to show units. Default: true
        """
        self._values = {
        }
        if label is not None: self._values["label"] = label
        if max is not None: self._values["max"] = max
        if min is not None: self._values["min"] = min
        if show_units is not None: self._values["show_units"] = show_units

    @builtins.property
    def label(self) -> typing.Optional[str]:
        """The label.

        default
        :default: No label
        """
        return self._values.get('label')

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        """The max value.

        default
        :default: No maximum value
        """
        return self._values.get('max')

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """The min value.

        default
        :default: 0
        """
        return self._values.get('min')

    @builtins.property
    def show_units(self) -> typing.Optional[bool]:
        """Whether to show units.

        default
        :default: true
        """
        return self._values.get('show_units')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'YAxisProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["Alarm", "AlarmActionConfig", "AlarmProps", "AlarmWidget", "AlarmWidgetProps", "CfnAlarm", "CfnAlarmProps", "CfnAnomalyDetector", "CfnAnomalyDetectorProps", "CfnDashboard", "CfnDashboardProps", "CfnInsightRule", "CfnInsightRuleProps", "Column", "CommonMetricOptions", "ComparisonOperator", "ConcreteWidget", "CreateAlarmOptions", "Dashboard", "DashboardProps", "Dimension", "GraphWidget", "GraphWidgetProps", "HorizontalAnnotation", "IAlarm", "IAlarmAction", "IMetric", "IWidget", "MathExpression", "MathExpressionOptions", "MathExpressionProps", "Metric", "MetricAlarmConfig", "MetricConfig", "MetricExpressionConfig", "MetricGraphConfig", "MetricOptions", "MetricProps", "MetricRenderingProperties", "MetricStatConfig", "MetricWidgetProps", "PeriodOverride", "Row", "Shading", "SingleValueWidget", "SingleValueWidgetProps", "Spacer", "SpacerProps", "Statistic", "TextWidget", "TextWidgetProps", "TreatMissingData", "Unit", "YAxisProps", "__jsii_assembly__"]

publication.publish()
