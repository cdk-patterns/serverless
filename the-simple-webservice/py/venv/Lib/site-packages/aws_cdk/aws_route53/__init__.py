"""
## Amazon Route53 Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

To add a public hosted zone:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as route53

route53.PublicHostedZone(self, "HostedZone",
    zone_name="fully.qualified.domain.com"
)
```

To add a private hosted zone, use `PrivateHostedZone`. Note that
`enableDnsHostnames` and `enableDnsSupport` must have been enabled for the
VPC you're configuring for private hosted zones.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_route53 as route53

vpc = ec2.Vpc(self, "VPC")

zone = route53.PrivateHostedZone(self, "HostedZone",
    zone_name="fully.qualified.domain.com",
    vpc=vpc
)
```

Additional VPCs can be added with `zone.addVpc()`.

### Adding Records

To add a TXT record to your zone:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as route53

route53.TxtRecord(self, "TXTRecord",
    zone=my_zone,
    record_name="_foo", # If the name ends with a ".", it will be used as-is;
    # if it ends with a "." followed by the zone name, a trailing "." will be added automatically;
    # otherwise, a ".", the zone name, and a trailing "." will be added automatically.
    # Defaults to zone root if not specified.
    values=["Bar!", "Baz?"],
    ttl=Duration.minutes(90)
)
```

To add a A record to your zone:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as route53

route53.ARecord(self, "ARecord",
    zone=my_zone,
    target=route53.RecordTarget.from_ip_addresses("1.2.3.4", "5.6.7.8")
)
```

To add a AAAA record pointing to a CloudFront distribution:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_route53_targets as targets

route53.AaaaRecord(self, "Alias",
    zone=my_zone,
    target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution))
)
```

Constructs are available for A, AAAA, CAA, CNAME, MX, NS, SRV and TXT records.

Use the `CaaAmazonRecord` construct to easily restrict certificate authorities
allowed to issue certificates for a domain to Amazon only.

### Adding records to existing hosted zones

If you know the ID and Name of a Hosted Zone, you can import it directly:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
zone = HostedZone.from_hosted_zone_attributes(self, "MyZone",
    zone_name="example.com",
    hosted_zone_id="ZOJJZC49E0EPZ"
)
```

If you don't know the ID of a Hosted Zone, you can use the `HostedZone.fromLookup`
to discover and import it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HostedZone.from_lookup(self, "MyZone",
    domain_name="example.com"
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

import aws_cdk.aws_ec2
import aws_cdk.aws_logs
import aws_cdk.core
import aws_cdk.cx_api

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-route53", "1.23.0", __name__, "aws-route53@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.AliasRecordTargetConfig", jsii_struct_bases=[], name_mapping={'dns_name': 'dnsName', 'hosted_zone_id': 'hostedZoneId'})
class AliasRecordTargetConfig():
    def __init__(self, *, dns_name: str, hosted_zone_id: str):
        """Represents the properties of an alias target destination.

        :param dns_name: DNS name of the target.
        :param hosted_zone_id: Hosted zone ID of the target.
        """
        self._values = {
            'dns_name': dns_name,
            'hosted_zone_id': hosted_zone_id,
        }

    @builtins.property
    def dns_name(self) -> str:
        """DNS name of the target."""
        return self._values.get('dns_name')

    @builtins.property
    def hosted_zone_id(self) -> str:
        """Hosted zone ID of the target."""
        return self._values.get('hosted_zone_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AliasRecordTargetConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CaaRecordValue", jsii_struct_bases=[], name_mapping={'flag': 'flag', 'tag': 'tag', 'value': 'value'})
class CaaRecordValue():
    def __init__(self, *, flag: jsii.Number, tag: "CaaTag", value: str):
        """Properties for a CAA record value.

        :param flag: The flag.
        :param tag: The tag.
        :param value: The value associated with the tag.
        """
        self._values = {
            'flag': flag,
            'tag': tag,
            'value': value,
        }

    @builtins.property
    def flag(self) -> jsii.Number:
        """The flag."""
        return self._values.get('flag')

    @builtins.property
    def tag(self) -> "CaaTag":
        """The tag."""
        return self._values.get('tag')

    @builtins.property
    def value(self) -> str:
        """The value associated with the tag."""
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CaaRecordValue(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-route53.CaaTag")
class CaaTag(enum.Enum):
    """The CAA tag."""
    ISSUE = "ISSUE"
    """Explicity authorizes a single certificate authority to issue a certificate (any type) for the hostname."""
    ISSUEWILD = "ISSUEWILD"
    """Explicity authorizes a single certificate authority to issue a wildcard certificate (and only wildcard) for the hostname."""
    IODEF = "IODEF"
    """Specifies a URL to which a certificate authority may report policy violations."""

@jsii.implements(aws_cdk.core.IInspectable)
class CfnHealthCheck(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnHealthCheck"):
    """A CloudFormation ``AWS::Route53::HealthCheck``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html
    cloudformationResource:
    :cloudformationResource:: AWS::Route53::HealthCheck
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, health_check_config: typing.Union["HealthCheckConfigProperty", aws_cdk.core.IResolvable], health_check_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "HealthCheckTagProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Route53::HealthCheck``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param health_check_config: ``AWS::Route53::HealthCheck.HealthCheckConfig``.
        :param health_check_tags: ``AWS::Route53::HealthCheck.HealthCheckTags``.
        """
        props = CfnHealthCheckProps(health_check_config=health_check_config, health_check_tags=health_check_tags)

        jsii.create(CfnHealthCheck, self, [scope, id, props])

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
    @jsii.member(jsii_name="healthCheckConfig")
    def health_check_config(self) -> typing.Union["HealthCheckConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::Route53::HealthCheck.HealthCheckConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthcheckconfig
        """
        return jsii.get(self, "healthCheckConfig")

    @health_check_config.setter
    def health_check_config(self, value: typing.Union["HealthCheckConfigProperty", aws_cdk.core.IResolvable]):
        jsii.set(self, "healthCheckConfig", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckTags")
    def health_check_tags(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "HealthCheckTagProperty"]]]]]:
        """``AWS::Route53::HealthCheck.HealthCheckTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthchecktags
        """
        return jsii.get(self, "healthCheckTags")

    @health_check_tags.setter
    def health_check_tags(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "HealthCheckTagProperty"]]]]]):
        jsii.set(self, "healthCheckTags", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.AlarmIdentifierProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'region': 'region'})
    class AlarmIdentifierProperty():
        def __init__(self, *, name: str, region: str):
            """
            :param name: ``CfnHealthCheck.AlarmIdentifierProperty.Name``.
            :param region: ``CfnHealthCheck.AlarmIdentifierProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html
            """
            self._values = {
                'name': name,
                'region': region,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnHealthCheck.AlarmIdentifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html#cfn-route53-healthcheck-alarmidentifier-name
            """
            return self._values.get('name')

        @builtins.property
        def region(self) -> str:
            """``CfnHealthCheck.AlarmIdentifierProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html#cfn-route53-healthcheck-alarmidentifier-region
            """
            return self._values.get('region')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AlarmIdentifierProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.HealthCheckConfigProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'alarm_identifier': 'alarmIdentifier', 'child_health_checks': 'childHealthChecks', 'enable_sni': 'enableSni', 'failure_threshold': 'failureThreshold', 'fully_qualified_domain_name': 'fullyQualifiedDomainName', 'health_threshold': 'healthThreshold', 'insufficient_data_health_status': 'insufficientDataHealthStatus', 'inverted': 'inverted', 'ip_address': 'ipAddress', 'measure_latency': 'measureLatency', 'port': 'port', 'regions': 'regions', 'request_interval': 'requestInterval', 'resource_path': 'resourcePath', 'search_string': 'searchString'})
    class HealthCheckConfigProperty():
        def __init__(self, *, type: str, alarm_identifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnHealthCheck.AlarmIdentifierProperty"]]]=None, child_health_checks: typing.Optional[typing.List[str]]=None, enable_sni: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, failure_threshold: typing.Optional[jsii.Number]=None, fully_qualified_domain_name: typing.Optional[str]=None, health_threshold: typing.Optional[jsii.Number]=None, insufficient_data_health_status: typing.Optional[str]=None, inverted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ip_address: typing.Optional[str]=None, measure_latency: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, port: typing.Optional[jsii.Number]=None, regions: typing.Optional[typing.List[str]]=None, request_interval: typing.Optional[jsii.Number]=None, resource_path: typing.Optional[str]=None, search_string: typing.Optional[str]=None):
            """
            :param type: ``CfnHealthCheck.HealthCheckConfigProperty.Type``.
            :param alarm_identifier: ``CfnHealthCheck.HealthCheckConfigProperty.AlarmIdentifier``.
            :param child_health_checks: ``CfnHealthCheck.HealthCheckConfigProperty.ChildHealthChecks``.
            :param enable_sni: ``CfnHealthCheck.HealthCheckConfigProperty.EnableSNI``.
            :param failure_threshold: ``CfnHealthCheck.HealthCheckConfigProperty.FailureThreshold``.
            :param fully_qualified_domain_name: ``CfnHealthCheck.HealthCheckConfigProperty.FullyQualifiedDomainName``.
            :param health_threshold: ``CfnHealthCheck.HealthCheckConfigProperty.HealthThreshold``.
            :param insufficient_data_health_status: ``CfnHealthCheck.HealthCheckConfigProperty.InsufficientDataHealthStatus``.
            :param inverted: ``CfnHealthCheck.HealthCheckConfigProperty.Inverted``.
            :param ip_address: ``CfnHealthCheck.HealthCheckConfigProperty.IPAddress``.
            :param measure_latency: ``CfnHealthCheck.HealthCheckConfigProperty.MeasureLatency``.
            :param port: ``CfnHealthCheck.HealthCheckConfigProperty.Port``.
            :param regions: ``CfnHealthCheck.HealthCheckConfigProperty.Regions``.
            :param request_interval: ``CfnHealthCheck.HealthCheckConfigProperty.RequestInterval``.
            :param resource_path: ``CfnHealthCheck.HealthCheckConfigProperty.ResourcePath``.
            :param search_string: ``CfnHealthCheck.HealthCheckConfigProperty.SearchString``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html
            """
            self._values = {
                'type': type,
            }
            if alarm_identifier is not None: self._values["alarm_identifier"] = alarm_identifier
            if child_health_checks is not None: self._values["child_health_checks"] = child_health_checks
            if enable_sni is not None: self._values["enable_sni"] = enable_sni
            if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold
            if fully_qualified_domain_name is not None: self._values["fully_qualified_domain_name"] = fully_qualified_domain_name
            if health_threshold is not None: self._values["health_threshold"] = health_threshold
            if insufficient_data_health_status is not None: self._values["insufficient_data_health_status"] = insufficient_data_health_status
            if inverted is not None: self._values["inverted"] = inverted
            if ip_address is not None: self._values["ip_address"] = ip_address
            if measure_latency is not None: self._values["measure_latency"] = measure_latency
            if port is not None: self._values["port"] = port
            if regions is not None: self._values["regions"] = regions
            if request_interval is not None: self._values["request_interval"] = request_interval
            if resource_path is not None: self._values["resource_path"] = resource_path
            if search_string is not None: self._values["search_string"] = search_string

        @builtins.property
        def type(self) -> str:
            """``CfnHealthCheck.HealthCheckConfigProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-type
            """
            return self._values.get('type')

        @builtins.property
        def alarm_identifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnHealthCheck.AlarmIdentifierProperty"]]]:
            """``CfnHealthCheck.HealthCheckConfigProperty.AlarmIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-alarmidentifier
            """
            return self._values.get('alarm_identifier')

        @builtins.property
        def child_health_checks(self) -> typing.Optional[typing.List[str]]:
            """``CfnHealthCheck.HealthCheckConfigProperty.ChildHealthChecks``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-childhealthchecks
            """
            return self._values.get('child_health_checks')

        @builtins.property
        def enable_sni(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnHealthCheck.HealthCheckConfigProperty.EnableSNI``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-enablesni
            """
            return self._values.get('enable_sni')

        @builtins.property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnHealthCheck.HealthCheckConfigProperty.FailureThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-failurethreshold
            """
            return self._values.get('failure_threshold')

        @builtins.property
        def fully_qualified_domain_name(self) -> typing.Optional[str]:
            """``CfnHealthCheck.HealthCheckConfigProperty.FullyQualifiedDomainName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-fullyqualifieddomainname
            """
            return self._values.get('fully_qualified_domain_name')

        @builtins.property
        def health_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnHealthCheck.HealthCheckConfigProperty.HealthThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-healththreshold
            """
            return self._values.get('health_threshold')

        @builtins.property
        def insufficient_data_health_status(self) -> typing.Optional[str]:
            """``CfnHealthCheck.HealthCheckConfigProperty.InsufficientDataHealthStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-insufficientdatahealthstatus
            """
            return self._values.get('insufficient_data_health_status')

        @builtins.property
        def inverted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnHealthCheck.HealthCheckConfigProperty.Inverted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-inverted
            """
            return self._values.get('inverted')

        @builtins.property
        def ip_address(self) -> typing.Optional[str]:
            """``CfnHealthCheck.HealthCheckConfigProperty.IPAddress``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-ipaddress
            """
            return self._values.get('ip_address')

        @builtins.property
        def measure_latency(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnHealthCheck.HealthCheckConfigProperty.MeasureLatency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-measurelatency
            """
            return self._values.get('measure_latency')

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnHealthCheck.HealthCheckConfigProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-port
            """
            return self._values.get('port')

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[str]]:
            """``CfnHealthCheck.HealthCheckConfigProperty.Regions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-regions
            """
            return self._values.get('regions')

        @builtins.property
        def request_interval(self) -> typing.Optional[jsii.Number]:
            """``CfnHealthCheck.HealthCheckConfigProperty.RequestInterval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-requestinterval
            """
            return self._values.get('request_interval')

        @builtins.property
        def resource_path(self) -> typing.Optional[str]:
            """``CfnHealthCheck.HealthCheckConfigProperty.ResourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-resourcepath
            """
            return self._values.get('resource_path')

        @builtins.property
        def search_string(self) -> typing.Optional[str]:
            """``CfnHealthCheck.HealthCheckConfigProperty.SearchString``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-searchstring
            """
            return self._values.get('search_string')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.HealthCheckTagProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class HealthCheckTagProperty():
        def __init__(self, *, key: str, value: str):
            """
            :param key: ``CfnHealthCheck.HealthCheckTagProperty.Key``.
            :param value: ``CfnHealthCheck.HealthCheckTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnHealthCheck.HealthCheckTagProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html#cfn-route53-healthchecktags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnHealthCheck.HealthCheckTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html#cfn-route53-healthchecktags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckTagProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheckProps", jsii_struct_bases=[], name_mapping={'health_check_config': 'healthCheckConfig', 'health_check_tags': 'healthCheckTags'})
class CfnHealthCheckProps():
    def __init__(self, *, health_check_config: typing.Union["CfnHealthCheck.HealthCheckConfigProperty", aws_cdk.core.IResolvable], health_check_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnHealthCheck.HealthCheckTagProperty"]]]]]=None):
        """Properties for defining a ``AWS::Route53::HealthCheck``.

        :param health_check_config: ``AWS::Route53::HealthCheck.HealthCheckConfig``.
        :param health_check_tags: ``AWS::Route53::HealthCheck.HealthCheckTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html
        """
        self._values = {
            'health_check_config': health_check_config,
        }
        if health_check_tags is not None: self._values["health_check_tags"] = health_check_tags

    @builtins.property
    def health_check_config(self) -> typing.Union["CfnHealthCheck.HealthCheckConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::Route53::HealthCheck.HealthCheckConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthcheckconfig
        """
        return self._values.get('health_check_config')

    @builtins.property
    def health_check_tags(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnHealthCheck.HealthCheckTagProperty"]]]]]:
        """``AWS::Route53::HealthCheck.HealthCheckTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthchecktags
        """
        return self._values.get('health_check_tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnHealthCheckProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnHostedZone(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnHostedZone"):
    """A CloudFormation ``AWS::Route53::HostedZone``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html
    cloudformationResource:
    :cloudformationResource:: AWS::Route53::HostedZone
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, hosted_zone_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HostedZoneConfigProperty"]]]=None, hosted_zone_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "HostedZoneTagProperty"]]]]]=None, query_logging_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["QueryLoggingConfigProperty"]]]=None, vpcs: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VPCProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Route53::HostedZone``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Route53::HostedZone.Name``.
        :param hosted_zone_config: ``AWS::Route53::HostedZone.HostedZoneConfig``.
        :param hosted_zone_tags: ``AWS::Route53::HostedZone.HostedZoneTags``.
        :param query_logging_config: ``AWS::Route53::HostedZone.QueryLoggingConfig``.
        :param vpcs: ``AWS::Route53::HostedZone.VPCs``.
        """
        props = CfnHostedZoneProps(name=name, hosted_zone_config=hosted_zone_config, hosted_zone_tags=hosted_zone_tags, query_logging_config=query_logging_config, vpcs=vpcs)

        jsii.create(CfnHostedZone, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrNameServers")
    def attr_name_servers(self) -> typing.List[str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NameServers
        """
        return jsii.get(self, "attrNameServers")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Route53::HostedZone.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZoneConfig")
    def hosted_zone_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HostedZoneConfigProperty"]]]:
        """``AWS::Route53::HostedZone.HostedZoneConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzoneconfig
        """
        return jsii.get(self, "hostedZoneConfig")

    @hosted_zone_config.setter
    def hosted_zone_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HostedZoneConfigProperty"]]]):
        jsii.set(self, "hostedZoneConfig", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZoneTags")
    def hosted_zone_tags(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "HostedZoneTagProperty"]]]]]:
        """``AWS::Route53::HostedZone.HostedZoneTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzonetags
        """
        return jsii.get(self, "hostedZoneTags")

    @hosted_zone_tags.setter
    def hosted_zone_tags(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "HostedZoneTagProperty"]]]]]):
        jsii.set(self, "hostedZoneTags", value)

    @builtins.property
    @jsii.member(jsii_name="queryLoggingConfig")
    def query_logging_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["QueryLoggingConfigProperty"]]]:
        """``AWS::Route53::HostedZone.QueryLoggingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-queryloggingconfig
        """
        return jsii.get(self, "queryLoggingConfig")

    @query_logging_config.setter
    def query_logging_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["QueryLoggingConfigProperty"]]]):
        jsii.set(self, "queryLoggingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="vpcs")
    def vpcs(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VPCProperty"]]]]]:
        """``AWS::Route53::HostedZone.VPCs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-vpcs
        """
        return jsii.get(self, "vpcs")

    @vpcs.setter
    def vpcs(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VPCProperty"]]]]]):
        jsii.set(self, "vpcs", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.HostedZoneConfigProperty", jsii_struct_bases=[], name_mapping={'comment': 'comment'})
    class HostedZoneConfigProperty():
        def __init__(self, *, comment: typing.Optional[str]=None):
            """
            :param comment: ``CfnHostedZone.HostedZoneConfigProperty.Comment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzoneconfig.html
            """
            self._values = {
            }
            if comment is not None: self._values["comment"] = comment

        @builtins.property
        def comment(self) -> typing.Optional[str]:
            """``CfnHostedZone.HostedZoneConfigProperty.Comment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzoneconfig.html#cfn-route53-hostedzone-hostedzoneconfig-comment
            """
            return self._values.get('comment')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostedZoneConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.HostedZoneTagProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class HostedZoneTagProperty():
        def __init__(self, *, key: str, value: str):
            """
            :param key: ``CfnHostedZone.HostedZoneTagProperty.Key``.
            :param value: ``CfnHostedZone.HostedZoneTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetags.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnHostedZone.HostedZoneTagProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetags.html#cfn-route53-hostedzonetags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnHostedZone.HostedZoneTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetags.html#cfn-route53-hostedzonetags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostedZoneTagProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.QueryLoggingConfigProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_logs_log_group_arn': 'cloudWatchLogsLogGroupArn'})
    class QueryLoggingConfigProperty():
        def __init__(self, *, cloud_watch_logs_log_group_arn: str):
            """
            :param cloud_watch_logs_log_group_arn: ``CfnHostedZone.QueryLoggingConfigProperty.CloudWatchLogsLogGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-queryloggingconfig.html
            """
            self._values = {
                'cloud_watch_logs_log_group_arn': cloud_watch_logs_log_group_arn,
            }

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> str:
            """``CfnHostedZone.QueryLoggingConfigProperty.CloudWatchLogsLogGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-queryloggingconfig.html#cfn-route53-hostedzone-queryloggingconfig-cloudwatchlogsloggrouparn
            """
            return self._values.get('cloud_watch_logs_log_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'QueryLoggingConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.VPCProperty", jsii_struct_bases=[], name_mapping={'vpc_id': 'vpcId', 'vpc_region': 'vpcRegion'})
    class VPCProperty():
        def __init__(self, *, vpc_id: str, vpc_region: str):
            """
            :param vpc_id: ``CfnHostedZone.VPCProperty.VPCId``.
            :param vpc_region: ``CfnHostedZone.VPCProperty.VPCRegion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone-hostedzonevpcs.html
            """
            self._values = {
                'vpc_id': vpc_id,
                'vpc_region': vpc_region,
            }

        @builtins.property
        def vpc_id(self) -> str:
            """``CfnHostedZone.VPCProperty.VPCId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone-hostedzonevpcs.html#cfn-route53-hostedzone-hostedzonevpcs-vpcid
            """
            return self._values.get('vpc_id')

        @builtins.property
        def vpc_region(self) -> str:
            """``CfnHostedZone.VPCProperty.VPCRegion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone-hostedzonevpcs.html#cfn-route53-hostedzone-hostedzonevpcs-vpcregion
            """
            return self._values.get('vpc_region')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VPCProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZoneProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'hosted_zone_config': 'hostedZoneConfig', 'hosted_zone_tags': 'hostedZoneTags', 'query_logging_config': 'queryLoggingConfig', 'vpcs': 'vpcs'})
class CfnHostedZoneProps():
    def __init__(self, *, name: str, hosted_zone_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnHostedZone.HostedZoneConfigProperty"]]]=None, hosted_zone_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnHostedZone.HostedZoneTagProperty"]]]]]=None, query_logging_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnHostedZone.QueryLoggingConfigProperty"]]]=None, vpcs: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnHostedZone.VPCProperty"]]]]]=None):
        """Properties for defining a ``AWS::Route53::HostedZone``.

        :param name: ``AWS::Route53::HostedZone.Name``.
        :param hosted_zone_config: ``AWS::Route53::HostedZone.HostedZoneConfig``.
        :param hosted_zone_tags: ``AWS::Route53::HostedZone.HostedZoneTags``.
        :param query_logging_config: ``AWS::Route53::HostedZone.QueryLoggingConfig``.
        :param vpcs: ``AWS::Route53::HostedZone.VPCs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html
        """
        self._values = {
            'name': name,
        }
        if hosted_zone_config is not None: self._values["hosted_zone_config"] = hosted_zone_config
        if hosted_zone_tags is not None: self._values["hosted_zone_tags"] = hosted_zone_tags
        if query_logging_config is not None: self._values["query_logging_config"] = query_logging_config
        if vpcs is not None: self._values["vpcs"] = vpcs

    @builtins.property
    def name(self) -> str:
        """``AWS::Route53::HostedZone.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-name
        """
        return self._values.get('name')

    @builtins.property
    def hosted_zone_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnHostedZone.HostedZoneConfigProperty"]]]:
        """``AWS::Route53::HostedZone.HostedZoneConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzoneconfig
        """
        return self._values.get('hosted_zone_config')

    @builtins.property
    def hosted_zone_tags(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnHostedZone.HostedZoneTagProperty"]]]]]:
        """``AWS::Route53::HostedZone.HostedZoneTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzonetags
        """
        return self._values.get('hosted_zone_tags')

    @builtins.property
    def query_logging_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnHostedZone.QueryLoggingConfigProperty"]]]:
        """``AWS::Route53::HostedZone.QueryLoggingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-queryloggingconfig
        """
        return self._values.get('query_logging_config')

    @builtins.property
    def vpcs(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnHostedZone.VPCProperty"]]]]]:
        """``AWS::Route53::HostedZone.VPCs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-vpcs
        """
        return self._values.get('vpcs')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnHostedZoneProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRecordSet(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnRecordSet"):
    """A CloudFormation ``AWS::Route53::RecordSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html
    cloudformationResource:
    :cloudformationResource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, type: str, alias_target: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AliasTargetProperty"]]]=None, comment: typing.Optional[str]=None, failover: typing.Optional[str]=None, geo_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GeoLocationProperty"]]]=None, health_check_id: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, multi_value_answer: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, region: typing.Optional[str]=None, resource_records: typing.Optional[typing.List[str]]=None, set_identifier: typing.Optional[str]=None, ttl: typing.Optional[str]=None, weight: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::Route53::RecordSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Route53::RecordSet.Name``.
        :param type: ``AWS::Route53::RecordSet.Type``.
        :param alias_target: ``AWS::Route53::RecordSet.AliasTarget``.
        :param comment: ``AWS::Route53::RecordSet.Comment``.
        :param failover: ``AWS::Route53::RecordSet.Failover``.
        :param geo_location: ``AWS::Route53::RecordSet.GeoLocation``.
        :param health_check_id: ``AWS::Route53::RecordSet.HealthCheckId``.
        :param hosted_zone_id: ``AWS::Route53::RecordSet.HostedZoneId``.
        :param hosted_zone_name: ``AWS::Route53::RecordSet.HostedZoneName``.
        :param multi_value_answer: ``AWS::Route53::RecordSet.MultiValueAnswer``.
        :param region: ``AWS::Route53::RecordSet.Region``.
        :param resource_records: ``AWS::Route53::RecordSet.ResourceRecords``.
        :param set_identifier: ``AWS::Route53::RecordSet.SetIdentifier``.
        :param ttl: ``AWS::Route53::RecordSet.TTL``.
        :param weight: ``AWS::Route53::RecordSet.Weight``.
        """
        props = CfnRecordSetProps(name=name, type=type, alias_target=alias_target, comment=comment, failover=failover, geo_location=geo_location, health_check_id=health_check_id, hosted_zone_id=hosted_zone_id, hosted_zone_name=hosted_zone_name, multi_value_answer=multi_value_answer, region=region, resource_records=resource_records, set_identifier=set_identifier, ttl=ttl, weight=weight)

        jsii.create(CfnRecordSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Route53::RecordSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::Route53::RecordSet.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="aliasTarget")
    def alias_target(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AliasTargetProperty"]]]:
        """``AWS::Route53::RecordSet.AliasTarget``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-aliastarget
        """
        return jsii.get(self, "aliasTarget")

    @alias_target.setter
    def alias_target(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AliasTargetProperty"]]]):
        jsii.set(self, "aliasTarget", value)

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.Comment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-comment
        """
        return jsii.get(self, "comment")

    @comment.setter
    def comment(self, value: typing.Optional[str]):
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="failover")
    def failover(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.Failover``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-failover
        """
        return jsii.get(self, "failover")

    @failover.setter
    def failover(self, value: typing.Optional[str]):
        jsii.set(self, "failover", value)

    @builtins.property
    @jsii.member(jsii_name="geoLocation")
    def geo_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GeoLocationProperty"]]]:
        """``AWS::Route53::RecordSet.GeoLocation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-geolocation
        """
        return jsii.get(self, "geoLocation")

    @geo_location.setter
    def geo_location(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GeoLocationProperty"]]]):
        jsii.set(self, "geoLocation", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.HealthCheckId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-healthcheckid
        """
        return jsii.get(self, "healthCheckId")

    @health_check_id.setter
    def health_check_id(self, value: typing.Optional[str]):
        jsii.set(self, "healthCheckId", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.HostedZoneId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzoneid
        """
        return jsii.get(self, "hostedZoneId")

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: typing.Optional[str]):
        jsii.set(self, "hostedZoneId", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZoneName")
    def hosted_zone_name(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.HostedZoneName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzonename
        """
        return jsii.get(self, "hostedZoneName")

    @hosted_zone_name.setter
    def hosted_zone_name(self, value: typing.Optional[str]):
        jsii.set(self, "hostedZoneName", value)

    @builtins.property
    @jsii.member(jsii_name="multiValueAnswer")
    def multi_value_answer(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Route53::RecordSet.MultiValueAnswer``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-multivalueanswer
        """
        return jsii.get(self, "multiValueAnswer")

    @multi_value_answer.setter
    def multi_value_answer(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "multiValueAnswer", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-region
        """
        return jsii.get(self, "region")

    @region.setter
    def region(self, value: typing.Optional[str]):
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="resourceRecords")
    def resource_records(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Route53::RecordSet.ResourceRecords``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-resourcerecords
        """
        return jsii.get(self, "resourceRecords")

    @resource_records.setter
    def resource_records(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "resourceRecords", value)

    @builtins.property
    @jsii.member(jsii_name="setIdentifier")
    def set_identifier(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.SetIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-setidentifier
        """
        return jsii.get(self, "setIdentifier")

    @set_identifier.setter
    def set_identifier(self, value: typing.Optional[str]):
        jsii.set(self, "setIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.TTL``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-ttl
        """
        return jsii.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: typing.Optional[str]):
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> typing.Optional[jsii.Number]:
        """``AWS::Route53::RecordSet.Weight``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-weight
        """
        return jsii.get(self, "weight")

    @weight.setter
    def weight(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "weight", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSet.AliasTargetProperty", jsii_struct_bases=[], name_mapping={'dns_name': 'dnsName', 'hosted_zone_id': 'hostedZoneId', 'evaluate_target_health': 'evaluateTargetHealth'})
    class AliasTargetProperty():
        def __init__(self, *, dns_name: str, hosted_zone_id: str, evaluate_target_health: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param dns_name: ``CfnRecordSet.AliasTargetProperty.DNSName``.
            :param hosted_zone_id: ``CfnRecordSet.AliasTargetProperty.HostedZoneId``.
            :param evaluate_target_health: ``CfnRecordSet.AliasTargetProperty.EvaluateTargetHealth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html
            """
            self._values = {
                'dns_name': dns_name,
                'hosted_zone_id': hosted_zone_id,
            }
            if evaluate_target_health is not None: self._values["evaluate_target_health"] = evaluate_target_health

        @builtins.property
        def dns_name(self) -> str:
            """``CfnRecordSet.AliasTargetProperty.DNSName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-dnshostname
            """
            return self._values.get('dns_name')

        @builtins.property
        def hosted_zone_id(self) -> str:
            """``CfnRecordSet.AliasTargetProperty.HostedZoneId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-hostedzoneid
            """
            return self._values.get('hosted_zone_id')

        @builtins.property
        def evaluate_target_health(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnRecordSet.AliasTargetProperty.EvaluateTargetHealth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
            """
            return self._values.get('evaluate_target_health')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AliasTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSet.GeoLocationProperty", jsii_struct_bases=[], name_mapping={'continent_code': 'continentCode', 'country_code': 'countryCode', 'subdivision_code': 'subdivisionCode'})
    class GeoLocationProperty():
        def __init__(self, *, continent_code: typing.Optional[str]=None, country_code: typing.Optional[str]=None, subdivision_code: typing.Optional[str]=None):
            """
            :param continent_code: ``CfnRecordSet.GeoLocationProperty.ContinentCode``.
            :param country_code: ``CfnRecordSet.GeoLocationProperty.CountryCode``.
            :param subdivision_code: ``CfnRecordSet.GeoLocationProperty.SubdivisionCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html
            """
            self._values = {
            }
            if continent_code is not None: self._values["continent_code"] = continent_code
            if country_code is not None: self._values["country_code"] = country_code
            if subdivision_code is not None: self._values["subdivision_code"] = subdivision_code

        @builtins.property
        def continent_code(self) -> typing.Optional[str]:
            """``CfnRecordSet.GeoLocationProperty.ContinentCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-continentcode
            """
            return self._values.get('continent_code')

        @builtins.property
        def country_code(self) -> typing.Optional[str]:
            """``CfnRecordSet.GeoLocationProperty.CountryCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-countrycode
            """
            return self._values.get('country_code')

        @builtins.property
        def subdivision_code(self) -> typing.Optional[str]:
            """``CfnRecordSet.GeoLocationProperty.SubdivisionCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-subdivisioncode
            """
            return self._values.get('subdivision_code')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GeoLocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnRecordSetGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup"):
    """A CloudFormation ``AWS::Route53::RecordSetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Route53::RecordSetGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, record_sets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "RecordSetProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Route53::RecordSetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param comment: ``AWS::Route53::RecordSetGroup.Comment``.
        :param hosted_zone_id: ``AWS::Route53::RecordSetGroup.HostedZoneId``.
        :param hosted_zone_name: ``AWS::Route53::RecordSetGroup.HostedZoneName``.
        :param record_sets: ``AWS::Route53::RecordSetGroup.RecordSets``.
        """
        props = CfnRecordSetGroupProps(comment=comment, hosted_zone_id=hosted_zone_id, hosted_zone_name=hosted_zone_name, record_sets=record_sets)

        jsii.create(CfnRecordSetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="comment")
    def comment(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSetGroup.Comment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-comment
        """
        return jsii.get(self, "comment")

    @comment.setter
    def comment(self, value: typing.Optional[str]):
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSetGroup.HostedZoneId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzoneid
        """
        return jsii.get(self, "hostedZoneId")

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: typing.Optional[str]):
        jsii.set(self, "hostedZoneId", value)

    @builtins.property
    @jsii.member(jsii_name="hostedZoneName")
    def hosted_zone_name(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSetGroup.HostedZoneName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzonename
        """
        return jsii.get(self, "hostedZoneName")

    @hosted_zone_name.setter
    def hosted_zone_name(self, value: typing.Optional[str]):
        jsii.set(self, "hostedZoneName", value)

    @builtins.property
    @jsii.member(jsii_name="recordSets")
    def record_sets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "RecordSetProperty"]]]]]:
        """``AWS::Route53::RecordSetGroup.RecordSets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-recordsets
        """
        return jsii.get(self, "recordSets")

    @record_sets.setter
    def record_sets(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "RecordSetProperty"]]]]]):
        jsii.set(self, "recordSets", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.AliasTargetProperty", jsii_struct_bases=[], name_mapping={'dns_name': 'dnsName', 'hosted_zone_id': 'hostedZoneId', 'evaluate_target_health': 'evaluateTargetHealth'})
    class AliasTargetProperty():
        def __init__(self, *, dns_name: str, hosted_zone_id: str, evaluate_target_health: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param dns_name: ``CfnRecordSetGroup.AliasTargetProperty.DNSName``.
            :param hosted_zone_id: ``CfnRecordSetGroup.AliasTargetProperty.HostedZoneId``.
            :param evaluate_target_health: ``CfnRecordSetGroup.AliasTargetProperty.EvaluateTargetHealth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html
            """
            self._values = {
                'dns_name': dns_name,
                'hosted_zone_id': hosted_zone_id,
            }
            if evaluate_target_health is not None: self._values["evaluate_target_health"] = evaluate_target_health

        @builtins.property
        def dns_name(self) -> str:
            """``CfnRecordSetGroup.AliasTargetProperty.DNSName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-dnshostname
            """
            return self._values.get('dns_name')

        @builtins.property
        def hosted_zone_id(self) -> str:
            """``CfnRecordSetGroup.AliasTargetProperty.HostedZoneId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-hostedzoneid
            """
            return self._values.get('hosted_zone_id')

        @builtins.property
        def evaluate_target_health(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnRecordSetGroup.AliasTargetProperty.EvaluateTargetHealth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
            """
            return self._values.get('evaluate_target_health')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AliasTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.GeoLocationProperty", jsii_struct_bases=[], name_mapping={'continent_code': 'continentCode', 'country_code': 'countryCode', 'subdivision_code': 'subdivisionCode'})
    class GeoLocationProperty():
        def __init__(self, *, continent_code: typing.Optional[str]=None, country_code: typing.Optional[str]=None, subdivision_code: typing.Optional[str]=None):
            """
            :param continent_code: ``CfnRecordSetGroup.GeoLocationProperty.ContinentCode``.
            :param country_code: ``CfnRecordSetGroup.GeoLocationProperty.CountryCode``.
            :param subdivision_code: ``CfnRecordSetGroup.GeoLocationProperty.SubdivisionCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html
            """
            self._values = {
            }
            if continent_code is not None: self._values["continent_code"] = continent_code
            if country_code is not None: self._values["country_code"] = country_code
            if subdivision_code is not None: self._values["subdivision_code"] = subdivision_code

        @builtins.property
        def continent_code(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.GeoLocationProperty.ContinentCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordsetgroup-geolocation-continentcode
            """
            return self._values.get('continent_code')

        @builtins.property
        def country_code(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.GeoLocationProperty.CountryCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-countrycode
            """
            return self._values.get('country_code')

        @builtins.property
        def subdivision_code(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.GeoLocationProperty.SubdivisionCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-subdivisioncode
            """
            return self._values.get('subdivision_code')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GeoLocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.RecordSetProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'type': 'type', 'alias_target': 'aliasTarget', 'comment': 'comment', 'failover': 'failover', 'geo_location': 'geoLocation', 'health_check_id': 'healthCheckId', 'hosted_zone_id': 'hostedZoneId', 'hosted_zone_name': 'hostedZoneName', 'multi_value_answer': 'multiValueAnswer', 'region': 'region', 'resource_records': 'resourceRecords', 'set_identifier': 'setIdentifier', 'ttl': 'ttl', 'weight': 'weight'})
    class RecordSetProperty():
        def __init__(self, *, name: str, type: str, alias_target: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSetGroup.AliasTargetProperty"]]]=None, comment: typing.Optional[str]=None, failover: typing.Optional[str]=None, geo_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSetGroup.GeoLocationProperty"]]]=None, health_check_id: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, multi_value_answer: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, region: typing.Optional[str]=None, resource_records: typing.Optional[typing.List[str]]=None, set_identifier: typing.Optional[str]=None, ttl: typing.Optional[str]=None, weight: typing.Optional[jsii.Number]=None):
            """
            :param name: ``CfnRecordSetGroup.RecordSetProperty.Name``.
            :param type: ``CfnRecordSetGroup.RecordSetProperty.Type``.
            :param alias_target: ``CfnRecordSetGroup.RecordSetProperty.AliasTarget``.
            :param comment: ``CfnRecordSetGroup.RecordSetProperty.Comment``.
            :param failover: ``CfnRecordSetGroup.RecordSetProperty.Failover``.
            :param geo_location: ``CfnRecordSetGroup.RecordSetProperty.GeoLocation``.
            :param health_check_id: ``CfnRecordSetGroup.RecordSetProperty.HealthCheckId``.
            :param hosted_zone_id: ``CfnRecordSetGroup.RecordSetProperty.HostedZoneId``.
            :param hosted_zone_name: ``CfnRecordSetGroup.RecordSetProperty.HostedZoneName``.
            :param multi_value_answer: ``CfnRecordSetGroup.RecordSetProperty.MultiValueAnswer``.
            :param region: ``CfnRecordSetGroup.RecordSetProperty.Region``.
            :param resource_records: ``CfnRecordSetGroup.RecordSetProperty.ResourceRecords``.
            :param set_identifier: ``CfnRecordSetGroup.RecordSetProperty.SetIdentifier``.
            :param ttl: ``CfnRecordSetGroup.RecordSetProperty.TTL``.
            :param weight: ``CfnRecordSetGroup.RecordSetProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html
            """
            self._values = {
                'name': name,
                'type': type,
            }
            if alias_target is not None: self._values["alias_target"] = alias_target
            if comment is not None: self._values["comment"] = comment
            if failover is not None: self._values["failover"] = failover
            if geo_location is not None: self._values["geo_location"] = geo_location
            if health_check_id is not None: self._values["health_check_id"] = health_check_id
            if hosted_zone_id is not None: self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None: self._values["hosted_zone_name"] = hosted_zone_name
            if multi_value_answer is not None: self._values["multi_value_answer"] = multi_value_answer
            if region is not None: self._values["region"] = region
            if resource_records is not None: self._values["resource_records"] = resource_records
            if set_identifier is not None: self._values["set_identifier"] = set_identifier
            if ttl is not None: self._values["ttl"] = ttl
            if weight is not None: self._values["weight"] = weight

        @builtins.property
        def name(self) -> str:
            """``CfnRecordSetGroup.RecordSetProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-name
            """
            return self._values.get('name')

        @builtins.property
        def type(self) -> str:
            """``CfnRecordSetGroup.RecordSetProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-type
            """
            return self._values.get('type')

        @builtins.property
        def alias_target(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSetGroup.AliasTargetProperty"]]]:
            """``CfnRecordSetGroup.RecordSetProperty.AliasTarget``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-aliastarget
            """
            return self._values.get('alias_target')

        @builtins.property
        def comment(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.Comment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-comment
            """
            return self._values.get('comment')

        @builtins.property
        def failover(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.Failover``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-failover
            """
            return self._values.get('failover')

        @builtins.property
        def geo_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSetGroup.GeoLocationProperty"]]]:
            """``CfnRecordSetGroup.RecordSetProperty.GeoLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-geolocation
            """
            return self._values.get('geo_location')

        @builtins.property
        def health_check_id(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.HealthCheckId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-healthcheckid
            """
            return self._values.get('health_check_id')

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.HostedZoneId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzoneid
            """
            return self._values.get('hosted_zone_id')

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.HostedZoneName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzonename
            """
            return self._values.get('hosted_zone_name')

        @builtins.property
        def multi_value_answer(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnRecordSetGroup.RecordSetProperty.MultiValueAnswer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-multivalueanswer
            """
            return self._values.get('multi_value_answer')

        @builtins.property
        def region(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-region
            """
            return self._values.get('region')

        @builtins.property
        def resource_records(self) -> typing.Optional[typing.List[str]]:
            """``CfnRecordSetGroup.RecordSetProperty.ResourceRecords``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-resourcerecords
            """
            return self._values.get('resource_records')

        @builtins.property
        def set_identifier(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.SetIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-setidentifier
            """
            return self._values.get('set_identifier')

        @builtins.property
        def ttl(self) -> typing.Optional[str]:
            """``CfnRecordSetGroup.RecordSetProperty.TTL``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-ttl
            """
            return self._values.get('ttl')

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            """``CfnRecordSetGroup.RecordSetProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-weight
            """
            return self._values.get('weight')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RecordSetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroupProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'hosted_zone_id': 'hostedZoneId', 'hosted_zone_name': 'hostedZoneName', 'record_sets': 'recordSets'})
class CfnRecordSetGroupProps():
    def __init__(self, *, comment: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, record_sets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecordSetGroup.RecordSetProperty"]]]]]=None):
        """Properties for defining a ``AWS::Route53::RecordSetGroup``.

        :param comment: ``AWS::Route53::RecordSetGroup.Comment``.
        :param hosted_zone_id: ``AWS::Route53::RecordSetGroup.HostedZoneId``.
        :param hosted_zone_name: ``AWS::Route53::RecordSetGroup.HostedZoneName``.
        :param record_sets: ``AWS::Route53::RecordSetGroup.RecordSets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if hosted_zone_id is not None: self._values["hosted_zone_id"] = hosted_zone_id
        if hosted_zone_name is not None: self._values["hosted_zone_name"] = hosted_zone_name
        if record_sets is not None: self._values["record_sets"] = record_sets

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSetGroup.Comment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-comment
        """
        return self._values.get('comment')

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSetGroup.HostedZoneId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzoneid
        """
        return self._values.get('hosted_zone_id')

    @builtins.property
    def hosted_zone_name(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSetGroup.HostedZoneName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzonename
        """
        return self._values.get('hosted_zone_name')

    @builtins.property
    def record_sets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecordSetGroup.RecordSetProperty"]]]]]:
        """``AWS::Route53::RecordSetGroup.RecordSets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-recordsets
        """
        return self._values.get('record_sets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRecordSetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'type': 'type', 'alias_target': 'aliasTarget', 'comment': 'comment', 'failover': 'failover', 'geo_location': 'geoLocation', 'health_check_id': 'healthCheckId', 'hosted_zone_id': 'hostedZoneId', 'hosted_zone_name': 'hostedZoneName', 'multi_value_answer': 'multiValueAnswer', 'region': 'region', 'resource_records': 'resourceRecords', 'set_identifier': 'setIdentifier', 'ttl': 'ttl', 'weight': 'weight'})
class CfnRecordSetProps():
    def __init__(self, *, name: str, type: str, alias_target: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSet.AliasTargetProperty"]]]=None, comment: typing.Optional[str]=None, failover: typing.Optional[str]=None, geo_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSet.GeoLocationProperty"]]]=None, health_check_id: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, multi_value_answer: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, region: typing.Optional[str]=None, resource_records: typing.Optional[typing.List[str]]=None, set_identifier: typing.Optional[str]=None, ttl: typing.Optional[str]=None, weight: typing.Optional[jsii.Number]=None):
        """Properties for defining a ``AWS::Route53::RecordSet``.

        :param name: ``AWS::Route53::RecordSet.Name``.
        :param type: ``AWS::Route53::RecordSet.Type``.
        :param alias_target: ``AWS::Route53::RecordSet.AliasTarget``.
        :param comment: ``AWS::Route53::RecordSet.Comment``.
        :param failover: ``AWS::Route53::RecordSet.Failover``.
        :param geo_location: ``AWS::Route53::RecordSet.GeoLocation``.
        :param health_check_id: ``AWS::Route53::RecordSet.HealthCheckId``.
        :param hosted_zone_id: ``AWS::Route53::RecordSet.HostedZoneId``.
        :param hosted_zone_name: ``AWS::Route53::RecordSet.HostedZoneName``.
        :param multi_value_answer: ``AWS::Route53::RecordSet.MultiValueAnswer``.
        :param region: ``AWS::Route53::RecordSet.Region``.
        :param resource_records: ``AWS::Route53::RecordSet.ResourceRecords``.
        :param set_identifier: ``AWS::Route53::RecordSet.SetIdentifier``.
        :param ttl: ``AWS::Route53::RecordSet.TTL``.
        :param weight: ``AWS::Route53::RecordSet.Weight``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html
        """
        self._values = {
            'name': name,
            'type': type,
        }
        if alias_target is not None: self._values["alias_target"] = alias_target
        if comment is not None: self._values["comment"] = comment
        if failover is not None: self._values["failover"] = failover
        if geo_location is not None: self._values["geo_location"] = geo_location
        if health_check_id is not None: self._values["health_check_id"] = health_check_id
        if hosted_zone_id is not None: self._values["hosted_zone_id"] = hosted_zone_id
        if hosted_zone_name is not None: self._values["hosted_zone_name"] = hosted_zone_name
        if multi_value_answer is not None: self._values["multi_value_answer"] = multi_value_answer
        if region is not None: self._values["region"] = region
        if resource_records is not None: self._values["resource_records"] = resource_records
        if set_identifier is not None: self._values["set_identifier"] = set_identifier
        if ttl is not None: self._values["ttl"] = ttl
        if weight is not None: self._values["weight"] = weight

    @builtins.property
    def name(self) -> str:
        """``AWS::Route53::RecordSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-name
        """
        return self._values.get('name')

    @builtins.property
    def type(self) -> str:
        """``AWS::Route53::RecordSet.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-type
        """
        return self._values.get('type')

    @builtins.property
    def alias_target(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSet.AliasTargetProperty"]]]:
        """``AWS::Route53::RecordSet.AliasTarget``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-aliastarget
        """
        return self._values.get('alias_target')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.Comment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-comment
        """
        return self._values.get('comment')

    @builtins.property
    def failover(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.Failover``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-failover
        """
        return self._values.get('failover')

    @builtins.property
    def geo_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRecordSet.GeoLocationProperty"]]]:
        """``AWS::Route53::RecordSet.GeoLocation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-geolocation
        """
        return self._values.get('geo_location')

    @builtins.property
    def health_check_id(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.HealthCheckId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-healthcheckid
        """
        return self._values.get('health_check_id')

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.HostedZoneId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzoneid
        """
        return self._values.get('hosted_zone_id')

    @builtins.property
    def hosted_zone_name(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.HostedZoneName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzonename
        """
        return self._values.get('hosted_zone_name')

    @builtins.property
    def multi_value_answer(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Route53::RecordSet.MultiValueAnswer``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-multivalueanswer
        """
        return self._values.get('multi_value_answer')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-region
        """
        return self._values.get('region')

    @builtins.property
    def resource_records(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Route53::RecordSet.ResourceRecords``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-resourcerecords
        """
        return self._values.get('resource_records')

    @builtins.property
    def set_identifier(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.SetIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-setidentifier
        """
        return self._values.get('set_identifier')

    @builtins.property
    def ttl(self) -> typing.Optional[str]:
        """``AWS::Route53::RecordSet.TTL``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-ttl
        """
        return self._values.get('ttl')

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        """``AWS::Route53::RecordSet.Weight``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-weight
        """
        return self._values.get('weight')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRecordSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CommonHostedZoneProps", jsii_struct_bases=[], name_mapping={'zone_name': 'zoneName', 'comment': 'comment', 'query_logs_log_group_arn': 'queryLogsLogGroupArn'})
class CommonHostedZoneProps():
    def __init__(self, *, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None):
        """
        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        self._values = {
            'zone_name': zone_name,
        }
        if comment is not None: self._values["comment"] = comment
        if query_logs_log_group_arn is not None: self._values["query_logs_log_group_arn"] = query_logs_log_group_arn

    @builtins.property
    def zone_name(self) -> str:
        """The name of the domain.

        For resource record types that include a domain
        name, specify a fully qualified domain name.
        """
        return self._values.get('zone_name')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """Any comments that you want to include about the hosted zone.

        default
        :default: none
        """
        return self._values.get('comment')

    @builtins.property
    def query_logs_log_group_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to.

        default
        :default: disabled
        """
        return self._values.get('query_logs_log_group_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonHostedZoneProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneAttributes", jsii_struct_bases=[], name_mapping={'hosted_zone_id': 'hostedZoneId', 'zone_name': 'zoneName'})
class HostedZoneAttributes():
    def __init__(self, *, hosted_zone_id: str, zone_name: str):
        """Reference to a hosted zone.

        :param hosted_zone_id: Identifier of the hosted zone.
        :param zone_name: Name of the hosted zone.
        """
        self._values = {
            'hosted_zone_id': hosted_zone_id,
            'zone_name': zone_name,
        }

    @builtins.property
    def hosted_zone_id(self) -> str:
        """Identifier of the hosted zone."""
        return self._values.get('hosted_zone_id')

    @builtins.property
    def zone_name(self) -> str:
        """Name of the hosted zone."""
        return self._values.get('zone_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HostedZoneAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneProps", jsii_struct_bases=[CommonHostedZoneProps], name_mapping={'zone_name': 'zoneName', 'comment': 'comment', 'query_logs_log_group_arn': 'queryLogsLogGroupArn', 'vpcs': 'vpcs'})
class HostedZoneProps(CommonHostedZoneProps):
    def __init__(self, *, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None, vpcs: typing.Optional[typing.List[aws_cdk.aws_ec2.IVpc]]=None):
        """Properties of a new hosted zone.

        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        :param vpcs: A VPC that you want to associate with this hosted zone. When you specify this property, a private hosted zone will be created. You can associate additional VPCs to this private zone using ``addVpc(vpc)``. Default: public (no VPCs associated)
        """
        self._values = {
            'zone_name': zone_name,
        }
        if comment is not None: self._values["comment"] = comment
        if query_logs_log_group_arn is not None: self._values["query_logs_log_group_arn"] = query_logs_log_group_arn
        if vpcs is not None: self._values["vpcs"] = vpcs

    @builtins.property
    def zone_name(self) -> str:
        """The name of the domain.

        For resource record types that include a domain
        name, specify a fully qualified domain name.
        """
        return self._values.get('zone_name')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """Any comments that you want to include about the hosted zone.

        default
        :default: none
        """
        return self._values.get('comment')

    @builtins.property
    def query_logs_log_group_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to.

        default
        :default: disabled
        """
        return self._values.get('query_logs_log_group_arn')

    @builtins.property
    def vpcs(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.IVpc]]:
        """A VPC that you want to associate with this hosted zone.

        When you specify
        this property, a private hosted zone will be created.

        You can associate additional VPCs to this private zone using ``addVpc(vpc)``.

        default
        :default: public (no VPCs associated)
        """
        return self._values.get('vpcs')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HostedZoneProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneProviderProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'private_zone': 'privateZone', 'vpc_id': 'vpcId'})
class HostedZoneProviderProps():
    def __init__(self, *, domain_name: str, private_zone: typing.Optional[bool]=None, vpc_id: typing.Optional[str]=None):
        """Zone properties for looking up the Hosted Zone.

        :param domain_name: The zone domain e.g. example.com.
        :param private_zone: Is this a private zone.
        :param vpc_id: If this is a private zone which VPC is assocaitated.
        """
        self._values = {
            'domain_name': domain_name,
        }
        if private_zone is not None: self._values["private_zone"] = private_zone
        if vpc_id is not None: self._values["vpc_id"] = vpc_id

    @builtins.property
    def domain_name(self) -> str:
        """The zone domain e.g. example.com."""
        return self._values.get('domain_name')

    @builtins.property
    def private_zone(self) -> typing.Optional[bool]:
        """Is this a private zone."""
        return self._values.get('private_zone')

    @builtins.property
    def vpc_id(self) -> typing.Optional[str]:
        """If this is a private zone which VPC is assocaitated."""
        return self._values.get('vpc_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HostedZoneProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IAliasRecordTarget")
class IAliasRecordTarget(jsii.compat.Protocol):
    """Classes that are valid alias record targets, like CloudFront distributions and load balancers, should implement this interface."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAliasRecordTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(self, record: "IRecordSet") -> "AliasRecordTargetConfig":
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param record: -
        """
        ...


class _IAliasRecordTargetProxy():
    """Classes that are valid alias record targets, like CloudFront distributions and load balancers, should implement this interface."""
    __jsii_type__ = "@aws-cdk/aws-route53.IAliasRecordTarget"
    @jsii.member(jsii_name="bind")
    def bind(self, record: "IRecordSet") -> "AliasRecordTargetConfig":
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param record: -
        """
        return jsii.invoke(self, "bind", [record])


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IHostedZone")
class IHostedZone(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Imported or created hosted zone."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHostedZoneProxy

    @builtins.property
    @jsii.member(jsii_name="hostedZoneArn")
    def hosted_zone_arn(self) -> str:
        """ARN of this hosted zone, such as arn:${Partition}:route53:::hostedzone/${Id}.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """ID of this hosted zone, such as "Z23ABC4XYZL05B".

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        """FQDN of this hosted zone."""
        ...

    @builtins.property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        """Returns the set of name servers for the specific hosted zone. For example: ns1.example.com.

        This attribute will be undefined for private hosted zones or hosted zones imported from another stack.

        attribute:
        :attribute:: true
        """
        ...


class _IHostedZoneProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Imported or created hosted zone."""
    __jsii_type__ = "@aws-cdk/aws-route53.IHostedZone"
    @builtins.property
    @jsii.member(jsii_name="hostedZoneArn")
    def hosted_zone_arn(self) -> str:
        """ARN of this hosted zone, such as arn:${Partition}:route53:::hostedzone/${Id}.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "hostedZoneArn")

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """ID of this hosted zone, such as "Z23ABC4XYZL05B".

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "hostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        """FQDN of this hosted zone."""
        return jsii.get(self, "zoneName")

    @builtins.property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        """Returns the set of name servers for the specific hosted zone. For example: ns1.example.com.

        This attribute will be undefined for private hosted zones or hosted zones imported from another stack.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "hostedZoneNameServers")


@jsii.implements(IHostedZone)
class HostedZone(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.HostedZone"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpcs: typing.Optional[typing.List[aws_cdk.aws_ec2.IVpc]]=None, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param vpcs: A VPC that you want to associate with this hosted zone. When you specify this property, a private hosted zone will be created. You can associate additional VPCs to this private zone using ``addVpc(vpc)``. Default: public (no VPCs associated)
        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        props = HostedZoneProps(vpcs=vpcs, zone_name=zone_name, comment=comment, query_logs_log_group_arn=query_logs_log_group_arn)

        jsii.create(HostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="fromHostedZoneAttributes")
    @builtins.classmethod
    def from_hosted_zone_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, hosted_zone_id: str, zone_name: str) -> "IHostedZone":
        """Imports a hosted zone from another stack.

        :param scope: -
        :param id: -
        :param hosted_zone_id: Identifier of the hosted zone.
        :param zone_name: Name of the hosted zone.
        """
        attrs = HostedZoneAttributes(hosted_zone_id=hosted_zone_id, zone_name=zone_name)

        return jsii.sinvoke(cls, "fromHostedZoneAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromHostedZoneId")
    @builtins.classmethod
    def from_hosted_zone_id(cls, scope: aws_cdk.core.Construct, id: str, hosted_zone_id: str) -> "IHostedZone":
        """
        :param scope: -
        :param id: -
        :param hosted_zone_id: -
        """
        return jsii.sinvoke(cls, "fromHostedZoneId", [scope, id, hosted_zone_id])

    @jsii.member(jsii_name="fromLookup")
    @builtins.classmethod
    def from_lookup(cls, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, private_zone: typing.Optional[bool]=None, vpc_id: typing.Optional[str]=None) -> "IHostedZone":
        """Lookup a hosted zone in the current account/region based on query parameters.

        :param scope: -
        :param id: -
        :param domain_name: The zone domain e.g. example.com.
        :param private_zone: Is this a private zone.
        :param vpc_id: If this is a private zone which VPC is assocaitated.
        """
        query = HostedZoneProviderProps(domain_name=domain_name, private_zone=private_zone, vpc_id=vpc_id)

        return jsii.sinvoke(cls, "fromLookup", [scope, id, query])

    @jsii.member(jsii_name="addVpc")
    def add_vpc(self, vpc: aws_cdk.aws_ec2.IVpc) -> None:
        """Add another VPC to this private hosted zone.

        :param vpc: the other VPC to add.
        """
        return jsii.invoke(self, "addVpc", [vpc])

    @builtins.property
    @jsii.member(jsii_name="hostedZoneArn")
    def hosted_zone_arn(self) -> str:
        """ARN of this hosted zone, such as arn:${Partition}:route53:::hostedzone/${Id}."""
        return jsii.get(self, "hostedZoneArn")

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """ID of this hosted zone, such as "Z23ABC4XYZL05B"."""
        return jsii.get(self, "hostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="vpcs")
    def _vpcs(self) -> typing.List["CfnHostedZone.VPCProperty"]:
        """VPCs to which this hosted zone will be added."""
        return jsii.get(self, "vpcs")

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        """FQDN of this hosted zone."""
        return jsii.get(self, "zoneName")

    @builtins.property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        """Returns the set of name servers for the specific hosted zone. For example: ns1.example.com.

        This attribute will be undefined for private hosted zones or hosted zones imported from another stack.
        """
        return jsii.get(self, "hostedZoneNameServers")


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IPrivateHostedZone")
class IPrivateHostedZone(IHostedZone, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPrivateHostedZoneProxy

    pass

class _IPrivateHostedZoneProxy(jsii.proxy_for(IHostedZone)):
    __jsii_type__ = "@aws-cdk/aws-route53.IPrivateHostedZone"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-route53.IPublicHostedZone")
class IPublicHostedZone(IHostedZone, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPublicHostedZoneProxy

    pass

class _IPublicHostedZoneProxy(jsii.proxy_for(IHostedZone)):
    __jsii_type__ = "@aws-cdk/aws-route53.IPublicHostedZone"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-route53.IRecordSet")
class IRecordSet(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A record set."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRecordSetProxy

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the record."""
        ...


class _IRecordSetProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A record set."""
    __jsii_type__ = "@aws-cdk/aws-route53.IRecordSet"
    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the record."""
        return jsii.get(self, "domainName")


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.MxRecordValue", jsii_struct_bases=[], name_mapping={'host_name': 'hostName', 'priority': 'priority'})
class MxRecordValue():
    def __init__(self, *, host_name: str, priority: jsii.Number):
        """Properties for a MX record value.

        :param host_name: The mail server host name.
        :param priority: The priority.
        """
        self._values = {
            'host_name': host_name,
            'priority': priority,
        }

    @builtins.property
    def host_name(self) -> str:
        """The mail server host name."""
        return self._values.get('host_name')

    @builtins.property
    def priority(self) -> jsii.Number:
        """The priority."""
        return self._values.get('priority')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MxRecordValue(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPrivateHostedZone)
class PrivateHostedZone(HostedZone, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.PrivateHostedZone"):
    """Create a Route53 private hosted zone for use in one or more VPCs.

    Note that ``enableDnsHostnames`` and ``enableDnsSupport`` must have been enabled
    for the VPC you're configuring for private hosted zones.

    resource:
    :resource:: AWS::Route53::HostedZone
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpc, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: A VPC that you want to associate with this hosted zone. Private hosted zones must be associated with at least one VPC. You can associated additional VPCs using ``addVpc(vpc)``.
        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        props = PrivateHostedZoneProps(vpc=vpc, zone_name=zone_name, comment=comment, query_logs_log_group_arn=query_logs_log_group_arn)

        jsii.create(PrivateHostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="fromPrivateHostedZoneId")
    @builtins.classmethod
    def from_private_hosted_zone_id(cls, scope: aws_cdk.core.Construct, id: str, private_hosted_zone_id: str) -> "IPrivateHostedZone":
        """
        :param scope: -
        :param id: -
        :param private_hosted_zone_id: -
        """
        return jsii.sinvoke(cls, "fromPrivateHostedZoneId", [scope, id, private_hosted_zone_id])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.PrivateHostedZoneProps", jsii_struct_bases=[CommonHostedZoneProps], name_mapping={'zone_name': 'zoneName', 'comment': 'comment', 'query_logs_log_group_arn': 'queryLogsLogGroupArn', 'vpc': 'vpc'})
class PrivateHostedZoneProps(CommonHostedZoneProps):
    def __init__(self, *, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None, vpc: aws_cdk.aws_ec2.IVpc):
        """
        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        :param vpc: A VPC that you want to associate with this hosted zone. Private hosted zones must be associated with at least one VPC. You can associated additional VPCs using ``addVpc(vpc)``.
        """
        self._values = {
            'zone_name': zone_name,
            'vpc': vpc,
        }
        if comment is not None: self._values["comment"] = comment
        if query_logs_log_group_arn is not None: self._values["query_logs_log_group_arn"] = query_logs_log_group_arn

    @builtins.property
    def zone_name(self) -> str:
        """The name of the domain.

        For resource record types that include a domain
        name, specify a fully qualified domain name.
        """
        return self._values.get('zone_name')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """Any comments that you want to include about the hosted zone.

        default
        :default: none
        """
        return self._values.get('comment')

    @builtins.property
    def query_logs_log_group_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to.

        default
        :default: disabled
        """
        return self._values.get('query_logs_log_group_arn')

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """A VPC that you want to associate with this hosted zone.

        Private hosted zones must be associated with at least one VPC. You can
        associated additional VPCs using ``addVpc(vpc)``.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PrivateHostedZoneProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPublicHostedZone)
class PublicHostedZone(HostedZone, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.PublicHostedZone"):
    """Create a Route53 public hosted zone.

    resource:
    :resource:: AWS::Route53::HostedZone
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, caa_amazon: typing.Optional[bool]=None, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param caa_amazon: Whether to create a CAA record to restrict certificate authorities allowed to issue certificates for this domain to Amazon only. Default: false
        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        props = PublicHostedZoneProps(caa_amazon=caa_amazon, zone_name=zone_name, comment=comment, query_logs_log_group_arn=query_logs_log_group_arn)

        jsii.create(PublicHostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="fromPublicHostedZoneId")
    @builtins.classmethod
    def from_public_hosted_zone_id(cls, scope: aws_cdk.core.Construct, id: str, public_hosted_zone_id: str) -> "IPublicHostedZone":
        """
        :param scope: -
        :param id: -
        :param public_hosted_zone_id: -
        """
        return jsii.sinvoke(cls, "fromPublicHostedZoneId", [scope, id, public_hosted_zone_id])

    @jsii.member(jsii_name="addDelegation")
    def add_delegation(self, delegate: "IPublicHostedZone", *, comment: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Adds a delegation from this zone to a designated zone.

        :param delegate: the zone being delegated to.
        :param comment: A comment to add on the DNS record created to incorporate the delegation. Default: none
        :param ttl: The TTL (Time To Live) of the DNS delegation record in DNS caches. Default: 172800
        """
        opts = ZoneDelegationOptions(comment=comment, ttl=ttl)

        return jsii.invoke(self, "addDelegation", [delegate, opts])

    @jsii.member(jsii_name="addVpc")
    def add_vpc(self, _vpc: aws_cdk.aws_ec2.IVpc) -> None:
        """Add another VPC to this private hosted zone.

        :param _vpc: -
        """
        return jsii.invoke(self, "addVpc", [_vpc])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.PublicHostedZoneProps", jsii_struct_bases=[CommonHostedZoneProps], name_mapping={'zone_name': 'zoneName', 'comment': 'comment', 'query_logs_log_group_arn': 'queryLogsLogGroupArn', 'caa_amazon': 'caaAmazon'})
class PublicHostedZoneProps(CommonHostedZoneProps):
    def __init__(self, *, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None, caa_amazon: typing.Optional[bool]=None):
        """Construction properties for a PublicHostedZone.

        :param zone_name: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
        :param comment: Any comments that you want to include about the hosted zone. Default: none
        :param query_logs_log_group_arn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        :param caa_amazon: Whether to create a CAA record to restrict certificate authorities allowed to issue certificates for this domain to Amazon only. Default: false
        """
        self._values = {
            'zone_name': zone_name,
        }
        if comment is not None: self._values["comment"] = comment
        if query_logs_log_group_arn is not None: self._values["query_logs_log_group_arn"] = query_logs_log_group_arn
        if caa_amazon is not None: self._values["caa_amazon"] = caa_amazon

    @builtins.property
    def zone_name(self) -> str:
        """The name of the domain.

        For resource record types that include a domain
        name, specify a fully qualified domain name.
        """
        return self._values.get('zone_name')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """Any comments that you want to include about the hosted zone.

        default
        :default: none
        """
        return self._values.get('comment')

    @builtins.property
    def query_logs_log_group_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to.

        default
        :default: disabled
        """
        return self._values.get('query_logs_log_group_arn')

    @builtins.property
    def caa_amazon(self) -> typing.Optional[bool]:
        """Whether to create a CAA record to restrict certificate authorities allowed to issue certificates for this domain to Amazon only.

        default
        :default: false
        """
        return self._values.get('caa_amazon')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PublicHostedZoneProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IRecordSet)
class RecordSet(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.RecordSet"):
    """A record set."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, record_type: "RecordType", target: "RecordTarget", zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param record_type: The record type.
        :param target: The target for this record, either ``RecordTarget.fromValues()`` or ``RecordTarget.fromAlias()``.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = RecordSetProps(record_type=record_type, target=target, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(RecordSet, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the record."""
        return jsii.get(self, "domainName")


class ARecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.ARecord"):
    """A DNS A record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, target: "RecordTarget", zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param target: The target.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = ARecordProps(target=target, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(ARecord, self, [scope, id, props])


class AaaaRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.AaaaRecord"):
    """A DNS AAAA record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, target: "RecordTarget", zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param target: The target.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = AaaaRecordProps(target=target, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(AaaaRecord, self, [scope, id, props])


class CaaRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CaaRecord"):
    """A DNS CAA record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, values: typing.List["CaaRecordValue"], zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param values: The values.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = CaaRecordProps(values=values, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(CaaRecord, self, [scope, id, props])


class CaaAmazonRecord(CaaRecord, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CaaAmazonRecord"):
    """A DNS Amazon CAA record.

    A CAA record to restrict certificate authorities allowed
    to issue certificates for a domain to Amazon only.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = CaaAmazonRecordProps(zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(CaaAmazonRecord, self, [scope, id, props])


class CnameRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CnameRecord"):
    """A DNS CNAME record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param domain_name: The domain name.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = CnameRecordProps(domain_name=domain_name, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(CnameRecord, self, [scope, id, props])


class MxRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.MxRecord"):
    """A DNS MX record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, values: typing.List["MxRecordValue"], zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param values: The values.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = MxRecordProps(values=values, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(MxRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.RecordSetOptions", jsii_struct_bases=[], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl'})
class RecordSetOptions():
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None):
        """Options for a RecordSet.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        self._values = {
            'zone': zone,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RecordSetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ARecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'target': 'target'})
class ARecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, target: "RecordTarget"):
        """Construction properties for a ARecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param target: The target.
        """
        self._values = {
            'zone': zone,
            'target': target,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def target(self) -> "RecordTarget":
        """The target."""
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ARecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.AaaaRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'target': 'target'})
class AaaaRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, target: "RecordTarget"):
        """Construction properties for a AaaaRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param target: The target.
        """
        self._values = {
            'zone': zone,
            'target': target,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def target(self) -> "RecordTarget":
        """The target."""
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AaaaRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CaaAmazonRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl'})
class CaaAmazonRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None):
        """Construction properties for a CaaAmazonRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        self._values = {
            'zone': zone,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CaaAmazonRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CaaRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'values': 'values'})
class CaaRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, values: typing.List["CaaRecordValue"]):
        """Construction properties for a CaaRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param values: The values.
        """
        self._values = {
            'zone': zone,
            'values': values,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def values(self) -> typing.List["CaaRecordValue"]:
        """The values."""
        return self._values.get('values')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CaaRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CnameRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'domain_name': 'domainName'})
class CnameRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, domain_name: str):
        """Construction properties for a CnameRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param domain_name: The domain name.
        """
        self._values = {
            'zone': zone,
            'domain_name': domain_name,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def domain_name(self) -> str:
        """The domain name."""
        return self._values.get('domain_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CnameRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.MxRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'values': 'values'})
class MxRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, values: typing.List["MxRecordValue"]):
        """Construction properties for a MxRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param values: The values.
        """
        self._values = {
            'zone': zone,
            'values': values,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def values(self) -> typing.List["MxRecordValue"]:
        """The values."""
        return self._values.get('values')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MxRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.RecordSetProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'record_type': 'recordType', 'target': 'target'})
class RecordSetProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, record_type: "RecordType", target: "RecordTarget"):
        """Construction properties for a RecordSet.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param record_type: The record type.
        :param target: The target for this record, either ``RecordTarget.fromValues()`` or ``RecordTarget.fromAlias()``.
        """
        self._values = {
            'zone': zone,
            'record_type': record_type,
            'target': target,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def record_type(self) -> "RecordType":
        """The record type."""
        return self._values.get('record_type')

    @builtins.property
    def target(self) -> "RecordTarget":
        """The target for this record, either ``RecordTarget.fromValues()`` or ``RecordTarget.fromAlias()``."""
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RecordSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class RecordTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.RecordTarget"):
    """Type union for a record that accepts multiple types of target."""
    def __init__(self, values: typing.Optional[typing.List[str]]=None, alias_target: typing.Optional["IAliasRecordTarget"]=None) -> None:
        """
        :param values: -
        :param alias_target: -
        """
        jsii.create(RecordTarget, self, [values, alias_target])

    @jsii.member(jsii_name="fromAlias")
    @builtins.classmethod
    def from_alias(cls, alias_target: "IAliasRecordTarget") -> "RecordTarget":
        """Use an alias as target.

        :param alias_target: -
        """
        return jsii.sinvoke(cls, "fromAlias", [alias_target])

    @jsii.member(jsii_name="fromIpAddresses")
    @builtins.classmethod
    def from_ip_addresses(cls, *ip_addresses: str) -> "RecordTarget":
        """Use ip adresses as target.

        :param ip_addresses: -
        """
        return jsii.sinvoke(cls, "fromIpAddresses", [*ip_addresses])

    @jsii.member(jsii_name="fromValues")
    @builtins.classmethod
    def from_values(cls, *values: str) -> "RecordTarget":
        """Use string values as target.

        :param values: -
        """
        return jsii.sinvoke(cls, "fromValues", [*values])

    @builtins.property
    @jsii.member(jsii_name="aliasTarget")
    def alias_target(self) -> typing.Optional["IAliasRecordTarget"]:
        return jsii.get(self, "aliasTarget")

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "values")


class AddressRecordTarget(RecordTarget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.AddressRecordTarget"):
    """
    deprecated
    :deprecated: Use RecordTarget

    stability
    :stability: deprecated
    """
    def __init__(self, values: typing.Optional[typing.List[str]]=None, alias_target: typing.Optional["IAliasRecordTarget"]=None) -> None:
        """
        :param values: -
        :param alias_target: -
        """
        jsii.create(AddressRecordTarget, self, [values, alias_target])


@jsii.enum(jsii_type="@aws-cdk/aws-route53.RecordType")
class RecordType(enum.Enum):
    """The record type."""
    A = "A"
    AAAA = "AAAA"
    CAA = "CAA"
    CNAME = "CNAME"
    MX = "MX"
    NAPTR = "NAPTR"
    NS = "NS"
    PTR = "PTR"
    SOA = "SOA"
    SPF = "SPF"
    SRV = "SRV"
    TXT = "TXT"

class SrvRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.SrvRecord"):
    """A DNS SRV record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, values: typing.List["SrvRecordValue"], zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param values: The values.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = SrvRecordProps(values=values, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(SrvRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.SrvRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'values': 'values'})
class SrvRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, values: typing.List["SrvRecordValue"]):
        """Construction properties for a SrvRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param values: The values.
        """
        self._values = {
            'zone': zone,
            'values': values,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def values(self) -> typing.List["SrvRecordValue"]:
        """The values."""
        return self._values.get('values')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SrvRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.SrvRecordValue", jsii_struct_bases=[], name_mapping={'host_name': 'hostName', 'port': 'port', 'priority': 'priority', 'weight': 'weight'})
class SrvRecordValue():
    def __init__(self, *, host_name: str, port: jsii.Number, priority: jsii.Number, weight: jsii.Number):
        """Properties for a SRV record value.

        :param host_name: The server host name.
        :param port: The port.
        :param priority: The priority.
        :param weight: The weight.
        """
        self._values = {
            'host_name': host_name,
            'port': port,
            'priority': priority,
            'weight': weight,
        }

    @builtins.property
    def host_name(self) -> str:
        """The server host name."""
        return self._values.get('host_name')

    @builtins.property
    def port(self) -> jsii.Number:
        """The port."""
        return self._values.get('port')

    @builtins.property
    def priority(self) -> jsii.Number:
        """The priority."""
        return self._values.get('priority')

    @builtins.property
    def weight(self) -> jsii.Number:
        """The weight."""
        return self._values.get('weight')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SrvRecordValue(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TxtRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.TxtRecord"):
    """A DNS TXT record.

    resource:
    :resource:: AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, values: typing.List[str], zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param values: The text values.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = TxtRecordProps(values=values, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(TxtRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.TxtRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'values': 'values'})
class TxtRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, values: typing.List[str]):
        """Construction properties for a TxtRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param values: The text values.
        """
        self._values = {
            'zone': zone,
            'values': values,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def values(self) -> typing.List[str]:
        """The text values."""
        return self._values.get('values')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TxtRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ZoneDelegationOptions", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'ttl': 'ttl'})
class ZoneDelegationOptions():
    def __init__(self, *, comment: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None):
        """Options available when creating a delegation relationship from one PublicHostedZone to another.

        :param comment: A comment to add on the DNS record created to incorporate the delegation. Default: none
        :param ttl: The TTL (Time To Live) of the DNS delegation record in DNS caches. Default: 172800
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the DNS record created to incorporate the delegation.

        default
        :default: none
        """
        return self._values.get('comment')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The TTL (Time To Live) of the DNS delegation record in DNS caches.

        default
        :default: 172800
        """
        return self._values.get('ttl')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ZoneDelegationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ZoneDelegationRecord(RecordSet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.ZoneDelegationRecord"):
    """A record to delegate further lookups to a different set of name servers."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name_servers: typing.List[str], zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param name_servers: The name servers to report in the delegation records.
        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        """
        props = ZoneDelegationRecordProps(name_servers=name_servers, zone=zone, comment=comment, record_name=record_name, ttl=ttl)

        jsii.create(ZoneDelegationRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ZoneDelegationRecordProps", jsii_struct_bases=[RecordSetOptions], name_mapping={'zone': 'zone', 'comment': 'comment', 'record_name': 'recordName', 'ttl': 'ttl', 'name_servers': 'nameServers'})
class ZoneDelegationRecordProps(RecordSetOptions):
    def __init__(self, *, zone: "IHostedZone", comment: typing.Optional[str]=None, record_name: typing.Optional[str]=None, ttl: typing.Optional[aws_cdk.core.Duration]=None, name_servers: typing.List[str]):
        """Construction properties for a ZoneDelegationRecord.

        :param zone: The hosted zone in which to define the new record.
        :param comment: A comment to add on the record. Default: no comment
        :param record_name: The domain name for this record. Default: zone root
        :param ttl: The resource record cache time to live (TTL). Default: Duration.minutes(30)
        :param name_servers: The name servers to report in the delegation records.
        """
        self._values = {
            'zone': zone,
            'name_servers': name_servers,
        }
        if comment is not None: self._values["comment"] = comment
        if record_name is not None: self._values["record_name"] = record_name
        if ttl is not None: self._values["ttl"] = ttl

    @builtins.property
    def zone(self) -> "IHostedZone":
        """The hosted zone in which to define the new record."""
        return self._values.get('zone')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment to add on the record.

        default
        :default: no comment
        """
        return self._values.get('comment')

    @builtins.property
    def record_name(self) -> typing.Optional[str]:
        """The domain name for this record.

        default
        :default: zone root
        """
        return self._values.get('record_name')

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The resource record cache time to live (TTL).

        default
        :default: Duration.minutes(30)
        """
        return self._values.get('ttl')

    @builtins.property
    def name_servers(self) -> typing.List[str]:
        """The name servers to report in the delegation records."""
        return self._values.get('name_servers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ZoneDelegationRecordProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["ARecord", "ARecordProps", "AaaaRecord", "AaaaRecordProps", "AddressRecordTarget", "AliasRecordTargetConfig", "CaaAmazonRecord", "CaaAmazonRecordProps", "CaaRecord", "CaaRecordProps", "CaaRecordValue", "CaaTag", "CfnHealthCheck", "CfnHealthCheckProps", "CfnHostedZone", "CfnHostedZoneProps", "CfnRecordSet", "CfnRecordSetGroup", "CfnRecordSetGroupProps", "CfnRecordSetProps", "CnameRecord", "CnameRecordProps", "CommonHostedZoneProps", "HostedZone", "HostedZoneAttributes", "HostedZoneProps", "HostedZoneProviderProps", "IAliasRecordTarget", "IHostedZone", "IPrivateHostedZone", "IPublicHostedZone", "IRecordSet", "MxRecord", "MxRecordProps", "MxRecordValue", "PrivateHostedZone", "PrivateHostedZoneProps", "PublicHostedZone", "PublicHostedZoneProps", "RecordSet", "RecordSetOptions", "RecordSetProps", "RecordTarget", "RecordType", "SrvRecord", "SrvRecordProps", "SrvRecordValue", "TxtRecord", "TxtRecordProps", "ZoneDelegationOptions", "ZoneDelegationRecord", "ZoneDelegationRecordProps", "__jsii_assembly__"]

publication.publish()
