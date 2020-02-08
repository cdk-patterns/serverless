"""
## Amazon Elastic Load Balancing V2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-elasticloadbalancingv2` package provides constructs for
configuring application and network load balancers.

For more information, see the AWS documentation for
[Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
and [Network Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html).

### Defining an Application Load Balancer

You define an application load balancer by creating an instance of
`ApplicationLoadBalancer`, adding a Listener to the load balancer
and adding Targets to the Listener:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_autoscaling as autoscaling

# ...

vpc = ec2.Vpc(...)

# Create the load balancer in a VPC. 'internetFacing' is 'false'
# by default, which creates an internal load balancer.
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)

# Add a listener and open up the load balancer's security group
# to the world. 'open' is the default, set this to 'false'
# and use `listener.connections` if you want to be selective
# about who can access the listener.
listener = lb.add_listener("Listener",
    port=80,
    open=True
)

# Create an AutoScaling group and add it as a load balancing
# target to the listener.
asg = autoscaling.AutoScalingGroup(...)
listener.add_targets("ApplicationFleet",
    port=8080,
    targets=[asg]
)
```

The security groups of the load balancer and the target are automatically
updated to allow the network traffic.

Use the `addFixedResponse()` method to add fixed response rules on the listener:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_fixed_response("Fixed",
    path_pattern="/ok",
    content_type=elbv2.ContentType.TEXT_PLAIN,
    message_body="OK",
    status_code="200"
)
```

#### Conditions

It's possible to route traffic to targets based on conditions in the incoming
HTTP request. Path- and host-based conditions are supported. For example,
the following will route requests to the indicated AutoScalingGroup
only if the requested host in the request is `example.com`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("Example.Com Fleet",
    priority=10,
    host_header="example.com",
    port=8080,
    targets=[asg]
)
```

`priority` is a required field when you add targets with conditions. The lowest
number wins.

Every listener must have at least one target without conditions.

### Defining a Network Load Balancer

Network Load Balancers are defined in a similar way to Application Load
Balancers:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_autoscaling as autoscaling

# Create the load balancer in a VPC. 'internetFacing' is 'false'
# by default, which creates an internal load balancer.
lb = elbv2.NetworkLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)

# Add a listener on a particular port.
listener = lb.add_listener("Listener",
    port=443
)

# Add targets on a particular port.
listener.add_targets("AppFleet",
    port=443,
    targets=[asg]
)
```

One thing to keep in mind is that network load balancers do not have security
groups, and no automatic security group configuration is done for you. You will
have to configure the security groups of the target yourself to allow traffic by
clients and/or load balancer instances, depending on your target types.  See
[Target Groups for your Network Load
Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html)
and [Register targets with your Target
Group](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-register-targets.html)
for more information.

### Targets and Target Groups

Application and Network Load Balancers organize load balancing targets in Target
Groups. If you add your balancing targets (such as AutoScalingGroups, ECS
services or individual instances) to your listener directly, the appropriate
`TargetGroup` will be automatically created for you.

If you need more control over the Target Groups created, create an instance of
`ApplicationTargetGroup` or `NetworkTargetGroup`, add the members you desire,
and add it to the listener by calling `addTargetGroups` instead of `addTargets`.

`addTargets()` will always return the Target Group it just created for you:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
group = listener.add_targets("AppFleet",
    port=443,
    targets=[asg1]
)

group.add_target(asg2)
```

### Using Lambda Targets

To use a Lambda Function as a target, use the integration class in the
`@aws-cdk/aws-elasticloadbalancingv2-targets` package:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_elasticloadbalancingv2_targets as targets

lambda_function = lambda.Function(...)
lb = elbv2.ApplicationLoadBalancer(...)

listener = lb.add_listener("Listener", port=80)
listener.add_targets("Targets",
    targets=[targets.LambdaTarget(lambda_function)]
)
```

Only a single Lambda function can be added to a single listener rule.

### Configuring Health Checks

Health checks are configured upon creation of a target group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("AppFleet",
    port=8080,
    targets=[asg],
    health_check={
        "path": "/ping",
        "interval": cdk.Duration.minutes(1)
    }
)
```

The health check can also be configured after creation by calling
`configureHealthCheck()` on the created object.

No attempts are made to configure security groups for the port you're
configuring a health check for, but if the health check is on the same port
you're routing traffic to, the security group already allows the traffic.
If not, you will have to configure the security groups appropriately:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("AppFleet",
    port=8080,
    targets=[asg],
    health_check={
        "port": 8088
    }
)

listener.connections.allow_from(lb, ec2.Port.tcp(8088))
```

### Using a Load Balancer from a different Stack

If you want to put your Load Balancer and the Targets it is load balancing to in
different stacks, you may not be able to use the convenience methods
`loadBalancer.addListener()` and `listener.addTargets()`.

The reason is that these methods will create resources in the same Stack as the
object they're called on, which may lead to cyclic references between stacks.
Instead, you will have to create an `ApplicationListener` in the target stack,
or an empty `TargetGroup` in the load balancer stack that you attach your
service to.

For an example of the alternatives while load balancing to an ECS service, see the
[ecs/cross-stack-load-balancer
example](https://github.com/aws-samples/aws-cdk-examples/tree/master/typescript/ecs/cross-stack-load-balancer/).

### Protocol for Load Balancer Targets

Constructs that want to be a load balancer target should implement
`IApplicationLoadBalancerTarget` and/or `INetworkLoadBalancerTarget`, and
provide an implementation for the function `attachToXxxTargetGroup()`, which can
call functions on the load balancer and should return metadata about the
load balancing target:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
attach_to_application_target_group(target_group, ApplicationTargetGroup)LoadBalancerTargetProps
    target_group.register_connectable(...)return {
        "target_type": TargetType.Instance | TargetType.Ip,
        "target_json": {"id": , ..., "port": , ...}
    }
```

`targetType` should be one of `Instance` or `Ip`. If the target can be
directly added to the target group, `targetJson` should contain the `id` of
the target (either instance ID or IP address depending on the type) and
optionally a `port` or `availabilityZone` override.

Application load balancer targets can call `registerConnectable()` on the
target group to register themselves for addition to the load balancer's security
group rules.

If your load balancer target requires that the TargetGroup has been
associated with a LoadBalancer before registration can happen (such as is the
case for ECS Services for example), take a resource dependency on
`targetGroup.loadBalancerDependency()` as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Make sure that the listener has been created, and so the TargetGroup
# has been associated with the LoadBalancer, before 'resource' is created.
resourced.add_dependency(target_group.load_balancer_dependency())
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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticloadbalancingv2", "1.23.0", __name__, "aws-elasticloadbalancingv2@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddNetworkTargetsProps", jsii_struct_bases=[], name_mapping={'port': 'port', 'deregistration_delay': 'deregistrationDelay', 'health_check': 'healthCheck', 'proxy_protocol_v2': 'proxyProtocolV2', 'target_group_name': 'targetGroupName', 'targets': 'targets'})
class AddNetworkTargetsProps():
    def __init__(self, *, port: jsii.Number, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, proxy_protocol_v2: typing.Optional[bool]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None):
        """Properties for adding new network targets to a listener.

        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
            'port': port,
        }
        if deregistration_delay is not None: self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None: self._values["health_check"] = health_check
        if proxy_protocol_v2 is not None: self._values["proxy_protocol_v2"] = proxy_protocol_v2
        if target_group_name is not None: self._values["target_group_name"] = target_group_name
        if targets is not None: self._values["targets"] = targets

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests.

        default
        :default: Determined from protocol if known
        """
        return self._values.get('port')

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('deregistration_delay')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        default
        :default: No health check
        """
        return self._values.get('health_check')

    @builtins.property
    def proxy_protocol_v2(self) -> typing.Optional[bool]:
        """Indicates whether Proxy Protocol version 2 is enabled.

        default
        :default: false
        """
        return self._values.get('proxy_protocol_v2')

    @builtins.property
    def target_group_name(self) -> typing.Optional[str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        default
        :default: Automatically generated
        """
        return self._values.get('target_group_name')

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["INetworkLoadBalancerTarget"]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddNetworkTargetsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddRuleProps", jsii_struct_bases=[], name_mapping={'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'priority': 'priority'})
class AddRuleProps():
    def __init__(self, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None):
        """Properties for adding a conditional load balancing rule.

        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        self._values = {
        }
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults
        """
        return self._values.get('priority')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetGroupsProps", jsii_struct_bases=[AddRuleProps], name_mapping={'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'priority': 'priority', 'target_groups': 'targetGroups'})
class AddApplicationTargetGroupsProps(AddRuleProps):
    def __init__(self, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, target_groups: typing.List["IApplicationTargetGroup"]):
        """Properties for adding a new target group to a listener.

        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param target_groups: Target groups to forward requests to.
        """
        self._values = {
            'target_groups': target_groups,
        }
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults
        """
        return self._values.get('priority')

    @builtins.property
    def target_groups(self) -> typing.List["IApplicationTargetGroup"]:
        """Target groups to forward requests to."""
        return self._values.get('target_groups')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddApplicationTargetGroupsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetsProps", jsii_struct_bases=[AddRuleProps], name_mapping={'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'priority': 'priority', 'deregistration_delay': 'deregistrationDelay', 'health_check': 'healthCheck', 'port': 'port', 'protocol': 'protocol', 'slow_start': 'slowStart', 'stickiness_cookie_duration': 'stickinessCookieDuration', 'target_group_name': 'targetGroupName', 'targets': 'targets'})
class AddApplicationTargetsProps(AddRuleProps):
    def __init__(self, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None):
        """Properties for adding new targets to a listener.

        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
        }
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority
        if deregistration_delay is not None: self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None: self._values["health_check"] = health_check
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if slow_start is not None: self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None: self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if target_group_name is not None: self._values["target_group_name"] = target_group_name
        if targets is not None: self._values["targets"] = targets

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults
        """
        return self._values.get('priority')

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('deregistration_delay')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        default
        :default: No health check
        """
        return self._values.get('health_check')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: Determined from protocol if known
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional["ApplicationProtocol"]:
        """The protocol to use.

        default
        :default: Determined from port if known
        """
        return self._values.get('protocol')

    @builtins.property
    def slow_start(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        default
        :default: 0
        """
        return self._values.get('slow_start')

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        default
        :default: Duration.days(1)
        """
        return self._values.get('stickiness_cookie_duration')

    @builtins.property
    def target_group_name(self) -> typing.Optional[str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        default
        :default: Automatically generated
        """
        return self._values.get('target_group_name')

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. All target must be of the same type.
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddApplicationTargetsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerAttributes", jsii_struct_bases=[], name_mapping={'listener_arn': 'listenerArn', 'default_port': 'defaultPort', 'security_group': 'securityGroup', 'security_group_allows_all_outbound': 'securityGroupAllowsAllOutbound', 'security_group_id': 'securityGroupId'})
class ApplicationListenerAttributes():
    def __init__(self, *, listener_arn: str, default_port: typing.Optional[jsii.Number]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_group_allows_all_outbound: typing.Optional[bool]=None, security_group_id: typing.Optional[str]=None):
        """Properties to reference an existing listener.

        :param listener_arn: ARN of the listener.
        :param default_port: The default port on which this listener is listening.
        :param security_group: Security group of the load balancer this listener is associated with.
        :param security_group_allows_all_outbound: Whether the imported security group allows all outbound traffic or not when imported using ``securityGroupId``. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param security_group_id: Security group ID of the load balancer this listener is associated with.
        """
        self._values = {
            'listener_arn': listener_arn,
        }
        if default_port is not None: self._values["default_port"] = default_port
        if security_group is not None: self._values["security_group"] = security_group
        if security_group_allows_all_outbound is not None: self._values["security_group_allows_all_outbound"] = security_group_allows_all_outbound
        if security_group_id is not None: self._values["security_group_id"] = security_group_id

    @builtins.property
    def listener_arn(self) -> str:
        """ARN of the listener."""
        return self._values.get('listener_arn')

    @builtins.property
    def default_port(self) -> typing.Optional[jsii.Number]:
        """The default port on which this listener is listening."""
        return self._values.get('default_port')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security group of the load balancer this listener is associated with."""
        return self._values.get('security_group')

    @builtins.property
    def security_group_allows_all_outbound(self) -> typing.Optional[bool]:
        """Whether the imported security group allows all outbound traffic or not when imported using ``securityGroupId``.

        Unless set to ``false``, no egress rules will be added to the security group.

        default
        :default: true

        deprecated
        :deprecated: use ``securityGroup`` instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group_allows_all_outbound')

    @builtins.property
    def security_group_id(self) -> typing.Optional[str]:
        """Security group ID of the load balancer this listener is associated with.

        deprecated
        :deprecated: use ``securityGroup`` instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationListenerAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationListenerCertificate(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificate"):
    """Add certificates to a listener."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, listener: "IApplicationListener", certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param listener: The listener to attach the rule to.
        :param certificate_arns: ARNs of certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        :param certificates: Certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        """
        props = ApplicationListenerCertificateProps(listener=listener, certificate_arns=certificate_arns, certificates=certificates)

        jsii.create(ApplicationListenerCertificate, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificateProps", jsii_struct_bases=[], name_mapping={'listener': 'listener', 'certificate_arns': 'certificateArns', 'certificates': 'certificates'})
class ApplicationListenerCertificateProps():
    def __init__(self, *, listener: "IApplicationListener", certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None):
        """Properties for adding a set of certificates to a listener.

        :param listener: The listener to attach the rule to.
        :param certificate_arns: ARNs of certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        :param certificates: Certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        """
        self._values = {
            'listener': listener,
        }
        if certificate_arns is not None: self._values["certificate_arns"] = certificate_arns
        if certificates is not None: self._values["certificates"] = certificates

    @builtins.property
    def listener(self) -> "IApplicationListener":
        """The listener to attach the rule to."""
        return self._values.get('listener')

    @builtins.property
    def certificate_arns(self) -> typing.Optional[typing.List[str]]:
        """ARNs of certificates to attach.

        Duplicates are not allowed.

        default
        :default: - One of 'certificates' and 'certificateArns' is required.

        deprecated
        :deprecated: Use ``certificates`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get('certificate_arns')

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificates to attach.

        Duplicates are not allowed.

        default
        :default: - One of 'certificates' and 'certificateArns' is required.
        """
        return self._values.get('certificates')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationListenerCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationListenerRule(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRule"):
    """Define a new listener rule."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, listener: "IApplicationListener", priority: jsii.Number, fixed_response: typing.Optional["FixedResponse"]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, redirect_response: typing.Optional["RedirectResponse"]=None, target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param listener: The listener to attach the rule to.
        :param priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param fixed_response: Fixed response to return. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Default: - No path condition.
        :param redirect_response: Redirect response to return. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No redirect response.
        :param target_groups: Target groups to forward requests to. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No target groups.
        """
        props = ApplicationListenerRuleProps(listener=listener, priority=priority, fixed_response=fixed_response, host_header=host_header, path_pattern=path_pattern, redirect_response=redirect_response, target_groups=target_groups)

        jsii.create(ApplicationListenerRule, self, [scope, id, props])

    @jsii.member(jsii_name="addFixedResponse")
    def add_fixed_response(self, *, status_code: str, content_type: typing.Optional["ContentType"]=None, message_body: typing.Optional[str]=None) -> None:
        """Add a fixed response.

        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message
        """
        fixed_response = FixedResponse(status_code=status_code, content_type=content_type, message_body=message_body)

        return jsii.invoke(self, "addFixedResponse", [fixed_response])

    @jsii.member(jsii_name="addRedirectResponse")
    def add_redirect_response(self, *, status_code: str, host: typing.Optional[str]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional[str]=None, query: typing.Optional[str]=None) -> None:
        """Add a redirect response.

        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request
        """
        redirect_response = RedirectResponse(status_code=status_code, host=host, path=path, port=port, protocol=protocol, query=query)

        return jsii.invoke(self, "addRedirectResponse", [redirect_response])

    @jsii.member(jsii_name="addTargetGroup")
    def add_target_group(self, target_group: "IApplicationTargetGroup") -> None:
        """Add a TargetGroup to load balance to.

        :param target_group: -
        """
        return jsii.invoke(self, "addTargetGroup", [target_group])

    @jsii.member(jsii_name="setCondition")
    def set_condition(self, field: str, values: typing.Optional[typing.List[str]]=None) -> None:
        """Add a non-standard condition to this rule.

        :param field: -
        :param values: -
        """
        return jsii.invoke(self, "setCondition", [field, values])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the rule."""
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> str:
        """The ARN of this rule."""
        return jsii.get(self, "listenerRuleArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerAttributes", jsii_struct_bases=[], name_mapping={'load_balancer_arn': 'loadBalancerArn', 'security_group_id': 'securityGroupId', 'load_balancer_canonical_hosted_zone_id': 'loadBalancerCanonicalHostedZoneId', 'load_balancer_dns_name': 'loadBalancerDnsName', 'security_group_allows_all_outbound': 'securityGroupAllowsAllOutbound'})
class ApplicationLoadBalancerAttributes():
    def __init__(self, *, load_balancer_arn: str, security_group_id: str, load_balancer_canonical_hosted_zone_id: typing.Optional[str]=None, load_balancer_dns_name: typing.Optional[str]=None, security_group_allows_all_outbound: typing.Optional[bool]=None):
        """Properties to reference an existing load balancer.

        :param load_balancer_arn: ARN of the load balancer.
        :param security_group_id: ID of the load balancer's security group.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param security_group_allows_all_outbound: Whether the security group allows all outbound traffic or not. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        """
        self._values = {
            'load_balancer_arn': load_balancer_arn,
            'security_group_id': security_group_id,
        }
        if load_balancer_canonical_hosted_zone_id is not None: self._values["load_balancer_canonical_hosted_zone_id"] = load_balancer_canonical_hosted_zone_id
        if load_balancer_dns_name is not None: self._values["load_balancer_dns_name"] = load_balancer_dns_name
        if security_group_allows_all_outbound is not None: self._values["security_group_allows_all_outbound"] = security_group_allows_all_outbound

    @builtins.property
    def load_balancer_arn(self) -> str:
        """ARN of the load balancer."""
        return self._values.get('load_balancer_arn')

    @builtins.property
    def security_group_id(self) -> str:
        """ID of the load balancer's security group."""
        return self._values.get('security_group_id')

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> typing.Optional[str]:
        """The canonical hosted zone ID of this load balancer.

        default
        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        return self._values.get('load_balancer_canonical_hosted_zone_id')

    @builtins.property
    def load_balancer_dns_name(self) -> typing.Optional[str]:
        """The DNS name of this load balancer.

        default
        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        return self._values.get('load_balancer_dns_name')

    @builtins.property
    def security_group_allows_all_outbound(self) -> typing.Optional[bool]:
        """Whether the security group allows all outbound traffic or not.

        Unless set to ``false``, no egress rules will be added to the security group.

        default
        :default: true
        """
        return self._values.get('security_group_allows_all_outbound')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancerAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationProtocol")
class ApplicationProtocol(enum.Enum):
    """Load balancing protocol for application load balancers."""
    HTTP = "HTTP"
    """HTTP."""
    HTTPS = "HTTPS"
    """HTTPS."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerProps", jsii_struct_bases=[], name_mapping={'certificate_arns': 'certificateArns', 'certificates': 'certificates', 'default_target_groups': 'defaultTargetGroups', 'open': 'open', 'port': 'port', 'protocol': 'protocol', 'ssl_policy': 'sslPolicy'})
class BaseApplicationListenerProps():
    def __init__(self, *, certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None):
        """Basic properties for an ApplicationListener.

        :param certificate_arns: The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        self._values = {
        }
        if certificate_arns is not None: self._values["certificate_arns"] = certificate_arns
        if certificates is not None: self._values["certificates"] = certificates
        if default_target_groups is not None: self._values["default_target_groups"] = default_target_groups
        if open is not None: self._values["open"] = open
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if ssl_policy is not None: self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def certificate_arns(self) -> typing.Optional[typing.List[str]]:
        """The certificates to use on this listener.

        default
        :default: - No certificates.

        deprecated
        :deprecated: Use the ``certificates`` property instead

        stability
        :stability: deprecated
        """
        return self._values.get('certificate_arns')

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificate list of ACM cert ARNs.

        default
        :default: - No certificates.
        """
        return self._values.get('certificates')

    @builtins.property
    def default_target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Default target groups to load balance to.

        default
        :default: - None.
        """
        return self._values.get('default_target_groups')

    @builtins.property
    def open(self) -> typing.Optional[bool]:
        """Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        default
        :default: true
        """
        return self._values.get('open')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: - Determined from protocol if known.
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional["ApplicationProtocol"]:
        """The protocol to use.

        default
        :default: - Determined from port if known.
        """
        return self._values.get('protocol')

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """The security policy that defines which ciphers and protocols are supported.

        default
        :default: - The current predefined security policy.
        """
        return self._values.get('ssl_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseApplicationListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerProps", jsii_struct_bases=[BaseApplicationListenerProps], name_mapping={'certificate_arns': 'certificateArns', 'certificates': 'certificates', 'default_target_groups': 'defaultTargetGroups', 'open': 'open', 'port': 'port', 'protocol': 'protocol', 'ssl_policy': 'sslPolicy', 'load_balancer': 'loadBalancer'})
class ApplicationListenerProps(BaseApplicationListenerProps):
    def __init__(self, *, certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None, load_balancer: "IApplicationLoadBalancer"):
        """Properties for defining a standalone ApplicationListener.

        :param certificate_arns: The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        :param load_balancer: The load balancer to attach this listener to.
        """
        self._values = {
            'load_balancer': load_balancer,
        }
        if certificate_arns is not None: self._values["certificate_arns"] = certificate_arns
        if certificates is not None: self._values["certificates"] = certificates
        if default_target_groups is not None: self._values["default_target_groups"] = default_target_groups
        if open is not None: self._values["open"] = open
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if ssl_policy is not None: self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def certificate_arns(self) -> typing.Optional[typing.List[str]]:
        """The certificates to use on this listener.

        default
        :default: - No certificates.

        deprecated
        :deprecated: Use the ``certificates`` property instead

        stability
        :stability: deprecated
        """
        return self._values.get('certificate_arns')

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificate list of ACM cert ARNs.

        default
        :default: - No certificates.
        """
        return self._values.get('certificates')

    @builtins.property
    def default_target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Default target groups to load balance to.

        default
        :default: - None.
        """
        return self._values.get('default_target_groups')

    @builtins.property
    def open(self) -> typing.Optional[bool]:
        """Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        default
        :default: true
        """
        return self._values.get('open')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: - Determined from protocol if known.
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional["ApplicationProtocol"]:
        """The protocol to use.

        default
        :default: - Determined from port if known.
        """
        return self._values.get('protocol')

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """The security policy that defines which ciphers and protocols are supported.

        default
        :default: - The current predefined security policy.
        """
        return self._values.get('ssl_policy')

    @builtins.property
    def load_balancer(self) -> "IApplicationLoadBalancer":
        """The load balancer to attach this listener to."""
        return self._values.get('load_balancer')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerRuleProps", jsii_struct_bases=[], name_mapping={'priority': 'priority', 'fixed_response': 'fixedResponse', 'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'redirect_response': 'redirectResponse', 'target_groups': 'targetGroups'})
class BaseApplicationListenerRuleProps():
    def __init__(self, *, priority: jsii.Number, fixed_response: typing.Optional["FixedResponse"]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, redirect_response: typing.Optional["RedirectResponse"]=None, target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None):
        """Basic properties for defining a rule on a listener.

        :param priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param fixed_response: Fixed response to return. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Default: - No path condition.
        :param redirect_response: Redirect response to return. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No redirect response.
        :param target_groups: Target groups to forward requests to. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No target groups.
        """
        if isinstance(fixed_response, dict): fixed_response = FixedResponse(**fixed_response)
        if isinstance(redirect_response, dict): redirect_response = RedirectResponse(**redirect_response)
        self._values = {
            'priority': priority,
        }
        if fixed_response is not None: self._values["fixed_response"] = fixed_response
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if redirect_response is not None: self._values["redirect_response"] = redirect_response
        if target_groups is not None: self._values["target_groups"] = target_groups

    @builtins.property
    def priority(self) -> jsii.Number:
        """Priority of the rule.

        The rule with the lowest priority will be used for every request.

        Priorities must be unique.
        """
        return self._values.get('priority')

    @builtins.property
    def fixed_response(self) -> typing.Optional["FixedResponse"]:
        """Fixed response to return.

        Only one of ``fixedResponse``, ``redirectResponse`` or
        ``targetGroups`` can be specified.

        default
        :default: - No fixed response.
        """
        return self._values.get('fixed_response')

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        default
        :default: - No host condition.

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        default
        :default: - No path condition.

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def redirect_response(self) -> typing.Optional["RedirectResponse"]:
        """Redirect response to return.

        Only one of ``fixedResponse``, ``redirectResponse`` or
        ``targetGroups`` can be specified.

        default
        :default: - No redirect response.
        """
        return self._values.get('redirect_response')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Target groups to forward requests to.

        Only one of ``fixedResponse``, ``redirectResponse`` or
        ``targetGroups`` can be specified.

        default
        :default: - No target groups.
        """
        return self._values.get('target_groups')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseApplicationListenerRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRuleProps", jsii_struct_bases=[BaseApplicationListenerRuleProps], name_mapping={'priority': 'priority', 'fixed_response': 'fixedResponse', 'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'redirect_response': 'redirectResponse', 'target_groups': 'targetGroups', 'listener': 'listener'})
class ApplicationListenerRuleProps(BaseApplicationListenerRuleProps):
    def __init__(self, *, priority: jsii.Number, fixed_response: typing.Optional["FixedResponse"]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, redirect_response: typing.Optional["RedirectResponse"]=None, target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, listener: "IApplicationListener"):
        """Properties for defining a listener rule.

        :param priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param fixed_response: Fixed response to return. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Default: - No path condition.
        :param redirect_response: Redirect response to return. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No redirect response.
        :param target_groups: Target groups to forward requests to. Only one of ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No target groups.
        :param listener: The listener to attach the rule to.
        """
        if isinstance(fixed_response, dict): fixed_response = FixedResponse(**fixed_response)
        if isinstance(redirect_response, dict): redirect_response = RedirectResponse(**redirect_response)
        self._values = {
            'priority': priority,
            'listener': listener,
        }
        if fixed_response is not None: self._values["fixed_response"] = fixed_response
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if redirect_response is not None: self._values["redirect_response"] = redirect_response
        if target_groups is not None: self._values["target_groups"] = target_groups

    @builtins.property
    def priority(self) -> jsii.Number:
        """Priority of the rule.

        The rule with the lowest priority will be used for every request.

        Priorities must be unique.
        """
        return self._values.get('priority')

    @builtins.property
    def fixed_response(self) -> typing.Optional["FixedResponse"]:
        """Fixed response to return.

        Only one of ``fixedResponse``, ``redirectResponse`` or
        ``targetGroups`` can be specified.

        default
        :default: - No fixed response.
        """
        return self._values.get('fixed_response')

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        default
        :default: - No host condition.

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        default
        :default: - No path condition.

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def redirect_response(self) -> typing.Optional["RedirectResponse"]:
        """Redirect response to return.

        Only one of ``fixedResponse``, ``redirectResponse`` or
        ``targetGroups`` can be specified.

        default
        :default: - No redirect response.
        """
        return self._values.get('redirect_response')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Target groups to forward requests to.

        Only one of ``fixedResponse``, ``redirectResponse`` or
        ``targetGroups`` can be specified.

        default
        :default: - No target groups.
        """
        return self._values.get('target_groups')

    @builtins.property
    def listener(self) -> "IApplicationListener":
        """The listener to attach the rule to."""
        return self._values.get('listener')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationListenerRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BaseListener(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseListener"):
    """Base class for listeners."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseListenerProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, additional_props: typing.Any) -> None:
        """
        :param scope: -
        :param id: -
        :param additional_props: -
        """
        jsii.create(BaseListener, self, [scope, id, additional_props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this listener."""
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "listenerArn")


class _BaseListenerProxy(BaseListener, jsii.proxy_for(aws_cdk.core.Resource)):
    pass

class BaseLoadBalancer(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancer"):
    """Base class for both Application and Network Load Balancers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseLoadBalancerProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, base_props: "BaseLoadBalancerProps", additional_props: typing.Any) -> None:
        """
        :param scope: -
        :param id: -
        :param base_props: -
        :param additional_props: -
        """
        jsii.create(BaseLoadBalancer, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="removeAttribute")
    def remove_attribute(self, key: str) -> None:
        """Remove an attribute from the load balancer.

        :param key: -
        """
        return jsii.invoke(self, "removeAttribute", [key])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: str, value: typing.Optional[str]=None) -> None:
        """Set a non-standard attribute on the load balancer.

        :param key: -
        :param value: -

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#load-balancer-attributes
        """
        return jsii.invoke(self, "setAttribute", [key, value])

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:elasticloadbalancing:us-west-2123456789012loadbalancer / app / my - internal - load - balancer / 50dc6c495c0c9188
        """
        return jsii.get(self, "loadBalancerArn")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """The canonical hosted zone ID of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """The DNS name of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        """
        return jsii.get(self, "loadBalancerDnsName")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerFullName")
    def load_balancer_full_name(self) -> str:
        """The full name of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 50dc6c495c0c9188
        """
        return jsii.get(self, "loadBalancerFullName")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        """The name of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer
        """
        return jsii.get(self, "loadBalancerName")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSecurityGroups")
    def load_balancer_security_groups(self) -> typing.List[str]:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerSecurityGroups")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in, if available.

        If the Load Balancer was imported, the VPC is not available.
        """
        return jsii.get(self, "vpc")


class _BaseLoadBalancerProxy(BaseLoadBalancer, jsii.proxy_for(aws_cdk.core.Resource)):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancerProps", jsii_struct_bases=[], name_mapping={'vpc': 'vpc', 'deletion_protection': 'deletionProtection', 'internet_facing': 'internetFacing', 'load_balancer_name': 'loadBalancerName', 'vpc_subnets': 'vpcSubnets'})
class BaseLoadBalancerProps():
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None):
        """Shared properties of both Application and Network Load Balancers.

        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, Private subnets if internal and there are Private subnets, Isolated subnets if internal and there are no Private subnets.
        """
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'vpc': vpc,
        }
        if deletion_protection is not None: self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None: self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network to place the load balancer in."""
        return self._values.get('vpc')

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether deletion protection is enabled.

        default
        :default: false
        """
        return self._values.get('deletion_protection')

    @builtins.property
    def internet_facing(self) -> typing.Optional[bool]:
        """Whether the load balancer has an internet-routable address.

        default
        :default: false
        """
        return self._values.get('internet_facing')

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[str]:
        """Name of the load balancer.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('load_balancer_name')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where in the VPC to place the load balancer.

        default
        :default:

        - Public subnets if internetFacing, Private subnets if internal and
          there are Private subnets, Isolated subnets if internal and there are no
          Private subnets.
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerProps", jsii_struct_bases=[BaseLoadBalancerProps], name_mapping={'vpc': 'vpc', 'deletion_protection': 'deletionProtection', 'internet_facing': 'internetFacing', 'load_balancer_name': 'loadBalancerName', 'vpc_subnets': 'vpcSubnets', 'http2_enabled': 'http2Enabled', 'idle_timeout': 'idleTimeout', 'ip_address_type': 'ipAddressType', 'security_group': 'securityGroup'})
class ApplicationLoadBalancerProps(BaseLoadBalancerProps):
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, http2_enabled: typing.Optional[bool]=None, idle_timeout: typing.Optional[aws_cdk.core.Duration]=None, ip_address_type: typing.Optional["IpAddressType"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None):
        """Properties for defining an Application Load Balancer.

        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, Private subnets if internal and there are Private subnets, Isolated subnets if internal and there are no Private subnets.
        :param http2_enabled: Indicates whether HTTP/2 is enabled. Default: true
        :param idle_timeout: The load balancer idle timeout, in seconds. Default: 60
        :param ip_address_type: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param security_group: Security group to associate with this load balancer. Default: A security group is created
        """
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'vpc': vpc,
        }
        if deletion_protection is not None: self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None: self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if http2_enabled is not None: self._values["http2_enabled"] = http2_enabled
        if idle_timeout is not None: self._values["idle_timeout"] = idle_timeout
        if ip_address_type is not None: self._values["ip_address_type"] = ip_address_type
        if security_group is not None: self._values["security_group"] = security_group

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network to place the load balancer in."""
        return self._values.get('vpc')

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether deletion protection is enabled.

        default
        :default: false
        """
        return self._values.get('deletion_protection')

    @builtins.property
    def internet_facing(self) -> typing.Optional[bool]:
        """Whether the load balancer has an internet-routable address.

        default
        :default: false
        """
        return self._values.get('internet_facing')

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[str]:
        """Name of the load balancer.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('load_balancer_name')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where in the VPC to place the load balancer.

        default
        :default:

        - Public subnets if internetFacing, Private subnets if internal and
          there are Private subnets, Isolated subnets if internal and there are no
          Private subnets.
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def http2_enabled(self) -> typing.Optional[bool]:
        """Indicates whether HTTP/2 is enabled.

        default
        :default: true
        """
        return self._values.get('http2_enabled')

    @builtins.property
    def idle_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The load balancer idle timeout, in seconds.

        default
        :default: 60
        """
        return self._values.get('idle_timeout')

    @builtins.property
    def ip_address_type(self) -> typing.Optional["IpAddressType"]:
        """The type of IP addresses to use.

        Only applies to application load balancers.

        default
        :default: IpAddressType.Ipv4
        """
        return self._values.get('ip_address_type')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security group to associate with this load balancer.

        default
        :default: A security group is created
        """
        return self._values.get('security_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseNetworkListenerProps", jsii_struct_bases=[], name_mapping={'port': 'port', 'certificates': 'certificates', 'default_target_groups': 'defaultTargetGroups', 'protocol': 'protocol', 'ssl_policy': 'sslPolicy'})
class BaseNetworkListenerProps():
    def __init__(self, *, port: jsii.Number, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None):
        """Basic properties for a Network Listener.

        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.
        """
        self._values = {
            'port': port,
        }
        if certificates is not None: self._values["certificates"] = certificates
        if default_target_groups is not None: self._values["default_target_groups"] = default_target_groups
        if protocol is not None: self._values["protocol"] = protocol
        if ssl_policy is not None: self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests."""
        return self._values.get('port')

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificate list of ACM cert ARNs.

        default
        :default: - No certificates.
        """
        return self._values.get('certificates')

    @builtins.property
    def default_target_groups(self) -> typing.Optional[typing.List["INetworkTargetGroup"]]:
        """Default target groups to load balance to.

        default
        :default: - None.
        """
        return self._values.get('default_target_groups')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """Protocol for listener, expects TCP or TLS.

        default
        :default: - TLS if certificates are provided. TCP otherwise.
        """
        return self._values.get('protocol')

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """SSL Policy.

        default
        :default: - Current predefined security policy.
        """
        return self._values.get('ssl_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseNetworkListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseTargetGroupProps", jsii_struct_bases=[], name_mapping={'deregistration_delay': 'deregistrationDelay', 'health_check': 'healthCheck', 'target_group_name': 'targetGroupName', 'target_type': 'targetType', 'vpc': 'vpc'})
class BaseTargetGroupProps():
    def __init__(self, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """Basic properties of both Application and Network Target Groups.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
        }
        if deregistration_delay is not None: self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None: self._values["health_check"] = health_check
        if target_group_name is not None: self._values["target_group_name"] = target_group_name
        if target_type is not None: self._values["target_type"] = target_type
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        default
        :default: 300
        """
        return self._values.get('deregistration_delay')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        default
        :default: - None.
        """
        return self._values.get('health_check')

    @builtins.property
    def target_group_name(self) -> typing.Optional[str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        default
        :default: - Automatically generated.
        """
        return self._values.get('target_group_name')

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        """The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        default
        :default: - Determined automatically.
        """
        return self._values.get('target_type')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        default
        :default: - undefined
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseTargetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroupProps", jsii_struct_bases=[BaseTargetGroupProps], name_mapping={'deregistration_delay': 'deregistrationDelay', 'health_check': 'healthCheck', 'target_group_name': 'targetGroupName', 'target_type': 'targetType', 'vpc': 'vpc', 'port': 'port', 'protocol': 'protocol', 'slow_start': 'slowStart', 'stickiness_cookie_duration': 'stickinessCookieDuration', 'targets': 'targets'})
class ApplicationTargetGroupProps(BaseTargetGroupProps):
    def __init__(self, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None):
        """Properties for defining an Application Target Group.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known, optional for Lambda targets.
        :param protocol: The protocol to use. Default: - Determined from port if known, optional for Lambda targets.
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
        }
        if deregistration_delay is not None: self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None: self._values["health_check"] = health_check
        if target_group_name is not None: self._values["target_group_name"] = target_group_name
        if target_type is not None: self._values["target_type"] = target_type
        if vpc is not None: self._values["vpc"] = vpc
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if slow_start is not None: self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None: self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if targets is not None: self._values["targets"] = targets

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        default
        :default: 300
        """
        return self._values.get('deregistration_delay')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        default
        :default: - None.
        """
        return self._values.get('health_check')

    @builtins.property
    def target_group_name(self) -> typing.Optional[str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        default
        :default: - Automatically generated.
        """
        return self._values.get('target_group_name')

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        """The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        default
        :default: - Determined automatically.
        """
        return self._values.get('target_type')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        default
        :default: - undefined
        """
        return self._values.get('vpc')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: - Determined from protocol if known, optional for Lambda targets.
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional["ApplicationProtocol"]:
        """The protocol to use.

        default
        :default: - Determined from port if known, optional for Lambda targets.
        """
        return self._values.get('protocol')

    @builtins.property
    def slow_start(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        default
        :default: 0
        """
        return self._values.get('slow_start')

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        default
        :default: Duration.days(1)
        """
        return self._values.get('stickiness_cookie_duration')

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        default
        :default: - No targets.
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationTargetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListener(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::Listener``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticLoadBalancingV2::Listener
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, default_actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ActionProperty", aws_cdk.core.IResolvable]]], load_balancer_arn: str, port: jsii.Number, protocol: str, certificates: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CertificateProperty"]]]]]=None, ssl_policy: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_actions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
        :param load_balancer_arn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
        :param port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
        :param certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
        :param ssl_policy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.
        """
        props = CfnListenerProps(default_actions=default_actions, load_balancer_arn=load_balancer_arn, port=port, protocol=protocol, certificates=certificates, ssl_policy=ssl_policy)

        jsii.create(CfnListener, self, [scope, id, props])

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
    @jsii.member(jsii_name="defaultActions")
    def default_actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ActionProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        """
        return jsii.get(self, "defaultActions")

    @default_actions.setter
    def default_actions(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ActionProperty", aws_cdk.core.IResolvable]]]):
        jsii.set(self, "defaultActions", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        """
        return jsii.get(self, "loadBalancerArn")

    @load_balancer_arn.setter
    def load_balancer_arn(self, value: str):
        jsii.set(self, "loadBalancerArn", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """``AWS::ElasticLoadBalancingV2::Listener.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: jsii.Number):
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> str:
        """``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: str):
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="certificates")
    def certificates(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CertificateProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        """
        return jsii.get(self, "certificates")

    @certificates.setter
    def certificates(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CertificateProperty"]]]]]):
        jsii.set(self, "certificates", value)

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        """
        return jsii.get(self, "sslPolicy")

    @ssl_policy.setter
    def ssl_policy(self, value: typing.Optional[str]):
        jsii.set(self, "sslPolicy", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.ActionProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'authenticate_cognito_config': 'authenticateCognitoConfig', 'authenticate_oidc_config': 'authenticateOidcConfig', 'fixed_response_config': 'fixedResponseConfig', 'order': 'order', 'redirect_config': 'redirectConfig', 'target_group_arn': 'targetGroupArn'})
    class ActionProperty():
        def __init__(self, *, type: str, authenticate_cognito_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.AuthenticateCognitoConfigProperty"]]]=None, authenticate_oidc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.AuthenticateOidcConfigProperty"]]]=None, fixed_response_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.FixedResponseConfigProperty"]]]=None, order: typing.Optional[jsii.Number]=None, redirect_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.RedirectConfigProperty"]]]=None, target_group_arn: typing.Optional[str]=None):
            """
            :param type: ``CfnListener.ActionProperty.Type``.
            :param authenticate_cognito_config: ``CfnListener.ActionProperty.AuthenticateCognitoConfig``.
            :param authenticate_oidc_config: ``CfnListener.ActionProperty.AuthenticateOidcConfig``.
            :param fixed_response_config: ``CfnListener.ActionProperty.FixedResponseConfig``.
            :param order: ``CfnListener.ActionProperty.Order``.
            :param redirect_config: ``CfnListener.ActionProperty.RedirectConfig``.
            :param target_group_arn: ``CfnListener.ActionProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html
            """
            self._values = {
                'type': type,
            }
            if authenticate_cognito_config is not None: self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None: self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None: self._values["fixed_response_config"] = fixed_response_config
            if order is not None: self._values["order"] = order
            if redirect_config is not None: self._values["redirect_config"] = redirect_config
            if target_group_arn is not None: self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def type(self) -> str:
            """``CfnListener.ActionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-defaultactions-type
            """
            return self._values.get('type')

        @builtins.property
        def authenticate_cognito_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.AuthenticateCognitoConfigProperty"]]]:
            """``CfnListener.ActionProperty.AuthenticateCognitoConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-authenticatecognitoconfig
            """
            return self._values.get('authenticate_cognito_config')

        @builtins.property
        def authenticate_oidc_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.AuthenticateOidcConfigProperty"]]]:
            """``CfnListener.ActionProperty.AuthenticateOidcConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-authenticateoidcconfig
            """
            return self._values.get('authenticate_oidc_config')

        @builtins.property
        def fixed_response_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.FixedResponseConfigProperty"]]]:
            """``CfnListener.ActionProperty.FixedResponseConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-fixedresponseconfig
            """
            return self._values.get('fixed_response_config')

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            """``CfnListener.ActionProperty.Order``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-order
            """
            return self._values.get('order')

        @builtins.property
        def redirect_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListener.RedirectConfigProperty"]]]:
            """``CfnListener.ActionProperty.RedirectConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-redirectconfig
            """
            return self._values.get('redirect_config')

        @builtins.property
        def target_group_arn(self) -> typing.Optional[str]:
            """``CfnListener.ActionProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-defaultactions-targetgrouparn
            """
            return self._values.get('target_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateCognitoConfigProperty", jsii_struct_bases=[], name_mapping={'user_pool_arn': 'userPoolArn', 'user_pool_client_id': 'userPoolClientId', 'user_pool_domain': 'userPoolDomain', 'authentication_request_extra_params': 'authenticationRequestExtraParams', 'on_unauthenticated_request': 'onUnauthenticatedRequest', 'scope': 'scope', 'session_cookie_name': 'sessionCookieName', 'session_timeout': 'sessionTimeout'})
    class AuthenticateCognitoConfigProperty():
        def __init__(self, *, user_pool_arn: str, user_pool_client_id: str, user_pool_domain: str, authentication_request_extra_params: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, on_unauthenticated_request: typing.Optional[str]=None, scope: typing.Optional[str]=None, session_cookie_name: typing.Optional[str]=None, session_timeout: typing.Optional[jsii.Number]=None):
            """
            :param user_pool_arn: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.
            :param user_pool_client_id: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.
            :param user_pool_domain: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.
            :param authentication_request_extra_params: ``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListener.AuthenticateCognitoConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html
            """
            self._values = {
                'user_pool_arn': user_pool_arn,
                'user_pool_client_id': user_pool_client_id,
                'user_pool_domain': user_pool_domain,
            }
            if authentication_request_extra_params is not None: self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None: self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None: self._values["scope"] = scope
            if session_cookie_name is not None: self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None: self._values["session_timeout"] = session_timeout

        @builtins.property
        def user_pool_arn(self) -> str:
            """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolarn
            """
            return self._values.get('user_pool_arn')

        @builtins.property
        def user_pool_client_id(self) -> str:
            """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolclientid
            """
            return self._values.get('user_pool_client_id')

        @builtins.property
        def user_pool_domain(self) -> str:
            """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpooldomain
            """
            return self._values.get('user_pool_domain')

        @builtins.property
        def authentication_request_extra_params(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-authenticationrequestextraparams
            """
            return self._values.get('authentication_request_extra_params')

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-onunauthenticatedrequest
            """
            return self._values.get('on_unauthenticated_request')

        @builtins.property
        def scope(self) -> typing.Optional[str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-scope
            """
            return self._values.get('scope')

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessioncookiename
            """
            return self._values.get('session_cookie_name')

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessiontimeout
            """
            return self._values.get('session_timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AuthenticateCognitoConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateOidcConfigProperty", jsii_struct_bases=[], name_mapping={'authorization_endpoint': 'authorizationEndpoint', 'client_id': 'clientId', 'client_secret': 'clientSecret', 'issuer': 'issuer', 'token_endpoint': 'tokenEndpoint', 'user_info_endpoint': 'userInfoEndpoint', 'authentication_request_extra_params': 'authenticationRequestExtraParams', 'on_unauthenticated_request': 'onUnauthenticatedRequest', 'scope': 'scope', 'session_cookie_name': 'sessionCookieName', 'session_timeout': 'sessionTimeout'})
    class AuthenticateOidcConfigProperty():
        def __init__(self, *, authorization_endpoint: str, client_id: str, client_secret: str, issuer: str, token_endpoint: str, user_info_endpoint: str, authentication_request_extra_params: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, on_unauthenticated_request: typing.Optional[str]=None, scope: typing.Optional[str]=None, session_cookie_name: typing.Optional[str]=None, session_timeout: typing.Optional[jsii.Number]=None):
            """
            :param authorization_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.
            :param client_id: ``CfnListener.AuthenticateOidcConfigProperty.ClientId``.
            :param client_secret: ``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.
            :param issuer: ``CfnListener.AuthenticateOidcConfigProperty.Issuer``.
            :param token_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.
            :param user_info_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.
            :param authentication_request_extra_params: ``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListener.AuthenticateOidcConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html
            """
            self._values = {
                'authorization_endpoint': authorization_endpoint,
                'client_id': client_id,
                'client_secret': client_secret,
                'issuer': issuer,
                'token_endpoint': token_endpoint,
                'user_info_endpoint': user_info_endpoint,
            }
            if authentication_request_extra_params is not None: self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None: self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None: self._values["scope"] = scope
            if session_cookie_name is not None: self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None: self._values["session_timeout"] = session_timeout

        @builtins.property
        def authorization_endpoint(self) -> str:
            """``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authorizationendpoint
            """
            return self._values.get('authorization_endpoint')

        @builtins.property
        def client_id(self) -> str:
            """``CfnListener.AuthenticateOidcConfigProperty.ClientId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientid
            """
            return self._values.get('client_id')

        @builtins.property
        def client_secret(self) -> str:
            """``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientsecret
            """
            return self._values.get('client_secret')

        @builtins.property
        def issuer(self) -> str:
            """``CfnListener.AuthenticateOidcConfigProperty.Issuer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-issuer
            """
            return self._values.get('issuer')

        @builtins.property
        def token_endpoint(self) -> str:
            """``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-tokenendpoint
            """
            return self._values.get('token_endpoint')

        @builtins.property
        def user_info_endpoint(self) -> str:
            """``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-userinfoendpoint
            """
            return self._values.get('user_info_endpoint')

        @builtins.property
        def authentication_request_extra_params(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authenticationrequestextraparams
            """
            return self._values.get('authentication_request_extra_params')

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[str]:
            """``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-onunauthenticatedrequest
            """
            return self._values.get('on_unauthenticated_request')

        @builtins.property
        def scope(self) -> typing.Optional[str]:
            """``CfnListener.AuthenticateOidcConfigProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-scope
            """
            return self._values.get('scope')

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[str]:
            """``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessioncookiename
            """
            return self._values.get('session_cookie_name')

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessiontimeout
            """
            return self._values.get('session_timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AuthenticateOidcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.CertificateProperty", jsii_struct_bases=[], name_mapping={'certificate_arn': 'certificateArn'})
    class CertificateProperty():
        def __init__(self, *, certificate_arn: typing.Optional[str]=None):
            """
            :param certificate_arn: ``CfnListener.CertificateProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html
            """
            self._values = {
            }
            if certificate_arn is not None: self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[str]:
            """``CfnListener.CertificateProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html#cfn-elasticloadbalancingv2-listener-certificates-certificatearn
            """
            return self._values.get('certificate_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CertificateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'content_type': 'contentType', 'message_body': 'messageBody'})
    class FixedResponseConfigProperty():
        def __init__(self, *, status_code: str, content_type: typing.Optional[str]=None, message_body: typing.Optional[str]=None):
            """
            :param status_code: ``CfnListener.FixedResponseConfigProperty.StatusCode``.
            :param content_type: ``CfnListener.FixedResponseConfigProperty.ContentType``.
            :param message_body: ``CfnListener.FixedResponseConfigProperty.MessageBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html
            """
            self._values = {
                'status_code': status_code,
            }
            if content_type is not None: self._values["content_type"] = content_type
            if message_body is not None: self._values["message_body"] = message_body

        @builtins.property
        def status_code(self) -> str:
            """``CfnListener.FixedResponseConfigProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def content_type(self) -> typing.Optional[str]:
            """``CfnListener.FixedResponseConfigProperty.ContentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-contenttype
            """
            return self._values.get('content_type')

        @builtins.property
        def message_body(self) -> typing.Optional[str]:
            """``CfnListener.FixedResponseConfigProperty.MessageBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-messagebody
            """
            return self._values.get('message_body')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FixedResponseConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.RedirectConfigProperty", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'host': 'host', 'path': 'path', 'port': 'port', 'protocol': 'protocol', 'query': 'query'})
    class RedirectConfigProperty():
        def __init__(self, *, status_code: str, host: typing.Optional[str]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional[str]=None, query: typing.Optional[str]=None):
            """
            :param status_code: ``CfnListener.RedirectConfigProperty.StatusCode``.
            :param host: ``CfnListener.RedirectConfigProperty.Host``.
            :param path: ``CfnListener.RedirectConfigProperty.Path``.
            :param port: ``CfnListener.RedirectConfigProperty.Port``.
            :param protocol: ``CfnListener.RedirectConfigProperty.Protocol``.
            :param query: ``CfnListener.RedirectConfigProperty.Query``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html
            """
            self._values = {
                'status_code': status_code,
            }
            if host is not None: self._values["host"] = host
            if path is not None: self._values["path"] = path
            if port is not None: self._values["port"] = port
            if protocol is not None: self._values["protocol"] = protocol
            if query is not None: self._values["query"] = query

        @builtins.property
        def status_code(self) -> str:
            """``CfnListener.RedirectConfigProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def host(self) -> typing.Optional[str]:
            """``CfnListener.RedirectConfigProperty.Host``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-host
            """
            return self._values.get('host')

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnListener.RedirectConfigProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-path
            """
            return self._values.get('path')

        @builtins.property
        def port(self) -> typing.Optional[str]:
            """``CfnListener.RedirectConfigProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-port
            """
            return self._values.get('port')

        @builtins.property
        def protocol(self) -> typing.Optional[str]:
            """``CfnListener.RedirectConfigProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-protocol
            """
            return self._values.get('protocol')

        @builtins.property
        def query(self) -> typing.Optional[str]:
            """``CfnListener.RedirectConfigProperty.Query``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-query
            """
            return self._values.get('query')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RedirectConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnListenerCertificate(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticLoadBalancingV2::ListenerCertificate
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, certificates: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CertificateProperty"]]], listener_arn: str) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.
        """
        props = CfnListenerCertificateProps(certificates=certificates, listener_arn=listener_arn)

        jsii.create(CfnListenerCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="certificates")
    def certificates(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CertificateProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        """
        return jsii.get(self, "certificates")

    @certificates.setter
    def certificates(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CertificateProperty"]]]):
        jsii.set(self, "certificates", value)

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        """
        return jsii.get(self, "listenerArn")

    @listener_arn.setter
    def listener_arn(self, value: str):
        jsii.set(self, "listenerArn", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate.CertificateProperty", jsii_struct_bases=[], name_mapping={'certificate_arn': 'certificateArn'})
    class CertificateProperty():
        def __init__(self, *, certificate_arn: typing.Optional[str]=None):
            """
            :param certificate_arn: ``CfnListenerCertificate.CertificateProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html
            """
            self._values = {
            }
            if certificate_arn is not None: self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[str]:
            """``CfnListenerCertificate.CertificateProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html#cfn-elasticloadbalancingv2-listener-certificates-certificatearn
            """
            return self._values.get('certificate_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CertificateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificateProps", jsii_struct_bases=[], name_mapping={'certificates': 'certificates', 'listener_arn': 'listenerArn'})
class CfnListenerCertificateProps():
    def __init__(self, *, certificates: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerCertificate.CertificateProperty"]]], listener_arn: str):
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
        """
        self._values = {
            'certificates': certificates,
            'listener_arn': listener_arn,
        }

    @builtins.property
    def certificates(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerCertificate.CertificateProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        """
        return self._values.get('certificates')

    @builtins.property
    def listener_arn(self) -> str:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        """
        return self._values.get('listener_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnListenerCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerProps", jsii_struct_bases=[], name_mapping={'default_actions': 'defaultActions', 'load_balancer_arn': 'loadBalancerArn', 'port': 'port', 'protocol': 'protocol', 'certificates': 'certificates', 'ssl_policy': 'sslPolicy'})
class CfnListenerProps():
    def __init__(self, *, default_actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.core.IResolvable]]], load_balancer_arn: str, port: jsii.Number, protocol: str, certificates: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.CertificateProperty"]]]]]=None, ssl_policy: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::Listener``.

        :param default_actions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
        :param load_balancer_arn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
        :param port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
        :param certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
        :param ssl_policy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
        """
        self._values = {
            'default_actions': default_actions,
            'load_balancer_arn': load_balancer_arn,
            'port': port,
            'protocol': protocol,
        }
        if certificates is not None: self._values["certificates"] = certificates
        if ssl_policy is not None: self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def default_actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        """
        return self._values.get('default_actions')

    @builtins.property
    def load_balancer_arn(self) -> str:
        """``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        """
        return self._values.get('load_balancer_arn')

    @builtins.property
    def port(self) -> jsii.Number:
        """``AWS::ElasticLoadBalancingV2::Listener.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> str:
        """``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        """
        return self._values.get('protocol')

    @builtins.property
    def certificates(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.CertificateProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        """
        return self._values.get('certificates')

    @builtins.property
    def ssl_policy(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        """
        return self._values.get('ssl_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListenerRule(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerRule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticLoadBalancingV2::ListenerRule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActionProperty"]]], conditions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "RuleConditionProperty"]]], listener_arn: str, priority: jsii.Number) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
        :param conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
        :param priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.
        """
        props = CfnListenerRuleProps(actions=actions, conditions=conditions, listener_arn=listener_arn, priority=priority)

        jsii.create(CfnListenerRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActionProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        """
        return jsii.get(self, "actions")

    @actions.setter
    def actions(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActionProperty"]]]):
        jsii.set(self, "actions", value)

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "RuleConditionProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        """
        return jsii.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "RuleConditionProperty"]]]):
        jsii.set(self, "conditions", value)

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        """
        return jsii.get(self, "listenerArn")

    @listener_arn.setter
    def listener_arn(self, value: str):
        jsii.set(self, "listenerArn", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        """
        return jsii.get(self, "priority")

    @priority.setter
    def priority(self, value: jsii.Number):
        jsii.set(self, "priority", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.ActionProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'authenticate_cognito_config': 'authenticateCognitoConfig', 'authenticate_oidc_config': 'authenticateOidcConfig', 'fixed_response_config': 'fixedResponseConfig', 'order': 'order', 'redirect_config': 'redirectConfig', 'target_group_arn': 'targetGroupArn'})
    class ActionProperty():
        def __init__(self, *, type: str, authenticate_cognito_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.AuthenticateCognitoConfigProperty"]]]=None, authenticate_oidc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.AuthenticateOidcConfigProperty"]]]=None, fixed_response_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.FixedResponseConfigProperty"]]]=None, order: typing.Optional[jsii.Number]=None, redirect_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.RedirectConfigProperty"]]]=None, target_group_arn: typing.Optional[str]=None):
            """
            :param type: ``CfnListenerRule.ActionProperty.Type``.
            :param authenticate_cognito_config: ``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.
            :param authenticate_oidc_config: ``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.
            :param fixed_response_config: ``CfnListenerRule.ActionProperty.FixedResponseConfig``.
            :param order: ``CfnListenerRule.ActionProperty.Order``.
            :param redirect_config: ``CfnListenerRule.ActionProperty.RedirectConfig``.
            :param target_group_arn: ``CfnListenerRule.ActionProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html
            """
            self._values = {
                'type': type,
            }
            if authenticate_cognito_config is not None: self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None: self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None: self._values["fixed_response_config"] = fixed_response_config
            if order is not None: self._values["order"] = order
            if redirect_config is not None: self._values["redirect_config"] = redirect_config
            if target_group_arn is not None: self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def type(self) -> str:
            """``CfnListenerRule.ActionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listener-actions-type
            """
            return self._values.get('type')

        @builtins.property
        def authenticate_cognito_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.AuthenticateCognitoConfigProperty"]]]:
            """``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticatecognitoconfig
            """
            return self._values.get('authenticate_cognito_config')

        @builtins.property
        def authenticate_oidc_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.AuthenticateOidcConfigProperty"]]]:
            """``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticateoidcconfig
            """
            return self._values.get('authenticate_oidc_config')

        @builtins.property
        def fixed_response_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.FixedResponseConfigProperty"]]]:
            """``CfnListenerRule.ActionProperty.FixedResponseConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-fixedresponseconfig
            """
            return self._values.get('fixed_response_config')

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.ActionProperty.Order``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-order
            """
            return self._values.get('order')

        @builtins.property
        def redirect_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.RedirectConfigProperty"]]]:
            """``CfnListenerRule.ActionProperty.RedirectConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-redirectconfig
            """
            return self._values.get('redirect_config')

        @builtins.property
        def target_group_arn(self) -> typing.Optional[str]:
            """``CfnListenerRule.ActionProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listener-actions-targetgrouparn
            """
            return self._values.get('target_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateCognitoConfigProperty", jsii_struct_bases=[], name_mapping={'user_pool_arn': 'userPoolArn', 'user_pool_client_id': 'userPoolClientId', 'user_pool_domain': 'userPoolDomain', 'authentication_request_extra_params': 'authenticationRequestExtraParams', 'on_unauthenticated_request': 'onUnauthenticatedRequest', 'scope': 'scope', 'session_cookie_name': 'sessionCookieName', 'session_timeout': 'sessionTimeout'})
    class AuthenticateCognitoConfigProperty():
        def __init__(self, *, user_pool_arn: str, user_pool_client_id: str, user_pool_domain: str, authentication_request_extra_params: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, on_unauthenticated_request: typing.Optional[str]=None, scope: typing.Optional[str]=None, session_cookie_name: typing.Optional[str]=None, session_timeout: typing.Optional[jsii.Number]=None):
            """
            :param user_pool_arn: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.
            :param user_pool_client_id: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.
            :param user_pool_domain: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.
            :param authentication_request_extra_params: ``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html
            """
            self._values = {
                'user_pool_arn': user_pool_arn,
                'user_pool_client_id': user_pool_client_id,
                'user_pool_domain': user_pool_domain,
            }
            if authentication_request_extra_params is not None: self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None: self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None: self._values["scope"] = scope
            if session_cookie_name is not None: self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None: self._values["session_timeout"] = session_timeout

        @builtins.property
        def user_pool_arn(self) -> str:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolarn
            """
            return self._values.get('user_pool_arn')

        @builtins.property
        def user_pool_client_id(self) -> str:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolclientid
            """
            return self._values.get('user_pool_client_id')

        @builtins.property
        def user_pool_domain(self) -> str:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpooldomain
            """
            return self._values.get('user_pool_domain')

        @builtins.property
        def authentication_request_extra_params(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-authenticationrequestextraparams
            """
            return self._values.get('authentication_request_extra_params')

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[str]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-onunauthenticatedrequest
            """
            return self._values.get('on_unauthenticated_request')

        @builtins.property
        def scope(self) -> typing.Optional[str]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-scope
            """
            return self._values.get('scope')

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[str]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessioncookiename
            """
            return self._values.get('session_cookie_name')

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessiontimeout
            """
            return self._values.get('session_timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AuthenticateCognitoConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateOidcConfigProperty", jsii_struct_bases=[], name_mapping={'authorization_endpoint': 'authorizationEndpoint', 'client_id': 'clientId', 'client_secret': 'clientSecret', 'issuer': 'issuer', 'token_endpoint': 'tokenEndpoint', 'user_info_endpoint': 'userInfoEndpoint', 'authentication_request_extra_params': 'authenticationRequestExtraParams', 'on_unauthenticated_request': 'onUnauthenticatedRequest', 'scope': 'scope', 'session_cookie_name': 'sessionCookieName', 'session_timeout': 'sessionTimeout'})
    class AuthenticateOidcConfigProperty():
        def __init__(self, *, authorization_endpoint: str, client_id: str, client_secret: str, issuer: str, token_endpoint: str, user_info_endpoint: str, authentication_request_extra_params: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, on_unauthenticated_request: typing.Optional[str]=None, scope: typing.Optional[str]=None, session_cookie_name: typing.Optional[str]=None, session_timeout: typing.Optional[jsii.Number]=None):
            """
            :param authorization_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.
            :param client_id: ``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.
            :param client_secret: ``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.
            :param issuer: ``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.
            :param token_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.
            :param user_info_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.
            :param authentication_request_extra_params: ``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html
            """
            self._values = {
                'authorization_endpoint': authorization_endpoint,
                'client_id': client_id,
                'client_secret': client_secret,
                'issuer': issuer,
                'token_endpoint': token_endpoint,
                'user_info_endpoint': user_info_endpoint,
            }
            if authentication_request_extra_params is not None: self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None: self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None: self._values["scope"] = scope
            if session_cookie_name is not None: self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None: self._values["session_timeout"] = session_timeout

        @builtins.property
        def authorization_endpoint(self) -> str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authorizationendpoint
            """
            return self._values.get('authorization_endpoint')

        @builtins.property
        def client_id(self) -> str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientid
            """
            return self._values.get('client_id')

        @builtins.property
        def client_secret(self) -> str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientsecret
            """
            return self._values.get('client_secret')

        @builtins.property
        def issuer(self) -> str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-issuer
            """
            return self._values.get('issuer')

        @builtins.property
        def token_endpoint(self) -> str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-tokenendpoint
            """
            return self._values.get('token_endpoint')

        @builtins.property
        def user_info_endpoint(self) -> str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-userinfoendpoint
            """
            return self._values.get('user_info_endpoint')

        @builtins.property
        def authentication_request_extra_params(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authenticationrequestextraparams
            """
            return self._values.get('authentication_request_extra_params')

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[str]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-onunauthenticatedrequest
            """
            return self._values.get('on_unauthenticated_request')

        @builtins.property
        def scope(self) -> typing.Optional[str]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-scope
            """
            return self._values.get('scope')

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[str]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessioncookiename
            """
            return self._values.get('session_cookie_name')

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessiontimeout
            """
            return self._values.get('session_timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AuthenticateOidcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.FixedResponseConfigProperty", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'content_type': 'contentType', 'message_body': 'messageBody'})
    class FixedResponseConfigProperty():
        def __init__(self, *, status_code: str, content_type: typing.Optional[str]=None, message_body: typing.Optional[str]=None):
            """
            :param status_code: ``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.
            :param content_type: ``CfnListenerRule.FixedResponseConfigProperty.ContentType``.
            :param message_body: ``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html
            """
            self._values = {
                'status_code': status_code,
            }
            if content_type is not None: self._values["content_type"] = content_type
            if message_body is not None: self._values["message_body"] = message_body

        @builtins.property
        def status_code(self) -> str:
            """``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def content_type(self) -> typing.Optional[str]:
            """``CfnListenerRule.FixedResponseConfigProperty.ContentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-contenttype
            """
            return self._values.get('content_type')

        @builtins.property
        def message_body(self) -> typing.Optional[str]:
            """``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-messagebody
            """
            return self._values.get('message_body')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FixedResponseConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.HostHeaderConfigProperty", jsii_struct_bases=[], name_mapping={'values': 'values'})
    class HostHeaderConfigProperty():
        def __init__(self, *, values: typing.Optional[typing.List[str]]=None):
            """
            :param values: ``CfnListenerRule.HostHeaderConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html
            """
            self._values = {
            }
            if values is not None: self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnListenerRule.HostHeaderConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-hostheaderconfig-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostHeaderConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.HttpHeaderConfigProperty", jsii_struct_bases=[], name_mapping={'http_header_name': 'httpHeaderName', 'values': 'values'})
    class HttpHeaderConfigProperty():
        def __init__(self, *, http_header_name: typing.Optional[str]=None, values: typing.Optional[typing.List[str]]=None):
            """
            :param http_header_name: ``CfnListenerRule.HttpHeaderConfigProperty.HttpHeaderName``.
            :param values: ``CfnListenerRule.HttpHeaderConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html
            """
            self._values = {
            }
            if http_header_name is not None: self._values["http_header_name"] = http_header_name
            if values is not None: self._values["values"] = values

        @builtins.property
        def http_header_name(self) -> typing.Optional[str]:
            """``CfnListenerRule.HttpHeaderConfigProperty.HttpHeaderName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-httpheadername
            """
            return self._values.get('http_header_name')

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnListenerRule.HttpHeaderConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpHeaderConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.HttpRequestMethodConfigProperty", jsii_struct_bases=[], name_mapping={'values': 'values'})
    class HttpRequestMethodConfigProperty():
        def __init__(self, *, values: typing.Optional[typing.List[str]]=None):
            """
            :param values: ``CfnListenerRule.HttpRequestMethodConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html
            """
            self._values = {
            }
            if values is not None: self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnListenerRule.HttpRequestMethodConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html#cfn-elasticloadbalancingv2-listenerrule-httprequestmethodconfig-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpRequestMethodConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.PathPatternConfigProperty", jsii_struct_bases=[], name_mapping={'values': 'values'})
    class PathPatternConfigProperty():
        def __init__(self, *, values: typing.Optional[typing.List[str]]=None):
            """
            :param values: ``CfnListenerRule.PathPatternConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html
            """
            self._values = {
            }
            if values is not None: self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnListenerRule.PathPatternConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html#cfn-elasticloadbalancingv2-listenerrule-pathpatternconfig-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PathPatternConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.QueryStringConfigProperty", jsii_struct_bases=[], name_mapping={'values': 'values'})
    class QueryStringConfigProperty():
        def __init__(self, *, values: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.QueryStringKeyValueProperty"]]]]]=None):
            """
            :param values: ``CfnListenerRule.QueryStringConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html
            """
            self._values = {
            }
            if values is not None: self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.QueryStringKeyValueProperty"]]]]]:
            """``CfnListenerRule.QueryStringConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html#cfn-elasticloadbalancingv2-listenerrule-querystringconfig-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'QueryStringConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.QueryStringKeyValueProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class QueryStringKeyValueProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param key: ``CfnListenerRule.QueryStringKeyValueProperty.Key``.
            :param value: ``CfnListenerRule.QueryStringKeyValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnListenerRule.QueryStringKeyValueProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnListenerRule.QueryStringKeyValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'QueryStringKeyValueProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RedirectConfigProperty", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'host': 'host', 'path': 'path', 'port': 'port', 'protocol': 'protocol', 'query': 'query'})
    class RedirectConfigProperty():
        def __init__(self, *, status_code: str, host: typing.Optional[str]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional[str]=None, query: typing.Optional[str]=None):
            """
            :param status_code: ``CfnListenerRule.RedirectConfigProperty.StatusCode``.
            :param host: ``CfnListenerRule.RedirectConfigProperty.Host``.
            :param path: ``CfnListenerRule.RedirectConfigProperty.Path``.
            :param port: ``CfnListenerRule.RedirectConfigProperty.Port``.
            :param protocol: ``CfnListenerRule.RedirectConfigProperty.Protocol``.
            :param query: ``CfnListenerRule.RedirectConfigProperty.Query``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html
            """
            self._values = {
                'status_code': status_code,
            }
            if host is not None: self._values["host"] = host
            if path is not None: self._values["path"] = path
            if port is not None: self._values["port"] = port
            if protocol is not None: self._values["protocol"] = protocol
            if query is not None: self._values["query"] = query

        @builtins.property
        def status_code(self) -> str:
            """``CfnListenerRule.RedirectConfigProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def host(self) -> typing.Optional[str]:
            """``CfnListenerRule.RedirectConfigProperty.Host``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-host
            """
            return self._values.get('host')

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnListenerRule.RedirectConfigProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-path
            """
            return self._values.get('path')

        @builtins.property
        def port(self) -> typing.Optional[str]:
            """``CfnListenerRule.RedirectConfigProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-port
            """
            return self._values.get('port')

        @builtins.property
        def protocol(self) -> typing.Optional[str]:
            """``CfnListenerRule.RedirectConfigProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-protocol
            """
            return self._values.get('protocol')

        @builtins.property
        def query(self) -> typing.Optional[str]:
            """``CfnListenerRule.RedirectConfigProperty.Query``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-query
            """
            return self._values.get('query')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RedirectConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RuleConditionProperty", jsii_struct_bases=[], name_mapping={'field': 'field', 'host_header_config': 'hostHeaderConfig', 'http_header_config': 'httpHeaderConfig', 'http_request_method_config': 'httpRequestMethodConfig', 'path_pattern_config': 'pathPatternConfig', 'query_string_config': 'queryStringConfig', 'source_ip_config': 'sourceIpConfig', 'values': 'values'})
    class RuleConditionProperty():
        def __init__(self, *, field: typing.Optional[str]=None, host_header_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.HostHeaderConfigProperty"]]]=None, http_header_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.HttpHeaderConfigProperty"]]]=None, http_request_method_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.HttpRequestMethodConfigProperty"]]]=None, path_pattern_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.PathPatternConfigProperty"]]]=None, query_string_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.QueryStringConfigProperty"]]]=None, source_ip_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.SourceIpConfigProperty"]]]=None, values: typing.Optional[typing.List[str]]=None):
            """
            :param field: ``CfnListenerRule.RuleConditionProperty.Field``.
            :param host_header_config: ``CfnListenerRule.RuleConditionProperty.HostHeaderConfig``.
            :param http_header_config: ``CfnListenerRule.RuleConditionProperty.HttpHeaderConfig``.
            :param http_request_method_config: ``CfnListenerRule.RuleConditionProperty.HttpRequestMethodConfig``.
            :param path_pattern_config: ``CfnListenerRule.RuleConditionProperty.PathPatternConfig``.
            :param query_string_config: ``CfnListenerRule.RuleConditionProperty.QueryStringConfig``.
            :param source_ip_config: ``CfnListenerRule.RuleConditionProperty.SourceIpConfig``.
            :param values: ``CfnListenerRule.RuleConditionProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html
            """
            self._values = {
            }
            if field is not None: self._values["field"] = field
            if host_header_config is not None: self._values["host_header_config"] = host_header_config
            if http_header_config is not None: self._values["http_header_config"] = http_header_config
            if http_request_method_config is not None: self._values["http_request_method_config"] = http_request_method_config
            if path_pattern_config is not None: self._values["path_pattern_config"] = path_pattern_config
            if query_string_config is not None: self._values["query_string_config"] = query_string_config
            if source_ip_config is not None: self._values["source_ip_config"] = source_ip_config
            if values is not None: self._values["values"] = values

        @builtins.property
        def field(self) -> typing.Optional[str]:
            """``CfnListenerRule.RuleConditionProperty.Field``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-conditions-field
            """
            return self._values.get('field')

        @builtins.property
        def host_header_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.HostHeaderConfigProperty"]]]:
            """``CfnListenerRule.RuleConditionProperty.HostHeaderConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-hostheaderconfig
            """
            return self._values.get('host_header_config')

        @builtins.property
        def http_header_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.HttpHeaderConfigProperty"]]]:
            """``CfnListenerRule.RuleConditionProperty.HttpHeaderConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httpheaderconfig
            """
            return self._values.get('http_header_config')

        @builtins.property
        def http_request_method_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.HttpRequestMethodConfigProperty"]]]:
            """``CfnListenerRule.RuleConditionProperty.HttpRequestMethodConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httprequestmethodconfig
            """
            return self._values.get('http_request_method_config')

        @builtins.property
        def path_pattern_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.PathPatternConfigProperty"]]]:
            """``CfnListenerRule.RuleConditionProperty.PathPatternConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-pathpatternconfig
            """
            return self._values.get('path_pattern_config')

        @builtins.property
        def query_string_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.QueryStringConfigProperty"]]]:
            """``CfnListenerRule.RuleConditionProperty.QueryStringConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-querystringconfig
            """
            return self._values.get('query_string_config')

        @builtins.property
        def source_ip_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnListenerRule.SourceIpConfigProperty"]]]:
            """``CfnListenerRule.RuleConditionProperty.SourceIpConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-sourceipconfig
            """
            return self._values.get('source_ip_config')

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnListenerRule.RuleConditionProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-conditions-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RuleConditionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.SourceIpConfigProperty", jsii_struct_bases=[], name_mapping={'values': 'values'})
    class SourceIpConfigProperty():
        def __init__(self, *, values: typing.Optional[typing.List[str]]=None):
            """
            :param values: ``CfnListenerRule.SourceIpConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html
            """
            self._values = {
            }
            if values is not None: self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnListenerRule.SourceIpConfigProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html#cfn-elasticloadbalancingv2-listenerrule-sourceipconfig-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SourceIpConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRuleProps", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'conditions': 'conditions', 'listener_arn': 'listenerArn', 'priority': 'priority'})
class CfnListenerRuleProps():
    def __init__(self, *, actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ActionProperty"]]], conditions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RuleConditionProperty"]]], listener_arn: str, priority: jsii.Number):
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
        :param conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
        :param priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
        """
        self._values = {
            'actions': actions,
            'conditions': conditions,
            'listener_arn': listener_arn,
            'priority': priority,
        }

    @builtins.property
    def actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ActionProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        """
        return self._values.get('actions')

    @builtins.property
    def conditions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RuleConditionProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        """
        return self._values.get('conditions')

    @builtins.property
    def listener_arn(self) -> str:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        """
        return self._values.get('listener_arn')

    @builtins.property
    def priority(self) -> jsii.Number:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        """
        return self._values.get('priority')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnListenerRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLoadBalancer(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticLoadBalancingV2::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, ip_address_type: typing.Optional[str]=None, load_balancer_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LoadBalancerAttributeProperty"]]]]]=None, name: typing.Optional[str]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnet_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SubnetMappingProperty"]]]]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ip_address_type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
        :param load_balancer_attributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
        :param name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
        :param scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
        :param subnet_mappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
        :param subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
        :param type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.
        """
        props = CfnLoadBalancerProps(ip_address_type=ip_address_type, load_balancer_attributes=load_balancer_attributes, name=name, scheme=scheme, security_groups=security_groups, subnet_mappings=subnet_mappings, subnets=subnets, tags=tags, type=type)

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCanonicalHostedZoneId")
    def attr_canonical_hosted_zone_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CanonicalHostedZoneID
        """
        return jsii.get(self, "attrCanonicalHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DNSName
        """
        return jsii.get(self, "attrDnsName")

    @builtins.property
    @jsii.member(jsii_name="attrLoadBalancerFullName")
    def attr_load_balancer_full_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: LoadBalancerFullName
        """
        return jsii.get(self, "attrLoadBalancerFullName")

    @builtins.property
    @jsii.member(jsii_name="attrLoadBalancerName")
    def attr_load_balancer_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: LoadBalancerName
        """
        return jsii.get(self, "attrLoadBalancerName")

    @builtins.property
    @jsii.member(jsii_name="attrSecurityGroups")
    def attr_security_groups(self) -> typing.List[str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SecurityGroups
        """
        return jsii.get(self, "attrSecurityGroups")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        """
        return jsii.get(self, "ipAddressType")

    @ip_address_type.setter
    def ip_address_type(self, value: typing.Optional[str]):
        jsii.set(self, "ipAddressType", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerAttributes")
    def load_balancer_attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LoadBalancerAttributeProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        """
        return jsii.get(self, "loadBalancerAttributes")

    @load_balancer_attributes.setter
    def load_balancer_attributes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LoadBalancerAttributeProperty"]]]]]):
        jsii.set(self, "loadBalancerAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        """
        return jsii.get(self, "scheme")

    @scheme.setter
    def scheme(self, value: typing.Optional[str]):
        jsii.set(self, "scheme", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter
    def security_groups(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnetMappings")
    def subnet_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SubnetMappingProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        """
        return jsii.get(self, "subnetMappings")

    @subnet_mappings.setter
    def subnet_mappings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "SubnetMappingProperty"]]]]]):
        jsii.set(self, "subnetMappings", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter
    def subnets(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: typing.Optional[str]):
        jsii.set(self, "type", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.LoadBalancerAttributeProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class LoadBalancerAttributeProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param key: ``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.
            :param value: ``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoadBalancerAttributeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.SubnetMappingProperty", jsii_struct_bases=[], name_mapping={'allocation_id': 'allocationId', 'subnet_id': 'subnetId'})
    class SubnetMappingProperty():
        def __init__(self, *, allocation_id: str, subnet_id: str):
            """
            :param allocation_id: ``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.
            :param subnet_id: ``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html
            """
            self._values = {
                'allocation_id': allocation_id,
                'subnet_id': subnet_id,
            }

        @builtins.property
        def allocation_id(self) -> str:
            """``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-allocationid
            """
            return self._values.get('allocation_id')

        @builtins.property
        def subnet_id(self) -> str:
            """``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-subnetid
            """
            return self._values.get('subnet_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SubnetMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancerProps", jsii_struct_bases=[], name_mapping={'ip_address_type': 'ipAddressType', 'load_balancer_attributes': 'loadBalancerAttributes', 'name': 'name', 'scheme': 'scheme', 'security_groups': 'securityGroups', 'subnet_mappings': 'subnetMappings', 'subnets': 'subnets', 'tags': 'tags', 'type': 'type'})
class CfnLoadBalancerProps():
    def __init__(self, *, ip_address_type: typing.Optional[str]=None, load_balancer_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]]]=None, name: typing.Optional[str]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnet_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.SubnetMappingProperty"]]]]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, type: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param ip_address_type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
        :param load_balancer_attributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
        :param name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
        :param scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
        :param subnet_mappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
        :param subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
        :param type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
        """
        self._values = {
        }
        if ip_address_type is not None: self._values["ip_address_type"] = ip_address_type
        if load_balancer_attributes is not None: self._values["load_balancer_attributes"] = load_balancer_attributes
        if name is not None: self._values["name"] = name
        if scheme is not None: self._values["scheme"] = scheme
        if security_groups is not None: self._values["security_groups"] = security_groups
        if subnet_mappings is not None: self._values["subnet_mappings"] = subnet_mappings
        if subnets is not None: self._values["subnets"] = subnets
        if tags is not None: self._values["tags"] = tags
        if type is not None: self._values["type"] = type

    @builtins.property
    def ip_address_type(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        """
        return self._values.get('ip_address_type')

    @builtins.property
    def load_balancer_attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        """
        return self._values.get('load_balancer_attributes')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        """
        return self._values.get('name')

    @builtins.property
    def scheme(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        """
        return self._values.get('scheme')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        """
        return self._values.get('security_groups')

    @builtins.property
    def subnet_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.SubnetMappingProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        """
        return self._values.get('subnet_mappings')

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        """
        return self._values.get('subnets')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        """
        return self._values.get('tags')

    @builtins.property
    def type(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTargetGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::TargetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticLoadBalancingV2::TargetGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, health_check_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check_interval_seconds: typing.Optional[jsii.Number]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[str]=None, health_check_protocol: typing.Optional[str]=None, health_check_timeout_seconds: typing.Optional[jsii.Number]=None, healthy_threshold_count: typing.Optional[jsii.Number]=None, matcher: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["MatcherProperty"]]]=None, name: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, target_group_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetGroupAttributeProperty"]]]]]=None, targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetDescriptionProperty"]]]]]=None, target_type: typing.Optional[str]=None, unhealthy_threshold_count: typing.Optional[jsii.Number]=None, vpc_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param health_check_enabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
        :param health_check_interval_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
        :param health_check_timeout_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
        :param healthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
        :param matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
        :param name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
        :param port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
        :param tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
        :param target_group_attributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
        :param targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
        :param target_type: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
        :param unhealthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
        :param vpc_id: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.
        """
        props = CfnTargetGroupProps(health_check_enabled=health_check_enabled, health_check_interval_seconds=health_check_interval_seconds, health_check_path=health_check_path, health_check_port=health_check_port, health_check_protocol=health_check_protocol, health_check_timeout_seconds=health_check_timeout_seconds, healthy_threshold_count=healthy_threshold_count, matcher=matcher, name=name, port=port, protocol=protocol, tags=tags, target_group_attributes=target_group_attributes, targets=targets, target_type=target_type, unhealthy_threshold_count=unhealthy_threshold_count, vpc_id=vpc_id)

        jsii.create(CfnTargetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrLoadBalancerArns")
    def attr_load_balancer_arns(self) -> typing.List[str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: LoadBalancerArns
        """
        return jsii.get(self, "attrLoadBalancerArns")

    @builtins.property
    @jsii.member(jsii_name="attrTargetGroupFullName")
    def attr_target_group_full_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: TargetGroupFullName
        """
        return jsii.get(self, "attrTargetGroupFullName")

    @builtins.property
    @jsii.member(jsii_name="attrTargetGroupName")
    def attr_target_group_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: TargetGroupName
        """
        return jsii.get(self, "attrTargetGroupName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="healthCheckEnabled")
    def health_check_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        """
        return jsii.get(self, "healthCheckEnabled")

    @health_check_enabled.setter
    def health_check_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "healthCheckEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        """
        return jsii.get(self, "healthCheckIntervalSeconds")

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        """
        return jsii.get(self, "healthCheckPath")

    @health_check_path.setter
    def health_check_path(self, value: typing.Optional[str]):
        jsii.set(self, "healthCheckPath", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        """
        return jsii.get(self, "healthCheckPort")

    @health_check_port.setter
    def health_check_port(self, value: typing.Optional[str]):
        jsii.set(self, "healthCheckPort", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        """
        return jsii.get(self, "healthCheckProtocol")

    @health_check_protocol.setter
    def health_check_protocol(self, value: typing.Optional[str]):
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckTimeoutSeconds")
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        """
        return jsii.get(self, "healthCheckTimeoutSeconds")

    @health_check_timeout_seconds.setter
    def health_check_timeout_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "healthCheckTimeoutSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdCount")
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        """
        return jsii.get(self, "healthyThresholdCount")

    @healthy_threshold_count.setter
    def healthy_threshold_count(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "healthyThresholdCount", value)

    @builtins.property
    @jsii.member(jsii_name="matcher")
    def matcher(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["MatcherProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        """
        return jsii.get(self, "matcher")

    @matcher.setter
    def matcher(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["MatcherProperty"]]]):
        jsii.set(self, "matcher", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: typing.Optional[str]):
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroupAttributes")
    def target_group_attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetGroupAttributeProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        """
        return jsii.get(self, "targetGroupAttributes")

    @target_group_attributes.setter
    def target_group_attributes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetGroupAttributeProperty"]]]]]):
        jsii.set(self, "targetGroupAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetDescriptionProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        """
        return jsii.get(self, "targets")

    @targets.setter
    def targets(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetDescriptionProperty"]]]]]):
        jsii.set(self, "targets", value)

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter
    def target_type(self, value: typing.Optional[str]):
        jsii.set(self, "targetType", value)

    @builtins.property
    @jsii.member(jsii_name="unhealthyThresholdCount")
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        """
        return jsii.get(self, "unhealthyThresholdCount")

    @unhealthy_threshold_count.setter
    def unhealthy_threshold_count(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "unhealthyThresholdCount", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        """
        return jsii.get(self, "vpcId")

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[str]):
        jsii.set(self, "vpcId", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.MatcherProperty", jsii_struct_bases=[], name_mapping={'http_code': 'httpCode'})
    class MatcherProperty():
        def __init__(self, *, http_code: str):
            """
            :param http_code: ``CfnTargetGroup.MatcherProperty.HttpCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html
            """
            self._values = {
                'http_code': http_code,
            }

        @builtins.property
        def http_code(self) -> str:
            """``CfnTargetGroup.MatcherProperty.HttpCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-httpcode
            """
            return self._values.get('http_code')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MatcherProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetDescriptionProperty", jsii_struct_bases=[], name_mapping={'id': 'id', 'availability_zone': 'availabilityZone', 'port': 'port'})
    class TargetDescriptionProperty():
        def __init__(self, *, id: str, availability_zone: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None):
            """
            :param id: ``CfnTargetGroup.TargetDescriptionProperty.Id``.
            :param availability_zone: ``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.
            :param port: ``CfnTargetGroup.TargetDescriptionProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html
            """
            self._values = {
                'id': id,
            }
            if availability_zone is not None: self._values["availability_zone"] = availability_zone
            if port is not None: self._values["port"] = port

        @builtins.property
        def id(self) -> str:
            """``CfnTargetGroup.TargetDescriptionProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-id
            """
            return self._values.get('id')

        @builtins.property
        def availability_zone(self) -> typing.Optional[str]:
            """``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-availabilityzone
            """
            return self._values.get('availability_zone')

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnTargetGroup.TargetDescriptionProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-port
            """
            return self._values.get('port')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetDescriptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetGroupAttributeProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TargetGroupAttributeProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param key: ``CfnTargetGroup.TargetGroupAttributeProperty.Key``.
            :param value: ``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnTargetGroup.TargetGroupAttributeProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetGroupAttributeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroupProps", jsii_struct_bases=[], name_mapping={'health_check_enabled': 'healthCheckEnabled', 'health_check_interval_seconds': 'healthCheckIntervalSeconds', 'health_check_path': 'healthCheckPath', 'health_check_port': 'healthCheckPort', 'health_check_protocol': 'healthCheckProtocol', 'health_check_timeout_seconds': 'healthCheckTimeoutSeconds', 'healthy_threshold_count': 'healthyThresholdCount', 'matcher': 'matcher', 'name': 'name', 'port': 'port', 'protocol': 'protocol', 'tags': 'tags', 'target_group_attributes': 'targetGroupAttributes', 'targets': 'targets', 'target_type': 'targetType', 'unhealthy_threshold_count': 'unhealthyThresholdCount', 'vpc_id': 'vpcId'})
class CfnTargetGroupProps():
    def __init__(self, *, health_check_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check_interval_seconds: typing.Optional[jsii.Number]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[str]=None, health_check_protocol: typing.Optional[str]=None, health_check_timeout_seconds: typing.Optional[jsii.Number]=None, healthy_threshold_count: typing.Optional[jsii.Number]=None, matcher: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTargetGroup.MatcherProperty"]]]=None, name: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, target_group_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetGroupAttributeProperty"]]]]]=None, targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetDescriptionProperty"]]]]]=None, target_type: typing.Optional[str]=None, unhealthy_threshold_count: typing.Optional[jsii.Number]=None, vpc_id: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param health_check_enabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
        :param health_check_interval_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
        :param health_check_timeout_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
        :param healthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
        :param matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
        :param name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
        :param port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
        :param tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
        :param target_group_attributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
        :param targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
        :param target_type: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
        :param unhealthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
        :param vpc_id: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
        """
        self._values = {
        }
        if health_check_enabled is not None: self._values["health_check_enabled"] = health_check_enabled
        if health_check_interval_seconds is not None: self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None: self._values["health_check_path"] = health_check_path
        if health_check_port is not None: self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None: self._values["health_check_protocol"] = health_check_protocol
        if health_check_timeout_seconds is not None: self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
        if healthy_threshold_count is not None: self._values["healthy_threshold_count"] = healthy_threshold_count
        if matcher is not None: self._values["matcher"] = matcher
        if name is not None: self._values["name"] = name
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if tags is not None: self._values["tags"] = tags
        if target_group_attributes is not None: self._values["target_group_attributes"] = target_group_attributes
        if targets is not None: self._values["targets"] = targets
        if target_type is not None: self._values["target_type"] = target_type
        if unhealthy_threshold_count is not None: self._values["unhealthy_threshold_count"] = unhealthy_threshold_count
        if vpc_id is not None: self._values["vpc_id"] = vpc_id

    @builtins.property
    def health_check_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        """
        return self._values.get('health_check_enabled')

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        """
        return self._values.get('health_check_interval_seconds')

    @builtins.property
    def health_check_path(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        """
        return self._values.get('health_check_path')

    @builtins.property
    def health_check_port(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        """
        return self._values.get('health_check_port')

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        """
        return self._values.get('health_check_protocol')

    @builtins.property
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        """
        return self._values.get('health_check_timeout_seconds')

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        """
        return self._values.get('healthy_threshold_count')

    @builtins.property
    def matcher(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTargetGroup.MatcherProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        """
        return self._values.get('matcher')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        """
        return self._values.get('name')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        """
        return self._values.get('protocol')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        """
        return self._values.get('tags')

    @builtins.property
    def target_group_attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetGroupAttributeProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        """
        return self._values.get('target_group_attributes')

    @builtins.property
    def targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetDescriptionProperty"]]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        """
        return self._values.get('targets')

    @builtins.property
    def target_type(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        """
        return self._values.get('target_type')

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        """
        return self._values.get('unhealthy_threshold_count')

    @builtins.property
    def vpc_id(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        """
        return self._values.get('vpc_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTargetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ContentType")
class ContentType(enum.Enum):
    """The content type for a fixed response."""
    TEXT_PLAIN = "TEXT_PLAIN"
    TEXT_CSS = "TEXT_CSS"
    TEXT_HTML = "TEXT_HTML"
    APPLICATION_JAVASCRIPT = "APPLICATION_JAVASCRIPT"
    APPLICATION_JSON = "APPLICATION_JSON"

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.FixedResponse", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'content_type': 'contentType', 'message_body': 'messageBody'})
class FixedResponse():
    def __init__(self, *, status_code: str, content_type: typing.Optional["ContentType"]=None, message_body: typing.Optional[str]=None):
        """A fixed response.

        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message
        """
        self._values = {
            'status_code': status_code,
        }
        if content_type is not None: self._values["content_type"] = content_type
        if message_body is not None: self._values["message_body"] = message_body

    @builtins.property
    def status_code(self) -> str:
        """The HTTP response code (2XX, 4XX or 5XX)."""
        return self._values.get('status_code')

    @builtins.property
    def content_type(self) -> typing.Optional["ContentType"]:
        """The content type.

        default
        :default: text/plain
        """
        return self._values.get('content_type')

    @builtins.property
    def message_body(self) -> typing.Optional[str]:
        """The message.

        default
        :default: no message
        """
        return self._values.get('message_body')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FixedResponse(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddFixedResponseProps", jsii_struct_bases=[AddRuleProps, FixedResponse], name_mapping={'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'priority': 'priority', 'status_code': 'statusCode', 'content_type': 'contentType', 'message_body': 'messageBody'})
class AddFixedResponseProps(AddRuleProps, FixedResponse):
    def __init__(self, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, status_code: str, content_type: typing.Optional["ContentType"]=None, message_body: typing.Optional[str]=None):
        """Properties for adding a fixed response to a listener.

        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message
        """
        self._values = {
            'status_code': status_code,
        }
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority
        if content_type is not None: self._values["content_type"] = content_type
        if message_body is not None: self._values["message_body"] = message_body

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults
        """
        return self._values.get('priority')

    @builtins.property
    def status_code(self) -> str:
        """The HTTP response code (2XX, 4XX or 5XX)."""
        return self._values.get('status_code')

    @builtins.property
    def content_type(self) -> typing.Optional["ContentType"]:
        """The content type.

        default
        :default: text/plain
        """
        return self._values.get('content_type')

    @builtins.property
    def message_body(self) -> typing.Optional[str]:
        """The message.

        default
        :default: no message
        """
        return self._values.get('message_body')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddFixedResponseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HealthCheck", jsii_struct_bases=[], name_mapping={'healthy_http_codes': 'healthyHttpCodes', 'healthy_threshold_count': 'healthyThresholdCount', 'interval': 'interval', 'path': 'path', 'port': 'port', 'protocol': 'protocol', 'timeout': 'timeout', 'unhealthy_threshold_count': 'unhealthyThresholdCount'})
class HealthCheck():
    def __init__(self, *, healthy_http_codes: typing.Optional[str]=None, healthy_threshold_count: typing.Optional[jsii.Number]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional["Protocol"]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, unhealthy_threshold_count: typing.Optional[jsii.Number]=None):
        """Properties for configuring a health check.

        :param healthy_http_codes: HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
        :param healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
        :param interval: The approximate number of seconds between health checks for an individual target. Default: Duration.seconds(30)
        :param path: The ping path destination where Elastic Load Balancing sends health check requests. Default: /
        :param port: The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
        :param protocol: The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP. The TLS, UDP, and TCP_UDP protocols are not supported for health checks. Default: HTTP for ALBs, TCP for NLBs
        :param timeout: The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2-60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        :param unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2
        """
        self._values = {
        }
        if healthy_http_codes is not None: self._values["healthy_http_codes"] = healthy_http_codes
        if healthy_threshold_count is not None: self._values["healthy_threshold_count"] = healthy_threshold_count
        if interval is not None: self._values["interval"] = interval
        if path is not None: self._values["path"] = path
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if timeout is not None: self._values["timeout"] = timeout
        if unhealthy_threshold_count is not None: self._values["unhealthy_threshold_count"] = unhealthy_threshold_count

    @builtins.property
    def healthy_http_codes(self) -> typing.Optional[str]:
        """HTTP code to use when checking for a successful response from a target.

        For Application Load Balancers, you can specify values between 200 and
        499, and the default value is 200. You can specify multiple values (for
        example, "200,202") or a range of values (for example, "200-299").
        """
        return self._values.get('healthy_http_codes')

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """The number of consecutive health checks successes required before considering an unhealthy target healthy.

        For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3.

        default
        :default: 5 for ALBs, 3 for NLBs
        """
        return self._values.get('healthy_threshold_count')

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The approximate number of seconds between health checks for an individual target.

        default
        :default: Duration.seconds(30)
        """
        return self._values.get('interval')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The ping path destination where Elastic Load Balancing sends health check requests.

        default
        :default: /
        """
        return self._values.get('path')

    @builtins.property
    def port(self) -> typing.Optional[str]:
        """The port that the load balancer uses when performing health checks on the targets.

        default
        :default: 'traffic-port'
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol the load balancer uses when performing health checks on targets.

        The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP.
        The TLS, UDP, and TCP_UDP protocols are not supported for health checks.

        default
        :default: HTTP for ALBs, TCP for NLBs
        """
        return self._values.get('protocol')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time, in seconds, during which no response from a target means a failed health check.

        For Application Load Balancers, the range is 2-60 seconds and the
        default is 5 seconds. For Network Load Balancers, this is 10 seconds for
        TCP and HTTPS health checks and 6 seconds for HTTP health checks.

        default
        :default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        """
        return self._values.get('timeout')

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """The number of consecutive health check failures required before considering a target unhealthy.

        For Application Load Balancers, the default is 2. For Network Load
        Balancers, this value must be the same as the healthy threshold count.

        default
        :default: 2
        """
        return self._values.get('unhealthy_threshold_count')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheck(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeElb")
class HttpCodeElb(enum.Enum):
    """Count of HTTP status originating from the load balancer.

    This count does not include any response codes generated by the targets.
    """
    ELB_3XX_COUNT = "ELB_3XX_COUNT"
    """The number of HTTP 3XX redirection codes that originate from the load balancer."""
    ELB_4XX_COUNT = "ELB_4XX_COUNT"
    """The number of HTTP 4XX client error codes that originate from the load balancer.

    Client errors are generated when requests are malformed or incomplete.
    These requests have not been received by the target. This count does not
    include any response codes generated by the targets.
    """
    ELB_5XX_COUNT = "ELB_5XX_COUNT"
    """The number of HTTP 5XX server error codes that originate from the load balancer."""

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeTarget")
class HttpCodeTarget(enum.Enum):
    """Count of HTTP status originating from the targets."""
    TARGET_2XX_COUNT = "TARGET_2XX_COUNT"
    """The number of 2xx response codes from targets."""
    TARGET_3XX_COUNT = "TARGET_3XX_COUNT"
    """The number of 3xx response codes from targets."""
    TARGET_4XX_COUNT = "TARGET_4XX_COUNT"
    """The number of 4xx response codes from targets."""
    TARGET_5XX_COUNT = "TARGET_5XX_COUNT"
    """The number of 5xx response codes from targets."""

@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener")
class IApplicationListener(aws_cdk.core.IResource, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """Properties to reference an existing listener."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationListenerProxy

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        """Add one or more certificates to this listener.

        :param id: -
        :param arns: -
        """
        ...

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: Target groups to forward requests to.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        ...

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        return
        :return: The newly created target group
        """
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.Port) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -
        """
        ...


class _IApplicationListenerProxy(jsii.proxy_for(aws_cdk.core.IResource), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """Properties to reference an existing listener."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener"
    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "listenerArn")

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        """Add one or more certificates to this listener.

        :param id: -
        :param arns: -
        """
        return jsii.invoke(self, "addCertificateArns", [id, arns])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: Target groups to forward requests to.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props = AddApplicationTargetGroupsProps(target_groups=target_groups, host_header=host_header, path_pattern=path_pattern, priority=priority)

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        return
        :return: The newly created target group
        """
        props = AddApplicationTargetsProps(deregistration_delay=deregistration_delay, health_check=health_check, port=port, protocol=protocol, slow_start=slow_start, stickiness_cookie_duration=stickiness_cookie_duration, target_group_name=target_group_name, targets=targets, host_header=host_header, path_pattern=path_pattern, priority=priority)

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.Port) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])


@jsii.implements(IApplicationListener)
class ApplicationListener(BaseListener, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListener"):
    """Define an ApplicationListener.

    resource:
    :resource:: AWS::ElasticLoadBalancingV2::Listener
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, load_balancer: "IApplicationLoadBalancer", certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param load_balancer: The load balancer to attach this listener to.
        :param certificate_arns: The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props = ApplicationListenerProps(load_balancer=load_balancer, certificate_arns=certificate_arns, certificates=certificates, default_target_groups=default_target_groups, open=open, port=port, protocol=protocol, ssl_policy=ssl_policy)

        jsii.create(ApplicationListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationListenerAttributes")
    @builtins.classmethod
    def from_application_listener_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, listener_arn: str, default_port: typing.Optional[jsii.Number]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_group_allows_all_outbound: typing.Optional[bool]=None, security_group_id: typing.Optional[str]=None) -> "IApplicationListener":
        """Import an existing listener.

        :param scope: -
        :param id: -
        :param listener_arn: ARN of the listener.
        :param default_port: The default port on which this listener is listening.
        :param security_group: Security group of the load balancer this listener is associated with.
        :param security_group_allows_all_outbound: Whether the imported security group allows all outbound traffic or not when imported using ``securityGroupId``. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param security_group_id: Security group ID of the load balancer this listener is associated with.
        """
        attrs = ApplicationListenerAttributes(listener_arn=listener_arn, default_port=default_port, security_group=security_group, security_group_allows_all_outbound=security_group_allows_all_outbound, security_group_id=security_group_id)

        return jsii.sinvoke(cls, "fromApplicationListenerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        """Add one or more certificates to this listener.

        After the first certificate, this creates ApplicationListenerCertificates
        resources since cloudformation requires the certificates array on the
        listener resource to have a length of 1.

        :param id: -
        :param arns: -

        deprecated
        :deprecated: Use ``addCertificates`` instead.

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "addCertificateArns", [id, arns])

    @jsii.member(jsii_name="addCertificates")
    def add_certificates(self, id: str, certificates: typing.List["IListenerCertificate"]) -> None:
        """Add one or more certificates to this listener.

        After the first certificate, this creates ApplicationListenerCertificates
        resources since cloudformation requires the certificates array on the
        listener resource to have a length of 1.

        :param id: -
        :param certificates: -
        """
        return jsii.invoke(self, "addCertificates", [id, certificates])

    @jsii.member(jsii_name="addFixedResponse")
    def add_fixed_response(self, id: str, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, status_code: str, content_type: typing.Optional["ContentType"]=None, message_body: typing.Optional[str]=None) -> None:
        """Add a fixed response.

        :param id: -
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message
        """
        props = AddFixedResponseProps(host_header=host_header, path_pattern=path_pattern, priority=priority, status_code=status_code, content_type=content_type, message_body=message_body)

        return jsii.invoke(self, "addFixedResponse", [id, props])

    @jsii.member(jsii_name="addRedirectResponse")
    def add_redirect_response(self, id: str, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, status_code: str, host: typing.Optional[str]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional[str]=None, query: typing.Optional[str]=None) -> None:
        """Add a redirect response.

        :param id: -
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request
        """
        props = AddRedirectResponseProps(host_header=host_header, path_pattern=path_pattern, priority=priority, status_code=status_code, host=host, path=path, port=port, protocol=protocol, query=query)

        return jsii.invoke(self, "addRedirectResponse", [id, props])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: Target groups to forward requests to.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props = AddApplicationTargetGroupsProps(target_groups=target_groups, host_header=host_header, path_pattern=path_pattern, priority=priority)

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        return
        :return: The newly created target group
        """
        props = AddApplicationTargetsProps(deregistration_delay=deregistration_delay, health_check=health_check, port=port, protocol=protocol, slow_start=slow_start, stickiness_cookie_duration=stickiness_cookie_duration, target_group_name=target_group_name, targets=targets, host_header=host_header, path_pattern=path_pattern, priority=priority)

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.Port) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this listener."""
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage connections to this ApplicationListener."""
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "IApplicationLoadBalancer":
        """Load balancer this listener is associated with."""
        return jsii.get(self, "loadBalancer")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget")
class IApplicationLoadBalancerTarget(jsii.compat.Protocol):
    """Interface for constructs that can be targets of an application load balancer."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "IApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        ...


class _IApplicationLoadBalancerTargetProxy():
    """Interface for constructs that can be targets of an application load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget"
    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "IApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IListenerCertificate")
class IListenerCertificate(jsii.compat.Protocol):
    """A certificate source for an ELBv2 listener."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListenerCertificateProxy

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The ARN of the certificate to use."""
        ...


class _IListenerCertificateProxy():
    """A certificate source for an ELBv2 listener."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IListenerCertificate"
    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The ARN of the certificate to use."""
        return jsii.get(self, "certificateArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ILoadBalancerV2")
class ILoadBalancerV2(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerV2Proxy

    @builtins.property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """The canonical hosted zone ID of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """The DNS name of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        """
        ...


class _ILoadBalancerV2Proxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.ILoadBalancerV2"
    @builtins.property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """The canonical hosted zone ID of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """The DNS name of this load balancer.

        attribute:
        :attribute:: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        """
        return jsii.get(self, "loadBalancerDnsName")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer")
class IApplicationLoadBalancer(ILoadBalancerV2, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """An application load balancer."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerProxy

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer."""
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        """Add a new listener to this load balancer.

        :param id: -
        :param certificate_arns: The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        ...


class _IApplicationLoadBalancerProxy(jsii.proxy_for(ILoadBalancerV2), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """An application load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer"
    @builtins.property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer."""
        return jsii.get(self, "loadBalancerArn")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        """Add a new listener to this load balancer.

        :param id: -
        :param certificate_arns: The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props = BaseApplicationListenerProps(certificate_arns=certificate_arns, certificates=certificates, default_target_groups=default_target_groups, open=open, port=port, protocol=protocol, ssl_policy=ssl_policy)

        return jsii.invoke(self, "addListener", [id, props])


@jsii.implements(IApplicationLoadBalancer)
class ApplicationLoadBalancer(BaseLoadBalancer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancer"):
    """Define an Application Load Balancer.

    resource:
    :resource:: AWS::ElasticLoadBalancingV2::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, http2_enabled: typing.Optional[bool]=None, idle_timeout: typing.Optional[aws_cdk.core.Duration]=None, ip_address_type: typing.Optional["IpAddressType"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param http2_enabled: Indicates whether HTTP/2 is enabled. Default: true
        :param idle_timeout: The load balancer idle timeout, in seconds. Default: 60
        :param ip_address_type: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param security_group: Security group to associate with this load balancer. Default: A security group is created
        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, Private subnets if internal and there are Private subnets, Isolated subnets if internal and there are no Private subnets.
        """
        props = ApplicationLoadBalancerProps(http2_enabled=http2_enabled, idle_timeout=idle_timeout, ip_address_type=ip_address_type, security_group=security_group, vpc=vpc, deletion_protection=deletion_protection, internet_facing=internet_facing, load_balancer_name=load_balancer_name, vpc_subnets=vpc_subnets)

        jsii.create(ApplicationLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationLoadBalancerAttributes")
    @builtins.classmethod
    def from_application_load_balancer_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, load_balancer_arn: str, security_group_id: str, load_balancer_canonical_hosted_zone_id: typing.Optional[str]=None, load_balancer_dns_name: typing.Optional[str]=None, security_group_allows_all_outbound: typing.Optional[bool]=None) -> "IApplicationLoadBalancer":
        """Import an existing Application Load Balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: ARN of the load balancer.
        :param security_group_id: ID of the load balancer's security group.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param security_group_allows_all_outbound: Whether the security group allows all outbound traffic or not. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        """
        attrs = ApplicationLoadBalancerAttributes(load_balancer_arn=load_balancer_arn, security_group_id=security_group_id, load_balancer_canonical_hosted_zone_id=load_balancer_canonical_hosted_zone_id, load_balancer_dns_name=load_balancer_dns_name, security_group_allows_all_outbound=security_group_allows_all_outbound)

        return jsii.sinvoke(cls, "fromApplicationLoadBalancerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        """Add a new listener to this load balancer.

        :param id: -
        :param certificate_arns: The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props = BaseApplicationListenerProps(certificate_arns=certificate_arns, certificates=certificates, default_target_groups=default_target_groups, open=open, port=port, protocol=protocol, ssl_policy=ssl_policy)

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(self, bucket: aws_cdk.aws_s3.IBucket, prefix: typing.Optional[str]=None) -> None:
        """Enable access logging for this load balancer.

        A region must be specified on the stack containing the load balancer; you cannot enable logging on
        environment-agnostic stacks. See https://docs.aws.amazon.com/cdk/latest/guide/environments.html

        :param bucket: -
        :param prefix: -
        """
        return jsii.invoke(self, "logAccessLogs", [bucket, prefix])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Application Load Balancer.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveConnectionCount")
    def metric_active_connection_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of concurrent TCP connections active from clients to the load balancer and from the load balancer to targets.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricActiveConnectionCount", [props])

    @jsii.member(jsii_name="metricClientTlsNegotiationErrorCount")
    def metric_client_tls_negotiation_error_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the client that did not establish a session with the load balancer.

        Possible causes include a
        mismatch of ciphers or protocols.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricClientTlsNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of load balancer capacity units (LCU) used by your load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricElbAuthError")
    def metric_elb_auth_error(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of user authentications that could not be completed.

        Because an authenticate action was misconfigured, the load balancer
        couldn't establish a connection with the IdP, or the load balancer
        couldn't complete the authentication flow due to an internal error.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricElbAuthError", [props])

    @jsii.member(jsii_name="metricElbAuthFailure")
    def metric_elb_auth_failure(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of user authentications that could not be completed because the IdP denied access to the user or an authorization code was used more than once.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricElbAuthFailure", [props])

    @jsii.member(jsii_name="metricElbAuthLatency")
    def metric_elb_auth_latency(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in milliseconds, to query the IdP for the ID token and user info.

        If one or more of these operations fail, this is the time to failure.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricElbAuthLatency", [props])

    @jsii.member(jsii_name="metricElbAuthSuccess")
    def metric_elb_auth_success(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of authenticate actions that were successful.

        This metric is incremented at the end of the authentication workflow,
        after the load balancer has retrieved the user claims from the IdP.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricElbAuthSuccess", [props])

    @jsii.member(jsii_name="metricHttpCodeElb")
    def metric_http_code_elb(self, code: "HttpCodeElb", *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 3xx/4xx/5xx codes that originate from the load balancer.

        This does not include any response codes generated by the targets.

        :param code: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHttpCodeElb", [code, props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(self, code: "HttpCodeTarget", *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in the load balancer.

        This does not include any response codes generated by the load balancer.

        :param code: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricHttpFixedResponseCount")
    def metric_http_fixed_response_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of fixed-response actions that were successful.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHttpFixedResponseCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectCount")
    def metric_http_redirect_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of redirect actions that were successful.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHttpRedirectCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectUrlLimitExceededCount")
    def metric_http_redirect_url_limit_exceeded_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of redirect actions that couldn't be completed because the URL in the response location header is larger than 8K.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHttpRedirectUrlLimitExceededCount", [props])

    @jsii.member(jsii_name="metricIpv6ProcessedBytes")
    def metric_ipv6_processed_bytes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer over IPv6.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricIpv6ProcessedBytes", [props])

    @jsii.member(jsii_name="metricIpv6RequestCount")
    def metric_ipv6_request_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of IPv6 requests received by the load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricIpv6RequestCount", [props])

    @jsii.member(jsii_name="metricNewConnectionCount")
    def metric_new_connection_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of new TCP connections established from clients to the load balancer and from the load balancer to targets.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNewConnectionCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer over IPv4 and IPv6.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricRejectedConnectionCount")
    def metric_rejected_connection_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were rejected because the load balancer had reached its maximum number of connections.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRejectedConnectionCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRuleEvaluations")
    def metric_rule_evaluations(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of rules processed by the load balancer given a request rate averaged over an hour.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRuleEvaluations", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were not successfully established between the load balancer and target.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListener")
class INetworkListener(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Properties to reference an existing listener."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerProxy

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
        :attribute:: true
        """
        ...


class _INetworkListenerProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Properties to reference an existing listener."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListener"
    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "listenerArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListenerCertificateProps")
class INetworkListenerCertificateProps(IListenerCertificate, jsii.compat.Protocol):
    """Properties for adding a certificate to a listener.

    This interface exists for backwards compatibility.

    deprecated
    :deprecated: Use IListenerCertificate instead

    stability
    :stability: deprecated
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerCertificatePropsProxy

    pass

class _INetworkListenerCertificatePropsProxy(jsii.proxy_for(IListenerCertificate)):
    """Properties for adding a certificate to a listener.

    This interface exists for backwards compatibility.

    deprecated
    :deprecated: Use IListenerCertificate instead

    stability
    :stability: deprecated
    """
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListenerCertificateProps"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer")
class INetworkLoadBalancer(ILoadBalancerV2, aws_cdk.aws_ec2.IVpcEndpointServiceLoadBalancer, jsii.compat.Protocol):
    """A network load balancer."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerProxy

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "NetworkListener":
        """Add a listener to this load balancer.

        :param id: -
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.

        return
        :return: The newly created listener
        """
        ...


class _INetworkLoadBalancerProxy(jsii.proxy_for(ILoadBalancerV2), jsii.proxy_for(aws_cdk.aws_ec2.IVpcEndpointServiceLoadBalancer)):
    """A network load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer"
    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "NetworkListener":
        """Add a listener to this load balancer.

        :param id: -
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.

        return
        :return: The newly created listener
        """
        props = BaseNetworkListenerProps(port=port, certificates=certificates, default_target_groups=default_target_groups, protocol=protocol, ssl_policy=ssl_policy)

        return jsii.invoke(self, "addListener", [id, props])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget")
class INetworkLoadBalancerTarget(jsii.compat.Protocol):
    """Interface for constructs that can be targets of an network load balancer."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "INetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        ...


class _INetworkLoadBalancerTargetProxy():
    """Interface for constructs that can be targets of an network load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget"
    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "INetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup")
class ITargetGroup(aws_cdk.core.IConstruct, jsii.compat.Protocol):
    """A target group."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITargetGroupProxy

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        ...

    @builtins.property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.core.IDependable:
        """Return an object to depend on the listeners added to this target group."""
        ...

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        """ARN of the target group."""
        ...


class _ITargetGroupProxy(jsii.proxy_for(aws_cdk.core.IConstruct)):
    """A target group."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup"
    @builtins.property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        return jsii.get(self, "loadBalancerArns")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.core.IDependable:
        """Return an object to depend on the listeners added to this target group."""
        return jsii.get(self, "loadBalancerAttached")

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        """ARN of the target group."""
        return jsii.get(self, "targetGroupArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup")
class IApplicationTargetGroup(ITargetGroup, jsii.compat.Protocol):
    """A Target Group for Application Load Balancers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationTargetGroupProxy

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "IApplicationLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: typing.Optional[aws_cdk.aws_ec2.Port]=None) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -
        """
        ...

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.core.IConstruct]=None) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -
        """
        ...


class _IApplicationTargetGroupProxy(jsii.proxy_for(ITargetGroup)):
    """A Target Group for Application Load Balancers."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup"
    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "IApplicationLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: typing.Optional[aws_cdk.aws_ec2.Port]=None) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.core.IConstruct]=None) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -
        """
        return jsii.invoke(self, "registerListener", [listener, associating_construct])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup")
class INetworkTargetGroup(ITargetGroup, jsii.compat.Protocol):
    """A network target group."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkTargetGroupProxy

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "INetworkLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        ...

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        """
        ...


class _INetworkTargetGroupProxy(jsii.proxy_for(ITargetGroup)):
    """A network target group."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup"
    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "INetworkLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        """
        return jsii.invoke(self, "registerListener", [listener])


@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class InstanceTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.InstanceTarget"):
    """An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    deprecated
    :deprecated: Use IpTarget from the

    stability
    :stability: deprecated
    aws-cdk:
    :aws-cdk:: /aws-elasticloadbalancingv2-targets package instead.
    """
    def __init__(self, instance_id: str, port: typing.Optional[jsii.Number]=None) -> None:
        """Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.

        stability
        :stability: deprecated
        """
        jsii.create(InstanceTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "IApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "INetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpAddressType")
class IpAddressType(enum.Enum):
    """What kind of addresses to allocate to the load balancer."""
    IPV4 = "IPV4"
    """Allocate IPv4 addresses."""
    DUAL_STACK = "DUAL_STACK"
    """Allocate both IPv4 and IPv6 addresses."""

@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class IpTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpTarget"):
    """An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    deprecated
    :deprecated: Use IpTarget from the

    stability
    :stability: deprecated
    aws-cdk:
    :aws-cdk:: /aws-elasticloadbalancingv2-targets package instead.
    """
    def __init__(self, ip_address: str, port: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None) -> None:
        """Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.

        stability
        :stability: deprecated
        """
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "IApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "INetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.implements(IListenerCertificate)
class ListenerCertificate(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ListenerCertificate"):
    """A certificate source for an ELBv2 listener."""
    def __init__(self, certificate_arn: str) -> None:
        """
        :param certificate_arn: -
        """
        jsii.create(ListenerCertificate, self, [certificate_arn])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(cls, certificate_arn: str) -> "ListenerCertificate":
        """Use any certificate, identified by its ARN, as a listener certificate.

        :param certificate_arn: -
        """
        return jsii.sinvoke(cls, "fromArn", [certificate_arn])

    @jsii.member(jsii_name="fromCertificateManager")
    @builtins.classmethod
    def from_certificate_manager(cls, acm_certificate: aws_cdk.aws_certificatemanager.ICertificate) -> "ListenerCertificate":
        """Use an ACM certificate as a listener certificate.

        :param acm_certificate: -
        """
        return jsii.sinvoke(cls, "fromCertificateManager", [acm_certificate])

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The ARN of the certificate to use."""
        return jsii.get(self, "certificateArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.LoadBalancerTargetProps", jsii_struct_bases=[], name_mapping={'target_type': 'targetType', 'target_json': 'targetJson'})
class LoadBalancerTargetProps():
    def __init__(self, *, target_type: "TargetType", target_json: typing.Any=None):
        """Result of attaching a target to load balancer.

        :param target_type: What kind of target this is.
        :param target_json: JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.
        """
        self._values = {
            'target_type': target_type,
        }
        if target_json is not None: self._values["target_json"] = target_json

    @builtins.property
    def target_type(self) -> "TargetType":
        """What kind of target this is."""
        return self._values.get('target_type')

    @builtins.property
    def target_json(self) -> typing.Any:
        """JSON representing the target's direct addition to the TargetGroup list.

        May be omitted if the target is going to register itself later.
        """
        return self._values.get('target_json')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancerTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(INetworkListener)
class NetworkListener(BaseListener, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListener"):
    """Define a Network Listener.

    resource:
    :resource:: AWS::ElasticLoadBalancingV2::Listener
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, load_balancer: "INetworkLoadBalancer", port: jsii.Number, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param load_balancer: The load balancer to attach this listener to.
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.
        """
        props = NetworkListenerProps(load_balancer=load_balancer, port=port, certificates=certificates, default_target_groups=default_target_groups, protocol=protocol, ssl_policy=ssl_policy)

        jsii.create(NetworkListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromNetworkListenerArn")
    @builtins.classmethod
    def from_network_listener_arn(cls, scope: aws_cdk.core.Construct, id: str, network_listener_arn: str) -> "INetworkListener":
        """Import an existing listener.

        :param scope: -
        :param id: -
        :param network_listener_arn: -
        """
        return jsii.sinvoke(cls, "fromNetworkListenerArn", [scope, id, network_listener_arn])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, _id: str, *target_groups: "INetworkTargetGroup") -> None:
        """Load balance incoming requests to the given target groups.

        :param _id: -
        :param target_groups: -
        """
        return jsii.invoke(self, "addTargetGroups", [_id, *target_groups])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, port: jsii.Number, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, proxy_protocol_v2: typing.Optional[bool]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None) -> "NetworkTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        :param id: -
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.

        return
        :return: The newly created target group
        """
        props = AddNetworkTargetsProps(port=port, deregistration_delay=deregistration_delay, health_check=health_check, proxy_protocol_v2=proxy_protocol_v2, target_group_name=target_group_name, targets=targets)

        return jsii.invoke(self, "addTargets", [id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerProps", jsii_struct_bases=[BaseNetworkListenerProps], name_mapping={'port': 'port', 'certificates': 'certificates', 'default_target_groups': 'defaultTargetGroups', 'protocol': 'protocol', 'ssl_policy': 'sslPolicy', 'load_balancer': 'loadBalancer'})
class NetworkListenerProps(BaseNetworkListenerProps):
    def __init__(self, *, port: jsii.Number, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None, load_balancer: "INetworkLoadBalancer"):
        """Properties for a Network Listener attached to a Load Balancer.

        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.
        :param load_balancer: The load balancer to attach this listener to.
        """
        self._values = {
            'port': port,
            'load_balancer': load_balancer,
        }
        if certificates is not None: self._values["certificates"] = certificates
        if default_target_groups is not None: self._values["default_target_groups"] = default_target_groups
        if protocol is not None: self._values["protocol"] = protocol
        if ssl_policy is not None: self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests."""
        return self._values.get('port')

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificate list of ACM cert ARNs.

        default
        :default: - No certificates.
        """
        return self._values.get('certificates')

    @builtins.property
    def default_target_groups(self) -> typing.Optional[typing.List["INetworkTargetGroup"]]:
        """Default target groups to load balance to.

        default
        :default: - None.
        """
        return self._values.get('default_target_groups')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """Protocol for listener, expects TCP or TLS.

        default
        :default: - TLS if certificates are provided. TCP otherwise.
        """
        return self._values.get('protocol')

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """SSL Policy.

        default
        :default: - Current predefined security policy.
        """
        return self._values.get('ssl_policy')

    @builtins.property
    def load_balancer(self) -> "INetworkLoadBalancer":
        """The load balancer to attach this listener to."""
        return self._values.get('load_balancer')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(INetworkLoadBalancer)
class NetworkLoadBalancer(BaseLoadBalancer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancer"):
    """Define a new network load balancer.

    resource:
    :resource:: AWS::ElasticLoadBalancingV2::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cross_zone_enabled: typing.Optional[bool]=None, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cross_zone_enabled: Indicates whether cross-zone load balancing is enabled. Default: false
        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, Private subnets if internal and there are Private subnets, Isolated subnets if internal and there are no Private subnets.
        """
        props = NetworkLoadBalancerProps(cross_zone_enabled=cross_zone_enabled, vpc=vpc, deletion_protection=deletion_protection, internet_facing=internet_facing, load_balancer_name=load_balancer_name, vpc_subnets=vpc_subnets)

        jsii.create(NetworkLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromNetworkLoadBalancerAttributes")
    @builtins.classmethod
    def from_network_load_balancer_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, load_balancer_arn: str, load_balancer_canonical_hosted_zone_id: typing.Optional[str]=None, load_balancer_dns_name: typing.Optional[str]=None) -> "INetworkLoadBalancer":
        """
        :param scope: -
        :param id: -
        :param load_balancer_arn: ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        attrs = NetworkLoadBalancerAttributes(load_balancer_arn=load_balancer_arn, load_balancer_canonical_hosted_zone_id=load_balancer_canonical_hosted_zone_id, load_balancer_dns_name=load_balancer_dns_name)

        return jsii.sinvoke(cls, "fromNetworkLoadBalancerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, certificates: typing.Optional[typing.List["IListenerCertificate"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "NetworkListener":
        """Add a listener to this load balancer.

        :param id: -
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_target_groups: Default target groups to load balance to. Default: - None.
        :param protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.

        return
        :return: The newly created listener
        """
        props = BaseNetworkListenerProps(port=port, certificates=certificates, default_target_groups=default_target_groups, protocol=protocol, ssl_policy=ssl_policy)

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Network Load Balancer.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveFlowCount")
    def metric_active_flow_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of concurrent TCP flows (or connections) from clients to targets.

        This metric includes connections in the SYN_SENT and ESTABLISHED states.
        TCP connections are not terminated at the load balancer, so a client
        opening a TCP connection to a target counts as a single flow.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricActiveFlowCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of load balancer capacity units (LCU) used by your load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of targets that are considered healthy.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricNewFlowCount")
    def metric_new_flow_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of new TCP flows (or connections) established from clients to targets in the time period.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricNewFlowCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer, including TCP/IP headers.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricTcpClientResetCount")
    def metric_tcp_client_reset_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets sent from a client to a target.

        These resets are generated by the client and forwarded by the load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTcpClientResetCount", [props])

    @jsii.member(jsii_name="metricTcpElbResetCount")
    def metric_tcp_elb_reset_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets generated by the load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTcpElbResetCount", [props])

    @jsii.member(jsii_name="metricTcpTargetResetCount")
    def metric_tcp_target_reset_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets sent from a target to a client.

        These resets are generated by the target and forwarded by the load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTcpTargetResetCount", [props])

    @jsii.member(jsii_name="metricUnHealthyHostCount")
    def metric_un_healthy_host_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of targets that are considered unhealthy.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricUnHealthyHostCount", [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerAttributes", jsii_struct_bases=[], name_mapping={'load_balancer_arn': 'loadBalancerArn', 'load_balancer_canonical_hosted_zone_id': 'loadBalancerCanonicalHostedZoneId', 'load_balancer_dns_name': 'loadBalancerDnsName'})
class NetworkLoadBalancerAttributes():
    def __init__(self, *, load_balancer_arn: str, load_balancer_canonical_hosted_zone_id: typing.Optional[str]=None, load_balancer_dns_name: typing.Optional[str]=None):
        """Properties to reference an existing load balancer.

        :param load_balancer_arn: ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        self._values = {
            'load_balancer_arn': load_balancer_arn,
        }
        if load_balancer_canonical_hosted_zone_id is not None: self._values["load_balancer_canonical_hosted_zone_id"] = load_balancer_canonical_hosted_zone_id
        if load_balancer_dns_name is not None: self._values["load_balancer_dns_name"] = load_balancer_dns_name

    @builtins.property
    def load_balancer_arn(self) -> str:
        """ARN of the load balancer."""
        return self._values.get('load_balancer_arn')

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> typing.Optional[str]:
        """The canonical hosted zone ID of this load balancer.

        default
        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        return self._values.get('load_balancer_canonical_hosted_zone_id')

    @builtins.property
    def load_balancer_dns_name(self) -> typing.Optional[str]:
        """The DNS name of this load balancer.

        default
        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        return self._values.get('load_balancer_dns_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancerAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerProps", jsii_struct_bases=[BaseLoadBalancerProps], name_mapping={'vpc': 'vpc', 'deletion_protection': 'deletionProtection', 'internet_facing': 'internetFacing', 'load_balancer_name': 'loadBalancerName', 'vpc_subnets': 'vpcSubnets', 'cross_zone_enabled': 'crossZoneEnabled'})
class NetworkLoadBalancerProps(BaseLoadBalancerProps):
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cross_zone_enabled: typing.Optional[bool]=None):
        """Properties for a network load balancer.

        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, Private subnets if internal and there are Private subnets, Isolated subnets if internal and there are no Private subnets.
        :param cross_zone_enabled: Indicates whether cross-zone load balancing is enabled. Default: false
        """
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'vpc': vpc,
        }
        if deletion_protection is not None: self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None: self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if cross_zone_enabled is not None: self._values["cross_zone_enabled"] = cross_zone_enabled

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network to place the load balancer in."""
        return self._values.get('vpc')

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether deletion protection is enabled.

        default
        :default: false
        """
        return self._values.get('deletion_protection')

    @builtins.property
    def internet_facing(self) -> typing.Optional[bool]:
        """Whether the load balancer has an internet-routable address.

        default
        :default: false
        """
        return self._values.get('internet_facing')

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[str]:
        """Name of the load balancer.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('load_balancer_name')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where in the VPC to place the load balancer.

        default
        :default:

        - Public subnets if internetFacing, Private subnets if internal and
          there are Private subnets, Isolated subnets if internal and there are no
          Private subnets.
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def cross_zone_enabled(self) -> typing.Optional[bool]:
        """Indicates whether cross-zone load balancing is enabled.

        default
        :default: false
        """
        return self._values.get('cross_zone_enabled')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroupProps", jsii_struct_bases=[BaseTargetGroupProps], name_mapping={'deregistration_delay': 'deregistrationDelay', 'health_check': 'healthCheck', 'target_group_name': 'targetGroupName', 'target_type': 'targetType', 'vpc': 'vpc', 'port': 'port', 'proxy_protocol_v2': 'proxyProtocolV2', 'targets': 'targets'})
class NetworkTargetGroupProps(BaseTargetGroupProps):
    def __init__(self, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, port: jsii.Number, proxy_protocol_v2: typing.Optional[bool]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None):
        """Properties for a new Network Target Group.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param port: The port on which the listener listens for requests.
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
            'port': port,
        }
        if deregistration_delay is not None: self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None: self._values["health_check"] = health_check
        if target_group_name is not None: self._values["target_group_name"] = target_group_name
        if target_type is not None: self._values["target_type"] = target_type
        if vpc is not None: self._values["vpc"] = vpc
        if proxy_protocol_v2 is not None: self._values["proxy_protocol_v2"] = proxy_protocol_v2
        if targets is not None: self._values["targets"] = targets

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        default
        :default: 300
        """
        return self._values.get('deregistration_delay')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        default
        :default: - None.
        """
        return self._values.get('health_check')

    @builtins.property
    def target_group_name(self) -> typing.Optional[str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        default
        :default: - Automatically generated.
        """
        return self._values.get('target_group_name')

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        """The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        default
        :default: - Determined automatically.
        """
        return self._values.get('target_type')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        default
        :default: - undefined
        """
        return self._values.get('vpc')

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests."""
        return self._values.get('port')

    @builtins.property
    def proxy_protocol_v2(self) -> typing.Optional[bool]:
        """Indicates whether Proxy Protocol version 2 is enabled.

        default
        :default: false
        """
        return self._values.get('proxy_protocol_v2')

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["INetworkLoadBalancerTarget"]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        default
        :default: - No targets.
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkTargetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.Protocol")
class Protocol(enum.Enum):
    """Backend protocol for network load balancers and health checks."""
    HTTP = "HTTP"
    """HTTP (ALB health checks and NLB health checks)."""
    HTTPS = "HTTPS"
    """HTTPS (ALB health checks and NLB health checks)."""
    TCP = "TCP"
    """TCP (NLB, NLB health checks)."""
    TLS = "TLS"
    """TLS (NLB)."""
    UDP = "UDP"
    """UDP (NLB)."""
    TCP_UDP = "TCP_UDP"
    """Listen to both TCP and UDP on the same port (NLB)."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.RedirectResponse", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'host': 'host', 'path': 'path', 'port': 'port', 'protocol': 'protocol', 'query': 'query'})
class RedirectResponse():
    def __init__(self, *, status_code: str, host: typing.Optional[str]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional[str]=None, query: typing.Optional[str]=None):
        """A redirect response.

        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request
        """
        self._values = {
            'status_code': status_code,
        }
        if host is not None: self._values["host"] = host
        if path is not None: self._values["path"] = path
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if query is not None: self._values["query"] = query

    @builtins.property
    def status_code(self) -> str:
        """The HTTP redirect code (HTTP_301 or HTTP_302)."""
        return self._values.get('status_code')

    @builtins.property
    def host(self) -> typing.Optional[str]:
        """The hostname.

        This component is not percent-encoded. The hostname can contain #{host}.

        default
        :default: origin host of request
        """
        return self._values.get('host')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The absolute path, starting with the leading "/".

        This component is not percent-encoded.
        The path can contain #{host}, #{path}, and #{port}.

        default
        :default: origin path of request
        """
        return self._values.get('path')

    @builtins.property
    def port(self) -> typing.Optional[str]:
        """The port.

        You can specify a value from 1 to 65535 or #{port}.

        default
        :default: origin port of request
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional[str]:
        """The protocol.

        You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP,
        HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP.

        default
        :default: origin protocol of request
        """
        return self._values.get('protocol')

    @builtins.property
    def query(self) -> typing.Optional[str]:
        """The query parameters, URL-encoded when necessary, but not percent-encoded.

        Do not include the leading "?", as it is automatically added.
        You can specify any of the reserved keywords.

        default
        :default: origin query string of request
        """
        return self._values.get('query')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RedirectResponse(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddRedirectResponseProps", jsii_struct_bases=[AddRuleProps, RedirectResponse], name_mapping={'host_header': 'hostHeader', 'path_pattern': 'pathPattern', 'priority': 'priority', 'status_code': 'statusCode', 'host': 'host', 'path': 'path', 'port': 'port', 'protocol': 'protocol', 'query': 'query'})
class AddRedirectResponseProps(AddRuleProps, RedirectResponse):
    def __init__(self, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, status_code: str, host: typing.Optional[str]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional[str]=None, query: typing.Optional[str]=None):
        """Properties for adding a redirect response to a listener.

        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request
        """
        self._values = {
            'status_code': status_code,
        }
        if host_header is not None: self._values["host_header"] = host_header
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority
        if host is not None: self._values["host"] = host
        if path is not None: self._values["path"] = path
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if query is not None: self._values["query"] = query

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults
        """
        return self._values.get('priority')

    @builtins.property
    def status_code(self) -> str:
        """The HTTP redirect code (HTTP_301 or HTTP_302)."""
        return self._values.get('status_code')

    @builtins.property
    def host(self) -> typing.Optional[str]:
        """The hostname.

        This component is not percent-encoded. The hostname can contain #{host}.

        default
        :default: origin host of request
        """
        return self._values.get('host')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The absolute path, starting with the leading "/".

        This component is not percent-encoded.
        The path can contain #{host}, #{path}, and #{port}.

        default
        :default: origin path of request
        """
        return self._values.get('path')

    @builtins.property
    def port(self) -> typing.Optional[str]:
        """The port.

        You can specify a value from 1 to 65535 or #{port}.

        default
        :default: origin port of request
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional[str]:
        """The protocol.

        You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP,
        HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP.

        default
        :default: origin protocol of request
        """
        return self._values.get('protocol')

    @builtins.property
    def query(self) -> typing.Optional[str]:
        """The query parameters, URL-encoded when necessary, but not percent-encoded.

        Do not include the leading "?", as it is automatically added.
        You can specify any of the reserved keywords.

        default
        :default: origin query string of request
        """
        return self._values.get('query')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddRedirectResponseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.SslPolicy")
class SslPolicy(enum.Enum):
    """Elastic Load Balancing provides the following security policies for Application Load Balancers.

    We recommend the Recommended policy for general use. You can
    use the ForwardSecrecy policy if you require Forward Secrecy
    (FS).

    You can use one of the TLS policies to meet compliance and security
    standards that require disabling certain TLS protocol versions, or to
    support legacy clients that require deprecated ciphers.

    see
    :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html
    """
    RECOMMENDED = "RECOMMENDED"
    """The recommended security policy."""
    FORWARD_SECRECY_TLS12_RES = "FORWARD_SECRECY_TLS12_RES"
    """Strong forward secrecy ciphers and TLS1.2 only."""
    FORWARD_SECRECY_TLS12 = "FORWARD_SECRECY_TLS12"
    """Forward secrecy ciphers and TLS1.2 only."""
    FORWARD_SECRECY_TLS11 = "FORWARD_SECRECY_TLS11"
    """Forward secrecy ciphers only with TLS1.1 and higher."""
    FORWARD_SECRECY = "FORWARD_SECRECY"
    """Forward secrecy ciphers only."""
    TLS12 = "TLS12"
    """TLS1.2 only and no SHA ciphers."""
    TLS12_EXT = "TLS12_EXT"
    """TLS1.2 only with all ciphers."""
    TLS11 = "TLS11"
    """TLS1.1 and higher with all ciphers."""
    LEGACY = "LEGACY"
    """Support for DES-CBC3-SHA.

    Do not use this security policy unless you must support a legacy client
    that requires the DES-CBC3-SHA cipher, which is a weak cipher.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupAttributes", jsii_struct_bases=[], name_mapping={'target_group_arn': 'targetGroupArn', 'default_port': 'defaultPort', 'load_balancer_arns': 'loadBalancerArns'})
class TargetGroupAttributes():
    def __init__(self, *, target_group_arn: str, default_port: typing.Optional[str]=None, load_balancer_arns: typing.Optional[str]=None):
        """Properties to reference an existing target group.

        :param target_group_arn: ARN of the target group.
        :param default_port: Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        self._values = {
            'target_group_arn': target_group_arn,
        }
        if default_port is not None: self._values["default_port"] = default_port
        if load_balancer_arns is not None: self._values["load_balancer_arns"] = load_balancer_arns

    @builtins.property
    def target_group_arn(self) -> str:
        """ARN of the target group."""
        return self._values.get('target_group_arn')

    @builtins.property
    def default_port(self) -> typing.Optional[str]:
        """Port target group is listening on.

        deprecated
        :deprecated: - This property is unused and the wrong type. No need to use it.

        stability
        :stability: deprecated
        """
        return self._values.get('default_port')

    @builtins.property
    def load_balancer_arns(self) -> typing.Optional[str]:
        """A Token representing the list of ARNs for the load balancer routing to this target group."""
        return self._values.get('load_balancer_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TargetGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ITargetGroup)
class TargetGroupBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupBase"):
    """Define the target of a load balancer."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TargetGroupBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, base_props: "BaseTargetGroupProps", additional_props: typing.Any) -> None:
        """
        :param scope: -
        :param id: -
        :param base_props: -
        :param additional_props: -
        """
        jsii.create(TargetGroupBase, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="addLoadBalancerTarget")
    def _add_load_balancer_target(self, *, target_type: "TargetType", target_json: typing.Any=None) -> None:
        """Register the given load balancing target as part of this group.

        :param target_type: What kind of target this is.
        :param target_json: JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.
        """
        props = LoadBalancerTargetProps(target_type=target_type, target_json=target_json)

        return jsii.invoke(self, "addLoadBalancerTarget", [props])

    @jsii.member(jsii_name="configureHealthCheck")
    def configure_health_check(self, *, healthy_http_codes: typing.Optional[str]=None, healthy_threshold_count: typing.Optional[jsii.Number]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional["Protocol"]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, unhealthy_threshold_count: typing.Optional[jsii.Number]=None) -> None:
        """Set/replace the target group's health check.

        :param healthy_http_codes: HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
        :param healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
        :param interval: The approximate number of seconds between health checks for an individual target. Default: Duration.seconds(30)
        :param path: The ping path destination where Elastic Load Balancing sends health check requests. Default: /
        :param port: The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
        :param protocol: The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP. The TLS, UDP, and TCP_UDP protocols are not supported for health checks. Default: HTTP for ALBs, TCP for NLBs
        :param timeout: The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2-60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        :param unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2
        """
        health_check = HealthCheck(healthy_http_codes=healthy_http_codes, healthy_threshold_count=healthy_threshold_count, interval=interval, path=path, port=port, protocol=protocol, timeout=timeout, unhealthy_threshold_count=unhealthy_threshold_count)

        return jsii.invoke(self, "configureHealthCheck", [health_check])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: str, value: typing.Optional[str]=None) -> None:
        """Set a non-standard attribute on the target group.

        :param key: -
        :param value: -

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#target-group-attributes
        """
        return jsii.invoke(self, "setAttribute", [key, value])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="defaultPort")
    def _default_port(self) -> jsii.Number:
        """Default port configured for members of this target group."""
        return jsii.get(self, "defaultPort")

    @builtins.property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    @abc.abstractmethod
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 123456789
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        return jsii.get(self, "loadBalancerArns")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.core.IDependable:
        """List of constructs that need to be depended on to ensure the TargetGroup is associated to a load balancer."""
        return jsii.get(self, "loadBalancerAttached")

    @builtins.property
    @jsii.member(jsii_name="loadBalancerAttachedDependencies")
    def _load_balancer_attached_dependencies(self) -> aws_cdk.core.ConcreteDependable:
        """Configurable dependable with all resources that lead to load balancer attachment."""
        return jsii.get(self, "loadBalancerAttachedDependencies")

    @builtins.property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        """The ARN of the target group."""
        return jsii.get(self, "targetGroupArn")

    @builtins.property
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> str:
        """The full name of the target group."""
        return jsii.get(self, "targetGroupFullName")

    @builtins.property
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[str]:
        """ARNs of load balancers load balancing to this TargetGroup."""
        return jsii.get(self, "targetGroupLoadBalancerArns")

    @builtins.property
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> str:
        """The name of the target group."""
        return jsii.get(self, "targetGroupName")

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> "HealthCheck":
        return jsii.get(self, "healthCheck")

    @health_check.setter
    def health_check(self, value: "HealthCheck"):
        jsii.set(self, "healthCheck", value)

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def _target_type(self) -> typing.Optional["TargetType"]:
        """The types of the directly registered members of this target group."""
        return jsii.get(self, "targetType")

    @_target_type.setter
    def _target_type(self, value: typing.Optional["TargetType"]):
        jsii.set(self, "targetType", value)


class _TargetGroupBaseProxy(TargetGroupBase):
    @builtins.property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 123456789
        """
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(IApplicationTargetGroup)
class ApplicationTargetGroup(TargetGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroup"):
    """Define an Application Target Group."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known, optional for Lambda targets.
        :param protocol: The protocol to use. Default: - Determined from port if known, optional for Lambda targets.
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        """
        props = ApplicationTargetGroupProps(port=port, protocol=protocol, slow_start=slow_start, stickiness_cookie_duration=stickiness_cookie_duration, targets=targets, deregistration_delay=deregistration_delay, health_check=health_check, target_group_name=target_group_name, target_type=target_type, vpc=vpc)

        jsii.create(ApplicationTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromTargetGroupAttributes")
    @builtins.classmethod
    def from_target_group_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, target_group_arn: str, default_port: typing.Optional[str]=None, load_balancer_arns: typing.Optional[str]=None) -> "IApplicationTargetGroup":
        """Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        attrs = TargetGroupAttributes(target_group_arn=target_group_arn, default_port=default_port, load_balancer_arns=load_balancer_arns)

        return jsii.sinvoke(cls, "fromTargetGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="import")
    @builtins.classmethod
    def import_(cls, scope: aws_cdk.core.Construct, id: str, *, target_group_arn: str, default_port: typing.Optional[str]=None, load_balancer_arns: typing.Optional[str]=None) -> "IApplicationTargetGroup":
        """Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.

        deprecated
        :deprecated: Use ``fromTargetGroupAttributes`` instead

        stability
        :stability: deprecated
        """
        props = TargetGroupImportProps(target_group_arn=target_group_arn, default_port=default_port, load_balancer_arns=load_balancer_arns)

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "IApplicationLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="enableCookieStickiness")
    def enable_cookie_stickiness(self, duration: aws_cdk.core.Duration) -> None:
        """Enable sticky routing via a cookie to members of this target group.

        :param duration: -
        """
        return jsii.invoke(self, "enableCookieStickiness", [duration])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Application Load Balancer Target Group.

        Returns the metric for this target group from the point of view of the first
        load balancer load balancing to it. If you have multiple load balancers load
        sending traffic to the same target group, you will have to override the dimensions
        on this metric.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of healthy hosts in the target group.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(self, code: "HttpCodeTarget", *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in this target group.

        This does not include any response codes generated by the load balancer.

        :param code: -
        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricIpv6RequestCount")
    def metric_ipv6_request_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of IPv6 requests received by the target group.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricIpv6RequestCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRequestCountPerTarget")
    def metric_request_count_per_target(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The average number of requests received by each target in a target group.

        The only valid statistic is Sum. Note that this represents the average not the sum.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRequestCountPerTarget", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were not successfully established between the load balancer and target.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricUnhealthyHostCount")
    def metric_unhealthy_host_count(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of unhealthy hosts in the target group.

        :param account: Account which this metric comes from. Default: Deployment account.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: All metric datums in the given metric stream

        default
        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricUnhealthyHostCount", [props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: typing.Optional[aws_cdk.aws_ec2.Port]=None) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.core.IConstruct]=None) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -
        """
        return jsii.invoke(self, "registerListener", [listener, associating_construct])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer."""
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(INetworkTargetGroup)
class NetworkTargetGroup(TargetGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroup"):
    """Define a Network Target Group."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, port: jsii.Number, proxy_protocol_v2: typing.Optional[bool]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param port: The port on which the listener listens for requests.
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        """
        props = NetworkTargetGroupProps(port=port, proxy_protocol_v2=proxy_protocol_v2, targets=targets, deregistration_delay=deregistration_delay, health_check=health_check, target_group_name=target_group_name, target_type=target_type, vpc=vpc)

        jsii.create(NetworkTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromTargetGroupAttributes")
    @builtins.classmethod
    def from_target_group_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, target_group_arn: str, default_port: typing.Optional[str]=None, load_balancer_arns: typing.Optional[str]=None) -> "INetworkTargetGroup":
        """Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        attrs = TargetGroupAttributes(target_group_arn=target_group_arn, default_port=default_port, load_balancer_arns=load_balancer_arns)

        return jsii.sinvoke(cls, "fromTargetGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="import")
    @builtins.classmethod
    def import_(cls, scope: aws_cdk.core.Construct, id: str, *, target_group_arn: str, default_port: typing.Optional[str]=None, load_balancer_arns: typing.Optional[str]=None) -> "INetworkTargetGroup":
        """Import an existing listener.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.

        deprecated
        :deprecated: Use ``fromTargetGroupAttributes`` instead

        stability
        :stability: deprecated
        """
        props = TargetGroupImportProps(target_group_arn=target_group_arn, default_port=default_port, load_balancer_arns=load_balancer_arns)

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "INetworkLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        """
        return jsii.invoke(self, "registerListener", [listener])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer."""
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupImportProps", jsii_struct_bases=[TargetGroupAttributes], name_mapping={'target_group_arn': 'targetGroupArn', 'default_port': 'defaultPort', 'load_balancer_arns': 'loadBalancerArns'})
class TargetGroupImportProps(TargetGroupAttributes):
    def __init__(self, *, target_group_arn: str, default_port: typing.Optional[str]=None, load_balancer_arns: typing.Optional[str]=None):
        """Properties to reference an existing target group.

        :param target_group_arn: ARN of the target group.
        :param default_port: Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.

        deprecated
        :deprecated: Use TargetGroupAttributes instead

        stability
        :stability: deprecated
        """
        self._values = {
            'target_group_arn': target_group_arn,
        }
        if default_port is not None: self._values["default_port"] = default_port
        if load_balancer_arns is not None: self._values["load_balancer_arns"] = load_balancer_arns

    @builtins.property
    def target_group_arn(self) -> str:
        """ARN of the target group."""
        return self._values.get('target_group_arn')

    @builtins.property
    def default_port(self) -> typing.Optional[str]:
        """Port target group is listening on.

        deprecated
        :deprecated: - This property is unused and the wrong type. No need to use it.

        stability
        :stability: deprecated
        """
        return self._values.get('default_port')

    @builtins.property
    def load_balancer_arns(self) -> typing.Optional[str]:
        """A Token representing the list of ARNs for the load balancer routing to this target group."""
        return self._values.get('load_balancer_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TargetGroupImportProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetType")
class TargetType(enum.Enum):
    """How to interpret the load balancing target identifiers."""
    INSTANCE = "INSTANCE"
    """Targets identified by instance ID."""
    IP = "IP"
    """Targets identified by IP address."""
    LAMBDA = "LAMBDA"
    """Target is a single Lambda Function."""

__all__ = ["AddApplicationTargetGroupsProps", "AddApplicationTargetsProps", "AddFixedResponseProps", "AddNetworkTargetsProps", "AddRedirectResponseProps", "AddRuleProps", "ApplicationListener", "ApplicationListenerAttributes", "ApplicationListenerCertificate", "ApplicationListenerCertificateProps", "ApplicationListenerProps", "ApplicationListenerRule", "ApplicationListenerRuleProps", "ApplicationLoadBalancer", "ApplicationLoadBalancerAttributes", "ApplicationLoadBalancerProps", "ApplicationProtocol", "ApplicationTargetGroup", "ApplicationTargetGroupProps", "BaseApplicationListenerProps", "BaseApplicationListenerRuleProps", "BaseListener", "BaseLoadBalancer", "BaseLoadBalancerProps", "BaseNetworkListenerProps", "BaseTargetGroupProps", "CfnListener", "CfnListenerCertificate", "CfnListenerCertificateProps", "CfnListenerProps", "CfnListenerRule", "CfnListenerRuleProps", "CfnLoadBalancer", "CfnLoadBalancerProps", "CfnTargetGroup", "CfnTargetGroupProps", "ContentType", "FixedResponse", "HealthCheck", "HttpCodeElb", "HttpCodeTarget", "IApplicationListener", "IApplicationLoadBalancer", "IApplicationLoadBalancerTarget", "IApplicationTargetGroup", "IListenerCertificate", "ILoadBalancerV2", "INetworkListener", "INetworkListenerCertificateProps", "INetworkLoadBalancer", "INetworkLoadBalancerTarget", "INetworkTargetGroup", "ITargetGroup", "InstanceTarget", "IpAddressType", "IpTarget", "ListenerCertificate", "LoadBalancerTargetProps", "NetworkListener", "NetworkListenerProps", "NetworkLoadBalancer", "NetworkLoadBalancerAttributes", "NetworkLoadBalancerProps", "NetworkTargetGroup", "NetworkTargetGroupProps", "Protocol", "RedirectResponse", "SslPolicy", "TargetGroupAttributes", "TargetGroupBase", "TargetGroupImportProps", "TargetType", "__jsii_assembly__"]

publication.publish()
