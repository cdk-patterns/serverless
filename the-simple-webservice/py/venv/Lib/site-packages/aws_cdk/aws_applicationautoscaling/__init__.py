"""
## AWS Auto Scaling Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

**Application AutoScaling** is used to configure autoscaling for all
services other than scaling EC2 instances. For example, you will use this to
scale ECS tasks, DynamoDB capacity, Spot Fleet sizes and more.

As a CDK user, you will probably not have to interact with this library
directly; instead, it will be used by other construct libraries to
offer AutoScaling features for their own constructs.

This document will describe the general autoscaling features and concepts;
your particular service may offer only a subset of these.

### AutoScaling basics

Resources can offer one or more **attributes** to autoscale, typically
representing some capacity dimension of the underlying service. For example,
a DynamoDB Table offers autoscaling of the read and write capacity of the
table proper and its Global Secondary Indexes, an ECS Service offers
autoscaling of its task count, an RDS Aurora cluster offers scaling of its
replica count, and so on.

When you enable autoscaling for an attribute, you specify a minimum and a
maximum value for the capacity. AutoScaling policies that respond to metrics
will never go higher or lower than the indicated capacity (but scheduled
scaling actions might, see below).

There are three ways to scale your capacity:

* **In response to a metric** (also known as step scaling); for example, you
  might want to scale out if the CPU usage across your cluster starts to rise,
  and scale in when it drops again.
* **By trying to keep a certain metric around a given value** (also known as
  target tracking scaling); you might want to automatically scale out an in to
  keep your CPU usage around 50%.
* **On a schedule**; you might want to organize your scaling around traffic
  flows you expect, by scaling out in the morning and scaling in in the
  evening.

The general pattern of autoscaling will look like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
capacity = resource.auto_scale_capacity(
    min_capacity=5,
    max_capacity=100
)

# Enable a type of metric scaling and/or schedule scaling
capacity.scale_on_metric(...)
capacity.scale_to_track_metric(...)
capacity.scale_on_schedule(...)
```

### Step Scaling

This type of scaling scales in and out in deterministic steps that you
configure, in response to metric values. For example, your scaling strategy
to scale in response to CPU usage might look like this:

```
 Scaling        -1          (no change)          +1       +3
            │        │                       │        │        │
            ├────────┼───────────────────────┼────────┼────────┤
            │        │                       │        │        │
CPU usage   0%      10%                     50%       70%     100%
```

(Note that this is not necessarily a recommended scaling strategy, but it's
a possible one. You will have to determine what thresholds are right for you).

You would configure it like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
capacity.scale_on_metric("ScaleToCPU",
    metric=service.metric_cpu_utilization(),
    scaling_steps=[{"upper": 10, "change": -1}, {"lower": 50, "change": +1}, {"lower": 70, "change": +3}
    ],

    # Change this to AdjustmentType.PercentChangeInCapacity to interpret the
    # 'change' numbers before as percentages instead of capacity counts.
    adjustment_type=autoscaling.AdjustmentType.CHANGE_IN_CAPACITY
)
```

The AutoScaling construct library will create the required CloudWatch alarms and
AutoScaling policies for you.

### Target Tracking Scaling

This type of scaling scales in and out in order to keep a metric (typically
representing utilization) around a value you prefer. This type of scaling is
typically heavily service-dependent in what metric you can use, and so
different services will have different methods here to set up target tracking
scaling.

The following example configures the read capacity of a DynamoDB table
to be around 60% utilization:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
read_capacity = table.auto_scale_read_capacity(
    min_capacity=10,
    max_capacity=1000
)
read_capacity.scale_on_utilization(
    target_utilization_percent=60
)
```

### Scheduled Scaling

This type of scaling is used to change capacities based on time. It works
by changing the `minCapacity` and `maxCapacity` of the attribute, and so
can be used for two purposes:

* Scale in and out on a schedule by setting the `minCapacity` high or
  the `maxCapacity` low.
* Still allow the regular scaling actions to do their job, but restrict
  the range they can scale over (by setting both `minCapacity` and
  `maxCapacity` but changing their range over time).

The following schedule expressions can be used:

* `at(yyyy-mm-ddThh:mm:ss)` -- scale at a particular moment in time
* `rate(value unit)` -- scale every minute/hour/day
* `cron(mm hh dd mm dow)` -- scale on arbitrary schedules

Of these, the cron expression is the most useful but also the most
complicated. A schedule is expressed as a cron expression. The `Schedule` class has a `cron` method to help build cron expressions.

The following example scales the fleet out in the morning, and lets natural
scaling take over at night:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
capacity = resource.auto_scale_capacity(
    min_capacity=1,
    max_capacity=50
)

capacity.scale_on_schedule("PrescaleInTheMorning",
    schedule=autoscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=20
)

capacity.scale_on_schedule("AllowDownscalingAtNight",
    schedule=autoscaling.Schedule.cron(hour="20", minute="0"),
    min_capacity=1
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

import aws_cdk.aws_autoscaling_common
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-applicationautoscaling", "1.23.0", __name__, "aws-applicationautoscaling@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.AdjustmentTier", jsii_struct_bases=[], name_mapping={'adjustment': 'adjustment', 'lower_bound': 'lowerBound', 'upper_bound': 'upperBound'})
class AdjustmentTier():
    def __init__(self, *, adjustment: jsii.Number, lower_bound: typing.Optional[jsii.Number]=None, upper_bound: typing.Optional[jsii.Number]=None):
        """An adjustment.

        :param adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
        :param lower_bound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        :param upper_bound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        self._values = {
            'adjustment': adjustment,
        }
        if lower_bound is not None: self._values["lower_bound"] = lower_bound
        if upper_bound is not None: self._values["upper_bound"] = upper_bound

    @builtins.property
    def adjustment(self) -> jsii.Number:
        """What number to adjust the capacity with.

        The number is interpeted as an added capacity, a new fixed capacity or an
        added percentage depending on the AdjustmentType value of the
        StepScalingPolicy.

        Can be positive or negative.
        """
        return self._values.get('adjustment')

    @builtins.property
    def lower_bound(self) -> typing.Optional[jsii.Number]:
        """Lower bound where this scaling tier applies.

        The scaling tier applies if the difference between the metric
        value and its alarm threshold is higher than this value.

        default
        :default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        """
        return self._values.get('lower_bound')

    @builtins.property
    def upper_bound(self) -> typing.Optional[jsii.Number]:
        """Upper bound where this scaling tier applies.

        The scaling tier applies if the difference between the metric
        value and its alarm threshold is lower than this value.

        default
        :default: +Infinity
        """
        return self._values.get('upper_bound')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AdjustmentTier(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.AdjustmentType")
class AdjustmentType(enum.Enum):
    """How adjustment numbers are interpreted."""
    CHANGE_IN_CAPACITY = "CHANGE_IN_CAPACITY"
    """Add the adjustment number to the current capacity.

    A positive number increases capacity, a negative number decreases capacity.
    """
    PERCENT_CHANGE_IN_CAPACITY = "PERCENT_CHANGE_IN_CAPACITY"
    """Add this percentage of the current capacity to itself.

    The number must be between -100 and 100; a positive number increases
    capacity and a negative number decreases it.
    """
    EXACT_CAPACITY = "EXACT_CAPACITY"
    """Make the capacity equal to the exact number given."""

class BaseScalableAttribute(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-applicationautoscaling.BaseScalableAttribute"):
    """Represent an attribute for which autoscaling can be configured.

    This class is basically a light wrapper around ScalableTarget, but with
    all methods protected instead of public so they can be selectively
    exposed and/or more specific versions of them can be exposed by derived
    classes for individual services support autoscaling.

    Typical use cases:

    - Hide away the PredefinedMetric enum for target tracking policies.
    - Don't expose all scaling methods (for example Dynamo tables don't support
      Step Scaling, so the Dynamo subclass won't expose this method).
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseScalableAttributeProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: "ServiceNamespace", max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param dimension: Scalable dimension of the attribute.
        :param resource_id: Resource ID of the attribute.
        :param role: Role to use for scaling.
        :param service_namespace: Service namespace of the scalable attribute.
        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        """
        props = BaseScalableAttributeProps(dimension=dimension, resource_id=resource_id, role=role, service_namespace=service_namespace, max_capacity=max_capacity, min_capacity=min_capacity)

        jsii.create(BaseScalableAttribute, self, [scope, id, props])

    @jsii.member(jsii_name="doScaleOnMetric")
    def _do_scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """Scale out or in based on a metric value.

        :param id: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = BasicStepScalingPolicyProps(metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, min_adjustment_magnitude=min_adjustment_magnitude)

        return jsii.invoke(self, "doScaleOnMetric", [id, props])

    @jsii.member(jsii_name="doScaleOnSchedule")
    def _do_scale_on_schedule(self, id: str, *, schedule: "Schedule", end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scale out or in based on time.

        :param id: -
        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        props = ScalingSchedule(schedule=schedule, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        return jsii.invoke(self, "doScaleOnSchedule", [id, props])

    @jsii.member(jsii_name="doScaleToTrackMetric")
    def _do_scale_to_track_metric(self, id: str, *, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
        :param resource_label: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = BasicTargetTrackingScalingPolicyProps(target_value=target_value, custom_metric=custom_metric, predefined_metric=predefined_metric, resource_label=resource_label, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "doScaleToTrackMetric", [id, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "BaseScalableAttributeProps":
        return jsii.get(self, "props")


class _BaseScalableAttributeProxy(BaseScalableAttribute):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BaseTargetTrackingProps", jsii_struct_bases=[], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown'})
class BaseTargetTrackingProps():
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None):
        """Base interface for target tracking props.

        Contains the attributes that are common to target tracking policies,
        except the ones relating to the metric and to the scalable target.

        This interface is reused by more specific target tracking props objects
        in other services.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        self._values = {
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseTargetTrackingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BasicStepScalingPolicyProps", jsii_struct_bases=[], name_mapping={'metric': 'metric', 'scaling_steps': 'scalingSteps', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'min_adjustment_magnitude': 'minAdjustmentMagnitude'})
class BasicStepScalingPolicyProps():
    def __init__(self, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None):
        """
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        self._values = {
            'metric': metric,
            'scaling_steps': scaling_steps,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @builtins.property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to scale on."""
        return self._values.get('metric')

    @builtins.property
    def scaling_steps(self) -> typing.List["ScalingInterval"]:
        """The intervals for scaling.

        Maps a range of metric values to a particular scaling behavior.
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def adjustment_type(self) -> typing.Optional["AdjustmentType"]:
        """How the adjustment numbers inside 'intervals' are interpreted.

        default
        :default: ChangeInCapacity
        """
        return self._values.get('adjustment_type')

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        Subsequent scale outs during the cooldown period are squashed so that only
        the biggest scale out happens.

        Subsequent scale ins during the cooldown period are ignored.

        default
        :default: No cooldown period

        see
        :see: https://docs.aws.amazon.com/autoscaling/application/APIReference/API_StepScalingPolicyConfiguration.html
        """
        return self._values.get('cooldown')

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        default
        :default: No minimum scaling effect
        """
        return self._values.get('min_adjustment_magnitude')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicStepScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BasicTargetTrackingScalingPolicyProps", jsii_struct_bases=[BaseTargetTrackingProps], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'target_value': 'targetValue', 'custom_metric': 'customMetric', 'predefined_metric': 'predefinedMetric', 'resource_label': 'resourceLabel'})
class BasicTargetTrackingScalingPolicyProps(BaseTargetTrackingProps):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None):
        """Properties for a Target Tracking policy that include the metric but exclude the target.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
        :param resource_label: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
        """
        self._values = {
            'target_value': target_value,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown
        if custom_metric is not None: self._values["custom_metric"] = custom_metric
        if predefined_metric is not None: self._values["predefined_metric"] = predefined_metric
        if resource_label is not None: self._values["resource_label"] = resource_label

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    @builtins.property
    def target_value(self) -> jsii.Number:
        """The target value for the metric."""
        return self._values.get('target_value')

    @builtins.property
    def custom_metric(self) -> typing.Optional[aws_cdk.aws_cloudwatch.IMetric]:
        """A custom metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No custom metric.
        """
        return self._values.get('custom_metric')

    @builtins.property
    def predefined_metric(self) -> typing.Optional["PredefinedMetric"]:
        """A predefined metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No predefined metrics.
        """
        return self._values.get('predefined_metric')

    @builtins.property
    def resource_label(self) -> typing.Optional[str]:
        """Identify the resource associated with the metric type.

        Only used for predefined metric ALBRequestCountPerTarget.

        default
        :default: - No resource label.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / <load-balancer - name > /<load-balancer-id>/targetgroup / <target-group - name > /<target-group-id>
        """
        return self._values.get('resource_label')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicTargetTrackingScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScalableTarget(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget"):
    """A CloudFormation ``AWS::ApplicationAutoScaling::ScalableTarget``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApplicationAutoScaling::ScalableTarget
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number, resource_id: str, role_arn: str, scalable_dimension: str, service_namespace: str, scheduled_actions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ScheduledActionProperty", aws_cdk.core.IResolvable]]]]]=None, suspended_state: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SuspendedStateProperty"]]]=None) -> None:
        """Create a new ``AWS::ApplicationAutoScaling::ScalableTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param max_capacity: ``AWS::ApplicationAutoScaling::ScalableTarget.MaxCapacity``.
        :param min_capacity: ``AWS::ApplicationAutoScaling::ScalableTarget.MinCapacity``.
        :param resource_id: ``AWS::ApplicationAutoScaling::ScalableTarget.ResourceId``.
        :param role_arn: ``AWS::ApplicationAutoScaling::ScalableTarget.RoleARN``.
        :param scalable_dimension: ``AWS::ApplicationAutoScaling::ScalableTarget.ScalableDimension``.
        :param service_namespace: ``AWS::ApplicationAutoScaling::ScalableTarget.ServiceNamespace``.
        :param scheduled_actions: ``AWS::ApplicationAutoScaling::ScalableTarget.ScheduledActions``.
        :param suspended_state: ``AWS::ApplicationAutoScaling::ScalableTarget.SuspendedState``.
        """
        props = CfnScalableTargetProps(max_capacity=max_capacity, min_capacity=min_capacity, resource_id=resource_id, role_arn=role_arn, scalable_dimension=scalable_dimension, service_namespace=service_namespace, scheduled_actions=scheduled_actions, suspended_state=suspended_state)

        jsii.create(CfnScalableTarget, self, [scope, id, props])

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
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        """``AWS::ApplicationAutoScaling::ScalableTarget.MaxCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-maxcapacity
        """
        return jsii.get(self, "maxCapacity")

    @max_capacity.setter
    def max_capacity(self, value: jsii.Number):
        jsii.set(self, "maxCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="minCapacity")
    def min_capacity(self) -> jsii.Number:
        """``AWS::ApplicationAutoScaling::ScalableTarget.MinCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-mincapacity
        """
        return jsii.get(self, "minCapacity")

    @min_capacity.setter
    def min_capacity(self, value: jsii.Number):
        jsii.set(self, "minCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ResourceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-resourceid
        """
        return jsii.get(self, "resourceId")

    @resource_id.setter
    def resource_id(self, value: str):
        jsii.set(self, "resourceId", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str):
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="scalableDimension")
    def scalable_dimension(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ScalableDimension``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scalabledimension
        """
        return jsii.get(self, "scalableDimension")

    @scalable_dimension.setter
    def scalable_dimension(self, value: str):
        jsii.set(self, "scalableDimension", value)

    @builtins.property
    @jsii.member(jsii_name="serviceNamespace")
    def service_namespace(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ServiceNamespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-servicenamespace
        """
        return jsii.get(self, "serviceNamespace")

    @service_namespace.setter
    def service_namespace(self, value: str):
        jsii.set(self, "serviceNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="scheduledActions")
    def scheduled_actions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ScheduledActionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ScheduledActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scheduledactions
        """
        return jsii.get(self, "scheduledActions")

    @scheduled_actions.setter
    def scheduled_actions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ScheduledActionProperty", aws_cdk.core.IResolvable]]]]]):
        jsii.set(self, "scheduledActions", value)

    @builtins.property
    @jsii.member(jsii_name="suspendedState")
    def suspended_state(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SuspendedStateProperty"]]]:
        """``AWS::ApplicationAutoScaling::ScalableTarget.SuspendedState``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-suspendedstate
        """
        return jsii.get(self, "suspendedState")

    @suspended_state.setter
    def suspended_state(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SuspendedStateProperty"]]]):
        jsii.set(self, "suspendedState", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.ScalableTargetActionProperty", jsii_struct_bases=[], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity'})
    class ScalableTargetActionProperty():
        def __init__(self, *, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None):
            """
            :param max_capacity: ``CfnScalableTarget.ScalableTargetActionProperty.MaxCapacity``.
            :param min_capacity: ``CfnScalableTarget.ScalableTargetActionProperty.MinCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html
            """
            self._values = {
            }
            if max_capacity is not None: self._values["max_capacity"] = max_capacity
            if min_capacity is not None: self._values["min_capacity"] = min_capacity

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnScalableTarget.ScalableTargetActionProperty.MaxCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html#cfn-applicationautoscaling-scalabletarget-scalabletargetaction-maxcapacity
            """
            return self._values.get('max_capacity')

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnScalableTarget.ScalableTargetActionProperty.MinCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html#cfn-applicationautoscaling-scalabletarget-scalabletargetaction-mincapacity
            """
            return self._values.get('min_capacity')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalableTargetActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.ScheduledActionProperty", jsii_struct_bases=[], name_mapping={'schedule': 'schedule', 'scheduled_action_name': 'scheduledActionName', 'end_time': 'endTime', 'scalable_target_action': 'scalableTargetAction', 'start_time': 'startTime'})
    class ScheduledActionProperty():
        def __init__(self, *, schedule: str, scheduled_action_name: str, end_time: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]=None, scalable_target_action: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalableTarget.ScalableTargetActionProperty"]]]=None, start_time: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]=None):
            """
            :param schedule: ``CfnScalableTarget.ScheduledActionProperty.Schedule``.
            :param scheduled_action_name: ``CfnScalableTarget.ScheduledActionProperty.ScheduledActionName``.
            :param end_time: ``CfnScalableTarget.ScheduledActionProperty.EndTime``.
            :param scalable_target_action: ``CfnScalableTarget.ScheduledActionProperty.ScalableTargetAction``.
            :param start_time: ``CfnScalableTarget.ScheduledActionProperty.StartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html
            """
            self._values = {
                'schedule': schedule,
                'scheduled_action_name': scheduled_action_name,
            }
            if end_time is not None: self._values["end_time"] = end_time
            if scalable_target_action is not None: self._values["scalable_target_action"] = scalable_target_action
            if start_time is not None: self._values["start_time"] = start_time

        @builtins.property
        def schedule(self) -> str:
            """``CfnScalableTarget.ScheduledActionProperty.Schedule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-schedule
            """
            return self._values.get('schedule')

        @builtins.property
        def scheduled_action_name(self) -> str:
            """``CfnScalableTarget.ScheduledActionProperty.ScheduledActionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-scheduledactionname
            """
            return self._values.get('scheduled_action_name')

        @builtins.property
        def end_time(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]:
            """``CfnScalableTarget.ScheduledActionProperty.EndTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-endtime
            """
            return self._values.get('end_time')

        @builtins.property
        def scalable_target_action(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalableTarget.ScalableTargetActionProperty"]]]:
            """``CfnScalableTarget.ScheduledActionProperty.ScalableTargetAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-scalabletargetaction
            """
            return self._values.get('scalable_target_action')

        @builtins.property
        def start_time(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[datetime.datetime]]]:
            """``CfnScalableTarget.ScheduledActionProperty.StartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-starttime
            """
            return self._values.get('start_time')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScheduledActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.SuspendedStateProperty", jsii_struct_bases=[], name_mapping={'dynamic_scaling_in_suspended': 'dynamicScalingInSuspended', 'dynamic_scaling_out_suspended': 'dynamicScalingOutSuspended', 'scheduled_scaling_suspended': 'scheduledScalingSuspended'})
    class SuspendedStateProperty():
        def __init__(self, *, dynamic_scaling_in_suspended: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, dynamic_scaling_out_suspended: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, scheduled_scaling_suspended: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param dynamic_scaling_in_suspended: ``CfnScalableTarget.SuspendedStateProperty.DynamicScalingInSuspended``.
            :param dynamic_scaling_out_suspended: ``CfnScalableTarget.SuspendedStateProperty.DynamicScalingOutSuspended``.
            :param scheduled_scaling_suspended: ``CfnScalableTarget.SuspendedStateProperty.ScheduledScalingSuspended``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html
            """
            self._values = {
            }
            if dynamic_scaling_in_suspended is not None: self._values["dynamic_scaling_in_suspended"] = dynamic_scaling_in_suspended
            if dynamic_scaling_out_suspended is not None: self._values["dynamic_scaling_out_suspended"] = dynamic_scaling_out_suspended
            if scheduled_scaling_suspended is not None: self._values["scheduled_scaling_suspended"] = scheduled_scaling_suspended

        @builtins.property
        def dynamic_scaling_in_suspended(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnScalableTarget.SuspendedStateProperty.DynamicScalingInSuspended``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html#cfn-applicationautoscaling-scalabletarget-suspendedstate-dynamicscalinginsuspended
            """
            return self._values.get('dynamic_scaling_in_suspended')

        @builtins.property
        def dynamic_scaling_out_suspended(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnScalableTarget.SuspendedStateProperty.DynamicScalingOutSuspended``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html#cfn-applicationautoscaling-scalabletarget-suspendedstate-dynamicscalingoutsuspended
            """
            return self._values.get('dynamic_scaling_out_suspended')

        @builtins.property
        def scheduled_scaling_suspended(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnScalableTarget.SuspendedStateProperty.ScheduledScalingSuspended``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html#cfn-applicationautoscaling-scalabletarget-suspendedstate-scheduledscalingsuspended
            """
            return self._values.get('scheduled_scaling_suspended')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SuspendedStateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTargetProps", jsii_struct_bases=[], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'resource_id': 'resourceId', 'role_arn': 'roleArn', 'scalable_dimension': 'scalableDimension', 'service_namespace': 'serviceNamespace', 'scheduled_actions': 'scheduledActions', 'suspended_state': 'suspendedState'})
class CfnScalableTargetProps():
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number, resource_id: str, role_arn: str, scalable_dimension: str, service_namespace: str, scheduled_actions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnScalableTarget.ScheduledActionProperty", aws_cdk.core.IResolvable]]]]]=None, suspended_state: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalableTarget.SuspendedStateProperty"]]]=None):
        """Properties for defining a ``AWS::ApplicationAutoScaling::ScalableTarget``.

        :param max_capacity: ``AWS::ApplicationAutoScaling::ScalableTarget.MaxCapacity``.
        :param min_capacity: ``AWS::ApplicationAutoScaling::ScalableTarget.MinCapacity``.
        :param resource_id: ``AWS::ApplicationAutoScaling::ScalableTarget.ResourceId``.
        :param role_arn: ``AWS::ApplicationAutoScaling::ScalableTarget.RoleARN``.
        :param scalable_dimension: ``AWS::ApplicationAutoScaling::ScalableTarget.ScalableDimension``.
        :param service_namespace: ``AWS::ApplicationAutoScaling::ScalableTarget.ServiceNamespace``.
        :param scheduled_actions: ``AWS::ApplicationAutoScaling::ScalableTarget.ScheduledActions``.
        :param suspended_state: ``AWS::ApplicationAutoScaling::ScalableTarget.SuspendedState``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html
        """
        self._values = {
            'max_capacity': max_capacity,
            'min_capacity': min_capacity,
            'resource_id': resource_id,
            'role_arn': role_arn,
            'scalable_dimension': scalable_dimension,
            'service_namespace': service_namespace,
        }
        if scheduled_actions is not None: self._values["scheduled_actions"] = scheduled_actions
        if suspended_state is not None: self._values["suspended_state"] = suspended_state

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        """``AWS::ApplicationAutoScaling::ScalableTarget.MaxCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-maxcapacity
        """
        return self._values.get('max_capacity')

    @builtins.property
    def min_capacity(self) -> jsii.Number:
        """``AWS::ApplicationAutoScaling::ScalableTarget.MinCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-mincapacity
        """
        return self._values.get('min_capacity')

    @builtins.property
    def resource_id(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ResourceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-resourceid
        """
        return self._values.get('resource_id')

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def scalable_dimension(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ScalableDimension``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scalabledimension
        """
        return self._values.get('scalable_dimension')

    @builtins.property
    def service_namespace(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ServiceNamespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-servicenamespace
        """
        return self._values.get('service_namespace')

    @builtins.property
    def scheduled_actions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnScalableTarget.ScheduledActionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ApplicationAutoScaling::ScalableTarget.ScheduledActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scheduledactions
        """
        return self._values.get('scheduled_actions')

    @builtins.property
    def suspended_state(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalableTarget.SuspendedStateProperty"]]]:
        """``AWS::ApplicationAutoScaling::ScalableTarget.SuspendedState``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-suspendedstate
        """
        return self._values.get('suspended_state')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnScalableTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScalingPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy"):
    """A CloudFormation ``AWS::ApplicationAutoScaling::ScalingPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApplicationAutoScaling::ScalingPolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, policy_name: str, policy_type: str, resource_id: typing.Optional[str]=None, scalable_dimension: typing.Optional[str]=None, scaling_target_id: typing.Optional[str]=None, service_namespace: typing.Optional[str]=None, step_scaling_policy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StepScalingPolicyConfigurationProperty"]]]=None, target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TargetTrackingScalingPolicyConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::ApplicationAutoScaling::ScalingPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_name: ``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyName``.
        :param policy_type: ``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyType``.
        :param resource_id: ``AWS::ApplicationAutoScaling::ScalingPolicy.ResourceId``.
        :param scalable_dimension: ``AWS::ApplicationAutoScaling::ScalingPolicy.ScalableDimension``.
        :param scaling_target_id: ``AWS::ApplicationAutoScaling::ScalingPolicy.ScalingTargetId``.
        :param service_namespace: ``AWS::ApplicationAutoScaling::ScalingPolicy.ServiceNamespace``.
        :param step_scaling_policy_configuration: ``AWS::ApplicationAutoScaling::ScalingPolicy.StepScalingPolicyConfiguration``.
        :param target_tracking_scaling_policy_configuration: ``AWS::ApplicationAutoScaling::ScalingPolicy.TargetTrackingScalingPolicyConfiguration``.
        """
        props = CfnScalingPolicyProps(policy_name=policy_name, policy_type=policy_type, resource_id=resource_id, scalable_dimension=scalable_dimension, scaling_target_id=scaling_target_id, service_namespace=service_namespace, step_scaling_policy_configuration=step_scaling_policy_configuration, target_tracking_scaling_policy_configuration=target_tracking_scaling_policy_configuration)

        jsii.create(CfnScalingPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policyname
        """
        return jsii.get(self, "policyName")

    @policy_name.setter
    def policy_name(self, value: str):
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policytype
        """
        return jsii.get(self, "policyType")

    @policy_type.setter
    def policy_type(self, value: str):
        jsii.set(self, "policyType", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ResourceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-resourceid
        """
        return jsii.get(self, "resourceId")

    @resource_id.setter
    def resource_id(self, value: typing.Optional[str]):
        jsii.set(self, "resourceId", value)

    @builtins.property
    @jsii.member(jsii_name="scalableDimension")
    def scalable_dimension(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ScalableDimension``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalabledimension
        """
        return jsii.get(self, "scalableDimension")

    @scalable_dimension.setter
    def scalable_dimension(self, value: typing.Optional[str]):
        jsii.set(self, "scalableDimension", value)

    @builtins.property
    @jsii.member(jsii_name="scalingTargetId")
    def scaling_target_id(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ScalingTargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalingtargetid
        """
        return jsii.get(self, "scalingTargetId")

    @scaling_target_id.setter
    def scaling_target_id(self, value: typing.Optional[str]):
        jsii.set(self, "scalingTargetId", value)

    @builtins.property
    @jsii.member(jsii_name="serviceNamespace")
    def service_namespace(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ServiceNamespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-servicenamespace
        """
        return jsii.get(self, "serviceNamespace")

    @service_namespace.setter
    def service_namespace(self, value: typing.Optional[str]):
        jsii.set(self, "serviceNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="stepScalingPolicyConfiguration")
    def step_scaling_policy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StepScalingPolicyConfigurationProperty"]]]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.StepScalingPolicyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration
        """
        return jsii.get(self, "stepScalingPolicyConfiguration")

    @step_scaling_policy_configuration.setter
    def step_scaling_policy_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StepScalingPolicyConfigurationProperty"]]]):
        jsii.set(self, "stepScalingPolicyConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="targetTrackingScalingPolicyConfiguration")
    def target_tracking_scaling_policy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TargetTrackingScalingPolicyConfigurationProperty"]]]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.TargetTrackingScalingPolicyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration
        """
        return jsii.get(self, "targetTrackingScalingPolicyConfiguration")

    @target_tracking_scaling_policy_configuration.setter
    def target_tracking_scaling_policy_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TargetTrackingScalingPolicyConfigurationProperty"]]]):
        jsii.set(self, "targetTrackingScalingPolicyConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'namespace': 'namespace', 'statistic': 'statistic', 'dimensions': 'dimensions', 'unit': 'unit'})
    class CustomizedMetricSpecificationProperty():
        def __init__(self, *, metric_name: str, namespace: str, statistic: str, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.MetricDimensionProperty"]]]]]=None, unit: typing.Optional[str]=None):
            """
            :param metric_name: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.
            :param namespace: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.
            :param statistic: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.
            :param dimensions: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.
            :param unit: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html
            """
            self._values = {
                'metric_name': metric_name,
                'namespace': namespace,
                'statistic': statistic,
            }
            if dimensions is not None: self._values["dimensions"] = dimensions
            if unit is not None: self._values["unit"] = unit

        @builtins.property
        def metric_name(self) -> str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-metricname
            """
            return self._values.get('metric_name')

        @builtins.property
        def namespace(self) -> str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-namespace
            """
            return self._values.get('namespace')

        @builtins.property
        def statistic(self) -> str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-statistic
            """
            return self._values.get('statistic')

        @builtins.property
        def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.MetricDimensionProperty"]]]]]:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-dimensions
            """
            return self._values.get('dimensions')

        @builtins.property
        def unit(self) -> typing.Optional[str]:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-unit
            """
            return self._values.get('unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CustomizedMetricSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.MetricDimensionProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class MetricDimensionProperty():
        def __init__(self, *, name: str, value: str):
            """
            :param name: ``CfnScalingPolicy.MetricDimensionProperty.Name``.
            :param value: ``CfnScalingPolicy.MetricDimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnScalingPolicy.MetricDimensionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html#cfn-applicationautoscaling-scalingpolicy-metricdimension-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> str:
            """``CfnScalingPolicy.MetricDimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html#cfn-applicationautoscaling-scalingpolicy-metricdimension-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricDimensionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty", jsii_struct_bases=[], name_mapping={'predefined_metric_type': 'predefinedMetricType', 'resource_label': 'resourceLabel'})
    class PredefinedMetricSpecificationProperty():
        def __init__(self, *, predefined_metric_type: str, resource_label: typing.Optional[str]=None):
            """
            :param predefined_metric_type: ``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.
            :param resource_label: ``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html
            """
            self._values = {
                'predefined_metric_type': predefined_metric_type,
            }
            if resource_label is not None: self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> str:
            """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
            """
            return self._values.get('predefined_metric_type')

        @builtins.property
        def resource_label(self) -> typing.Optional[str]:
            """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
            """
            return self._values.get('resource_label')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PredefinedMetricSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.StepAdjustmentProperty", jsii_struct_bases=[], name_mapping={'scaling_adjustment': 'scalingAdjustment', 'metric_interval_lower_bound': 'metricIntervalLowerBound', 'metric_interval_upper_bound': 'metricIntervalUpperBound'})
    class StepAdjustmentProperty():
        def __init__(self, *, scaling_adjustment: jsii.Number, metric_interval_lower_bound: typing.Optional[jsii.Number]=None, metric_interval_upper_bound: typing.Optional[jsii.Number]=None):
            """
            :param scaling_adjustment: ``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.
            :param metric_interval_lower_bound: ``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.
            :param metric_interval_upper_bound: ``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html
            """
            self._values = {
                'scaling_adjustment': scaling_adjustment,
            }
            if metric_interval_lower_bound is not None: self._values["metric_interval_lower_bound"] = metric_interval_lower_bound
            if metric_interval_upper_bound is not None: self._values["metric_interval_upper_bound"] = metric_interval_upper_bound

        @builtins.property
        def scaling_adjustment(self) -> jsii.Number:
            """``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment-scalingadjustment
            """
            return self._values.get('scaling_adjustment')

        @builtins.property
        def metric_interval_lower_bound(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment-metricintervallowerbound
            """
            return self._values.get('metric_interval_lower_bound')

        @builtins.property
        def metric_interval_upper_bound(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment-metricintervalupperbound
            """
            return self._values.get('metric_interval_upper_bound')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StepAdjustmentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.StepScalingPolicyConfigurationProperty", jsii_struct_bases=[], name_mapping={'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'metric_aggregation_type': 'metricAggregationType', 'min_adjustment_magnitude': 'minAdjustmentMagnitude', 'step_adjustments': 'stepAdjustments'})
    class StepScalingPolicyConfigurationProperty():
        def __init__(self, *, adjustment_type: typing.Optional[str]=None, cooldown: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional[str]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, step_adjustments: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]]]=None):
            """
            :param adjustment_type: ``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.AdjustmentType``.
            :param cooldown: ``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.Cooldown``.
            :param metric_aggregation_type: ``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.MetricAggregationType``.
            :param min_adjustment_magnitude: ``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.MinAdjustmentMagnitude``.
            :param step_adjustments: ``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.StepAdjustments``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html
            """
            self._values = {
            }
            if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
            if cooldown is not None: self._values["cooldown"] = cooldown
            if metric_aggregation_type is not None: self._values["metric_aggregation_type"] = metric_aggregation_type
            if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude
            if step_adjustments is not None: self._values["step_adjustments"] = step_adjustments

        @builtins.property
        def adjustment_type(self) -> typing.Optional[str]:
            """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.AdjustmentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-adjustmenttype
            """
            return self._values.get('adjustment_type')

        @builtins.property
        def cooldown(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.Cooldown``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-cooldown
            """
            return self._values.get('cooldown')

        @builtins.property
        def metric_aggregation_type(self) -> typing.Optional[str]:
            """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.MetricAggregationType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-metricaggregationtype
            """
            return self._values.get('metric_aggregation_type')

        @builtins.property
        def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.MinAdjustmentMagnitude``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-minadjustmentmagnitude
            """
            return self._values.get('min_adjustment_magnitude')

        @builtins.property
        def step_adjustments(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]]]:
            """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.StepAdjustments``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustments
            """
            return self._values.get('step_adjustments')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StepScalingPolicyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty", jsii_struct_bases=[], name_mapping={'target_value': 'targetValue', 'customized_metric_specification': 'customizedMetricSpecification', 'disable_scale_in': 'disableScaleIn', 'predefined_metric_specification': 'predefinedMetricSpecification', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown'})
    class TargetTrackingScalingPolicyConfigurationProperty():
        def __init__(self, *, target_value: jsii.Number, customized_metric_specification: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.CustomizedMetricSpecificationProperty"]]]=None, disable_scale_in: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, predefined_metric_specification: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.PredefinedMetricSpecificationProperty"]]]=None, scale_in_cooldown: typing.Optional[jsii.Number]=None, scale_out_cooldown: typing.Optional[jsii.Number]=None):
            """
            :param target_value: ``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.TargetValue``.
            :param customized_metric_specification: ``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.CustomizedMetricSpecification``.
            :param disable_scale_in: ``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.DisableScaleIn``.
            :param predefined_metric_specification: ``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.PredefinedMetricSpecification``.
            :param scale_in_cooldown: ``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.ScaleInCooldown``.
            :param scale_out_cooldown: ``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.ScaleOutCooldown``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html
            """
            self._values = {
                'target_value': target_value,
            }
            if customized_metric_specification is not None: self._values["customized_metric_specification"] = customized_metric_specification
            if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
            if predefined_metric_specification is not None: self._values["predefined_metric_specification"] = predefined_metric_specification
            if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
            if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

        @builtins.property
        def target_value(self) -> jsii.Number:
            """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.TargetValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-targetvalue
            """
            return self._values.get('target_value')

        @builtins.property
        def customized_metric_specification(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.CustomizedMetricSpecificationProperty"]]]:
            """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.CustomizedMetricSpecification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-customizedmetricspecification
            """
            return self._values.get('customized_metric_specification')

        @builtins.property
        def disable_scale_in(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.DisableScaleIn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-disablescalein
            """
            return self._values.get('disable_scale_in')

        @builtins.property
        def predefined_metric_specification(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.PredefinedMetricSpecificationProperty"]]]:
            """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.PredefinedMetricSpecification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-predefinedmetricspecification
            """
            return self._values.get('predefined_metric_specification')

        @builtins.property
        def scale_in_cooldown(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.ScaleInCooldown``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-scaleincooldown
            """
            return self._values.get('scale_in_cooldown')

        @builtins.property
        def scale_out_cooldown(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.ScaleOutCooldown``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-scaleoutcooldown
            """
            return self._values.get('scale_out_cooldown')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetTrackingScalingPolicyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicyProps", jsii_struct_bases=[], name_mapping={'policy_name': 'policyName', 'policy_type': 'policyType', 'resource_id': 'resourceId', 'scalable_dimension': 'scalableDimension', 'scaling_target_id': 'scalingTargetId', 'service_namespace': 'serviceNamespace', 'step_scaling_policy_configuration': 'stepScalingPolicyConfiguration', 'target_tracking_scaling_policy_configuration': 'targetTrackingScalingPolicyConfiguration'})
class CfnScalingPolicyProps():
    def __init__(self, *, policy_name: str, policy_type: str, resource_id: typing.Optional[str]=None, scalable_dimension: typing.Optional[str]=None, scaling_target_id: typing.Optional[str]=None, service_namespace: typing.Optional[str]=None, step_scaling_policy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.StepScalingPolicyConfigurationProperty"]]]=None, target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty"]]]=None):
        """Properties for defining a ``AWS::ApplicationAutoScaling::ScalingPolicy``.

        :param policy_name: ``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyName``.
        :param policy_type: ``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyType``.
        :param resource_id: ``AWS::ApplicationAutoScaling::ScalingPolicy.ResourceId``.
        :param scalable_dimension: ``AWS::ApplicationAutoScaling::ScalingPolicy.ScalableDimension``.
        :param scaling_target_id: ``AWS::ApplicationAutoScaling::ScalingPolicy.ScalingTargetId``.
        :param service_namespace: ``AWS::ApplicationAutoScaling::ScalingPolicy.ServiceNamespace``.
        :param step_scaling_policy_configuration: ``AWS::ApplicationAutoScaling::ScalingPolicy.StepScalingPolicyConfiguration``.
        :param target_tracking_scaling_policy_configuration: ``AWS::ApplicationAutoScaling::ScalingPolicy.TargetTrackingScalingPolicyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html
        """
        self._values = {
            'policy_name': policy_name,
            'policy_type': policy_type,
        }
        if resource_id is not None: self._values["resource_id"] = resource_id
        if scalable_dimension is not None: self._values["scalable_dimension"] = scalable_dimension
        if scaling_target_id is not None: self._values["scaling_target_id"] = scaling_target_id
        if service_namespace is not None: self._values["service_namespace"] = service_namespace
        if step_scaling_policy_configuration is not None: self._values["step_scaling_policy_configuration"] = step_scaling_policy_configuration
        if target_tracking_scaling_policy_configuration is not None: self._values["target_tracking_scaling_policy_configuration"] = target_tracking_scaling_policy_configuration

    @builtins.property
    def policy_name(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policyname
        """
        return self._values.get('policy_name')

    @builtins.property
    def policy_type(self) -> str:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policytype
        """
        return self._values.get('policy_type')

    @builtins.property
    def resource_id(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ResourceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-resourceid
        """
        return self._values.get('resource_id')

    @builtins.property
    def scalable_dimension(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ScalableDimension``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalabledimension
        """
        return self._values.get('scalable_dimension')

    @builtins.property
    def scaling_target_id(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ScalingTargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalingtargetid
        """
        return self._values.get('scaling_target_id')

    @builtins.property
    def service_namespace(self) -> typing.Optional[str]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.ServiceNamespace``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-servicenamespace
        """
        return self._values.get('service_namespace')

    @builtins.property
    def step_scaling_policy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.StepScalingPolicyConfigurationProperty"]]]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.StepScalingPolicyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration
        """
        return self._values.get('step_scaling_policy_configuration')

    @builtins.property
    def target_tracking_scaling_policy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty"]]]:
        """``AWS::ApplicationAutoScaling::ScalingPolicy.TargetTrackingScalingPolicyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration
        """
        return self._values.get('target_tracking_scaling_policy_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CronOptions", jsii_struct_bases=[], name_mapping={'day': 'day', 'hour': 'hour', 'minute': 'minute', 'month': 'month', 'week_day': 'weekDay', 'year': 'year'})
class CronOptions():
    def __init__(self, *, day: typing.Optional[str]=None, hour: typing.Optional[str]=None, minute: typing.Optional[str]=None, month: typing.Optional[str]=None, week_day: typing.Optional[str]=None, year: typing.Optional[str]=None):
        """Options to configure a cron expression.

        All fields are strings so you can use complex expresions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions
        """
        self._values = {
        }
        if day is not None: self._values["day"] = day
        if hour is not None: self._values["hour"] = hour
        if minute is not None: self._values["minute"] = minute
        if month is not None: self._values["month"] = month
        if week_day is not None: self._values["week_day"] = week_day
        if year is not None: self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[str]:
        """The day of the month to run this rule at.

        default
        :default: - Every day of the month
        """
        return self._values.get('day')

    @builtins.property
    def hour(self) -> typing.Optional[str]:
        """The hour to run this rule at.

        default
        :default: - Every hour
        """
        return self._values.get('hour')

    @builtins.property
    def minute(self) -> typing.Optional[str]:
        """The minute to run this rule at.

        default
        :default: - Every minute
        """
        return self._values.get('minute')

    @builtins.property
    def month(self) -> typing.Optional[str]:
        """The month to run this rule at.

        default
        :default: - Every month
        """
        return self._values.get('month')

    @builtins.property
    def week_day(self) -> typing.Optional[str]:
        """The day of the week to run this rule at.

        default
        :default: - Any day of the week
        """
        return self._values.get('week_day')

    @builtins.property
    def year(self) -> typing.Optional[str]:
        """The year to run this rule at.

        default
        :default: - Every year
        """
        return self._values.get('year')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CronOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.EnableScalingProps", jsii_struct_bases=[], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity'})
class EnableScalingProps():
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None):
        """Properties for enabling DynamoDB capacity scaling.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        """
        self._values = {
            'max_capacity': max_capacity,
        }
        if min_capacity is not None: self._values["min_capacity"] = min_capacity

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        """Maximum capacity to scale to."""
        return self._values.get('max_capacity')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum capacity to scale to.

        default
        :default: 1
        """
        return self._values.get('min_capacity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EnableScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BaseScalableAttributeProps", jsii_struct_bases=[EnableScalingProps], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'dimension': 'dimension', 'resource_id': 'resourceId', 'role': 'role', 'service_namespace': 'serviceNamespace'})
class BaseScalableAttributeProps(EnableScalingProps):
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: "ServiceNamespace"):
        """Properties for a ScalableTableAttribute.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        :param dimension: Scalable dimension of the attribute.
        :param resource_id: Resource ID of the attribute.
        :param role: Role to use for scaling.
        :param service_namespace: Service namespace of the scalable attribute.
        """
        self._values = {
            'max_capacity': max_capacity,
            'dimension': dimension,
            'resource_id': resource_id,
            'role': role,
            'service_namespace': service_namespace,
        }
        if min_capacity is not None: self._values["min_capacity"] = min_capacity

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        """Maximum capacity to scale to."""
        return self._values.get('max_capacity')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum capacity to scale to.

        default
        :default: 1
        """
        return self._values.get('min_capacity')

    @builtins.property
    def dimension(self) -> str:
        """Scalable dimension of the attribute."""
        return self._values.get('dimension')

    @builtins.property
    def resource_id(self) -> str:
        """Resource ID of the attribute."""
        return self._values.get('resource_id')

    @builtins.property
    def role(self) -> aws_cdk.aws_iam.IRole:
        """Role to use for scaling."""
        return self._values.get('role')

    @builtins.property
    def service_namespace(self) -> "ServiceNamespace":
        """Service namespace of the scalable attribute."""
        return self._values.get('service_namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseScalableAttributeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-applicationautoscaling.IScalableTarget")
class IScalableTarget(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IScalableTargetProxy

    @builtins.property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _IScalableTargetProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-applicationautoscaling.IScalableTarget"
    @builtins.property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "scalableTargetId")


@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    """How the scaling metric is going to be aggregated."""
    AVERAGE = "AVERAGE"
    """Average."""
    MINIMUM = "MINIMUM"
    """Minimum."""
    MAXIMUM = "MAXIMUM"
    """Maximum."""

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    """One of the predefined autoscaling metrics."""
    DYNAMODB_READ_CAPACITY_UTILIZATION = "DYNAMODB_READ_CAPACITY_UTILIZATION"
    DYANMODB_WRITE_CAPACITY_UTILIZATION = "DYANMODB_WRITE_CAPACITY_UTILIZATION"
    ALB_REQUEST_COUNT_PER_TARGET = "ALB_REQUEST_COUNT_PER_TARGET"
    RDS_READER_AVERAGE_CPU_UTILIZATION = "RDS_READER_AVERAGE_CPU_UTILIZATION"
    RDS_READER_AVERAGE_DATABASE_CONNECTIONS = "RDS_READER_AVERAGE_DATABASE_CONNECTIONS"
    EC2_SPOT_FLEET_REQUEST_AVERAGE_CPU_UTILIZATION = "EC2_SPOT_FLEET_REQUEST_AVERAGE_CPU_UTILIZATION"
    EC2_SPOT_FLEET_REQUEST_AVERAGE_NETWORK_IN = "EC2_SPOT_FLEET_REQUEST_AVERAGE_NETWORK_IN"
    EC2_SPOT_FLEET_REQUEST_AVERAGE_NETWORK_OUT = "EC2_SPOT_FLEET_REQUEST_AVERAGE_NETWORK_OUT"
    SAGEMAKER_VARIANT_INVOCATIONS_PER_INSTANCE = "SAGEMAKER_VARIANT_INVOCATIONS_PER_INSTANCE"
    ECS_SERVICE_AVERAGE_CPU_UTILIZATION = "ECS_SERVICE_AVERAGE_CPU_UTILIZATION"
    ECS_SERVICE_AVERAGE_MEMORY_UTILIZATION = "ECS_SERVICE_AVERAGE_MEMORY_UTILIZATION"

@jsii.implements(IScalableTarget)
class ScalableTarget(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.ScalableTarget"):
    """Define a scalable target."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number, resource_id: str, scalable_dimension: str, service_namespace: "ServiceNamespace", role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param max_capacity: The maximum value that Application Auto Scaling can use to scale a target during a scaling activity.
        :param min_capacity: The minimum value that Application Auto Scaling can use to scale a target during a scaling activity.
        :param resource_id: The resource identifier to associate with this scalable target. This string consists of the resource type and unique identifier.
        :param scalable_dimension: The scalable dimension that's associated with the scalable target. Specify the service namespace, resource type, and scaling property.
        :param service_namespace: The namespace of the AWS service that provides the resource or custom-resource for a resource provided by your own application or service. For valid AWS service namespace values, see the RegisterScalableTarget action in the Application Auto Scaling API Reference.
        :param role: Role that allows Application Auto Scaling to modify your scalable target. Default: A role is automatically created
        """
        props = ScalableTargetProps(max_capacity=max_capacity, min_capacity=min_capacity, resource_id=resource_id, scalable_dimension=scalable_dimension, service_namespace=service_namespace, role=role)

        jsii.create(ScalableTarget, self, [scope, id, props])

    @jsii.member(jsii_name="fromScalableTargetId")
    @builtins.classmethod
    def from_scalable_target_id(cls, scope: aws_cdk.core.Construct, id: str, scalable_target_id: str) -> "IScalableTarget":
        """
        :param scope: -
        :param id: -
        :param scalable_target_id: -
        """
        return jsii.sinvoke(cls, "fromScalableTargetId", [scope, id, scalable_target_id])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the role's policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        :param id: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = BasicStepScalingPolicyProps(metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, min_adjustment_magnitude=min_adjustment_magnitude)

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: "Schedule", end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scale out or in based on time.

        :param id: -
        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        action = ScalingSchedule(schedule=schedule, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        return jsii.invoke(self, "scaleOnSchedule", [id, action])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
        :param resource_label: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = BasicTargetTrackingScalingPolicyProps(target_value=target_value, custom_metric=custom_metric, predefined_metric=predefined_metric, resource_label=resource_label, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role used to give AutoScaling permissions to your resource."""
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        """ID of the Scalable Target.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            service / ecs_stack - MyECSCluster - AB12CDE3F4GH / ecs_stack - MyECSService - AB12CDE3F4GH | ecsservice:DesiredCount|ecs@attributeundefined
        """
        return jsii.get(self, "scalableTargetId")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalableTargetProps", jsii_struct_bases=[], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'resource_id': 'resourceId', 'scalable_dimension': 'scalableDimension', 'service_namespace': 'serviceNamespace', 'role': 'role'})
class ScalableTargetProps():
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number, resource_id: str, scalable_dimension: str, service_namespace: "ServiceNamespace", role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Properties for a scalable target.

        :param max_capacity: The maximum value that Application Auto Scaling can use to scale a target during a scaling activity.
        :param min_capacity: The minimum value that Application Auto Scaling can use to scale a target during a scaling activity.
        :param resource_id: The resource identifier to associate with this scalable target. This string consists of the resource type and unique identifier.
        :param scalable_dimension: The scalable dimension that's associated with the scalable target. Specify the service namespace, resource type, and scaling property.
        :param service_namespace: The namespace of the AWS service that provides the resource or custom-resource for a resource provided by your own application or service. For valid AWS service namespace values, see the RegisterScalableTarget action in the Application Auto Scaling API Reference.
        :param role: Role that allows Application Auto Scaling to modify your scalable target. Default: A role is automatically created
        """
        self._values = {
            'max_capacity': max_capacity,
            'min_capacity': min_capacity,
            'resource_id': resource_id,
            'scalable_dimension': scalable_dimension,
            'service_namespace': service_namespace,
        }
        if role is not None: self._values["role"] = role

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        """The maximum value that Application Auto Scaling can use to scale a target during a scaling activity."""
        return self._values.get('max_capacity')

    @builtins.property
    def min_capacity(self) -> jsii.Number:
        """The minimum value that Application Auto Scaling can use to scale a target during a scaling activity."""
        return self._values.get('min_capacity')

    @builtins.property
    def resource_id(self) -> str:
        """The resource identifier to associate with this scalable target.

        This string consists of the resource type and unique identifier.

        see
        :see: https://docs.aws.amazon.com/autoscaling/application/APIReference/API_RegisterScalableTarget.html

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            service / ecs_stack - MyECSCluster - AB12CDE3F4GH / ecs_stack - MyECSService - AB12CDE3F4GH
        """
        return self._values.get('resource_id')

    @builtins.property
    def scalable_dimension(self) -> str:
        """The scalable dimension that's associated with the scalable target.

        Specify the service namespace, resource type, and scaling property.

        see
        :see: https://docs.aws.amazon.com/autoscaling/application/APIReference/API_ScalingPolicy.html

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            ecs:service:DesiredCount
        """
        return self._values.get('scalable_dimension')

    @builtins.property
    def service_namespace(self) -> "ServiceNamespace":
        """The namespace of the AWS service that provides the resource or custom-resource for a resource provided by your own application or service.

        For valid AWS service namespace values, see the RegisterScalableTarget
        action in the Application Auto Scaling API Reference.

        see
        :see: https://docs.aws.amazon.com/autoscaling/application/APIReference/API_RegisterScalableTarget.html
        """
        return self._values.get('service_namespace')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role that allows Application Auto Scaling to modify your scalable target.

        default
        :default: A role is automatically created
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalableTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalingInterval", jsii_struct_bases=[], name_mapping={'change': 'change', 'lower': 'lower', 'upper': 'upper'})
class ScalingInterval():
    def __init__(self, *, change: jsii.Number, lower: typing.Optional[jsii.Number]=None, upper: typing.Optional[jsii.Number]=None):
        """A range of metric values in which to apply a certain scaling operation.

        :param change: The capacity adjustment to apply in this interval. The number is interpreted differently based on AdjustmentType: - ChangeInCapacity: add the adjustment to the current capacity. The number can be positive or negative. - PercentChangeInCapacity: add or remove the given percentage of the current capacity to itself. The number can be in the range [-100..100]. - ExactCapacity: set the capacity to this number. The number must be positive.
        :param lower: The lower bound of the interval. The scaling adjustment will be applied if the metric is higher than this value. Default: Threshold automatically derived from neighbouring intervals
        :param upper: The upper bound of the interval. The scaling adjustment will be applied if the metric is lower than this value. Default: Threshold automatically derived from neighbouring intervals
        """
        self._values = {
            'change': change,
        }
        if lower is not None: self._values["lower"] = lower
        if upper is not None: self._values["upper"] = upper

    @builtins.property
    def change(self) -> jsii.Number:
        """The capacity adjustment to apply in this interval.

        The number is interpreted differently based on AdjustmentType:

        - ChangeInCapacity: add the adjustment to the current capacity.
          The number can be positive or negative.
        - PercentChangeInCapacity: add or remove the given percentage of the current
          capacity to itself. The number can be in the range [-100..100].
        - ExactCapacity: set the capacity to this number. The number must
          be positive.
        """
        return self._values.get('change')

    @builtins.property
    def lower(self) -> typing.Optional[jsii.Number]:
        """The lower bound of the interval.

        The scaling adjustment will be applied if the metric is higher than this value.

        default
        :default: Threshold automatically derived from neighbouring intervals
        """
        return self._values.get('lower')

    @builtins.property
    def upper(self) -> typing.Optional[jsii.Number]:
        """The upper bound of the interval.

        The scaling adjustment will be applied if the metric is lower than this value.

        default
        :default: Threshold automatically derived from neighbouring intervals
        """
        return self._values.get('upper')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalingInterval(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalingSchedule", jsii_struct_bases=[], name_mapping={'schedule': 'schedule', 'end_time': 'endTime', 'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'start_time': 'startTime'})
class ScalingSchedule():
    def __init__(self, *, schedule: "Schedule", end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None):
        """A scheduled scaling action.

        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        self._values = {
            'schedule': schedule,
        }
        if end_time is not None: self._values["end_time"] = end_time
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if start_time is not None: self._values["start_time"] = start_time

    @builtins.property
    def schedule(self) -> "Schedule":
        """When to perform this action."""
        return self._values.get('schedule')

    @builtins.property
    def end_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action expires.

        default
        :default: The rule never expires.
        """
        return self._values.get('end_time')

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """The new maximum capacity.

        During the scheduled time, the current capacity is above the maximum
        capacity, Application Auto Scaling scales in to the maximum capacity.

        At least one of maxCapacity and minCapacity must be supplied.

        default
        :default: No new maximum capacity
        """
        return self._values.get('max_capacity')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """The new minimum capacity.

        During the scheduled time, if the current capacity is below the minimum
        capacity, Application Auto Scaling scales out to the minimum capacity.

        At least one of maxCapacity and minCapacity must be supplied.

        default
        :default: No new minimum capacity
        """
        return self._values.get('min_capacity')

    @builtins.property
    def start_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action becomes active.

        default
        :default: The rule is activate immediately
        """
        return self._values.get('start_time')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalingSchedule(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Schedule(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-applicationautoscaling.Schedule"):
    """Schedule for scheduled scaling actions."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ScheduleProxy

    def __init__(self) -> None:
        jsii.create(Schedule, self, [])

    @jsii.member(jsii_name="at")
    @builtins.classmethod
    def at(cls, moment: datetime.datetime) -> "Schedule":
        """Construct a Schedule from a moment in time.

        :param moment: -
        """
        return jsii.sinvoke(cls, "at", [moment])

    @jsii.member(jsii_name="cron")
    @builtins.classmethod
    def cron(cls, *, day: typing.Optional[str]=None, hour: typing.Optional[str]=None, minute: typing.Optional[str]=None, month: typing.Optional[str]=None, week_day: typing.Optional[str]=None, year: typing.Optional[str]=None) -> "Schedule":
        """Create a schedule from a set of cron fields.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year
        """
        options = CronOptions(day=day, hour=hour, minute=minute, month=month, week_day=week_day, year=year)

        return jsii.sinvoke(cls, "cron", [options])

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(cls, expression: str) -> "Schedule":
        """Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that Application AutoScaling will recognize
        """
        return jsii.sinvoke(cls, "expression", [expression])

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, duration: aws_cdk.core.Duration) -> "Schedule":
        """Construct a schedule from an interval and a time unit.

        :param duration: -
        """
        return jsii.sinvoke(cls, "rate", [duration])

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    @abc.abstractmethod
    def expression_string(self) -> str:
        """Retrieve the expression for this schedule."""
        ...


class _ScheduleProxy(Schedule):
    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> str:
        """Retrieve the expression for this schedule."""
        return jsii.get(self, "expressionString")


@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.ServiceNamespace")
class ServiceNamespace(enum.Enum):
    """The service that supports Application AutoScaling."""
    ECS = "ECS"
    """Elastic Container Service."""
    ELASTIC_MAP_REDUCE = "ELASTIC_MAP_REDUCE"
    """Elastic Map Reduce."""
    EC2 = "EC2"
    """Elastic Compute Cloud."""
    APPSTREAM = "APPSTREAM"
    """App Stream."""
    DYNAMODB = "DYNAMODB"
    """Dynamo DB."""
    RDS = "RDS"
    """Relational Database Service."""
    SAGEMAKER = "SAGEMAKER"
    """SageMaker."""
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    """Custom Resource."""

class StepScalingAction(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingAction"):
    """Define a step scaling action.

    This kind of scaling policy adjusts the target capacity in configurable
    steps. The size of the step is configurable based on the metric's distance
    to its alarm threshold.

    This Action must be used as the target of a CloudWatch alarm to take effect.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, scaling_target: "IScalableTarget", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, policy_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param scaling_target: The scalable target.
        :param adjustment_type: How the adjustment numbers are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. For scale out policies, multiple scale outs during the cooldown period are squashed so that only the biggest scale out happens. For scale in policies, subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Default: Average
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        :param policy_name: A name for the scaling policy. Default: Automatically generated name
        """
        props = StepScalingActionProps(scaling_target=scaling_target, adjustment_type=adjustment_type, cooldown=cooldown, metric_aggregation_type=metric_aggregation_type, min_adjustment_magnitude=min_adjustment_magnitude, policy_name=policy_name)

        jsii.create(StepScalingAction, self, [scope, id, props])

    @jsii.member(jsii_name="addAdjustment")
    def add_adjustment(self, *, adjustment: jsii.Number, lower_bound: typing.Optional[jsii.Number]=None, upper_bound: typing.Optional[jsii.Number]=None) -> None:
        """Add an adjusment interval to the ScalingAction.

        :param adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
        :param lower_bound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        :param upper_bound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        adjustment_ = AdjustmentTier(adjustment=adjustment, lower_bound=lower_bound, upper_bound=upper_bound)

        return jsii.invoke(self, "addAdjustment", [adjustment_])

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingActionProps", jsii_struct_bases=[], name_mapping={'scaling_target': 'scalingTarget', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'metric_aggregation_type': 'metricAggregationType', 'min_adjustment_magnitude': 'minAdjustmentMagnitude', 'policy_name': 'policyName'})
class StepScalingActionProps():
    def __init__(self, *, scaling_target: "IScalableTarget", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, policy_name: typing.Optional[str]=None):
        """Properties for a scaling policy.

        :param scaling_target: The scalable target.
        :param adjustment_type: How the adjustment numbers are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. For scale out policies, multiple scale outs during the cooldown period are squashed so that only the biggest scale out happens. For scale in policies, subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Default: Average
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        :param policy_name: A name for the scaling policy. Default: Automatically generated name
        """
        self._values = {
            'scaling_target': scaling_target,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if metric_aggregation_type is not None: self._values["metric_aggregation_type"] = metric_aggregation_type
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude
        if policy_name is not None: self._values["policy_name"] = policy_name

    @builtins.property
    def scaling_target(self) -> "IScalableTarget":
        """The scalable target."""
        return self._values.get('scaling_target')

    @builtins.property
    def adjustment_type(self) -> typing.Optional["AdjustmentType"]:
        """How the adjustment numbers are interpreted.

        default
        :default: ChangeInCapacity
        """
        return self._values.get('adjustment_type')

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        For scale out policies, multiple scale outs during the cooldown period are
        squashed so that only the biggest scale out happens.

        For scale in policies, subsequent scale ins during the cooldown period are
        ignored.

        default
        :default: No cooldown period

        see
        :see: https://docs.aws.amazon.com/autoscaling/application/APIReference/API_StepScalingPolicyConfiguration.html
        """
        return self._values.get('cooldown')

    @builtins.property
    def metric_aggregation_type(self) -> typing.Optional["MetricAggregationType"]:
        """The aggregation type for the CloudWatch metrics.

        default
        :default: Average
        """
        return self._values.get('metric_aggregation_type')

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        default
        :default: No minimum scaling effect
        """
        return self._values.get('min_adjustment_magnitude')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: Automatically generated name
        """
        return self._values.get('policy_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StepScalingActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class StepScalingPolicy(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingPolicy"):
    """Define a acaling strategy which scales depending on absolute values of some metric.

    You can specify the scaling behavior for various values of the metric.

    Implemented using one or more CloudWatch alarms and Step Scaling Policies.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, scaling_target: "IScalableTarget", metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param scaling_target: The scaling target.
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = StepScalingPolicyProps(scaling_target=scaling_target, metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, min_adjustment_magnitude=min_adjustment_magnitude)

        jsii.create(StepScalingPolicy, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lowerAction")
    def lower_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "lowerAction")

    @builtins.property
    @jsii.member(jsii_name="lowerAlarm")
    def lower_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "lowerAlarm")

    @builtins.property
    @jsii.member(jsii_name="upperAction")
    def upper_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "upperAction")

    @builtins.property
    @jsii.member(jsii_name="upperAlarm")
    def upper_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "upperAlarm")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingPolicyProps", jsii_struct_bases=[BasicStepScalingPolicyProps], name_mapping={'metric': 'metric', 'scaling_steps': 'scalingSteps', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'min_adjustment_magnitude': 'minAdjustmentMagnitude', 'scaling_target': 'scalingTarget'})
class StepScalingPolicyProps(BasicStepScalingPolicyProps):
    def __init__(self, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, scaling_target: "IScalableTarget"):
        """
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        :param scaling_target: The scaling target.
        """
        self._values = {
            'metric': metric,
            'scaling_steps': scaling_steps,
            'scaling_target': scaling_target,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @builtins.property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to scale on."""
        return self._values.get('metric')

    @builtins.property
    def scaling_steps(self) -> typing.List["ScalingInterval"]:
        """The intervals for scaling.

        Maps a range of metric values to a particular scaling behavior.
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def adjustment_type(self) -> typing.Optional["AdjustmentType"]:
        """How the adjustment numbers inside 'intervals' are interpreted.

        default
        :default: ChangeInCapacity
        """
        return self._values.get('adjustment_type')

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        Subsequent scale outs during the cooldown period are squashed so that only
        the biggest scale out happens.

        Subsequent scale ins during the cooldown period are ignored.

        default
        :default: No cooldown period

        see
        :see: https://docs.aws.amazon.com/autoscaling/application/APIReference/API_StepScalingPolicyConfiguration.html
        """
        return self._values.get('cooldown')

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        default
        :default: No minimum scaling effect
        """
        return self._values.get('min_adjustment_magnitude')

    @builtins.property
    def scaling_target(self) -> "IScalableTarget":
        """The scaling target."""
        return self._values.get('scaling_target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StepScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TargetTrackingScalingPolicy(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.TargetTrackingScalingPolicy"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, scaling_target: "IScalableTarget", target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param scaling_target: 
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
        :param resource_label: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = TargetTrackingScalingPolicyProps(scaling_target=scaling_target, target_value=target_value, custom_metric=custom_metric, predefined_metric=predefined_metric, resource_label=resource_label, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.TargetTrackingScalingPolicyProps", jsii_struct_bases=[BasicTargetTrackingScalingPolicyProps], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'target_value': 'targetValue', 'custom_metric': 'customMetric', 'predefined_metric': 'predefinedMetric', 'resource_label': 'resourceLabel', 'scaling_target': 'scalingTarget'})
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, scaling_target: "IScalableTarget"):
        """Properties for a concrete TargetTrackingPolicy.

        Adds the scalingTarget.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
        :param resource_label: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
        :param scaling_target: 
        """
        self._values = {
            'target_value': target_value,
            'scaling_target': scaling_target,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown
        if custom_metric is not None: self._values["custom_metric"] = custom_metric
        if predefined_metric is not None: self._values["predefined_metric"] = predefined_metric
        if resource_label is not None: self._values["resource_label"] = resource_label

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    @builtins.property
    def target_value(self) -> jsii.Number:
        """The target value for the metric."""
        return self._values.get('target_value')

    @builtins.property
    def custom_metric(self) -> typing.Optional[aws_cdk.aws_cloudwatch.IMetric]:
        """A custom metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No custom metric.
        """
        return self._values.get('custom_metric')

    @builtins.property
    def predefined_metric(self) -> typing.Optional["PredefinedMetric"]:
        """A predefined metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No predefined metrics.
        """
        return self._values.get('predefined_metric')

    @builtins.property
    def resource_label(self) -> typing.Optional[str]:
        """Identify the resource associated with the metric type.

        Only used for predefined metric ALBRequestCountPerTarget.

        default
        :default: - No resource label.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / <load-balancer - name > /<load-balancer-id>/targetgroup / <target-group - name > /<target-group-id>
        """
        return self._values.get('resource_label')

    @builtins.property
    def scaling_target(self) -> "IScalableTarget":
        return self._values.get('scaling_target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TargetTrackingScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AdjustmentTier", "AdjustmentType", "BaseScalableAttribute", "BaseScalableAttributeProps", "BaseTargetTrackingProps", "BasicStepScalingPolicyProps", "BasicTargetTrackingScalingPolicyProps", "CfnScalableTarget", "CfnScalableTargetProps", "CfnScalingPolicy", "CfnScalingPolicyProps", "CronOptions", "EnableScalingProps", "IScalableTarget", "MetricAggregationType", "PredefinedMetric", "ScalableTarget", "ScalableTargetProps", "ScalingInterval", "ScalingSchedule", "Schedule", "ServiceNamespace", "StepScalingAction", "StepScalingActionProps", "StepScalingPolicy", "StepScalingPolicyProps", "TargetTrackingScalingPolicy", "TargetTrackingScalingPolicyProps", "__jsii_assembly__"]

publication.publish()
