"""
## AWS AutoScaling Common Library

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

This is a sister package to `@aws-cdk/aws-autoscaling` and
`@aws-cdk/aws-applicationautoscaling`. It contains shared implementation
details between them.

It does not need to be used directly.
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

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling-common", "1.23.0", __name__, "aws-autoscaling-common@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.Alarms", jsii_struct_bases=[], name_mapping={'lower_alarm_interval_index': 'lowerAlarmIntervalIndex', 'upper_alarm_interval_index': 'upperAlarmIntervalIndex'})
class Alarms():
    def __init__(self, *, lower_alarm_interval_index: typing.Optional[jsii.Number]=None, upper_alarm_interval_index: typing.Optional[jsii.Number]=None):
        """
        :param lower_alarm_interval_index: 
        :param upper_alarm_interval_index: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if lower_alarm_interval_index is not None: self._values["lower_alarm_interval_index"] = lower_alarm_interval_index
        if upper_alarm_interval_index is not None: self._values["upper_alarm_interval_index"] = upper_alarm_interval_index

    @builtins.property
    def lower_alarm_interval_index(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lower_alarm_interval_index')

    @builtins.property
    def upper_alarm_interval_index(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('upper_alarm_interval_index')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Alarms(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.ArbitraryIntervals", jsii_struct_bases=[], name_mapping={'absolute': 'absolute', 'intervals': 'intervals'})
class ArbitraryIntervals():
    def __init__(self, *, absolute: bool, intervals: typing.List["ScalingInterval"]):
        """
        :param absolute: 
        :param intervals: 

        stability
        :stability: experimental
        """
        self._values = {
            'absolute': absolute,
            'intervals': intervals,
        }

    @builtins.property
    def absolute(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return self._values.get('absolute')

    @builtins.property
    def intervals(self) -> typing.List["ScalingInterval"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('intervals')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArbitraryIntervals(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.CompleteScalingInterval", jsii_struct_bases=[], name_mapping={'lower': 'lower', 'upper': 'upper', 'change': 'change'})
class CompleteScalingInterval():
    def __init__(self, *, lower: jsii.Number, upper: jsii.Number, change: typing.Optional[jsii.Number]=None):
        """
        :param lower: 
        :param upper: 
        :param change: 

        stability
        :stability: experimental
        """
        self._values = {
            'lower': lower,
            'upper': upper,
        }
        if change is not None: self._values["change"] = change

    @builtins.property
    def lower(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lower')

    @builtins.property
    def upper(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return self._values.get('upper')

    @builtins.property
    def change(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('change')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CompleteScalingInterval(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-common.IRandomGenerator")
class IRandomGenerator(jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRandomGeneratorProxy

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> bool:
        """
        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        """
        :param min: -
        :param max: -

        stability
        :stability: experimental
        """
        ...


class _IRandomGeneratorProxy():
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-autoscaling-common.IRandomGenerator"
    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "nextBoolean", [])

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        """
        :param min: -
        :param max: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "nextInt", [min, max])


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.ScalingInterval", jsii_struct_bases=[], name_mapping={'change': 'change', 'lower': 'lower', 'upper': 'upper'})
class ScalingInterval():
    def __init__(self, *, change: jsii.Number, lower: typing.Optional[jsii.Number]=None, upper: typing.Optional[jsii.Number]=None):
        """A range of metric values in which to apply a certain scaling operation.

        :param change: The capacity adjustment to apply in this interval. The number is interpreted differently based on AdjustmentType: - ChangeInCapacity: add the adjustment to the current capacity. The number can be positive or negative. - PercentChangeInCapacity: add or remove the given percentage of the current capacity to itself. The number can be in the range [-100..100]. - ExactCapacity: set the capacity to this number. The number must be positive.
        :param lower: The lower bound of the interval. The scaling adjustment will be applied if the metric is higher than this value. Default: Threshold automatically derived from neighbouring intervals
        :param upper: The upper bound of the interval. The scaling adjustment will be applied if the metric is lower than this value. Default: Threshold automatically derived from neighbouring intervals

        stability
        :stability: experimental
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

        stability
        :stability: experimental
        """
        return self._values.get('change')

    @builtins.property
    def lower(self) -> typing.Optional[jsii.Number]:
        """The lower bound of the interval.

        The scaling adjustment will be applied if the metric is higher than this value.

        default
        :default: Threshold automatically derived from neighbouring intervals

        stability
        :stability: experimental
        """
        return self._values.get('lower')

    @builtins.property
    def upper(self) -> typing.Optional[jsii.Number]:
        """The upper bound of the interval.

        The scaling adjustment will be applied if the metric is lower than this value.

        default
        :default: Threshold automatically derived from neighbouring intervals

        stability
        :stability: experimental
        """
        return self._values.get('upper')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalingInterval(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["Alarms", "ArbitraryIntervals", "CompleteScalingInterval", "IRandomGenerator", "ScalingInterval", "__jsii_assembly__"]

publication.publish()
