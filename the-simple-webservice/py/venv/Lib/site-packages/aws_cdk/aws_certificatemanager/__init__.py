"""
## Amazon Certificate Manager Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This package provides Constructs for provisioning and referencing
certificates which can be used in CloudFront and ELB.

The following requests a certificate for a given domain:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cert = certmgr.Certificate(self, "Certificate",
    domain_name="example.com"
)
```

After requesting a certificate, you will need to prove that you own the
domain in question before the certificate will be granted. The CloudFormation
deployment will wait until this verification process has been completed.

Because of this wait time, it's better to provision your certificates
either in a separate stack from your main service, or provision them
manually and import them into your CDK application.

The CDK also provides a custom resource which can be used for automatic
validation if the DNS records for the domain are managed through Route53 (see
below).

### Email validation

Email-validated certificates (the default) are validated by receiving an
email on one of a number of predefined domains and following the instructions
in the email.

See [Validate with Email](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html)
in the Amazon Certificate Manager User Guide.

### DNS validation

DNS-validated certificates are validated by configuring appropriate DNS
records for your domain.

See [Validate with DNS](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html)
in the Amazon Certificate Manager User Guide.

### Automatic DNS-validated certificates using Route53

The `DnsValidatedCertificateRequest` class provides a Custom Resource by which
you can request a TLS certificate from AWS Certificate Manager that is
automatically validated using a cryptographically secure DNS record. For this to
work, there must be a Route 53 public zone that is responsible for serving
records under the Domain Name of the requested certificate. For example, if you
request a certificate for `www.example.com`, there must be a Route 53 public
zone `example.com` that provides authoritative records for the domain.

Example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
hosted_zone = route53.HostedZone.from_lookup(self, "HostedZone",
    domain_name="example.com",
    private_zone=False
)

certificate = certmgr.DnsValidatedCertificate(self, "TestCertificate",
    domain_name="test.example.com",
    hosted_zone=hosted_zone
)
```

### Importing

If you want to import an existing certificate, you can do so from its ARN:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
arn = "arn:aws:..."
certificate = Certificate.from_certificate_arn(self, "Certificate", arn)
```

### Sharing between Stacks

To share the certificate between stacks in the same CDK application, simply
pass the `Certificate` object between the stacks.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_route53
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-certificatemanager", "1.23.0", __name__, "aws-certificatemanager@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CertificateProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'subject_alternative_names': 'subjectAlternativeNames', 'validation_domains': 'validationDomains', 'validation_method': 'validationMethod'})
class CertificateProps():
    def __init__(self, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str,str]]=None, validation_method: typing.Optional["ValidationMethod"]=None):
        """Properties for your certificate.

        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        """
        self._values = {
            'domain_name': domain_name,
        }
        if subject_alternative_names is not None: self._values["subject_alternative_names"] = subject_alternative_names
        if validation_domains is not None: self._values["validation_domains"] = validation_domains
        if validation_method is not None: self._values["validation_method"] = validation_method

    @builtins.property
    def domain_name(self) -> str:
        """Fully-qualified domain name to request a certificate for.

        May contain wildcards, such as ``*.domain.com``.
        """
        return self._values.get('domain_name')

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """Alternative domain names on your certificate.

        Use this to register alternative domain names that represent the same site.

        default
        :default: - No additional FQDNs will be included as alternative domain names.
        """
        return self._values.get('subject_alternative_names')

    @builtins.property
    def validation_domains(self) -> typing.Optional[typing.Mapping[str,str]]:
        """What validation domain to use for every requested domain.

        Has to be a superdomain of the requested domain.

        default
        :default: - Apex domain is used for every domain that's not overridden.
        """
        return self._values.get('validation_domains')

    @builtins.property
    def validation_method(self) -> typing.Optional["ValidationMethod"]:
        """Validation method used to assert domain ownership.

        default
        :default: ValidationMethod.EMAIL
        """
        return self._values.get('validation_method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificate(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificate"):
    """A CloudFormation ``AWS::CertificateManager::Certificate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
    cloudformationResource:
    :cloudformationResource:: AWS::CertificateManager::Certificate
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, domain_validation_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["DomainValidationOptionProperty", aws_cdk.core.IResolvable]]]]]=None, subject_alternative_names: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, validation_method: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CertificateManager::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::CertificateManager::Certificate.DomainName``.
        :param domain_validation_options: ``AWS::CertificateManager::Certificate.DomainValidationOptions``.
        :param subject_alternative_names: ``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.
        :param tags: ``AWS::CertificateManager::Certificate.Tags``.
        :param validation_method: ``AWS::CertificateManager::Certificate.ValidationMethod``.
        """
        props = CfnCertificateProps(domain_name=domain_name, domain_validation_options=domain_validation_options, subject_alternative_names=subject_alternative_names, tags=tags, validation_method=validation_method)

        jsii.create(CfnCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CertificateManager::Certificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::CertificateManager::Certificate.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str):
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="domainValidationOptions")
    def domain_validation_options(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["DomainValidationOptionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::CertificateManager::Certificate.DomainValidationOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        """
        return jsii.get(self, "domainValidationOptions")

    @domain_validation_options.setter
    def domain_validation_options(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["DomainValidationOptionProperty", aws_cdk.core.IResolvable]]]]]):
        jsii.set(self, "domainValidationOptions", value)

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        """
        return jsii.get(self, "subjectAlternativeNames")

    @subject_alternative_names.setter
    def subject_alternative_names(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "subjectAlternativeNames", value)

    @builtins.property
    @jsii.member(jsii_name="validationMethod")
    def validation_method(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.ValidationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        """
        return jsii.get(self, "validationMethod")

    @validation_method.setter
    def validation_method(self, value: typing.Optional[str]):
        jsii.set(self, "validationMethod", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificate.DomainValidationOptionProperty", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'validation_domain': 'validationDomain'})
    class DomainValidationOptionProperty():
        def __init__(self, *, domain_name: str, validation_domain: str):
            """
            :param domain_name: ``CfnCertificate.DomainValidationOptionProperty.DomainName``.
            :param validation_domain: ``CfnCertificate.DomainValidationOptionProperty.ValidationDomain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html
            """
            self._values = {
                'domain_name': domain_name,
                'validation_domain': validation_domain,
            }

        @builtins.property
        def domain_name(self) -> str:
            """``CfnCertificate.DomainValidationOptionProperty.DomainName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoptions-domainname
            """
            return self._values.get('domain_name')

        @builtins.property
        def validation_domain(self) -> str:
            """``CfnCertificate.DomainValidationOptionProperty.ValidationDomain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-validationdomain
            """
            return self._values.get('validation_domain')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DomainValidationOptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificateProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'domain_validation_options': 'domainValidationOptions', 'subject_alternative_names': 'subjectAlternativeNames', 'tags': 'tags', 'validation_method': 'validationMethod'})
class CfnCertificateProps():
    def __init__(self, *, domain_name: str, domain_validation_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnCertificate.DomainValidationOptionProperty", aws_cdk.core.IResolvable]]]]]=None, subject_alternative_names: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, validation_method: typing.Optional[str]=None):
        """Properties for defining a ``AWS::CertificateManager::Certificate``.

        :param domain_name: ``AWS::CertificateManager::Certificate.DomainName``.
        :param domain_validation_options: ``AWS::CertificateManager::Certificate.DomainValidationOptions``.
        :param subject_alternative_names: ``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.
        :param tags: ``AWS::CertificateManager::Certificate.Tags``.
        :param validation_method: ``AWS::CertificateManager::Certificate.ValidationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
        """
        self._values = {
            'domain_name': domain_name,
        }
        if domain_validation_options is not None: self._values["domain_validation_options"] = domain_validation_options
        if subject_alternative_names is not None: self._values["subject_alternative_names"] = subject_alternative_names
        if tags is not None: self._values["tags"] = tags
        if validation_method is not None: self._values["validation_method"] = validation_method

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::CertificateManager::Certificate.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_validation_options(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnCertificate.DomainValidationOptionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::CertificateManager::Certificate.DomainValidationOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        """
        return self._values.get('domain_validation_options')

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CertificateManager::Certificate.SubjectAlternativeNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        """
        return self._values.get('subject_alternative_names')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CertificateManager::Certificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        """
        return self._values.get('tags')

    @builtins.property
    def validation_method(self) -> typing.Optional[str]:
        """``AWS::CertificateManager::Certificate.ValidationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        """
        return self._values.get('validation_method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.DnsValidatedCertificateProps", jsii_struct_bases=[CertificateProps], name_mapping={'domain_name': 'domainName', 'subject_alternative_names': 'subjectAlternativeNames', 'validation_domains': 'validationDomains', 'validation_method': 'validationMethod', 'hosted_zone': 'hostedZone', 'custom_resource_role': 'customResourceRole', 'region': 'region'})
class DnsValidatedCertificateProps(CertificateProps):
    def __init__(self, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str,str]]=None, validation_method: typing.Optional["ValidationMethod"]=None, hosted_zone: aws_cdk.aws_route53.IHostedZone, custom_resource_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, region: typing.Optional[str]=None):
        """
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        :param hosted_zone: Route 53 Hosted Zone used to perform DNS validation of the request. The zone must be authoritative for the domain name specified in the Certificate Request.
        :param custom_resource_role: Role to use for the custom resource that creates the validated certificate. Default: - A new role will be created
        :param region: AWS region that will host the certificate. This is needed especially for certificates used for CloudFront distributions, which require the region to be us-east-1. Default: the region the stack is deployed in.

        stability
        :stability: experimental
        """
        self._values = {
            'domain_name': domain_name,
            'hosted_zone': hosted_zone,
        }
        if subject_alternative_names is not None: self._values["subject_alternative_names"] = subject_alternative_names
        if validation_domains is not None: self._values["validation_domains"] = validation_domains
        if validation_method is not None: self._values["validation_method"] = validation_method
        if custom_resource_role is not None: self._values["custom_resource_role"] = custom_resource_role
        if region is not None: self._values["region"] = region

    @builtins.property
    def domain_name(self) -> str:
        """Fully-qualified domain name to request a certificate for.

        May contain wildcards, such as ``*.domain.com``.
        """
        return self._values.get('domain_name')

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[str]]:
        """Alternative domain names on your certificate.

        Use this to register alternative domain names that represent the same site.

        default
        :default: - No additional FQDNs will be included as alternative domain names.
        """
        return self._values.get('subject_alternative_names')

    @builtins.property
    def validation_domains(self) -> typing.Optional[typing.Mapping[str,str]]:
        """What validation domain to use for every requested domain.

        Has to be a superdomain of the requested domain.

        default
        :default: - Apex domain is used for every domain that's not overridden.
        """
        return self._values.get('validation_domains')

    @builtins.property
    def validation_method(self) -> typing.Optional["ValidationMethod"]:
        """Validation method used to assert domain ownership.

        default
        :default: ValidationMethod.EMAIL
        """
        return self._values.get('validation_method')

    @builtins.property
    def hosted_zone(self) -> aws_cdk.aws_route53.IHostedZone:
        """Route 53 Hosted Zone used to perform DNS validation of the request.

        The zone
        must be authoritative for the domain name specified in the Certificate Request.

        stability
        :stability: experimental
        """
        return self._values.get('hosted_zone')

    @builtins.property
    def custom_resource_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role to use for the custom resource that creates the validated certificate.

        default
        :default: - A new role will be created

        stability
        :stability: experimental
        """
        return self._values.get('custom_resource_role')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """AWS region that will host the certificate.

        This is needed especially
        for certificates used for CloudFront distributions, which require the region
        to be us-east-1.

        default
        :default: the region the stack is deployed in.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DnsValidatedCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-certificatemanager.ICertificate")
class ICertificate(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICertificateProxy

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        attribute:
        :attribute:: true
        """
        ...


class _ICertificateProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-certificatemanager.ICertificate"
    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "certificateArn")


@jsii.implements(ICertificate)
class Certificate(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-certificatemanager.Certificate"):
    """A certificate managed by AWS Certificate Manager.

    IMPORTANT: if you are creating a certificate as part of your stack, the stack
    will not complete creating until you read and follow the instructions in the
    email that you will receive.

    ACM will send validation emails to the following addresses:

    admin@domain.com
    administrator@domain.com
    hostmaster@domain.com
    postmaster@domain.com
    webmaster@domain.com

    For every domain that you register.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str,str]]=None, validation_method: typing.Optional["ValidationMethod"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        """
        props = CertificateProps(domain_name=domain_name, subject_alternative_names=subject_alternative_names, validation_domains=validation_domains, validation_method=validation_method)

        jsii.create(Certificate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCertificateArn")
    @builtins.classmethod
    def from_certificate_arn(cls, scope: aws_cdk.core.Construct, id: str, certificate_arn: str) -> "ICertificate":
        """Import a certificate.

        :param scope: -
        :param id: -
        :param certificate_arn: -
        """
        return jsii.sinvoke(cls, "fromCertificateArn", [scope, id, certificate_arn])

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN."""
        return jsii.get(self, "certificateArn")


@jsii.implements(ICertificate)
class DnsValidatedCertificate(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-certificatemanager.DnsValidatedCertificate"):
    """A certificate managed by AWS Certificate Manager.

    Will be automatically
    validated using DNS validation against the specified Route 53 hosted zone.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CertificateManager::Certificate
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, hosted_zone: aws_cdk.aws_route53.IHostedZone, custom_resource_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, region: typing.Optional[str]=None, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str,str]]=None, validation_method: typing.Optional["ValidationMethod"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param hosted_zone: Route 53 Hosted Zone used to perform DNS validation of the request. The zone must be authoritative for the domain name specified in the Certificate Request.
        :param custom_resource_role: Role to use for the custom resource that creates the validated certificate. Default: - A new role will be created
        :param region: AWS region that will host the certificate. This is needed especially for certificates used for CloudFront distributions, which require the region to be us-east-1. Default: the region the stack is deployed in.
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation_domains: What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL

        stability
        :stability: experimental
        """
        props = DnsValidatedCertificateProps(hosted_zone=hosted_zone, custom_resource_role=custom_resource_role, region=region, domain_name=domain_name, subject_alternative_names=subject_alternative_names, validation_domains=validation_domains, validation_method=validation_method)

        jsii.create(DnsValidatedCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """The certificate's ARN.

        stability
        :stability: experimental
        """
        return jsii.get(self, "certificateArn")


@jsii.enum(jsii_type="@aws-cdk/aws-certificatemanager.ValidationMethod")
class ValidationMethod(enum.Enum):
    """Method used to assert ownership of the domain."""
    EMAIL = "EMAIL"
    """Send email to a number of email addresses associated with the domain.

    see
    :see: https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html
    """
    DNS = "DNS"
    """Validate ownership by adding appropriate DNS records.

    see
    :see: https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html
    """

__all__ = ["Certificate", "CertificateProps", "CfnCertificate", "CfnCertificateProps", "DnsValidatedCertificate", "DnsValidatedCertificateProps", "ICertificate", "ValidationMethod", "__jsii_assembly__"]

publication.publish()
