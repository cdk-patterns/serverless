"""
## Amazon API Gateway Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Amazon API Gateway is a fully managed service that makes it easy for developers
to publish, maintain, monitor, and secure APIs at any scale. Create an API to
access data, business logic, or functionality from your back-end services, such
as applications running on Amazon Elastic Compute Cloud (Amazon EC2), code
running on AWS Lambda, or any web application.

### Defining APIs

APIs are defined as a hierarchy of resources and methods. `addResource` and
`addMethod` can be used to build this hierarchy. The root resource is
`api.root`.

For example, the following code defines an API that includes the following HTTP
endpoints: `ANY /, GET /books`, `POST /books`, `GET /books/{book_id}`, `DELETE /books/{book_id}`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
api = apigateway.RestApi(self, "books-api")

api.root.add_method("ANY")

books = api.root.add_resource("books")
books.add_method("GET")
books.add_method("POST")

book = books.add_resource("{book_id}")
book.add_method("GET")
book.add_method("DELETE")
```

### AWS Lambda-backed APIs

A very common practice is to use Amazon API Gateway with AWS Lambda as the
backend integration. The `LambdaRestApi` construct makes it easy:

The following code defines a REST API that routes all requests to the
specified AWS Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
backend = lambda.Function(...)
apigateway.LambdaRestApi(self, "myapi",
    handler=backend
)
```

You can also supply `proxy: false`, in which case you will have to explicitly
define the API model:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
backend = lambda.Function(...)
api = apigateway.LambdaRestApi(self, "myapi",
    handler=backend,
    proxy=False
)

items = api.root.add_resource("items")
items.add_method("GET")# GET /items
items.add_method("POST")# POST /items

item = items.add_resource("{item}")
item.add_method("GET")# GET /items/{item}

# the default integration for methods is "handler", but one can
# customize this behavior per method or even a sub path.
item.add_method("DELETE", apigateway.HttpIntegration("http://amazon.com"))
```

### Integration Targets

Methods are associated with backend integrations, which are invoked when this
method is called. API Gateway supports the following integrations:

* `MockIntegration` - can be used to test APIs. This is the default
  integration if one is not specified.
* `LambdaIntegration` - can be used to invoke an AWS Lambda function.
* `AwsIntegration` - can be used to invoke arbitrary AWS service APIs.
* `HttpIntegration` - can be used to invoke HTTP endpoints.

The following example shows how to integrate the `GET /book/{book_id}` method to
an AWS Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_book_handler = lambda.Function(...)
get_book_integration = apigateway.LambdaIntegration(get_book_handler)
book.add_method("GET", get_book_integration)
```

Integration options can be optionally be specified:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_book_integration = apigateway.LambdaIntegration(get_book_handler,
    content_handling=apigateway.ContentHandling.CONVERT_TO_TEXT, # convert to base64
    credentials_passthrough=True
)
```

Method options can optionally be specified when adding methods:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
book.add_method("GET", get_book_integration,
    authorization_type=apigateway.AuthorizationType.IAM,
    api_key_required=True
)
```

The following example shows how to use an API Key with a usage plan:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
hello = lambda.Function(self, "hello",
    runtime=lambda.Runtime.NODEJS_10_X,
    handler="hello.handler",
    code=lambda.Code.from_asset("lambda")
)

api = apigateway.RestApi(self, "hello-api")
integration = apigateway.LambdaIntegration(hello)

v1 = api.root.add_resource("v1")
echo = v1.add_resource("echo")
echo_method = echo.add_method("GET", integration, api_key_required=True)
key = api.add_api_key("ApiKey")

plan = api.add_usage_plan("UsagePlan",
    name="Easy",
    api_key=key
)

plan.add_api_stage(
    stage=api.deployment_stage,
    throttle=[{
        "method": echo_method,
        "throttle": {
            "rate_limit": 10,
            "burst_limit": 2
        }
    }
    ]
)
```

### Working with models

When you work with Lambda integrations that are not Proxy integrations, you
have to define your models and mappings for the request, response, and integration.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
hello = lambda.Function(self, "hello",
    runtime=lambda.Runtime.NODEJS_10_X,
    handler="hello.handler",
    code=lambda.Code.from_asset("lambda")
)

api = apigateway.RestApi(self, "hello-api")
resource = api.root.add_resource("v1")
```

You can define more parameters on the integration to tune the behavior of API Gateway

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
integration = LambdaIntegration(hello,
    proxy=False,
    request_parameters={
        # You can define mapping parameters from your method to your integration
        # - Destination parameters (the key) are the integration parameters (used in mappings)
        # - Source parameters (the value) are the source request parameters or expressions
        # @see: https://docs.aws.amazon.com/apigateway/latest/developerguide/request-response-data-mappings.html
        "integration.request.querystring.who": "method.request.querystring.who"
    },
    allow_test_invoke=True,
    request_templates={
        # You can define a mapping that will build a payload for your integration, based
        #  on the integration parameters that you have specified
        # Check: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        "application/json": JSON.stringify(action="sayHello", poll_id="$util.escapeJavaScript($input.params('who'))")
    },
    # This parameter defines the behavior of the engine is no suitable response template is found
    passthrough_behavior=PassthroughBehavior.NEVER,
    integration_responses=[{
        # Successful response from the Lambda function, no filter defined
        #  - the selectionPattern filter only tests the error message
        # We will set the response status code to 200
        "status_code": "200",
        "response_templates": {
            # This template takes the "message" result from the Lambda function, adn embeds it in a JSON response
            # Check https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
            "application/json": JSON.stringify(state="ok", greeting="$util.escapeJavaScript($input.body)")
        },
        "response_parameters": {
            # We can map response parameters
            # - Destination parameters (the key) are the response parameters (used in mappings)
            # - Source parameters (the value) are the integration response parameters or expressions
            "method.response.header._content-_type": "'application/json'",
            "method.response.header._access-_control-_allow-_origin": "'*'",
            "method.response.header._access-_control-_allow-_credentials": "'true'"
        }
    }, {
        # For errors, we check if the error message is not empty, get the error data
        "selection_pattern": "(\n|.)+",
        # We will set the response status code to 200
        "status_code": "400",
        "response_templates": {
            "application/json": JSON.stringify(state="error", message="$util.escapeJavaScript($input.path('$.errorMessage'))")
        },
        "response_parameters": {
            "method.response.header._content-_type": "'application/json'",
            "method.response.header._access-_control-_allow-_origin": "'*'",
            "method.response.header._access-_control-_allow-_credentials": "'true'"
        }
    }
    ]
)
```

You can define models for your responses (and requests)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# We define the JSON Schema for the transformed valid response
response_model = api.add_model("ResponseModel",
    content_type="application/json",
    model_name="ResponseModel",
    schema={"$schema": "http://json-schema.org/draft-04/schema#", "title": "pollResponse", "type": "object", "properties": {"state": {"type": "string"}, "greeting": {"type": "string"}}}
)

# We define the JSON Schema for the transformed error response
error_response_model = api.add_model("ErrorResponseModel",
    content_type="application/json",
    model_name="ErrorResponseModel",
    schema={"$schema": "http://json-schema.org/draft-04/schema#", "title": "errorResponse", "type": "object", "properties": {"state": {"type": "string"}, "message": {"type": "string"}}}
)
```

And reference all on your method definition.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want to define parameter mappings for the request, you need a validator
validator = api.add_request_validator("DefaultValidator",
    validate_request_body=False,
    validate_request_parameters=True
)
resource.add_method("GET", integration,
    # We can mark the parameters as required
    request_parameters={
        "method.request.querystring.who": True
    },
    # We need to set the validator for ensuring they are passed
    request_validator=validator,
    method_responses=[{
        # Successful response from the integration
        "status_code": "200",
        # Define what parameters are allowed or not
        "response_parameters": {
            "method.response.header._content-_type": True,
            "method.response.header._access-_control-_allow-_origin": True,
            "method.response.header._access-_control-_allow-_credentials": True
        },
        # Validate the schema on the response
        "response_models": {
            "application/json": response_model
        }
    }, {
        # Same thing for the error responses
        "status_code": "400",
        "response_parameters": {
            "method.response.header._content-_type": True,
            "method.response.header._access-_control-_allow-_origin": True,
            "method.response.header._access-_control-_allow-_credentials": True
        },
        "response_models": {
            "application/json": error_response_model
        }
    }
    ]
)
```

#### Default Integration and Method Options

The `defaultIntegration` and `defaultMethodOptions` properties can be used to
configure a default integration at any resource level. These options will be
used when defining method under this resource (recursively) with undefined
integration or options.

> If not defined, the default integration is `MockIntegration`. See reference
> documentation for default method options.

The following example defines the `booksBackend` integration as a default
integration. This means that all API methods that do not explicitly define an
integration will be routed to this AWS Lambda function.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
books_backend = apigateway.LambdaIntegration(...)
api = apigateway.RestApi(self, "books",
    default_integration=books_backend
)

books = api.root.add_resource("books")
books.add_method("GET")# integrated with `booksBackend`
books.add_method("POST")# integrated with `booksBackend`

book = books.add_resource("{book_id}")
book.add_method("GET")
```

### Proxy Routes

The `addProxy` method can be used to install a greedy `{proxy+}` resource
on a path. By default, this also installs an `"ANY"` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
proxy = resource.add_proxy(
    default_integration=LambdaIntegration(handler),

    # "false" will require explicitly adding methods on the `proxy` resource
    any_method=True
)
```

### Authorizers

API Gateway [supports several different authorization types](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html)
that can be used for controlling access to your REST APIs.

#### IAM-based authorizer

The following CDK code provides 'excecute-api' permission to an IAM user, via IAM policies, for the 'GET' method on the `books` resource:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_books = books.add_method("GET", apigateway.HttpIntegration("http://amazon.com"),
    authorization_type=apigateway.AuthorizationType.IAM
)

iam_user.attach_inline_policy(iam.Policy(self, "AllowBooks",
    statements=[
        iam.PolicyStatement(
            actions=["execute-api:Invoke"],
            effect=iam.Effect.Allow,
            resources=[get_books.method_arn()]
        )
    ]
))
```

#### Lambda-based token authorizer

API Gateway also allows [lambda functions to be used as authorizers](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html).

This module provides support for token-based Lambda authorizers. When a client makes a request to an API's methods configured with such
an authorizer, API Gateway calls the Lambda authorizer, which takes the caller's identity as input and returns an IAM policy as output.
A token-based Lambda authorizer (also called a token authorizer) receives the caller's identity in a bearer token, such as
a JSON Web Token (JWT) or an OAuth token.

API Gateway interacts with the authorizer Lambda function handler by passing input and expecting the output in a specific format.
The event object that the handler is called with contains the `authorizationToken` and the `methodArn` from the request to the
API Gateway endpoint. The handler is expected to return the `principalId` (i.e. the client identifier) and a `policyDocument` stating
what the client is authorizer to perform.
See https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html for a detailed specification on
inputs and outputs of the lambda handler.

The following code attaches a token-based Lambda authorizer to the 'GET' Method of the Book resource:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auth_fn = lambda.Function(self, "booksAuthorizerLambda")

auth = apigateway.TokenAuthorizer(self, "booksAuthorizer",
    function=auth_fn
)

books.add_method("GET", apigateway.HttpIntegration("http://amazon.com"),
    authorizer=auth
)
```

By default, the `TokenAuthorizer` looks for the authorization token in the request header with the key 'Authorization'. This can,
however, be modified by changing the `identitySource` property.

Authorizers can also be passed via the `defaultMethodOptions` property within the `RestApi` construct or the `Method` construct. Unless
explicitly overridden, the specified defaults will be applied across all `Method`s across the `RestApi` or across all `Resource`s,
depending on where the defaults were specified.

### Deployments

By default, the `RestApi` construct will automatically create an API Gateway
[Deployment](https://docs.aws.amazon.com/apigateway/api-reference/resource/deployment/) and a "prod" [Stage](https://docs.aws.amazon.com/apigateway/api-reference/resource/stage/) which represent the API configuration you
defined in your CDK app. This means that when you deploy your app, your API will
be have open access from the internet via the stage URL.

The URL of your API can be obtained from the attribute `restApi.url`, and is
also exported as an `Output` from your stack, so it's printed when you `cdk deploy` your app:

```
$ cdk deploy
...
books.booksapiEndpointE230E8D5 = https://6lyktd4lpk.execute-api.us-east-1.amazonaws.com/prod/
```

To disable this behavior, you can set `{ deploy: false }` when creating your
API. This means that the API will not be deployed and a stage will not be
created for it. You will need to manually define a `apigateway.Deployment` and
`apigateway.Stage` resources.

Use the `deployOptions` property to customize the deployment options of your
API.

The following example will configure API Gateway to emit logs and data traces to
AWS CloudWatch for all API calls:

> By default, an IAM role will be created and associated with API Gateway to
> allow it to write logs and metrics to AWS CloudWatch unless `cloudWatchRole` is
> set to `false`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
api = apigateway.RestApi(self, "books",
    deploy_options={
        "logging_level": apigateway.MethodLoggingLevel.INFO,
        "data_trace_enabled": True
    }
)
```

#### Deeper dive: invalidation of deployments

API Gateway deployments are an immutable snapshot of the API. This means that we
want to automatically create a new deployment resource every time the API model
defined in our CDK app changes.

In order to achieve that, the AWS CloudFormation logical ID of the
`AWS::ApiGateway::Deployment` resource is dynamically calculated by hashing the
API configuration (resources, methods). This means that when the configuration
changes (i.e. a resource or method are added, configuration is changed), a new
logical ID will be assigned to the deployment resource. This will cause
CloudFormation to create a new deployment resource.

By default, old deployments are *deleted*. You can set `retainDeployments: true`
to allow users revert the stage to an old deployment manually.

### Custom Domains

To associate an API with a custom domain, use the `domainName` configuration when
you define your API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
api = apigw.RestApi(self, "MyDomain",
    domain_name={
        "domain_name": "example.com",
        "certificate": acm_certificate_for_example_com
    }
)
```

This will define a `DomainName` resource for you, along with a `BasePathMapping`
from the root of the domain to the deployment stage of the API. This is a common
set up.

To route domain traffic to an API Gateway API, use Amazon Route 53 to create an
alias record. An alias record is a Route 53 extension to DNS. It's similar to a
CNAME record, but you can create an alias record both for the root domain, such
as `example.com`, and for subdomains, such as `www.example.com`. (You can create
CNAME records only for subdomains.)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
route53.ARecord(self, "CustomDomainAliasRecord",
    zone=hosted_zone_for_example_com,
    target=route53.RecordTarget.from_alias(route53_targets.ApiGateway(api))
)
```

You can also define a `DomainName` resource directly in order to customize the default behavior:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
apigw.DomainName(self, "custom-domain",
    domain_name="example.com",
    certificate=acm_certificate_for_example_com,
    endpoint_type=apigw.EndpointType.EDGE
)
```

Once you have a domain, you can map base paths of the domain to APIs.
The following example will map the URL https://example.com/go-to-api1
to the `api1` API and https://example.com/boom to the `api2` API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain.add_base_path_mapping(api1, base_path="go-to-api1")
domain.add_base_path_mapping(api2, base_path="boom")
```

NOTE: currently, the mapping will always be assigned to the APIs
`deploymentStage`, which will automatically assigned to the latest API
deployment. Raise a GitHub issue if you require more granular control over
mapping base paths to stages.

If you don't specify `basePath`, all URLs under this domain will be mapped
to the API, and you won't be able to map another API to the same domain:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain.add_base_path_mapping(api)
```

This can also be achieved through the `mapping` configuration when defining the
domain as demonstrated above.

If you wish to setup this domain with an Amazon Route53 alias, use the `route53_targets.ApiGatewayDomain`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
route53.ARecord(self, "CustomDomainAliasRecord",
    zone=hosted_zone_for_example_com,
    target=route53.RecordTarget.from_alias(route53_targets.ApiGatewayDomain(domain_name))
)
```

### Cross Origin Resource Sharing (CORS)

[Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a mechanism
that uses additional HTTP headers to tell browsers to give a web application
running at one origin, access to selected resources from a different origin. A
web application executes a cross-origin HTTP request when it requests a resource
that has a different origin (domain, protocol, or port) from its own.

You can add the CORS [preflight](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Preflighted_requests) OPTIONS HTTP method to any API resource via the `defaultCorsPreflightOptions` option or by calling the `addCorsPreflight` on a specific resource.

The following example will enable CORS for all methods and all origins on all resources of the API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
apigateway.RestApi(self, "api",
    default_cors_preflight_options={
        "allow_origins": apigateway.Cors.ALL_ORIGINS,
        "allow_methods": apigateway.Cors.ALL_METHODS
    }
)
```

The following example will add an OPTIONS method to the `myResource` API resource, which
only allows GET and PUT HTTP requests from the origin https://amazon.com.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_resource.add_cors_preflight(
    allow_origins=["https://amazon.com"],
    allow_methods=["GET", "PUT"]
)
```

See the
[`CorsOptions`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.CorsOptions.html)
API reference for a detailed list of supported configuration options.

You can specify defaults this at the resource level, in which case they will be applied to the entire resource sub-tree:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
subtree = resource.add_resource("subtree",
    default_cors_preflight_options={
        "allow_origins": ["https://amazon.com"]
    }
)
```

This means that all resources under `subtree` (inclusive) will have a preflight
OPTIONS added to them.

See [#906](https://github.com/aws/aws-cdk/issues/906) for a list of CORS
features which are not yet supported.

## APIGateway v2

APIGateway v2 APIs are now moved to its own package named `aws-apigatewayv2`. For backwards compatibility, existing
APIGateway v2 "CFN resources" (such as `CfnApi`) that were previously exported as part of this package, are still
exported from here and have been marked deprecated. However, updates to these CloudFormation resources, such as new
properties and new resource types will not be available.

Move to using `aws-apigatewayv2` to get the latest APIs and updates.

---


This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-apigateway", "1.23.0", __name__, "aws-apigateway@1.23.0.jsii.tgz")


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.ApiKeySourceType")
class ApiKeySourceType(enum.Enum):
    HEADER = "HEADER"
    """To read the API key from the ``X-API-Key`` header of a request."""
    AUTHORIZER = "AUTHORIZER"
    """To read the API key from the ``UsageIdentifierKey`` from a custom authorizer."""

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.AuthorizationType")
class AuthorizationType(enum.Enum):
    NONE = "NONE"
    """Open access."""
    IAM = "IAM"
    """Use AWS IAM permissions."""
    CUSTOM = "CUSTOM"
    """Use a custom authorizer."""
    COGNITO = "COGNITO"
    """Use an AWS Cognito user pool."""

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.AwsIntegrationProps", jsii_struct_bases=[], name_mapping={'service': 'service', 'action': 'action', 'action_parameters': 'actionParameters', 'integration_http_method': 'integrationHttpMethod', 'options': 'options', 'path': 'path', 'proxy': 'proxy', 'subdomain': 'subdomain'})
class AwsIntegrationProps():
    def __init__(self, *, service: str, action: typing.Optional[str]=None, action_parameters: typing.Optional[typing.Mapping[str,str]]=None, integration_http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, path: typing.Optional[str]=None, proxy: typing.Optional[bool]=None, subdomain: typing.Optional[str]=None):
        """
        :param service: The name of the integrated AWS service (e.g. ``s3``).
        :param action: The AWS action to perform in the integration. Use ``actionParams`` to specify key-value params for the action. Mutually exclusive with ``path``.
        :param action_parameters: Parameters for the action. ``action`` must be set, and ``path`` must be undefined. The action params will be URL encoded.
        :param integration_http_method: The integration's HTTP method type. Default: POST
        :param options: Integration options, such as content handling, request/response mapping, etc.
        :param path: The path to use for path-base APIs. For example, for S3 GET, you can set path to ``bucket/key``. For lambda, you can set path to ``2015-03-31/functions/${function-arn}/invocations`` Mutually exclusive with the ``action`` options.
        :param proxy: Use AWS_PROXY integration. Default: false
        :param subdomain: A designated subdomain supported by certain AWS service for fast host-name lookup.
        """
        if isinstance(options, dict): options = IntegrationOptions(**options)
        self._values = {
            'service': service,
        }
        if action is not None: self._values["action"] = action
        if action_parameters is not None: self._values["action_parameters"] = action_parameters
        if integration_http_method is not None: self._values["integration_http_method"] = integration_http_method
        if options is not None: self._values["options"] = options
        if path is not None: self._values["path"] = path
        if proxy is not None: self._values["proxy"] = proxy
        if subdomain is not None: self._values["subdomain"] = subdomain

    @builtins.property
    def service(self) -> str:
        """The name of the integrated AWS service (e.g. ``s3``)."""
        return self._values.get('service')

    @builtins.property
    def action(self) -> typing.Optional[str]:
        """The AWS action to perform in the integration.

        Use ``actionParams`` to specify key-value params for the action.

        Mutually exclusive with ``path``.
        """
        return self._values.get('action')

    @builtins.property
    def action_parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Parameters for the action.

        ``action`` must be set, and ``path`` must be undefined.
        The action params will be URL encoded.
        """
        return self._values.get('action_parameters')

    @builtins.property
    def integration_http_method(self) -> typing.Optional[str]:
        """The integration's HTTP method type.

        default
        :default: POST
        """
        return self._values.get('integration_http_method')

    @builtins.property
    def options(self) -> typing.Optional["IntegrationOptions"]:
        """Integration options, such as content handling, request/response mapping, etc."""
        return self._values.get('options')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path to use for path-base APIs.

        For example, for S3 GET, you can set path to ``bucket/key``.
        For lambda, you can set path to ``2015-03-31/functions/${function-arn}/invocations``

        Mutually exclusive with the ``action`` options.
        """
        return self._values.get('path')

    @builtins.property
    def proxy(self) -> typing.Optional[bool]:
        """Use AWS_PROXY integration.

        default
        :default: false
        """
        return self._values.get('proxy')

    @builtins.property
    def subdomain(self) -> typing.Optional[str]:
        """A designated subdomain supported by certain AWS service for fast host-name lookup."""
        return self._values.get('subdomain')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsIntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BasePathMapping(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.BasePathMapping"):
    """This resource creates a base path that clients who call your API must use in the invocation URL.

    In most cases, you will probably want to use
    ``DomainName.addBasePathMapping()`` to define mappings.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: "IDomainName", rest_api: "IRestApi", base_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param domain_name: The DomainName to associate with this base path mapping.
        :param rest_api: The RestApi resource to target.
        :param base_path: The base path name that callers of the API must provide in the URL after the domain name (e.g. ``example.com/base-path``). If you specify this property, it can't be an empty string. Default: - map requests from the domain root (e.g. ``example.com``). If this is undefined, no additional mappings will be allowed on this domain name.
        """
        props = BasePathMappingProps(domain_name=domain_name, rest_api=rest_api, base_path=base_path)

        jsii.create(BasePathMapping, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.BasePathMappingOptions", jsii_struct_bases=[], name_mapping={'base_path': 'basePath'})
class BasePathMappingOptions():
    def __init__(self, *, base_path: typing.Optional[str]=None):
        """
        :param base_path: The base path name that callers of the API must provide in the URL after the domain name (e.g. ``example.com/base-path``). If you specify this property, it can't be an empty string. Default: - map requests from the domain root (e.g. ``example.com``). If this is undefined, no additional mappings will be allowed on this domain name.
        """
        self._values = {
        }
        if base_path is not None: self._values["base_path"] = base_path

    @builtins.property
    def base_path(self) -> typing.Optional[str]:
        """The base path name that callers of the API must provide in the URL after the domain name (e.g. ``example.com/base-path``). If you specify this property, it can't be an empty string.

        default
        :default:

        - map requests from the domain root (e.g. ``example.com``). If this
          is undefined, no additional mappings will be allowed on this domain name.
        """
        return self._values.get('base_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasePathMappingOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.BasePathMappingProps", jsii_struct_bases=[BasePathMappingOptions], name_mapping={'base_path': 'basePath', 'domain_name': 'domainName', 'rest_api': 'restApi'})
class BasePathMappingProps(BasePathMappingOptions):
    def __init__(self, *, base_path: typing.Optional[str]=None, domain_name: "IDomainName", rest_api: "IRestApi"):
        """
        :param base_path: The base path name that callers of the API must provide in the URL after the domain name (e.g. ``example.com/base-path``). If you specify this property, it can't be an empty string. Default: - map requests from the domain root (e.g. ``example.com``). If this is undefined, no additional mappings will be allowed on this domain name.
        :param domain_name: The DomainName to associate with this base path mapping.
        :param rest_api: The RestApi resource to target.
        """
        self._values = {
            'domain_name': domain_name,
            'rest_api': rest_api,
        }
        if base_path is not None: self._values["base_path"] = base_path

    @builtins.property
    def base_path(self) -> typing.Optional[str]:
        """The base path name that callers of the API must provide in the URL after the domain name (e.g. ``example.com/base-path``). If you specify this property, it can't be an empty string.

        default
        :default:

        - map requests from the domain root (e.g. ``example.com``). If this
          is undefined, no additional mappings will be allowed on this domain name.
        """
        return self._values.get('base_path')

    @builtins.property
    def domain_name(self) -> "IDomainName":
        """The DomainName to associate with this base path mapping."""
        return self._values.get('domain_name')

    @builtins.property
    def rest_api(self) -> "IRestApi":
        """The RestApi resource to target."""
        return self._values.get('rest_api')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasePathMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccount(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnAccount"):
    """A CloudFormation ``AWS::ApiGateway::Account``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Account
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cloud_watch_role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::Account``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cloud_watch_role_arn: ``AWS::ApiGateway::Account.CloudWatchRoleArn``.
        """
        props = CfnAccountProps(cloud_watch_role_arn=cloud_watch_role_arn)

        jsii.create(CfnAccount, self, [scope, id, props])

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
    @jsii.member(jsii_name="cloudWatchRoleArn")
    def cloud_watch_role_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Account.CloudWatchRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html#cfn-apigateway-account-cloudwatchrolearn
        """
        return jsii.get(self, "cloudWatchRoleArn")

    @cloud_watch_role_arn.setter
    def cloud_watch_role_arn(self, value: typing.Optional[str]):
        jsii.set(self, "cloudWatchRoleArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAccountProps", jsii_struct_bases=[], name_mapping={'cloud_watch_role_arn': 'cloudWatchRoleArn'})
class CfnAccountProps():
    def __init__(self, *, cloud_watch_role_arn: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::Account``.

        :param cloud_watch_role_arn: ``AWS::ApiGateway::Account.CloudWatchRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html
        """
        self._values = {
        }
        if cloud_watch_role_arn is not None: self._values["cloud_watch_role_arn"] = cloud_watch_role_arn

    @builtins.property
    def cloud_watch_role_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Account.CloudWatchRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html#cfn-apigateway-account-cloudwatchrolearn
        """
        return self._values.get('cloud_watch_role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAccountProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiKey(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnApiKey"):
    """A CloudFormation ``AWS::ApiGateway::ApiKey``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::ApiKey
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, customer_id: typing.Optional[str]=None, description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, generate_distinct_id: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, name: typing.Optional[str]=None, stage_keys: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StageKeyProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, value: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::ApiKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param customer_id: ``AWS::ApiGateway::ApiKey.CustomerId``.
        :param description: ``AWS::ApiGateway::ApiKey.Description``.
        :param enabled: ``AWS::ApiGateway::ApiKey.Enabled``.
        :param generate_distinct_id: ``AWS::ApiGateway::ApiKey.GenerateDistinctId``.
        :param name: ``AWS::ApiGateway::ApiKey.Name``.
        :param stage_keys: ``AWS::ApiGateway::ApiKey.StageKeys``.
        :param tags: ``AWS::ApiGateway::ApiKey.Tags``.
        :param value: ``AWS::ApiGateway::ApiKey.Value``.
        """
        props = CfnApiKeyProps(customer_id=customer_id, description=description, enabled=enabled, generate_distinct_id=generate_distinct_id, name=name, stage_keys=stage_keys, tags=tags, value=value)

        jsii.create(CfnApiKey, self, [scope, id, props])

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
        """``AWS::ApiGateway::ApiKey.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="customerId")
    def customer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.CustomerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-customerid
        """
        return jsii.get(self, "customerId")

    @customer_id.setter
    def customer_id(self, value: typing.Optional[str]):
        jsii.set(self, "customerId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::ApiKey.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="generateDistinctId")
    def generate_distinct_id(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::ApiKey.GenerateDistinctId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-generatedistinctid
        """
        return jsii.get(self, "generateDistinctId")

    @generate_distinct_id.setter
    def generate_distinct_id(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "generateDistinctId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="stageKeys")
    def stage_keys(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StageKeyProperty"]]]]]:
        """``AWS::ApiGateway::ApiKey.StageKeys``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-stagekeys
        """
        return jsii.get(self, "stageKeys")

    @stage_keys.setter
    def stage_keys(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StageKeyProperty"]]]]]):
        jsii.set(self, "stageKeys", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.Value``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-value
        """
        return jsii.get(self, "value")

    @value.setter
    def value(self, value: typing.Optional[str]):
        jsii.set(self, "value", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiKey.StageKeyProperty", jsii_struct_bases=[], name_mapping={'rest_api_id': 'restApiId', 'stage_name': 'stageName'})
    class StageKeyProperty():
        def __init__(self, *, rest_api_id: typing.Optional[str]=None, stage_name: typing.Optional[str]=None):
            """
            :param rest_api_id: ``CfnApiKey.StageKeyProperty.RestApiId``.
            :param stage_name: ``CfnApiKey.StageKeyProperty.StageName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-apikey-stagekey.html
            """
            self._values = {
            }
            if rest_api_id is not None: self._values["rest_api_id"] = rest_api_id
            if stage_name is not None: self._values["stage_name"] = stage_name

        @builtins.property
        def rest_api_id(self) -> typing.Optional[str]:
            """``CfnApiKey.StageKeyProperty.RestApiId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-apikey-stagekey.html#cfn-apigateway-apikey-stagekey-restapiid
            """
            return self._values.get('rest_api_id')

        @builtins.property
        def stage_name(self) -> typing.Optional[str]:
            """``CfnApiKey.StageKeyProperty.StageName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-apikey-stagekey.html#cfn-apigateway-apikey-stagekey-stagename
            """
            return self._values.get('stage_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StageKeyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiKeyProps", jsii_struct_bases=[], name_mapping={'customer_id': 'customerId', 'description': 'description', 'enabled': 'enabled', 'generate_distinct_id': 'generateDistinctId', 'name': 'name', 'stage_keys': 'stageKeys', 'tags': 'tags', 'value': 'value'})
class CfnApiKeyProps():
    def __init__(self, *, customer_id: typing.Optional[str]=None, description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, generate_distinct_id: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, name: typing.Optional[str]=None, stage_keys: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApiKey.StageKeyProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, value: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::ApiKey``.

        :param customer_id: ``AWS::ApiGateway::ApiKey.CustomerId``.
        :param description: ``AWS::ApiGateway::ApiKey.Description``.
        :param enabled: ``AWS::ApiGateway::ApiKey.Enabled``.
        :param generate_distinct_id: ``AWS::ApiGateway::ApiKey.GenerateDistinctId``.
        :param name: ``AWS::ApiGateway::ApiKey.Name``.
        :param stage_keys: ``AWS::ApiGateway::ApiKey.StageKeys``.
        :param tags: ``AWS::ApiGateway::ApiKey.Tags``.
        :param value: ``AWS::ApiGateway::ApiKey.Value``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html
        """
        self._values = {
        }
        if customer_id is not None: self._values["customer_id"] = customer_id
        if description is not None: self._values["description"] = description
        if enabled is not None: self._values["enabled"] = enabled
        if generate_distinct_id is not None: self._values["generate_distinct_id"] = generate_distinct_id
        if name is not None: self._values["name"] = name
        if stage_keys is not None: self._values["stage_keys"] = stage_keys
        if tags is not None: self._values["tags"] = tags
        if value is not None: self._values["value"] = value

    @builtins.property
    def customer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.CustomerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-customerid
        """
        return self._values.get('customer_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-description
        """
        return self._values.get('description')

    @builtins.property
    def enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::ApiKey.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-enabled
        """
        return self._values.get('enabled')

    @builtins.property
    def generate_distinct_id(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::ApiKey.GenerateDistinctId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-generatedistinctid
        """
        return self._values.get('generate_distinct_id')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-name
        """
        return self._values.get('name')

    @builtins.property
    def stage_keys(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApiKey.StageKeyProperty"]]]]]:
        """``AWS::ApiGateway::ApiKey.StageKeys``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-stagekeys
        """
        return self._values.get('stage_keys')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApiGateway::ApiKey.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-tags
        """
        return self._values.get('tags')

    @builtins.property
    def value(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ApiKey.Value``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-value
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApiKeyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiMappingV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnApiMappingV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::ApiMapping``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::ApiMapping
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, domain_name: str, stage: str, api_mapping_key: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::ApiMapping``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::ApiMapping.ApiId``.
        :param domain_name: ``AWS::ApiGatewayV2::ApiMapping.DomainName``.
        :param stage: ``AWS::ApiGatewayV2::ApiMapping.Stage``.
        :param api_mapping_key: ``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        stability
        :stability: deprecated
        """
        props = CfnApiMappingV2Props(api_id=api_id, domain_name=domain_name, stage=stage, api_mapping_key=api_mapping_key)

        jsii.create(CfnApiMappingV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        stability
        :stability: deprecated
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str):
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        stability
        :stability: deprecated
        """
        return jsii.get(self, "stage")

    @stage.setter
    def stage(self, value: str):
        jsii.set(self, "stage", value)

    @builtins.property
    @jsii.member(jsii_name="apiMappingKey")
    def api_mapping_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiMappingKey")

    @api_mapping_key.setter
    def api_mapping_key(self, value: typing.Optional[str]):
        jsii.set(self, "apiMappingKey", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiMappingV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'domain_name': 'domainName', 'stage': 'stage', 'api_mapping_key': 'apiMappingKey'})
class CfnApiMappingV2Props():
    def __init__(self, *, api_id: str, domain_name: str, stage: str, api_mapping_key: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::ApiMapping``.

        :param api_id: ``AWS::ApiGatewayV2::ApiMapping.ApiId``.
        :param domain_name: ``AWS::ApiGatewayV2::ApiMapping.DomainName``.
        :param stage: ``AWS::ApiGatewayV2::ApiMapping.Stage``.
        :param api_mapping_key: ``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'domain_name': domain_name,
            'stage': stage,
        }
        if api_mapping_key is not None: self._values["api_mapping_key"] = api_mapping_key

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        stability
        :stability: deprecated
        """
        return self._values.get('domain_name')

    @builtins.property
    def stage(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        stability
        :stability: deprecated
        """
        return self._values.get('stage')

    @builtins.property
    def api_mapping_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        stability
        :stability: deprecated
        """
        return self._values.get('api_mapping_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApiMappingV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnApiV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Api``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Api
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key_selection_expression: typing.Optional[str]=None, base_path: typing.Optional[str]=None, body: typing.Any=None, body_s3_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["BodyS3LocationProperty"]]]=None, cors_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CorsProperty"]]]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, disable_schema_validation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, fail_on_warnings: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, name: typing.Optional[str]=None, protocol_type: typing.Optional[str]=None, route_key: typing.Optional[str]=None, route_selection_expression: typing.Optional[str]=None, tags: typing.Any=None, target: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key_selection_expression: ``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.
        :param base_path: ``AWS::ApiGatewayV2::Api.BasePath``.
        :param body: ``AWS::ApiGatewayV2::Api.Body``.
        :param body_s3_location: ``AWS::ApiGatewayV2::Api.BodyS3Location``.
        :param cors_configuration: ``AWS::ApiGatewayV2::Api.CorsConfiguration``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Api.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Api.Description``.
        :param disable_schema_validation: ``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.
        :param fail_on_warnings: ``AWS::ApiGatewayV2::Api.FailOnWarnings``.
        :param name: ``AWS::ApiGatewayV2::Api.Name``.
        :param protocol_type: ``AWS::ApiGatewayV2::Api.ProtocolType``.
        :param route_key: ``AWS::ApiGatewayV2::Api.RouteKey``.
        :param route_selection_expression: ``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.
        :param tags: ``AWS::ApiGatewayV2::Api.Tags``.
        :param target: ``AWS::ApiGatewayV2::Api.Target``.
        :param version: ``AWS::ApiGatewayV2::Api.Version``.

        stability
        :stability: deprecated
        """
        props = CfnApiV2Props(api_key_selection_expression=api_key_selection_expression, base_path=base_path, body=body, body_s3_location=body_s3_location, cors_configuration=cors_configuration, credentials_arn=credentials_arn, description=description, disable_schema_validation=disable_schema_validation, fail_on_warnings=fail_on_warnings, name=name, protocol_type=protocol_type, route_key=route_key, route_selection_expression=route_selection_expression, tags=tags, target=target, version=version)

        jsii.create(CfnApiV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::Api.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        stability
        :stability: deprecated
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Body``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        stability
        :stability: deprecated
        """
        return jsii.get(self, "body")

    @body.setter
    def body(self, value: typing.Any):
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeySelectionExpression")
    def api_key_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiKeySelectionExpression")

    @api_key_selection_expression.setter
    def api_key_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "apiKeySelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="basePath")
    def base_path(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.BasePath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        stability
        :stability: deprecated
        """
        return jsii.get(self, "basePath")

    @base_path.setter
    def base_path(self, value: typing.Optional[str]):
        jsii.set(self, "basePath", value)

    @builtins.property
    @jsii.member(jsii_name="bodyS3Location")
    def body_s3_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["BodyS3LocationProperty"]]]:
        """``AWS::ApiGatewayV2::Api.BodyS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        stability
        :stability: deprecated
        """
        return jsii.get(self, "bodyS3Location")

    @body_s3_location.setter
    def body_s3_location(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["BodyS3LocationProperty"]]]):
        jsii.set(self, "bodyS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CorsProperty"]]]:
        """``AWS::ApiGatewayV2::Api.CorsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        stability
        :stability: deprecated
        """
        return jsii.get(self, "corsConfiguration")

    @cors_configuration.setter
    def cors_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CorsProperty"]]]):
        jsii.set(self, "corsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        stability
        :stability: deprecated
        """
        return jsii.get(self, "credentialsArn")

    @credentials_arn.setter
    def credentials_arn(self, value: typing.Optional[str]):
        jsii.set(self, "credentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        stability
        :stability: deprecated
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableSchemaValidation")
    def disable_schema_validation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        stability
        :stability: deprecated
        """
        return jsii.get(self, "disableSchemaValidation")

    @disable_schema_validation.setter
    def disable_schema_validation(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "disableSchemaValidation", value)

    @builtins.property
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Api.FailOnWarnings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        stability
        :stability: deprecated
        """
        return jsii.get(self, "failOnWarnings")

    @fail_on_warnings.setter
    def fail_on_warnings(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "failOnWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        stability
        :stability: deprecated
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ProtocolType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        stability
        :stability: deprecated
        """
        return jsii.get(self, "protocolType")

    @protocol_type.setter
    def protocol_type(self, value: typing.Optional[str]):
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeKey")

    @route_key.setter
    def route_key(self, value: typing.Optional[str]):
        jsii.set(self, "routeKey", value)

    @builtins.property
    @jsii.member(jsii_name="routeSelectionExpression")
    def route_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeSelectionExpression")

    @route_selection_expression.setter
    def route_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "routeSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        stability
        :stability: deprecated
        """
        return jsii.get(self, "target")

    @target.setter
    def target(self, value: typing.Optional[str]):
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        stability
        :stability: deprecated
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]):
        jsii.set(self, "version", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiV2.BodyS3LocationProperty", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'etag': 'etag', 'key': 'key', 'version': 'version'})
    class BodyS3LocationProperty():
        def __init__(self, *, bucket: typing.Optional[str]=None, etag: typing.Optional[str]=None, key: typing.Optional[str]=None, version: typing.Optional[str]=None):
            """
            :param bucket: ``CfnApiV2.BodyS3LocationProperty.Bucket``.
            :param etag: ``CfnApiV2.BodyS3LocationProperty.Etag``.
            :param key: ``CfnApiV2.BodyS3LocationProperty.Key``.
            :param version: ``CfnApiV2.BodyS3LocationProperty.Version``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html
            stability
            :stability: deprecated
            """
            self._values = {
            }
            if bucket is not None: self._values["bucket"] = bucket
            if etag is not None: self._values["etag"] = etag
            if key is not None: self._values["key"] = key
            if version is not None: self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[str]:
            """``CfnApiV2.BodyS3LocationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-bucket
            stability
            :stability: deprecated
            """
            return self._values.get('bucket')

        @builtins.property
        def etag(self) -> typing.Optional[str]:
            """``CfnApiV2.BodyS3LocationProperty.Etag``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-etag
            stability
            :stability: deprecated
            """
            return self._values.get('etag')

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnApiV2.BodyS3LocationProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-key
            stability
            :stability: deprecated
            """
            return self._values.get('key')

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """``CfnApiV2.BodyS3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-version
            stability
            :stability: deprecated
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BodyS3LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiV2.CorsProperty", jsii_struct_bases=[], name_mapping={'allow_credentials': 'allowCredentials', 'allow_headers': 'allowHeaders', 'allow_methods': 'allowMethods', 'allow_origins': 'allowOrigins', 'expose_headers': 'exposeHeaders', 'max_age': 'maxAge'})
    class CorsProperty():
        def __init__(self, *, allow_credentials: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List[str]]=None, allow_origins: typing.Optional[typing.List[str]]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[jsii.Number]=None):
            """
            :param allow_credentials: ``CfnApiV2.CorsProperty.AllowCredentials``.
            :param allow_headers: ``CfnApiV2.CorsProperty.AllowHeaders``.
            :param allow_methods: ``CfnApiV2.CorsProperty.AllowMethods``.
            :param allow_origins: ``CfnApiV2.CorsProperty.AllowOrigins``.
            :param expose_headers: ``CfnApiV2.CorsProperty.ExposeHeaders``.
            :param max_age: ``CfnApiV2.CorsProperty.MaxAge``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html
            stability
            :stability: deprecated
            """
            self._values = {
            }
            if allow_credentials is not None: self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None: self._values["allow_headers"] = allow_headers
            if allow_methods is not None: self._values["allow_methods"] = allow_methods
            if allow_origins is not None: self._values["allow_origins"] = allow_origins
            if expose_headers is not None: self._values["expose_headers"] = expose_headers
            if max_age is not None: self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnApiV2.CorsProperty.AllowCredentials``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowcredentials
            stability
            :stability: deprecated
            """
            return self._values.get('allow_credentials')

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnApiV2.CorsProperty.AllowHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowheaders
            stability
            :stability: deprecated
            """
            return self._values.get('allow_headers')

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[str]]:
            """``CfnApiV2.CorsProperty.AllowMethods``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowmethods
            stability
            :stability: deprecated
            """
            return self._values.get('allow_methods')

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[str]]:
            """``CfnApiV2.CorsProperty.AllowOrigins``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-alloworigins
            stability
            :stability: deprecated
            """
            return self._values.get('allow_origins')

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnApiV2.CorsProperty.ExposeHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-exposeheaders
            stability
            :stability: deprecated
            """
            return self._values.get('expose_headers')

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            """``CfnApiV2.CorsProperty.MaxAge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-maxage
            stability
            :stability: deprecated
            """
            return self._values.get('max_age')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CorsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnApiV2Props", jsii_struct_bases=[], name_mapping={'api_key_selection_expression': 'apiKeySelectionExpression', 'base_path': 'basePath', 'body': 'body', 'body_s3_location': 'bodyS3Location', 'cors_configuration': 'corsConfiguration', 'credentials_arn': 'credentialsArn', 'description': 'description', 'disable_schema_validation': 'disableSchemaValidation', 'fail_on_warnings': 'failOnWarnings', 'name': 'name', 'protocol_type': 'protocolType', 'route_key': 'routeKey', 'route_selection_expression': 'routeSelectionExpression', 'tags': 'tags', 'target': 'target', 'version': 'version'})
class CfnApiV2Props():
    def __init__(self, *, api_key_selection_expression: typing.Optional[str]=None, base_path: typing.Optional[str]=None, body: typing.Any=None, body_s3_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnApiV2.BodyS3LocationProperty"]]]=None, cors_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnApiV2.CorsProperty"]]]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, disable_schema_validation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, fail_on_warnings: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, name: typing.Optional[str]=None, protocol_type: typing.Optional[str]=None, route_key: typing.Optional[str]=None, route_selection_expression: typing.Optional[str]=None, tags: typing.Any=None, target: typing.Optional[str]=None, version: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Api``.

        :param api_key_selection_expression: ``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.
        :param base_path: ``AWS::ApiGatewayV2::Api.BasePath``.
        :param body: ``AWS::ApiGatewayV2::Api.Body``.
        :param body_s3_location: ``AWS::ApiGatewayV2::Api.BodyS3Location``.
        :param cors_configuration: ``AWS::ApiGatewayV2::Api.CorsConfiguration``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Api.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Api.Description``.
        :param disable_schema_validation: ``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.
        :param fail_on_warnings: ``AWS::ApiGatewayV2::Api.FailOnWarnings``.
        :param name: ``AWS::ApiGatewayV2::Api.Name``.
        :param protocol_type: ``AWS::ApiGatewayV2::Api.ProtocolType``.
        :param route_key: ``AWS::ApiGatewayV2::Api.RouteKey``.
        :param route_selection_expression: ``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.
        :param tags: ``AWS::ApiGatewayV2::Api.Tags``.
        :param target: ``AWS::ApiGatewayV2::Api.Target``.
        :param version: ``AWS::ApiGatewayV2::Api.Version``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
        stability
        :stability: deprecated
        """
        self._values = {
        }
        if api_key_selection_expression is not None: self._values["api_key_selection_expression"] = api_key_selection_expression
        if base_path is not None: self._values["base_path"] = base_path
        if body is not None: self._values["body"] = body
        if body_s3_location is not None: self._values["body_s3_location"] = body_s3_location
        if cors_configuration is not None: self._values["cors_configuration"] = cors_configuration
        if credentials_arn is not None: self._values["credentials_arn"] = credentials_arn
        if description is not None: self._values["description"] = description
        if disable_schema_validation is not None: self._values["disable_schema_validation"] = disable_schema_validation
        if fail_on_warnings is not None: self._values["fail_on_warnings"] = fail_on_warnings
        if name is not None: self._values["name"] = name
        if protocol_type is not None: self._values["protocol_type"] = protocol_type
        if route_key is not None: self._values["route_key"] = route_key
        if route_selection_expression is not None: self._values["route_selection_expression"] = route_selection_expression
        if tags is not None: self._values["tags"] = tags
        if target is not None: self._values["target"] = target
        if version is not None: self._values["version"] = version

    @builtins.property
    def api_key_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('api_key_selection_expression')

    @builtins.property
    def base_path(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.BasePath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        stability
        :stability: deprecated
        """
        return self._values.get('base_path')

    @builtins.property
    def body(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Body``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        stability
        :stability: deprecated
        """
        return self._values.get('body')

    @builtins.property
    def body_s3_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnApiV2.BodyS3LocationProperty"]]]:
        """``AWS::ApiGatewayV2::Api.BodyS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        stability
        :stability: deprecated
        """
        return self._values.get('body_s3_location')

    @builtins.property
    def cors_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnApiV2.CorsProperty"]]]:
        """``AWS::ApiGatewayV2::Api.CorsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        stability
        :stability: deprecated
        """
        return self._values.get('cors_configuration')

    @builtins.property
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        stability
        :stability: deprecated
        """
        return self._values.get('credentials_arn')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        stability
        :stability: deprecated
        """
        return self._values.get('description')

    @builtins.property
    def disable_schema_validation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        stability
        :stability: deprecated
        """
        return self._values.get('disable_schema_validation')

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Api.FailOnWarnings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        stability
        :stability: deprecated
        """
        return self._values.get('fail_on_warnings')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        stability
        :stability: deprecated
        """
        return self._values.get('name')

    @builtins.property
    def protocol_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ProtocolType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        stability
        :stability: deprecated
        """
        return self._values.get('protocol_type')

    @builtins.property
    def route_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        stability
        :stability: deprecated
        """
        return self._values.get('route_key')

    @builtins.property
    def route_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('route_selection_expression')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        stability
        :stability: deprecated
        """
        return self._values.get('tags')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        stability
        :stability: deprecated
        """
        return self._values.get('target')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        stability
        :stability: deprecated
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApiV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAuthorizer(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizer"):
    """A CloudFormation ``AWS::ApiGateway::Authorizer``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Authorizer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api_id: str, type: str, authorizer_credentials: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number]=None, authorizer_uri: typing.Optional[str]=None, auth_type: typing.Optional[str]=None, identity_source: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, name: typing.Optional[str]=None, provider_arns: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::ApiGateway::Authorizer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rest_api_id: ``AWS::ApiGateway::Authorizer.RestApiId``.
        :param type: ``AWS::ApiGateway::Authorizer.Type``.
        :param authorizer_credentials: ``AWS::ApiGateway::Authorizer.AuthorizerCredentials``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGateway::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGateway::Authorizer.AuthorizerUri``.
        :param auth_type: ``AWS::ApiGateway::Authorizer.AuthType``.
        :param identity_source: ``AWS::ApiGateway::Authorizer.IdentitySource``.
        :param identity_validation_expression: ``AWS::ApiGateway::Authorizer.IdentityValidationExpression``.
        :param name: ``AWS::ApiGateway::Authorizer.Name``.
        :param provider_arns: ``AWS::ApiGateway::Authorizer.ProviderARNs``.
        """
        props = CfnAuthorizerProps(rest_api_id=rest_api_id, type=type, authorizer_credentials=authorizer_credentials, authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds, authorizer_uri=authorizer_uri, auth_type=auth_type, identity_source=identity_source, identity_validation_expression=identity_validation_expression, name=name, provider_arns=provider_arns)

        jsii.create(CfnAuthorizer, self, [scope, id, props])

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
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Authorizer.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::ApiGateway::Authorizer.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentials")
    def authorizer_credentials(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.AuthorizerCredentials``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizercredentials
        """
        return jsii.get(self, "authorizerCredentials")

    @authorizer_credentials.setter
    def authorizer_credentials(self, value: typing.Optional[str]):
        jsii.set(self, "authorizerCredentials", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGateway::Authorizer.AuthorizerResultTtlInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizerresultttlinseconds
        """
        return jsii.get(self, "authorizerResultTtlInSeconds")

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "authorizerResultTtlInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.AuthorizerUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizeruri
        """
        return jsii.get(self, "authorizerUri")

    @authorizer_uri.setter
    def authorizer_uri(self, value: typing.Optional[str]):
        jsii.set(self, "authorizerUri", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authtype
        """
        return jsii.get(self, "authType")

    @auth_type.setter
    def auth_type(self, value: typing.Optional[str]):
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="identitySource")
    def identity_source(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.IdentitySource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-identitysource
        """
        return jsii.get(self, "identitySource")

    @identity_source.setter
    def identity_source(self, value: typing.Optional[str]):
        jsii.set(self, "identitySource", value)

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.IdentityValidationExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-identityvalidationexpression
        """
        return jsii.get(self, "identityValidationExpression")

    @identity_validation_expression.setter
    def identity_validation_expression(self, value: typing.Optional[str]):
        jsii.set(self, "identityValidationExpression", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="providerArns")
    def provider_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGateway::Authorizer.ProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-providerarns
        """
        return jsii.get(self, "providerArns")

    @provider_arns.setter
    def provider_arns(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "providerArns", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerProps", jsii_struct_bases=[], name_mapping={'rest_api_id': 'restApiId', 'type': 'type', 'authorizer_credentials': 'authorizerCredentials', 'authorizer_result_ttl_in_seconds': 'authorizerResultTtlInSeconds', 'authorizer_uri': 'authorizerUri', 'auth_type': 'authType', 'identity_source': 'identitySource', 'identity_validation_expression': 'identityValidationExpression', 'name': 'name', 'provider_arns': 'providerArns'})
class CfnAuthorizerProps():
    def __init__(self, *, rest_api_id: str, type: str, authorizer_credentials: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number]=None, authorizer_uri: typing.Optional[str]=None, auth_type: typing.Optional[str]=None, identity_source: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, name: typing.Optional[str]=None, provider_arns: typing.Optional[typing.List[str]]=None):
        """Properties for defining a ``AWS::ApiGateway::Authorizer``.

        :param rest_api_id: ``AWS::ApiGateway::Authorizer.RestApiId``.
        :param type: ``AWS::ApiGateway::Authorizer.Type``.
        :param authorizer_credentials: ``AWS::ApiGateway::Authorizer.AuthorizerCredentials``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGateway::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGateway::Authorizer.AuthorizerUri``.
        :param auth_type: ``AWS::ApiGateway::Authorizer.AuthType``.
        :param identity_source: ``AWS::ApiGateway::Authorizer.IdentitySource``.
        :param identity_validation_expression: ``AWS::ApiGateway::Authorizer.IdentityValidationExpression``.
        :param name: ``AWS::ApiGateway::Authorizer.Name``.
        :param provider_arns: ``AWS::ApiGateway::Authorizer.ProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html
        """
        self._values = {
            'rest_api_id': rest_api_id,
            'type': type,
        }
        if authorizer_credentials is not None: self._values["authorizer_credentials"] = authorizer_credentials
        if authorizer_result_ttl_in_seconds is not None: self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if authorizer_uri is not None: self._values["authorizer_uri"] = authorizer_uri
        if auth_type is not None: self._values["auth_type"] = auth_type
        if identity_source is not None: self._values["identity_source"] = identity_source
        if identity_validation_expression is not None: self._values["identity_validation_expression"] = identity_validation_expression
        if name is not None: self._values["name"] = name
        if provider_arns is not None: self._values["provider_arns"] = provider_arns

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Authorizer.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def type(self) -> str:
        """``AWS::ApiGateway::Authorizer.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-type
        """
        return self._values.get('type')

    @builtins.property
    def authorizer_credentials(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.AuthorizerCredentials``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizercredentials
        """
        return self._values.get('authorizer_credentials')

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGateway::Authorizer.AuthorizerResultTtlInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizerresultttlinseconds
        """
        return self._values.get('authorizer_result_ttl_in_seconds')

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.AuthorizerUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizeruri
        """
        return self._values.get('authorizer_uri')

    @builtins.property
    def auth_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authtype
        """
        return self._values.get('auth_type')

    @builtins.property
    def identity_source(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.IdentitySource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-identitysource
        """
        return self._values.get('identity_source')

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.IdentityValidationExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-identityvalidationexpression
        """
        return self._values.get('identity_validation_expression')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Authorizer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-name
        """
        return self._values.get('name')

    @builtins.property
    def provider_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGateway::Authorizer.ProviderARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-providerarns
        """
        return self._values.get('provider_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAuthorizerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAuthorizerV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Authorizer``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Authorizer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, authorizer_type: str, identity_source: typing.List[str], name: str, authorizer_credentials_arn: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number]=None, authorizer_uri: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, jwt_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["JWTConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Authorizer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Authorizer.ApiId``.
        :param authorizer_type: ``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.
        :param identity_source: ``AWS::ApiGatewayV2::Authorizer.IdentitySource``.
        :param name: ``AWS::ApiGatewayV2::Authorizer.Name``.
        :param authorizer_credentials_arn: ``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.
        :param identity_validation_expression: ``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.
        :param jwt_configuration: ``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        stability
        :stability: deprecated
        """
        props = CfnAuthorizerV2Props(api_id=api_id, authorizer_type=authorizer_type, identity_source=identity_source, name=name, authorizer_credentials_arn=authorizer_credentials_arn, authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds, authorizer_uri=authorizer_uri, identity_validation_expression=identity_validation_expression, jwt_configuration=jwt_configuration)

        jsii.create(CfnAuthorizerV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerType")
    def authorizer_type(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizerType")

    @authorizer_type.setter
    def authorizer_type(self, value: str):
        jsii.set(self, "authorizerType", value)

    @builtins.property
    @jsii.member(jsii_name="identitySource")
    def identity_source(self) -> typing.List[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentitySource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        stability
        :stability: deprecated
        """
        return jsii.get(self, "identitySource")

    @identity_source.setter
    def identity_source(self, value: typing.List[str]):
        jsii.set(self, "identitySource", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        stability
        :stability: deprecated
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialsArn")
    def authorizer_credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizerCredentialsArn")

    @authorizer_credentials_arn.setter
    def authorizer_credentials_arn(self, value: typing.Optional[str]):
        jsii.set(self, "authorizerCredentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizerResultTtlInSeconds")

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "authorizerResultTtlInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizerUri")

    @authorizer_uri.setter
    def authorizer_uri(self, value: typing.Optional[str]):
        jsii.set(self, "authorizerUri", value)

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "identityValidationExpression")

    @identity_validation_expression.setter
    def identity_validation_expression(self, value: typing.Optional[str]):
        jsii.set(self, "identityValidationExpression", value)

    @builtins.property
    @jsii.member(jsii_name="jwtConfiguration")
    def jwt_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["JWTConfigurationProperty"]]]:
        """``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        stability
        :stability: deprecated
        """
        return jsii.get(self, "jwtConfiguration")

    @jwt_configuration.setter
    def jwt_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["JWTConfigurationProperty"]]]):
        jsii.set(self, "jwtConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerV2.JWTConfigurationProperty", jsii_struct_bases=[], name_mapping={'audience': 'audience', 'issuer': 'issuer'})
    class JWTConfigurationProperty():
        def __init__(self, *, audience: typing.Optional[typing.List[str]]=None, issuer: typing.Optional[str]=None):
            """
            :param audience: ``CfnAuthorizerV2.JWTConfigurationProperty.Audience``.
            :param issuer: ``CfnAuthorizerV2.JWTConfigurationProperty.Issuer``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html
            stability
            :stability: deprecated
            """
            self._values = {
            }
            if audience is not None: self._values["audience"] = audience
            if issuer is not None: self._values["issuer"] = issuer

        @builtins.property
        def audience(self) -> typing.Optional[typing.List[str]]:
            """``CfnAuthorizerV2.JWTConfigurationProperty.Audience``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-audience
            stability
            :stability: deprecated
            """
            return self._values.get('audience')

        @builtins.property
        def issuer(self) -> typing.Optional[str]:
            """``CfnAuthorizerV2.JWTConfigurationProperty.Issuer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-issuer
            stability
            :stability: deprecated
            """
            return self._values.get('issuer')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'JWTConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnAuthorizerV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'authorizer_type': 'authorizerType', 'identity_source': 'identitySource', 'name': 'name', 'authorizer_credentials_arn': 'authorizerCredentialsArn', 'authorizer_result_ttl_in_seconds': 'authorizerResultTtlInSeconds', 'authorizer_uri': 'authorizerUri', 'identity_validation_expression': 'identityValidationExpression', 'jwt_configuration': 'jwtConfiguration'})
class CfnAuthorizerV2Props():
    def __init__(self, *, api_id: str, authorizer_type: str, identity_source: typing.List[str], name: str, authorizer_credentials_arn: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number]=None, authorizer_uri: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, jwt_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAuthorizerV2.JWTConfigurationProperty"]]]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Authorizer``.

        :param api_id: ``AWS::ApiGatewayV2::Authorizer.ApiId``.
        :param authorizer_type: ``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.
        :param identity_source: ``AWS::ApiGatewayV2::Authorizer.IdentitySource``.
        :param name: ``AWS::ApiGatewayV2::Authorizer.Name``.
        :param authorizer_credentials_arn: ``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.
        :param identity_validation_expression: ``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.
        :param jwt_configuration: ``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'authorizer_type': authorizer_type,
            'identity_source': identity_source,
            'name': name,
        }
        if authorizer_credentials_arn is not None: self._values["authorizer_credentials_arn"] = authorizer_credentials_arn
        if authorizer_result_ttl_in_seconds is not None: self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if authorizer_uri is not None: self._values["authorizer_uri"] = authorizer_uri
        if identity_validation_expression is not None: self._values["identity_validation_expression"] = identity_validation_expression
        if jwt_configuration is not None: self._values["jwt_configuration"] = jwt_configuration

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def authorizer_type(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        stability
        :stability: deprecated
        """
        return self._values.get('authorizer_type')

    @builtins.property
    def identity_source(self) -> typing.List[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentitySource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        stability
        :stability: deprecated
        """
        return self._values.get('identity_source')

    @builtins.property
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        stability
        :stability: deprecated
        """
        return self._values.get('name')

    @builtins.property
    def authorizer_credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        stability
        :stability: deprecated
        """
        return self._values.get('authorizer_credentials_arn')

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        stability
        :stability: deprecated
        """
        return self._values.get('authorizer_result_ttl_in_seconds')

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        stability
        :stability: deprecated
        """
        return self._values.get('authorizer_uri')

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        stability
        :stability: deprecated
        """
        return self._values.get('identity_validation_expression')

    @builtins.property
    def jwt_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAuthorizerV2.JWTConfigurationProperty"]]]:
        """``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        stability
        :stability: deprecated
        """
        return self._values.get('jwt_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAuthorizerV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnBasePathMapping(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnBasePathMapping"):
    """A CloudFormation ``AWS::ApiGateway::BasePathMapping``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::BasePathMapping
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, base_path: typing.Optional[str]=None, rest_api_id: typing.Optional[str]=None, stage: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::BasePathMapping``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::ApiGateway::BasePathMapping.DomainName``.
        :param base_path: ``AWS::ApiGateway::BasePathMapping.BasePath``.
        :param rest_api_id: ``AWS::ApiGateway::BasePathMapping.RestApiId``.
        :param stage: ``AWS::ApiGateway::BasePathMapping.Stage``.
        """
        props = CfnBasePathMappingProps(domain_name=domain_name, base_path=base_path, rest_api_id=rest_api_id, stage=stage)

        jsii.create(CfnBasePathMapping, self, [scope, id, props])

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
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::ApiGateway::BasePathMapping.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str):
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="basePath")
    def base_path(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::BasePathMapping.BasePath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-basepath
        """
        return jsii.get(self, "basePath")

    @base_path.setter
    def base_path(self, value: typing.Optional[str]):
        jsii.set(self, "basePath", value)

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::BasePathMapping.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: typing.Optional[str]):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::BasePathMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-stage
        """
        return jsii.get(self, "stage")

    @stage.setter
    def stage(self, value: typing.Optional[str]):
        jsii.set(self, "stage", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnBasePathMappingProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'base_path': 'basePath', 'rest_api_id': 'restApiId', 'stage': 'stage'})
class CfnBasePathMappingProps():
    def __init__(self, *, domain_name: str, base_path: typing.Optional[str]=None, rest_api_id: typing.Optional[str]=None, stage: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::BasePathMapping``.

        :param domain_name: ``AWS::ApiGateway::BasePathMapping.DomainName``.
        :param base_path: ``AWS::ApiGateway::BasePathMapping.BasePath``.
        :param rest_api_id: ``AWS::ApiGateway::BasePathMapping.RestApiId``.
        :param stage: ``AWS::ApiGateway::BasePathMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html
        """
        self._values = {
            'domain_name': domain_name,
        }
        if base_path is not None: self._values["base_path"] = base_path
        if rest_api_id is not None: self._values["rest_api_id"] = rest_api_id
        if stage is not None: self._values["stage"] = stage

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::ApiGateway::BasePathMapping.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def base_path(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::BasePathMapping.BasePath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-basepath
        """
        return self._values.get('base_path')

    @builtins.property
    def rest_api_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::BasePathMapping.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def stage(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::BasePathMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-stage
        """
        return self._values.get('stage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBasePathMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnClientCertificate(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnClientCertificate"):
    """A CloudFormation ``AWS::ApiGateway::ClientCertificate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::ClientCertificate
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ApiGateway::ClientCertificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::ApiGateway::ClientCertificate.Description``.
        :param tags: ``AWS::ApiGateway::ClientCertificate.Tags``.
        """
        props = CfnClientCertificateProps(description=description, tags=tags)

        jsii.create(CfnClientCertificate, self, [scope, id, props])

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
        """``AWS::ApiGateway::ClientCertificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html#cfn-apigateway-clientcertificate-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ClientCertificate.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html#cfn-apigateway-clientcertificate-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnClientCertificateProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'tags': 'tags'})
class CfnClientCertificateProps():
    def __init__(self, *, description: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ApiGateway::ClientCertificate``.

        :param description: ``AWS::ApiGateway::ClientCertificate.Description``.
        :param tags: ``AWS::ApiGateway::ClientCertificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::ClientCertificate.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html#cfn-apigateway-clientcertificate-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApiGateway::ClientCertificate.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html#cfn-apigateway-clientcertificate-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClientCertificateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeployment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDeployment"):
    """A CloudFormation ``AWS::ApiGateway::Deployment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Deployment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api_id: str, deployment_canary_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentCanarySettingsProperty"]]]=None, description: typing.Optional[str]=None, stage_description: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StageDescriptionProperty"]]]=None, stage_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rest_api_id: ``AWS::ApiGateway::Deployment.RestApiId``.
        :param deployment_canary_settings: ``AWS::ApiGateway::Deployment.DeploymentCanarySettings``.
        :param description: ``AWS::ApiGateway::Deployment.Description``.
        :param stage_description: ``AWS::ApiGateway::Deployment.StageDescription``.
        :param stage_name: ``AWS::ApiGateway::Deployment.StageName``.
        """
        props = CfnDeploymentProps(rest_api_id=rest_api_id, deployment_canary_settings=deployment_canary_settings, description=description, stage_description=stage_description, stage_name=stage_name)

        jsii.create(CfnDeployment, self, [scope, id, props])

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
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Deployment.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentCanarySettings")
    def deployment_canary_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentCanarySettingsProperty"]]]:
        """``AWS::ApiGateway::Deployment.DeploymentCanarySettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-deploymentcanarysettings
        """
        return jsii.get(self, "deploymentCanarySettings")

    @deployment_canary_settings.setter
    def deployment_canary_settings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentCanarySettingsProperty"]]]):
        jsii.set(self, "deploymentCanarySettings", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="stageDescription")
    def stage_description(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StageDescriptionProperty"]]]:
        """``AWS::ApiGateway::Deployment.StageDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-stagedescription
        """
        return jsii.get(self, "stageDescription")

    @stage_description.setter
    def stage_description(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StageDescriptionProperty"]]]):
        jsii.set(self, "stageDescription", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-stagename
        """
        return jsii.get(self, "stageName")

    @stage_name.setter
    def stage_name(self, value: typing.Optional[str]):
        jsii.set(self, "stageName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.AccessLogSettingProperty", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'format': 'format'})
    class AccessLogSettingProperty():
        def __init__(self, *, destination_arn: typing.Optional[str]=None, format: typing.Optional[str]=None):
            """
            :param destination_arn: ``CfnDeployment.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnDeployment.AccessLogSettingProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-accesslogsetting.html
            """
            self._values = {
            }
            if destination_arn is not None: self._values["destination_arn"] = destination_arn
            if format is not None: self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[str]:
            """``CfnDeployment.AccessLogSettingProperty.DestinationArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-accesslogsetting.html#cfn-apigateway-deployment-accesslogsetting-destinationarn
            """
            return self._values.get('destination_arn')

        @builtins.property
        def format(self) -> typing.Optional[str]:
            """``CfnDeployment.AccessLogSettingProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-accesslogsetting.html#cfn-apigateway-deployment-accesslogsetting-format
            """
            return self._values.get('format')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessLogSettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.CanarySettingProperty", jsii_struct_bases=[], name_mapping={'percent_traffic': 'percentTraffic', 'stage_variable_overrides': 'stageVariableOverrides', 'use_stage_cache': 'useStageCache'})
    class CanarySettingProperty():
        def __init__(self, *, percent_traffic: typing.Optional[jsii.Number]=None, stage_variable_overrides: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, use_stage_cache: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param percent_traffic: ``CfnDeployment.CanarySettingProperty.PercentTraffic``.
            :param stage_variable_overrides: ``CfnDeployment.CanarySettingProperty.StageVariableOverrides``.
            :param use_stage_cache: ``CfnDeployment.CanarySettingProperty.UseStageCache``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html
            """
            self._values = {
            }
            if percent_traffic is not None: self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None: self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None: self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.CanarySettingProperty.PercentTraffic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html#cfn-apigateway-deployment-canarysetting-percenttraffic
            """
            return self._values.get('percent_traffic')

        @builtins.property
        def stage_variable_overrides(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnDeployment.CanarySettingProperty.StageVariableOverrides``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html#cfn-apigateway-deployment-canarysetting-stagevariableoverrides
            """
            return self._values.get('stage_variable_overrides')

        @builtins.property
        def use_stage_cache(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.CanarySettingProperty.UseStageCache``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html#cfn-apigateway-deployment-canarysetting-usestagecache
            """
            return self._values.get('use_stage_cache')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CanarySettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.DeploymentCanarySettingsProperty", jsii_struct_bases=[], name_mapping={'percent_traffic': 'percentTraffic', 'stage_variable_overrides': 'stageVariableOverrides', 'use_stage_cache': 'useStageCache'})
    class DeploymentCanarySettingsProperty():
        def __init__(self, *, percent_traffic: typing.Optional[jsii.Number]=None, stage_variable_overrides: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, use_stage_cache: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param percent_traffic: ``CfnDeployment.DeploymentCanarySettingsProperty.PercentTraffic``.
            :param stage_variable_overrides: ``CfnDeployment.DeploymentCanarySettingsProperty.StageVariableOverrides``.
            :param use_stage_cache: ``CfnDeployment.DeploymentCanarySettingsProperty.UseStageCache``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html
            """
            self._values = {
            }
            if percent_traffic is not None: self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None: self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None: self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.DeploymentCanarySettingsProperty.PercentTraffic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html#cfn-apigateway-deployment-deploymentcanarysettings-percenttraffic
            """
            return self._values.get('percent_traffic')

        @builtins.property
        def stage_variable_overrides(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnDeployment.DeploymentCanarySettingsProperty.StageVariableOverrides``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html#cfn-apigateway-deployment-deploymentcanarysettings-stagevariableoverrides
            """
            return self._values.get('stage_variable_overrides')

        @builtins.property
        def use_stage_cache(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.DeploymentCanarySettingsProperty.UseStageCache``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html#cfn-apigateway-deployment-deploymentcanarysettings-usestagecache
            """
            return self._values.get('use_stage_cache')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentCanarySettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.MethodSettingProperty", jsii_struct_bases=[], name_mapping={'cache_data_encrypted': 'cacheDataEncrypted', 'cache_ttl_in_seconds': 'cacheTtlInSeconds', 'caching_enabled': 'cachingEnabled', 'data_trace_enabled': 'dataTraceEnabled', 'http_method': 'httpMethod', 'logging_level': 'loggingLevel', 'metrics_enabled': 'metricsEnabled', 'resource_path': 'resourcePath', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit'})
    class MethodSettingProperty():
        def __init__(self, *, cache_data_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache_ttl_in_seconds: typing.Optional[jsii.Number]=None, caching_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, data_trace_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, http_method: typing.Optional[str]=None, logging_level: typing.Optional[str]=None, metrics_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, resource_path: typing.Optional[str]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None):
            """
            :param cache_data_encrypted: ``CfnDeployment.MethodSettingProperty.CacheDataEncrypted``.
            :param cache_ttl_in_seconds: ``CfnDeployment.MethodSettingProperty.CacheTtlInSeconds``.
            :param caching_enabled: ``CfnDeployment.MethodSettingProperty.CachingEnabled``.
            :param data_trace_enabled: ``CfnDeployment.MethodSettingProperty.DataTraceEnabled``.
            :param http_method: ``CfnDeployment.MethodSettingProperty.HttpMethod``.
            :param logging_level: ``CfnDeployment.MethodSettingProperty.LoggingLevel``.
            :param metrics_enabled: ``CfnDeployment.MethodSettingProperty.MetricsEnabled``.
            :param resource_path: ``CfnDeployment.MethodSettingProperty.ResourcePath``.
            :param throttling_burst_limit: ``CfnDeployment.MethodSettingProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnDeployment.MethodSettingProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html
            """
            self._values = {
            }
            if cache_data_encrypted is not None: self._values["cache_data_encrypted"] = cache_data_encrypted
            if cache_ttl_in_seconds is not None: self._values["cache_ttl_in_seconds"] = cache_ttl_in_seconds
            if caching_enabled is not None: self._values["caching_enabled"] = caching_enabled
            if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
            if http_method is not None: self._values["http_method"] = http_method
            if logging_level is not None: self._values["logging_level"] = logging_level
            if metrics_enabled is not None: self._values["metrics_enabled"] = metrics_enabled
            if resource_path is not None: self._values["resource_path"] = resource_path
            if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def cache_data_encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.MethodSettingProperty.CacheDataEncrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-cachedataencrypted
            """
            return self._values.get('cache_data_encrypted')

        @builtins.property
        def cache_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.MethodSettingProperty.CacheTtlInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-cachettlinseconds
            """
            return self._values.get('cache_ttl_in_seconds')

        @builtins.property
        def caching_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.MethodSettingProperty.CachingEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-cachingenabled
            """
            return self._values.get('caching_enabled')

        @builtins.property
        def data_trace_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.MethodSettingProperty.DataTraceEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-datatraceenabled
            """
            return self._values.get('data_trace_enabled')

        @builtins.property
        def http_method(self) -> typing.Optional[str]:
            """``CfnDeployment.MethodSettingProperty.HttpMethod``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-httpmethod
            """
            return self._values.get('http_method')

        @builtins.property
        def logging_level(self) -> typing.Optional[str]:
            """``CfnDeployment.MethodSettingProperty.LoggingLevel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-logginglevel
            """
            return self._values.get('logging_level')

        @builtins.property
        def metrics_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.MethodSettingProperty.MetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-metricsenabled
            """
            return self._values.get('metrics_enabled')

        @builtins.property
        def resource_path(self) -> typing.Optional[str]:
            """``CfnDeployment.MethodSettingProperty.ResourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-resourcepath
            """
            return self._values.get('resource_path')

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.MethodSettingProperty.ThrottlingBurstLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-throttlingburstlimit
            """
            return self._values.get('throttling_burst_limit')

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.MethodSettingProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription-methodsetting.html#cfn-apigateway-deployment-stagedescription-methodsetting-throttlingratelimit
            """
            return self._values.get('throttling_rate_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MethodSettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeployment.StageDescriptionProperty", jsii_struct_bases=[], name_mapping={'access_log_setting': 'accessLogSetting', 'cache_cluster_enabled': 'cacheClusterEnabled', 'cache_cluster_size': 'cacheClusterSize', 'cache_data_encrypted': 'cacheDataEncrypted', 'cache_ttl_in_seconds': 'cacheTtlInSeconds', 'caching_enabled': 'cachingEnabled', 'canary_setting': 'canarySetting', 'client_certificate_id': 'clientCertificateId', 'data_trace_enabled': 'dataTraceEnabled', 'description': 'description', 'documentation_version': 'documentationVersion', 'logging_level': 'loggingLevel', 'method_settings': 'methodSettings', 'metrics_enabled': 'metricsEnabled', 'tags': 'tags', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit', 'tracing_enabled': 'tracingEnabled', 'variables': 'variables'})
    class StageDescriptionProperty():
        def __init__(self, *, access_log_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.AccessLogSettingProperty"]]]=None, cache_cluster_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache_cluster_size: typing.Optional[str]=None, cache_data_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache_ttl_in_seconds: typing.Optional[jsii.Number]=None, caching_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, canary_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.CanarySettingProperty"]]]=None, client_certificate_id: typing.Optional[str]=None, data_trace_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, logging_level: typing.Optional[str]=None, method_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeployment.MethodSettingProperty"]]]]]=None, metrics_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None, tracing_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, variables: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None):
            """
            :param access_log_setting: ``CfnDeployment.StageDescriptionProperty.AccessLogSetting``.
            :param cache_cluster_enabled: ``CfnDeployment.StageDescriptionProperty.CacheClusterEnabled``.
            :param cache_cluster_size: ``CfnDeployment.StageDescriptionProperty.CacheClusterSize``.
            :param cache_data_encrypted: ``CfnDeployment.StageDescriptionProperty.CacheDataEncrypted``.
            :param cache_ttl_in_seconds: ``CfnDeployment.StageDescriptionProperty.CacheTtlInSeconds``.
            :param caching_enabled: ``CfnDeployment.StageDescriptionProperty.CachingEnabled``.
            :param canary_setting: ``CfnDeployment.StageDescriptionProperty.CanarySetting``.
            :param client_certificate_id: ``CfnDeployment.StageDescriptionProperty.ClientCertificateId``.
            :param data_trace_enabled: ``CfnDeployment.StageDescriptionProperty.DataTraceEnabled``.
            :param description: ``CfnDeployment.StageDescriptionProperty.Description``.
            :param documentation_version: ``CfnDeployment.StageDescriptionProperty.DocumentationVersion``.
            :param logging_level: ``CfnDeployment.StageDescriptionProperty.LoggingLevel``.
            :param method_settings: ``CfnDeployment.StageDescriptionProperty.MethodSettings``.
            :param metrics_enabled: ``CfnDeployment.StageDescriptionProperty.MetricsEnabled``.
            :param tags: ``CfnDeployment.StageDescriptionProperty.Tags``.
            :param throttling_burst_limit: ``CfnDeployment.StageDescriptionProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnDeployment.StageDescriptionProperty.ThrottlingRateLimit``.
            :param tracing_enabled: ``CfnDeployment.StageDescriptionProperty.TracingEnabled``.
            :param variables: ``CfnDeployment.StageDescriptionProperty.Variables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html
            """
            self._values = {
            }
            if access_log_setting is not None: self._values["access_log_setting"] = access_log_setting
            if cache_cluster_enabled is not None: self._values["cache_cluster_enabled"] = cache_cluster_enabled
            if cache_cluster_size is not None: self._values["cache_cluster_size"] = cache_cluster_size
            if cache_data_encrypted is not None: self._values["cache_data_encrypted"] = cache_data_encrypted
            if cache_ttl_in_seconds is not None: self._values["cache_ttl_in_seconds"] = cache_ttl_in_seconds
            if caching_enabled is not None: self._values["caching_enabled"] = caching_enabled
            if canary_setting is not None: self._values["canary_setting"] = canary_setting
            if client_certificate_id is not None: self._values["client_certificate_id"] = client_certificate_id
            if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
            if description is not None: self._values["description"] = description
            if documentation_version is not None: self._values["documentation_version"] = documentation_version
            if logging_level is not None: self._values["logging_level"] = logging_level
            if method_settings is not None: self._values["method_settings"] = method_settings
            if metrics_enabled is not None: self._values["metrics_enabled"] = metrics_enabled
            if tags is not None: self._values["tags"] = tags
            if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit
            if tracing_enabled is not None: self._values["tracing_enabled"] = tracing_enabled
            if variables is not None: self._values["variables"] = variables

        @builtins.property
        def access_log_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.AccessLogSettingProperty"]]]:
            """``CfnDeployment.StageDescriptionProperty.AccessLogSetting``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-accesslogsetting
            """
            return self._values.get('access_log_setting')

        @builtins.property
        def cache_cluster_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.StageDescriptionProperty.CacheClusterEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cacheclusterenabled
            """
            return self._values.get('cache_cluster_enabled')

        @builtins.property
        def cache_cluster_size(self) -> typing.Optional[str]:
            """``CfnDeployment.StageDescriptionProperty.CacheClusterSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cacheclustersize
            """
            return self._values.get('cache_cluster_size')

        @builtins.property
        def cache_data_encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.StageDescriptionProperty.CacheDataEncrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cachedataencrypted
            """
            return self._values.get('cache_data_encrypted')

        @builtins.property
        def cache_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.StageDescriptionProperty.CacheTtlInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cachettlinseconds
            """
            return self._values.get('cache_ttl_in_seconds')

        @builtins.property
        def caching_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.StageDescriptionProperty.CachingEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cachingenabled
            """
            return self._values.get('caching_enabled')

        @builtins.property
        def canary_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.CanarySettingProperty"]]]:
            """``CfnDeployment.StageDescriptionProperty.CanarySetting``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-canarysetting
            """
            return self._values.get('canary_setting')

        @builtins.property
        def client_certificate_id(self) -> typing.Optional[str]:
            """``CfnDeployment.StageDescriptionProperty.ClientCertificateId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-clientcertificateid
            """
            return self._values.get('client_certificate_id')

        @builtins.property
        def data_trace_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.StageDescriptionProperty.DataTraceEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-datatraceenabled
            """
            return self._values.get('data_trace_enabled')

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """``CfnDeployment.StageDescriptionProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-description
            """
            return self._values.get('description')

        @builtins.property
        def documentation_version(self) -> typing.Optional[str]:
            """``CfnDeployment.StageDescriptionProperty.DocumentationVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-documentationversion
            """
            return self._values.get('documentation_version')

        @builtins.property
        def logging_level(self) -> typing.Optional[str]:
            """``CfnDeployment.StageDescriptionProperty.LoggingLevel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-logginglevel
            """
            return self._values.get('logging_level')

        @builtins.property
        def method_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeployment.MethodSettingProperty"]]]]]:
            """``CfnDeployment.StageDescriptionProperty.MethodSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-methodsettings
            """
            return self._values.get('method_settings')

        @builtins.property
        def metrics_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.StageDescriptionProperty.MetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-metricsenabled
            """
            return self._values.get('metrics_enabled')

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
            """``CfnDeployment.StageDescriptionProperty.Tags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-tags
            """
            return self._values.get('tags')

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.StageDescriptionProperty.ThrottlingBurstLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-throttlingburstlimit
            """
            return self._values.get('throttling_burst_limit')

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnDeployment.StageDescriptionProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-throttlingratelimit
            """
            return self._values.get('throttling_rate_limit')

        @builtins.property
        def tracing_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeployment.StageDescriptionProperty.TracingEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-tracingenabled
            """
            return self._values.get('tracing_enabled')

        @builtins.property
        def variables(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnDeployment.StageDescriptionProperty.Variables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-variables
            """
            return self._values.get('variables')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StageDescriptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeploymentProps", jsii_struct_bases=[], name_mapping={'rest_api_id': 'restApiId', 'deployment_canary_settings': 'deploymentCanarySettings', 'description': 'description', 'stage_description': 'stageDescription', 'stage_name': 'stageName'})
class CfnDeploymentProps():
    def __init__(self, *, rest_api_id: str, deployment_canary_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.DeploymentCanarySettingsProperty"]]]=None, description: typing.Optional[str]=None, stage_description: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.StageDescriptionProperty"]]]=None, stage_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::Deployment``.

        :param rest_api_id: ``AWS::ApiGateway::Deployment.RestApiId``.
        :param deployment_canary_settings: ``AWS::ApiGateway::Deployment.DeploymentCanarySettings``.
        :param description: ``AWS::ApiGateway::Deployment.Description``.
        :param stage_description: ``AWS::ApiGateway::Deployment.StageDescription``.
        :param stage_name: ``AWS::ApiGateway::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html
        """
        self._values = {
            'rest_api_id': rest_api_id,
        }
        if deployment_canary_settings is not None: self._values["deployment_canary_settings"] = deployment_canary_settings
        if description is not None: self._values["description"] = description
        if stage_description is not None: self._values["stage_description"] = stage_description
        if stage_name is not None: self._values["stage_name"] = stage_name

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Deployment.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def deployment_canary_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.DeploymentCanarySettingsProperty"]]]:
        """``AWS::ApiGateway::Deployment.DeploymentCanarySettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-deploymentcanarysettings
        """
        return self._values.get('deployment_canary_settings')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-description
        """
        return self._values.get('description')

    @builtins.property
    def stage_description(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeployment.StageDescriptionProperty"]]]:
        """``AWS::ApiGateway::Deployment.StageDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-stagedescription
        """
        return self._values.get('stage_description')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-stagename
        """
        return self._values.get('stage_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeploymentV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDeploymentV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Deployment``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Deployment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, description: typing.Optional[str]=None, stage_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Deployment.ApiId``.
        :param description: ``AWS::ApiGatewayV2::Deployment.Description``.
        :param stage_name: ``AWS::ApiGatewayV2::Deployment.StageName``.

        stability
        :stability: deprecated
        """
        props = CfnDeploymentV2Props(api_id=api_id, description=description, stage_name=stage_name)

        jsii.create(CfnDeploymentV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Deployment.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        stability
        :stability: deprecated
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        stability
        :stability: deprecated
        """
        return jsii.get(self, "stageName")

    @stage_name.setter
    def stage_name(self, value: typing.Optional[str]):
        jsii.set(self, "stageName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDeploymentV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'description': 'description', 'stage_name': 'stageName'})
class CfnDeploymentV2Props():
    def __init__(self, *, api_id: str, description: typing.Optional[str]=None, stage_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Deployment``.

        :param api_id: ``AWS::ApiGatewayV2::Deployment.ApiId``.
        :param description: ``AWS::ApiGatewayV2::Deployment.Description``.
        :param stage_name: ``AWS::ApiGatewayV2::Deployment.StageName``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
        }
        if description is not None: self._values["description"] = description
        if stage_name is not None: self._values["stage_name"] = stage_name

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Deployment.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        stability
        :stability: deprecated
        """
        return self._values.get('description')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        stability
        :stability: deprecated
        """
        return self._values.get('stage_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDocumentationPart(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationPart"):
    """A CloudFormation ``AWS::ApiGateway::DocumentationPart``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::DocumentationPart
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, location: typing.Union["LocationProperty", aws_cdk.core.IResolvable], properties: str, rest_api_id: str) -> None:
        """Create a new ``AWS::ApiGateway::DocumentationPart``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param location: ``AWS::ApiGateway::DocumentationPart.Location``.
        :param properties: ``AWS::ApiGateway::DocumentationPart.Properties``.
        :param rest_api_id: ``AWS::ApiGateway::DocumentationPart.RestApiId``.
        """
        props = CfnDocumentationPartProps(location=location, properties=properties, rest_api_id=rest_api_id)

        jsii.create(CfnDocumentationPart, self, [scope, id, props])

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
    @jsii.member(jsii_name="location")
    def location(self) -> typing.Union["LocationProperty", aws_cdk.core.IResolvable]:
        """``AWS::ApiGateway::DocumentationPart.Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-location
        """
        return jsii.get(self, "location")

    @location.setter
    def location(self, value: typing.Union["LocationProperty", aws_cdk.core.IResolvable]):
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> str:
        """``AWS::ApiGateway::DocumentationPart.Properties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-properties
        """
        return jsii.get(self, "properties")

    @properties.setter
    def properties(self, value: str):
        jsii.set(self, "properties", value)

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::DocumentationPart.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationPart.LocationProperty", jsii_struct_bases=[], name_mapping={'method': 'method', 'name': 'name', 'path': 'path', 'status_code': 'statusCode', 'type': 'type'})
    class LocationProperty():
        def __init__(self, *, method: typing.Optional[str]=None, name: typing.Optional[str]=None, path: typing.Optional[str]=None, status_code: typing.Optional[str]=None, type: typing.Optional[str]=None):
            """
            :param method: ``CfnDocumentationPart.LocationProperty.Method``.
            :param name: ``CfnDocumentationPart.LocationProperty.Name``.
            :param path: ``CfnDocumentationPart.LocationProperty.Path``.
            :param status_code: ``CfnDocumentationPart.LocationProperty.StatusCode``.
            :param type: ``CfnDocumentationPart.LocationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html
            """
            self._values = {
            }
            if method is not None: self._values["method"] = method
            if name is not None: self._values["name"] = name
            if path is not None: self._values["path"] = path
            if status_code is not None: self._values["status_code"] = status_code
            if type is not None: self._values["type"] = type

        @builtins.property
        def method(self) -> typing.Optional[str]:
            """``CfnDocumentationPart.LocationProperty.Method``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-method
            """
            return self._values.get('method')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnDocumentationPart.LocationProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-name
            """
            return self._values.get('name')

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnDocumentationPart.LocationProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-path
            """
            return self._values.get('path')

        @builtins.property
        def status_code(self) -> typing.Optional[str]:
            """``CfnDocumentationPart.LocationProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnDocumentationPart.LocationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationPartProps", jsii_struct_bases=[], name_mapping={'location': 'location', 'properties': 'properties', 'rest_api_id': 'restApiId'})
class CfnDocumentationPartProps():
    def __init__(self, *, location: typing.Union["CfnDocumentationPart.LocationProperty", aws_cdk.core.IResolvable], properties: str, rest_api_id: str):
        """Properties for defining a ``AWS::ApiGateway::DocumentationPart``.

        :param location: ``AWS::ApiGateway::DocumentationPart.Location``.
        :param properties: ``AWS::ApiGateway::DocumentationPart.Properties``.
        :param rest_api_id: ``AWS::ApiGateway::DocumentationPart.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html
        """
        self._values = {
            'location': location,
            'properties': properties,
            'rest_api_id': rest_api_id,
        }

    @builtins.property
    def location(self) -> typing.Union["CfnDocumentationPart.LocationProperty", aws_cdk.core.IResolvable]:
        """``AWS::ApiGateway::DocumentationPart.Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-location
        """
        return self._values.get('location')

    @builtins.property
    def properties(self) -> str:
        """``AWS::ApiGateway::DocumentationPart.Properties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-properties
        """
        return self._values.get('properties')

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::DocumentationPart.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-restapiid
        """
        return self._values.get('rest_api_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDocumentationPartProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDocumentationVersion(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationVersion"):
    """A CloudFormation ``AWS::ApiGateway::DocumentationVersion``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::DocumentationVersion
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, documentation_version: str, rest_api_id: str, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::DocumentationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param documentation_version: ``AWS::ApiGateway::DocumentationVersion.DocumentationVersion``.
        :param rest_api_id: ``AWS::ApiGateway::DocumentationVersion.RestApiId``.
        :param description: ``AWS::ApiGateway::DocumentationVersion.Description``.
        """
        props = CfnDocumentationVersionProps(documentation_version=documentation_version, rest_api_id=rest_api_id, description=description)

        jsii.create(CfnDocumentationVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="documentationVersion")
    def documentation_version(self) -> str:
        """``AWS::ApiGateway::DocumentationVersion.DocumentationVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-documentationversion
        """
        return jsii.get(self, "documentationVersion")

    @documentation_version.setter
    def documentation_version(self, value: str):
        jsii.set(self, "documentationVersion", value)

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::DocumentationVersion.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DocumentationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDocumentationVersionProps", jsii_struct_bases=[], name_mapping={'documentation_version': 'documentationVersion', 'rest_api_id': 'restApiId', 'description': 'description'})
class CfnDocumentationVersionProps():
    def __init__(self, *, documentation_version: str, rest_api_id: str, description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::DocumentationVersion``.

        :param documentation_version: ``AWS::ApiGateway::DocumentationVersion.DocumentationVersion``.
        :param rest_api_id: ``AWS::ApiGateway::DocumentationVersion.RestApiId``.
        :param description: ``AWS::ApiGateway::DocumentationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html
        """
        self._values = {
            'documentation_version': documentation_version,
            'rest_api_id': rest_api_id,
        }
        if description is not None: self._values["description"] = description

    @builtins.property
    def documentation_version(self) -> str:
        """``AWS::ApiGateway::DocumentationVersion.DocumentationVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-documentationversion
        """
        return self._values.get('documentation_version')

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::DocumentationVersion.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DocumentationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDocumentationVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDomainName(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDomainName"):
    """A CloudFormation ``AWS::ApiGateway::DomainName``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::DomainName
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, certificate_arn: typing.Optional[str]=None, endpoint_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EndpointConfigurationProperty"]]]=None, regional_certificate_arn: typing.Optional[str]=None, security_policy: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ApiGateway::DomainName``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::ApiGateway::DomainName.DomainName``.
        :param certificate_arn: ``AWS::ApiGateway::DomainName.CertificateArn``.
        :param endpoint_configuration: ``AWS::ApiGateway::DomainName.EndpointConfiguration``.
        :param regional_certificate_arn: ``AWS::ApiGateway::DomainName.RegionalCertificateArn``.
        :param security_policy: ``AWS::ApiGateway::DomainName.SecurityPolicy``.
        :param tags: ``AWS::ApiGateway::DomainName.Tags``.
        """
        props = CfnDomainNameProps(domain_name=domain_name, certificate_arn=certificate_arn, endpoint_configuration=endpoint_configuration, regional_certificate_arn=regional_certificate_arn, security_policy=security_policy, tags=tags)

        jsii.create(CfnDomainName, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDistributionDomainName")
    def attr_distribution_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DistributionDomainName
        """
        return jsii.get(self, "attrDistributionDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrDistributionHostedZoneId")
    def attr_distribution_hosted_zone_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DistributionHostedZoneId
        """
        return jsii.get(self, "attrDistributionHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalDomainName
        """
        return jsii.get(self, "attrRegionalDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalHostedZoneId")
    def attr_regional_hosted_zone_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalHostedZoneId
        """
        return jsii.get(self, "attrRegionalHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGateway::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::ApiGateway::DomainName.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str):
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DomainName.CertificateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-certificatearn
        """
        return jsii.get(self, "certificateArn")

    @certificate_arn.setter
    def certificate_arn(self, value: typing.Optional[str]):
        jsii.set(self, "certificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EndpointConfigurationProperty"]]]:
        """``AWS::ApiGateway::DomainName.EndpointConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-endpointconfiguration
        """
        return jsii.get(self, "endpointConfiguration")

    @endpoint_configuration.setter
    def endpoint_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EndpointConfigurationProperty"]]]):
        jsii.set(self, "endpointConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="regionalCertificateArn")
    def regional_certificate_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DomainName.RegionalCertificateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-regionalcertificatearn
        """
        return jsii.get(self, "regionalCertificateArn")

    @regional_certificate_arn.setter
    def regional_certificate_arn(self, value: typing.Optional[str]):
        jsii.set(self, "regionalCertificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DomainName.SecurityPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-securitypolicy
        """
        return jsii.get(self, "securityPolicy")

    @security_policy.setter
    def security_policy(self, value: typing.Optional[str]):
        jsii.set(self, "securityPolicy", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDomainName.EndpointConfigurationProperty", jsii_struct_bases=[], name_mapping={'types': 'types'})
    class EndpointConfigurationProperty():
        def __init__(self, *, types: typing.Optional[typing.List[str]]=None):
            """
            :param types: ``CfnDomainName.EndpointConfigurationProperty.Types``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-endpointconfiguration.html
            """
            self._values = {
            }
            if types is not None: self._values["types"] = types

        @builtins.property
        def types(self) -> typing.Optional[typing.List[str]]:
            """``CfnDomainName.EndpointConfigurationProperty.Types``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-endpointconfiguration.html#cfn-apigateway-domainname-endpointconfiguration-types
            """
            return self._values.get('types')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EndpointConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDomainNameProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'certificate_arn': 'certificateArn', 'endpoint_configuration': 'endpointConfiguration', 'regional_certificate_arn': 'regionalCertificateArn', 'security_policy': 'securityPolicy', 'tags': 'tags'})
class CfnDomainNameProps():
    def __init__(self, *, domain_name: str, certificate_arn: typing.Optional[str]=None, endpoint_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDomainName.EndpointConfigurationProperty"]]]=None, regional_certificate_arn: typing.Optional[str]=None, security_policy: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ApiGateway::DomainName``.

        :param domain_name: ``AWS::ApiGateway::DomainName.DomainName``.
        :param certificate_arn: ``AWS::ApiGateway::DomainName.CertificateArn``.
        :param endpoint_configuration: ``AWS::ApiGateway::DomainName.EndpointConfiguration``.
        :param regional_certificate_arn: ``AWS::ApiGateway::DomainName.RegionalCertificateArn``.
        :param security_policy: ``AWS::ApiGateway::DomainName.SecurityPolicy``.
        :param tags: ``AWS::ApiGateway::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html
        """
        self._values = {
            'domain_name': domain_name,
        }
        if certificate_arn is not None: self._values["certificate_arn"] = certificate_arn
        if endpoint_configuration is not None: self._values["endpoint_configuration"] = endpoint_configuration
        if regional_certificate_arn is not None: self._values["regional_certificate_arn"] = regional_certificate_arn
        if security_policy is not None: self._values["security_policy"] = security_policy
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::ApiGateway::DomainName.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def certificate_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DomainName.CertificateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-certificatearn
        """
        return self._values.get('certificate_arn')

    @builtins.property
    def endpoint_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDomainName.EndpointConfigurationProperty"]]]:
        """``AWS::ApiGateway::DomainName.EndpointConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-endpointconfiguration
        """
        return self._values.get('endpoint_configuration')

    @builtins.property
    def regional_certificate_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DomainName.RegionalCertificateArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-regionalcertificatearn
        """
        return self._values.get('regional_certificate_arn')

    @builtins.property
    def security_policy(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::DomainName.SecurityPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-securitypolicy
        """
        return self._values.get('security_policy')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApiGateway::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDomainNameProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDomainNameV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnDomainNameV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::DomainName``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::DomainName
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, domain_name_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DomainNameConfigurationProperty"]]]]]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::DomainName``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::ApiGatewayV2::DomainName.DomainName``.
        :param domain_name_configurations: ``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.
        :param tags: ``AWS::ApiGatewayV2::DomainName.Tags``.

        stability
        :stability: deprecated
        """
        props = CfnDomainNameV2Props(domain_name=domain_name, domain_name_configurations=domain_name_configurations, tags=tags)

        jsii.create(CfnDomainNameV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> str:
        """
        stability
        :stability: deprecated
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalDomainName
        """
        return jsii.get(self, "attrRegionalDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalHostedZoneId")
    def attr_regional_hosted_zone_id(self) -> str:
        """
        stability
        :stability: deprecated
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalHostedZoneId
        """
        return jsii.get(self, "attrRegionalHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        stability
        :stability: deprecated
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::DomainName.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        stability
        :stability: deprecated
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str):
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="domainNameConfigurations")
    def domain_name_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DomainNameConfigurationProperty"]]]]]:
        """``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        stability
        :stability: deprecated
        """
        return jsii.get(self, "domainNameConfigurations")

    @domain_name_configurations.setter
    def domain_name_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DomainNameConfigurationProperty"]]]]]):
        jsii.set(self, "domainNameConfigurations", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDomainNameV2.DomainNameConfigurationProperty", jsii_struct_bases=[], name_mapping={'certificate_arn': 'certificateArn', 'certificate_name': 'certificateName', 'endpoint_type': 'endpointType'})
    class DomainNameConfigurationProperty():
        def __init__(self, *, certificate_arn: typing.Optional[str]=None, certificate_name: typing.Optional[str]=None, endpoint_type: typing.Optional[str]=None):
            """
            :param certificate_arn: ``CfnDomainNameV2.DomainNameConfigurationProperty.CertificateArn``.
            :param certificate_name: ``CfnDomainNameV2.DomainNameConfigurationProperty.CertificateName``.
            :param endpoint_type: ``CfnDomainNameV2.DomainNameConfigurationProperty.EndpointType``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html
            stability
            :stability: deprecated
            """
            self._values = {
            }
            if certificate_arn is not None: self._values["certificate_arn"] = certificate_arn
            if certificate_name is not None: self._values["certificate_name"] = certificate_name
            if endpoint_type is not None: self._values["endpoint_type"] = endpoint_type

        @builtins.property
        def certificate_arn(self) -> typing.Optional[str]:
            """``CfnDomainNameV2.DomainNameConfigurationProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatearn
            stability
            :stability: deprecated
            """
            return self._values.get('certificate_arn')

        @builtins.property
        def certificate_name(self) -> typing.Optional[str]:
            """``CfnDomainNameV2.DomainNameConfigurationProperty.CertificateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatename
            stability
            :stability: deprecated
            """
            return self._values.get('certificate_name')

        @builtins.property
        def endpoint_type(self) -> typing.Optional[str]:
            """``CfnDomainNameV2.DomainNameConfigurationProperty.EndpointType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-endpointtype
            stability
            :stability: deprecated
            """
            return self._values.get('endpoint_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DomainNameConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnDomainNameV2Props", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'domain_name_configurations': 'domainNameConfigurations', 'tags': 'tags'})
class CfnDomainNameV2Props():
    def __init__(self, *, domain_name: str, domain_name_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainNameV2.DomainNameConfigurationProperty"]]]]]=None, tags: typing.Any=None):
        """Properties for defining a ``AWS::ApiGatewayV2::DomainName``.

        :param domain_name: ``AWS::ApiGatewayV2::DomainName.DomainName``.
        :param domain_name_configurations: ``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.
        :param tags: ``AWS::ApiGatewayV2::DomainName.Tags``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
        stability
        :stability: deprecated
        """
        self._values = {
            'domain_name': domain_name,
        }
        if domain_name_configurations is not None: self._values["domain_name_configurations"] = domain_name_configurations
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::DomainName.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        stability
        :stability: deprecated
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_name_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainNameV2.DomainNameConfigurationProperty"]]]]]:
        """``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        stability
        :stability: deprecated
        """
        return self._values.get('domain_name_configurations')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        stability
        :stability: deprecated
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDomainNameV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnGatewayResponse(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnGatewayResponse"):
    """A CloudFormation ``AWS::ApiGateway::GatewayResponse``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::GatewayResponse
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, response_type: str, rest_api_id: str, response_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, response_templates: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, status_code: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::GatewayResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param response_type: ``AWS::ApiGateway::GatewayResponse.ResponseType``.
        :param rest_api_id: ``AWS::ApiGateway::GatewayResponse.RestApiId``.
        :param response_parameters: ``AWS::ApiGateway::GatewayResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGateway::GatewayResponse.ResponseTemplates``.
        :param status_code: ``AWS::ApiGateway::GatewayResponse.StatusCode``.
        """
        props = CfnGatewayResponseProps(response_type=response_type, rest_api_id=rest_api_id, response_parameters=response_parameters, response_templates=response_templates, status_code=status_code)

        jsii.create(CfnGatewayResponse, self, [scope, id, props])

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
    @jsii.member(jsii_name="responseType")
    def response_type(self) -> str:
        """``AWS::ApiGateway::GatewayResponse.ResponseType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responsetype
        """
        return jsii.get(self, "responseType")

    @response_type.setter
    def response_type(self, value: str):
        jsii.set(self, "responseType", value)

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::GatewayResponse.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::GatewayResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responseparameters
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter
    def response_parameters(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="responseTemplates")
    def response_templates(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::GatewayResponse.ResponseTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responsetemplates
        """
        return jsii.get(self, "responseTemplates")

    @response_templates.setter
    def response_templates(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        jsii.set(self, "responseTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::GatewayResponse.StatusCode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-statuscode
        """
        return jsii.get(self, "statusCode")

    @status_code.setter
    def status_code(self, value: typing.Optional[str]):
        jsii.set(self, "statusCode", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnGatewayResponseProps", jsii_struct_bases=[], name_mapping={'response_type': 'responseType', 'rest_api_id': 'restApiId', 'response_parameters': 'responseParameters', 'response_templates': 'responseTemplates', 'status_code': 'statusCode'})
class CfnGatewayResponseProps():
    def __init__(self, *, response_type: str, rest_api_id: str, response_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, response_templates: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, status_code: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::GatewayResponse``.

        :param response_type: ``AWS::ApiGateway::GatewayResponse.ResponseType``.
        :param rest_api_id: ``AWS::ApiGateway::GatewayResponse.RestApiId``.
        :param response_parameters: ``AWS::ApiGateway::GatewayResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGateway::GatewayResponse.ResponseTemplates``.
        :param status_code: ``AWS::ApiGateway::GatewayResponse.StatusCode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html
        """
        self._values = {
            'response_type': response_type,
            'rest_api_id': rest_api_id,
        }
        if response_parameters is not None: self._values["response_parameters"] = response_parameters
        if response_templates is not None: self._values["response_templates"] = response_templates
        if status_code is not None: self._values["status_code"] = status_code

    @builtins.property
    def response_type(self) -> str:
        """``AWS::ApiGateway::GatewayResponse.ResponseType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responsetype
        """
        return self._values.get('response_type')

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::GatewayResponse.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def response_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::GatewayResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responseparameters
        """
        return self._values.get('response_parameters')

    @builtins.property
    def response_templates(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::GatewayResponse.ResponseTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responsetemplates
        """
        return self._values.get('response_templates')

    @builtins.property
    def status_code(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::GatewayResponse.StatusCode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-statuscode
        """
        return self._values.get('status_code')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnGatewayResponseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegrationResponseV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationResponseV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::IntegrationResponse``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::IntegrationResponse
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, integration_id: str, integration_response_key: str, content_handling_strategy: typing.Optional[str]=None, response_parameters: typing.Any=None, response_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.
        :param integration_id: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.
        :param integration_response_key: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.
        :param response_parameters: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        stability
        :stability: deprecated
        """
        props = CfnIntegrationResponseV2Props(api_id=api_id, integration_id=integration_id, integration_response_key=integration_response_key, content_handling_strategy=content_handling_strategy, response_parameters=response_parameters, response_templates=response_templates, template_selection_expression=template_selection_expression)

        jsii.create(CfnIntegrationResponseV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "integrationId")

    @integration_id.setter
    def integration_id(self, value: str):
        jsii.set(self, "integrationId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationResponseKey")
    def integration_response_key(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        stability
        :stability: deprecated
        """
        return jsii.get(self, "integrationResponseKey")

    @integration_response_key.setter
    def integration_response_key(self, value: str):
        jsii.set(self, "integrationResponseKey", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        stability
        :stability: deprecated
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter
    def response_parameters(self, value: typing.Any):
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="responseTemplates")
    def response_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        stability
        :stability: deprecated
        """
        return jsii.get(self, "responseTemplates")

    @response_templates.setter
    def response_templates(self, value: typing.Any):
        jsii.set(self, "responseTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        stability
        :stability: deprecated
        """
        return jsii.get(self, "contentHandlingStrategy")

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: typing.Optional[str]):
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "templateSelectionExpression")

    @template_selection_expression.setter
    def template_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "templateSelectionExpression", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationResponseV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'integration_id': 'integrationId', 'integration_response_key': 'integrationResponseKey', 'content_handling_strategy': 'contentHandlingStrategy', 'response_parameters': 'responseParameters', 'response_templates': 'responseTemplates', 'template_selection_expression': 'templateSelectionExpression'})
class CfnIntegrationResponseV2Props():
    def __init__(self, *, api_id: str, integration_id: str, integration_response_key: str, content_handling_strategy: typing.Optional[str]=None, response_parameters: typing.Any=None, response_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param api_id: ``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.
        :param integration_id: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.
        :param integration_response_key: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.
        :param response_parameters: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'integration_id': integration_id,
            'integration_response_key': integration_response_key,
        }
        if content_handling_strategy is not None: self._values["content_handling_strategy"] = content_handling_strategy
        if response_parameters is not None: self._values["response_parameters"] = response_parameters
        if response_templates is not None: self._values["response_templates"] = response_templates
        if template_selection_expression is not None: self._values["template_selection_expression"] = template_selection_expression

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def integration_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        stability
        :stability: deprecated
        """
        return self._values.get('integration_id')

    @builtins.property
    def integration_response_key(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        stability
        :stability: deprecated
        """
        return self._values.get('integration_response_key')

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        stability
        :stability: deprecated
        """
        return self._values.get('content_handling_strategy')

    @builtins.property
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        stability
        :stability: deprecated
        """
        return self._values.get('response_parameters')

    @builtins.property
    def response_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        stability
        :stability: deprecated
        """
        return self._values.get('response_templates')

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('template_selection_expression')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIntegrationResponseV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegrationV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Integration``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Integration
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, integration_type: str, connection_type: typing.Optional[str]=None, content_handling_strategy: typing.Optional[str]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, integration_method: typing.Optional[str]=None, integration_uri: typing.Optional[str]=None, passthrough_behavior: typing.Optional[str]=None, payload_format_version: typing.Optional[str]=None, request_parameters: typing.Any=None, request_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None, timeout_in_millis: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Integration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Integration.ApiId``.
        :param integration_type: ``AWS::ApiGatewayV2::Integration.IntegrationType``.
        :param connection_type: ``AWS::ApiGatewayV2::Integration.ConnectionType``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Integration.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Integration.Description``.
        :param integration_method: ``AWS::ApiGatewayV2::Integration.IntegrationMethod``.
        :param integration_uri: ``AWS::ApiGatewayV2::Integration.IntegrationUri``.
        :param passthrough_behavior: ``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.
        :param payload_format_version: ``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.
        :param request_parameters: ``AWS::ApiGatewayV2::Integration.RequestParameters``.
        :param request_templates: ``AWS::ApiGatewayV2::Integration.RequestTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.
        :param timeout_in_millis: ``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        stability
        :stability: deprecated
        """
        props = CfnIntegrationV2Props(api_id=api_id, integration_type=integration_type, connection_type=connection_type, content_handling_strategy=content_handling_strategy, credentials_arn=credentials_arn, description=description, integration_method=integration_method, integration_uri=integration_uri, passthrough_behavior=passthrough_behavior, payload_format_version=payload_format_version, request_parameters=request_parameters, request_templates=request_templates, template_selection_expression=template_selection_expression, timeout_in_millis=timeout_in_millis)

        jsii.create(CfnIntegrationV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Integration.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> str:
        """``AWS::ApiGatewayV2::Integration.IntegrationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        stability
        :stability: deprecated
        """
        return jsii.get(self, "integrationType")

    @integration_type.setter
    def integration_type(self, value: str):
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        stability
        :stability: deprecated
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter
    def request_parameters(self, value: typing.Any):
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="requestTemplates")
    def request_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        stability
        :stability: deprecated
        """
        return jsii.get(self, "requestTemplates")

    @request_templates.setter
    def request_templates(self, value: typing.Any):
        jsii.set(self, "requestTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        stability
        :stability: deprecated
        """
        return jsii.get(self, "connectionType")

    @connection_type.setter
    def connection_type(self, value: typing.Optional[str]):
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        stability
        :stability: deprecated
        """
        return jsii.get(self, "contentHandlingStrategy")

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: typing.Optional[str]):
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        stability
        :stability: deprecated
        """
        return jsii.get(self, "credentialsArn")

    @credentials_arn.setter
    def credentials_arn(self, value: typing.Optional[str]):
        jsii.set(self, "credentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        stability
        :stability: deprecated
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="integrationMethod")
    def integration_method(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        stability
        :stability: deprecated
        """
        return jsii.get(self, "integrationMethod")

    @integration_method.setter
    def integration_method(self, value: typing.Optional[str]):
        jsii.set(self, "integrationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationUri")
    def integration_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        stability
        :stability: deprecated
        """
        return jsii.get(self, "integrationUri")

    @integration_uri.setter
    def integration_uri(self, value: typing.Optional[str]):
        jsii.set(self, "integrationUri", value)

    @builtins.property
    @jsii.member(jsii_name="passthroughBehavior")
    def passthrough_behavior(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        stability
        :stability: deprecated
        """
        return jsii.get(self, "passthroughBehavior")

    @passthrough_behavior.setter
    def passthrough_behavior(self, value: typing.Optional[str]):
        jsii.set(self, "passthroughBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def payload_format_version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        stability
        :stability: deprecated
        """
        return jsii.get(self, "payloadFormatVersion")

    @payload_format_version.setter
    def payload_format_version(self, value: typing.Optional[str]):
        jsii.set(self, "payloadFormatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "templateSelectionExpression")

    @template_selection_expression.setter
    def template_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "templateSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMillis")
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        stability
        :stability: deprecated
        """
        return jsii.get(self, "timeoutInMillis")

    @timeout_in_millis.setter
    def timeout_in_millis(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "timeoutInMillis", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnIntegrationV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'integration_type': 'integrationType', 'connection_type': 'connectionType', 'content_handling_strategy': 'contentHandlingStrategy', 'credentials_arn': 'credentialsArn', 'description': 'description', 'integration_method': 'integrationMethod', 'integration_uri': 'integrationUri', 'passthrough_behavior': 'passthroughBehavior', 'payload_format_version': 'payloadFormatVersion', 'request_parameters': 'requestParameters', 'request_templates': 'requestTemplates', 'template_selection_expression': 'templateSelectionExpression', 'timeout_in_millis': 'timeoutInMillis'})
class CfnIntegrationV2Props():
    def __init__(self, *, api_id: str, integration_type: str, connection_type: typing.Optional[str]=None, content_handling_strategy: typing.Optional[str]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, integration_method: typing.Optional[str]=None, integration_uri: typing.Optional[str]=None, passthrough_behavior: typing.Optional[str]=None, payload_format_version: typing.Optional[str]=None, request_parameters: typing.Any=None, request_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None, timeout_in_millis: typing.Optional[jsii.Number]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Integration``.

        :param api_id: ``AWS::ApiGatewayV2::Integration.ApiId``.
        :param integration_type: ``AWS::ApiGatewayV2::Integration.IntegrationType``.
        :param connection_type: ``AWS::ApiGatewayV2::Integration.ConnectionType``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Integration.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Integration.Description``.
        :param integration_method: ``AWS::ApiGatewayV2::Integration.IntegrationMethod``.
        :param integration_uri: ``AWS::ApiGatewayV2::Integration.IntegrationUri``.
        :param passthrough_behavior: ``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.
        :param payload_format_version: ``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.
        :param request_parameters: ``AWS::ApiGatewayV2::Integration.RequestParameters``.
        :param request_templates: ``AWS::ApiGatewayV2::Integration.RequestTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.
        :param timeout_in_millis: ``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'integration_type': integration_type,
        }
        if connection_type is not None: self._values["connection_type"] = connection_type
        if content_handling_strategy is not None: self._values["content_handling_strategy"] = content_handling_strategy
        if credentials_arn is not None: self._values["credentials_arn"] = credentials_arn
        if description is not None: self._values["description"] = description
        if integration_method is not None: self._values["integration_method"] = integration_method
        if integration_uri is not None: self._values["integration_uri"] = integration_uri
        if passthrough_behavior is not None: self._values["passthrough_behavior"] = passthrough_behavior
        if payload_format_version is not None: self._values["payload_format_version"] = payload_format_version
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if request_templates is not None: self._values["request_templates"] = request_templates
        if template_selection_expression is not None: self._values["template_selection_expression"] = template_selection_expression
        if timeout_in_millis is not None: self._values["timeout_in_millis"] = timeout_in_millis

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Integration.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def integration_type(self) -> str:
        """``AWS::ApiGatewayV2::Integration.IntegrationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        stability
        :stability: deprecated
        """
        return self._values.get('integration_type')

    @builtins.property
    def connection_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        stability
        :stability: deprecated
        """
        return self._values.get('connection_type')

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        stability
        :stability: deprecated
        """
        return self._values.get('content_handling_strategy')

    @builtins.property
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        stability
        :stability: deprecated
        """
        return self._values.get('credentials_arn')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        stability
        :stability: deprecated
        """
        return self._values.get('description')

    @builtins.property
    def integration_method(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        stability
        :stability: deprecated
        """
        return self._values.get('integration_method')

    @builtins.property
    def integration_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        stability
        :stability: deprecated
        """
        return self._values.get('integration_uri')

    @builtins.property
    def passthrough_behavior(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        stability
        :stability: deprecated
        """
        return self._values.get('passthrough_behavior')

    @builtins.property
    def payload_format_version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        stability
        :stability: deprecated
        """
        return self._values.get('payload_format_version')

    @builtins.property
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        stability
        :stability: deprecated
        """
        return self._values.get('request_parameters')

    @builtins.property
    def request_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        stability
        :stability: deprecated
        """
        return self._values.get('request_templates')

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('template_selection_expression')

    @builtins.property
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        stability
        :stability: deprecated
        """
        return self._values.get('timeout_in_millis')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIntegrationV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMethod(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnMethod"):
    """A CloudFormation ``AWS::ApiGateway::Method``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Method
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, http_method: str, resource_id: str, rest_api_id: str, api_key_required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, integration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["IntegrationProperty"]]]=None, method_responses: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MethodResponseProperty"]]]]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, request_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]=None, request_validator_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::Method``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param http_method: ``AWS::ApiGateway::Method.HttpMethod``.
        :param resource_id: ``AWS::ApiGateway::Method.ResourceId``.
        :param rest_api_id: ``AWS::ApiGateway::Method.RestApiId``.
        :param api_key_required: ``AWS::ApiGateway::Method.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGateway::Method.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGateway::Method.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGateway::Method.AuthorizerId``.
        :param integration: ``AWS::ApiGateway::Method.Integration``.
        :param method_responses: ``AWS::ApiGateway::Method.MethodResponses``.
        :param operation_name: ``AWS::ApiGateway::Method.OperationName``.
        :param request_models: ``AWS::ApiGateway::Method.RequestModels``.
        :param request_parameters: ``AWS::ApiGateway::Method.RequestParameters``.
        :param request_validator_id: ``AWS::ApiGateway::Method.RequestValidatorId``.
        """
        props = CfnMethodProps(http_method=http_method, resource_id=resource_id, rest_api_id=rest_api_id, api_key_required=api_key_required, authorization_scopes=authorization_scopes, authorization_type=authorization_type, authorizer_id=authorizer_id, integration=integration, method_responses=method_responses, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, request_validator_id=request_validator_id)

        jsii.create(CfnMethod, self, [scope, id, props])

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
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> str:
        """``AWS::ApiGateway::Method.HttpMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-httpmethod
        """
        return jsii.get(self, "httpMethod")

    @http_method.setter
    def http_method(self, value: str):
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        """``AWS::ApiGateway::Method.ResourceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-resourceid
        """
        return jsii.get(self, "resourceId")

    @resource_id.setter
    def resource_id(self, value: str):
        jsii.set(self, "resourceId", value)

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Method.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeyRequired")
    def api_key_required(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::Method.ApiKeyRequired``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-apikeyrequired
        """
        return jsii.get(self, "apiKeyRequired")

    @api_key_required.setter
    def api_key_required(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "apiKeyRequired", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationScopes")
    def authorization_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGateway::Method.AuthorizationScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizationscopes
        """
        return jsii.get(self, "authorizationScopes")

    @authorization_scopes.setter
    def authorization_scopes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "authorizationScopes", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.AuthorizationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizationtype
        """
        return jsii.get(self, "authorizationType")

    @authorization_type.setter
    def authorization_type(self, value: typing.Optional[str]):
        jsii.set(self, "authorizationType", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.AuthorizerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizerid
        """
        return jsii.get(self, "authorizerId")

    @authorizer_id.setter
    def authorizer_id(self, value: typing.Optional[str]):
        jsii.set(self, "authorizerId", value)

    @builtins.property
    @jsii.member(jsii_name="integration")
    def integration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["IntegrationProperty"]]]:
        """``AWS::ApiGateway::Method.Integration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-integration
        """
        return jsii.get(self, "integration")

    @integration.setter
    def integration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["IntegrationProperty"]]]):
        jsii.set(self, "integration", value)

    @builtins.property
    @jsii.member(jsii_name="methodResponses")
    def method_responses(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MethodResponseProperty"]]]]]:
        """``AWS::ApiGateway::Method.MethodResponses``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-methodresponses
        """
        return jsii.get(self, "methodResponses")

    @method_responses.setter
    def method_responses(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MethodResponseProperty"]]]]]):
        jsii.set(self, "methodResponses", value)

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.OperationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-operationname
        """
        return jsii.get(self, "operationName")

    @operation_name.setter
    def operation_name(self, value: typing.Optional[str]):
        jsii.set(self, "operationName", value)

    @builtins.property
    @jsii.member(jsii_name="requestModels")
    def request_models(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::Method.RequestModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestmodels
        """
        return jsii.get(self, "requestModels")

    @request_models.setter
    def request_models(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        jsii.set(self, "requestModels", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]:
        """``AWS::ApiGateway::Method.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestparameters
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter
    def request_parameters(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]):
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="requestValidatorId")
    def request_validator_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.RequestValidatorId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestvalidatorid
        """
        return jsii.get(self, "requestValidatorId")

    @request_validator_id.setter
    def request_validator_id(self, value: typing.Optional[str]):
        jsii.set(self, "requestValidatorId", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethod.IntegrationProperty", jsii_struct_bases=[], name_mapping={'cache_key_parameters': 'cacheKeyParameters', 'cache_namespace': 'cacheNamespace', 'connection_id': 'connectionId', 'connection_type': 'connectionType', 'content_handling': 'contentHandling', 'credentials': 'credentials', 'integration_http_method': 'integrationHttpMethod', 'integration_responses': 'integrationResponses', 'passthrough_behavior': 'passthroughBehavior', 'request_parameters': 'requestParameters', 'request_templates': 'requestTemplates', 'timeout_in_millis': 'timeoutInMillis', 'type': 'type', 'uri': 'uri'})
    class IntegrationProperty():
        def __init__(self, *, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_id: typing.Optional[str]=None, connection_type: typing.Optional[str]=None, content_handling: typing.Optional[str]=None, credentials: typing.Optional[str]=None, integration_http_method: typing.Optional[str]=None, integration_responses: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMethod.IntegrationResponseProperty"]]]]]=None, passthrough_behavior: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, request_templates: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, timeout_in_millis: typing.Optional[jsii.Number]=None, type: typing.Optional[str]=None, uri: typing.Optional[str]=None):
            """
            :param cache_key_parameters: ``CfnMethod.IntegrationProperty.CacheKeyParameters``.
            :param cache_namespace: ``CfnMethod.IntegrationProperty.CacheNamespace``.
            :param connection_id: ``CfnMethod.IntegrationProperty.ConnectionId``.
            :param connection_type: ``CfnMethod.IntegrationProperty.ConnectionType``.
            :param content_handling: ``CfnMethod.IntegrationProperty.ContentHandling``.
            :param credentials: ``CfnMethod.IntegrationProperty.Credentials``.
            :param integration_http_method: ``CfnMethod.IntegrationProperty.IntegrationHttpMethod``.
            :param integration_responses: ``CfnMethod.IntegrationProperty.IntegrationResponses``.
            :param passthrough_behavior: ``CfnMethod.IntegrationProperty.PassthroughBehavior``.
            :param request_parameters: ``CfnMethod.IntegrationProperty.RequestParameters``.
            :param request_templates: ``CfnMethod.IntegrationProperty.RequestTemplates``.
            :param timeout_in_millis: ``CfnMethod.IntegrationProperty.TimeoutInMillis``.
            :param type: ``CfnMethod.IntegrationProperty.Type``.
            :param uri: ``CfnMethod.IntegrationProperty.Uri``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html
            """
            self._values = {
            }
            if cache_key_parameters is not None: self._values["cache_key_parameters"] = cache_key_parameters
            if cache_namespace is not None: self._values["cache_namespace"] = cache_namespace
            if connection_id is not None: self._values["connection_id"] = connection_id
            if connection_type is not None: self._values["connection_type"] = connection_type
            if content_handling is not None: self._values["content_handling"] = content_handling
            if credentials is not None: self._values["credentials"] = credentials
            if integration_http_method is not None: self._values["integration_http_method"] = integration_http_method
            if integration_responses is not None: self._values["integration_responses"] = integration_responses
            if passthrough_behavior is not None: self._values["passthrough_behavior"] = passthrough_behavior
            if request_parameters is not None: self._values["request_parameters"] = request_parameters
            if request_templates is not None: self._values["request_templates"] = request_templates
            if timeout_in_millis is not None: self._values["timeout_in_millis"] = timeout_in_millis
            if type is not None: self._values["type"] = type
            if uri is not None: self._values["uri"] = uri

        @builtins.property
        def cache_key_parameters(self) -> typing.Optional[typing.List[str]]:
            """``CfnMethod.IntegrationProperty.CacheKeyParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-cachekeyparameters
            """
            return self._values.get('cache_key_parameters')

        @builtins.property
        def cache_namespace(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.CacheNamespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-cachenamespace
            """
            return self._values.get('cache_namespace')

        @builtins.property
        def connection_id(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.ConnectionId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-connectionid
            """
            return self._values.get('connection_id')

        @builtins.property
        def connection_type(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.ConnectionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-connectiontype
            """
            return self._values.get('connection_type')

        @builtins.property
        def content_handling(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.ContentHandling``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-contenthandling
            """
            return self._values.get('content_handling')

        @builtins.property
        def credentials(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.Credentials``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-credentials
            """
            return self._values.get('credentials')

        @builtins.property
        def integration_http_method(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.IntegrationHttpMethod``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-integrationhttpmethod
            """
            return self._values.get('integration_http_method')

        @builtins.property
        def integration_responses(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMethod.IntegrationResponseProperty"]]]]]:
            """``CfnMethod.IntegrationProperty.IntegrationResponses``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-integrationresponses
            """
            return self._values.get('integration_responses')

        @builtins.property
        def passthrough_behavior(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.PassthroughBehavior``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-passthroughbehavior
            """
            return self._values.get('passthrough_behavior')

        @builtins.property
        def request_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnMethod.IntegrationProperty.RequestParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-requestparameters
            """
            return self._values.get('request_parameters')

        @builtins.property
        def request_templates(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnMethod.IntegrationProperty.RequestTemplates``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-requesttemplates
            """
            return self._values.get('request_templates')

        @builtins.property
        def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
            """``CfnMethod.IntegrationProperty.TimeoutInMillis``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-timeoutinmillis
            """
            return self._values.get('timeout_in_millis')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-type
            """
            return self._values.get('type')

        @builtins.property
        def uri(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationProperty.Uri``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html#cfn-apigateway-method-integration-uri
            """
            return self._values.get('uri')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IntegrationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethod.IntegrationResponseProperty", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'content_handling': 'contentHandling', 'response_parameters': 'responseParameters', 'response_templates': 'responseTemplates', 'selection_pattern': 'selectionPattern'})
    class IntegrationResponseProperty():
        def __init__(self, *, status_code: str, content_handling: typing.Optional[str]=None, response_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, response_templates: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, selection_pattern: typing.Optional[str]=None):
            """
            :param status_code: ``CfnMethod.IntegrationResponseProperty.StatusCode``.
            :param content_handling: ``CfnMethod.IntegrationResponseProperty.ContentHandling``.
            :param response_parameters: ``CfnMethod.IntegrationResponseProperty.ResponseParameters``.
            :param response_templates: ``CfnMethod.IntegrationResponseProperty.ResponseTemplates``.
            :param selection_pattern: ``CfnMethod.IntegrationResponseProperty.SelectionPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration-integrationresponse.html
            """
            self._values = {
                'status_code': status_code,
            }
            if content_handling is not None: self._values["content_handling"] = content_handling
            if response_parameters is not None: self._values["response_parameters"] = response_parameters
            if response_templates is not None: self._values["response_templates"] = response_templates
            if selection_pattern is not None: self._values["selection_pattern"] = selection_pattern

        @builtins.property
        def status_code(self) -> str:
            """``CfnMethod.IntegrationResponseProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration-integrationresponse.html#cfn-apigateway-method-integration-integrationresponse-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def content_handling(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationResponseProperty.ContentHandling``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration-integrationresponse.html#cfn-apigateway-method-integrationresponse-contenthandling
            """
            return self._values.get('content_handling')

        @builtins.property
        def response_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnMethod.IntegrationResponseProperty.ResponseParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration-integrationresponse.html#cfn-apigateway-method-integration-integrationresponse-responseparameters
            """
            return self._values.get('response_parameters')

        @builtins.property
        def response_templates(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnMethod.IntegrationResponseProperty.ResponseTemplates``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration-integrationresponse.html#cfn-apigateway-method-integration-integrationresponse-responsetemplates
            """
            return self._values.get('response_templates')

        @builtins.property
        def selection_pattern(self) -> typing.Optional[str]:
            """``CfnMethod.IntegrationResponseProperty.SelectionPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration-integrationresponse.html#cfn-apigateway-method-integration-integrationresponse-selectionpattern
            """
            return self._values.get('selection_pattern')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IntegrationResponseProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethod.MethodResponseProperty", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'response_models': 'responseModels', 'response_parameters': 'responseParameters'})
    class MethodResponseProperty():
        def __init__(self, *, status_code: str, response_models: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, response_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]=None):
            """
            :param status_code: ``CfnMethod.MethodResponseProperty.StatusCode``.
            :param response_models: ``CfnMethod.MethodResponseProperty.ResponseModels``.
            :param response_parameters: ``CfnMethod.MethodResponseProperty.ResponseParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-methodresponse.html
            """
            self._values = {
                'status_code': status_code,
            }
            if response_models is not None: self._values["response_models"] = response_models
            if response_parameters is not None: self._values["response_parameters"] = response_parameters

        @builtins.property
        def status_code(self) -> str:
            """``CfnMethod.MethodResponseProperty.StatusCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-methodresponse.html#cfn-apigateway-method-methodresponse-statuscode
            """
            return self._values.get('status_code')

        @builtins.property
        def response_models(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnMethod.MethodResponseProperty.ResponseModels``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-methodresponse.html#cfn-apigateway-method-methodresponse-responsemodels
            """
            return self._values.get('response_models')

        @builtins.property
        def response_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]:
            """``CfnMethod.MethodResponseProperty.ResponseParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-methodresponse.html#cfn-apigateway-method-methodresponse-responseparameters
            """
            return self._values.get('response_parameters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MethodResponseProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnMethodProps", jsii_struct_bases=[], name_mapping={'http_method': 'httpMethod', 'resource_id': 'resourceId', 'rest_api_id': 'restApiId', 'api_key_required': 'apiKeyRequired', 'authorization_scopes': 'authorizationScopes', 'authorization_type': 'authorizationType', 'authorizer_id': 'authorizerId', 'integration': 'integration', 'method_responses': 'methodResponses', 'operation_name': 'operationName', 'request_models': 'requestModels', 'request_parameters': 'requestParameters', 'request_validator_id': 'requestValidatorId'})
class CfnMethodProps():
    def __init__(self, *, http_method: str, resource_id: str, rest_api_id: str, api_key_required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, integration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnMethod.IntegrationProperty"]]]=None, method_responses: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMethod.MethodResponseProperty"]]]]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, request_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]=None, request_validator_id: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::Method``.

        :param http_method: ``AWS::ApiGateway::Method.HttpMethod``.
        :param resource_id: ``AWS::ApiGateway::Method.ResourceId``.
        :param rest_api_id: ``AWS::ApiGateway::Method.RestApiId``.
        :param api_key_required: ``AWS::ApiGateway::Method.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGateway::Method.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGateway::Method.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGateway::Method.AuthorizerId``.
        :param integration: ``AWS::ApiGateway::Method.Integration``.
        :param method_responses: ``AWS::ApiGateway::Method.MethodResponses``.
        :param operation_name: ``AWS::ApiGateway::Method.OperationName``.
        :param request_models: ``AWS::ApiGateway::Method.RequestModels``.
        :param request_parameters: ``AWS::ApiGateway::Method.RequestParameters``.
        :param request_validator_id: ``AWS::ApiGateway::Method.RequestValidatorId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html
        """
        self._values = {
            'http_method': http_method,
            'resource_id': resource_id,
            'rest_api_id': rest_api_id,
        }
        if api_key_required is not None: self._values["api_key_required"] = api_key_required
        if authorization_scopes is not None: self._values["authorization_scopes"] = authorization_scopes
        if authorization_type is not None: self._values["authorization_type"] = authorization_type
        if authorizer_id is not None: self._values["authorizer_id"] = authorizer_id
        if integration is not None: self._values["integration"] = integration
        if method_responses is not None: self._values["method_responses"] = method_responses
        if operation_name is not None: self._values["operation_name"] = operation_name
        if request_models is not None: self._values["request_models"] = request_models
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if request_validator_id is not None: self._values["request_validator_id"] = request_validator_id

    @builtins.property
    def http_method(self) -> str:
        """``AWS::ApiGateway::Method.HttpMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-httpmethod
        """
        return self._values.get('http_method')

    @builtins.property
    def resource_id(self) -> str:
        """``AWS::ApiGateway::Method.ResourceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-resourceid
        """
        return self._values.get('resource_id')

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Method.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def api_key_required(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::Method.ApiKeyRequired``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-apikeyrequired
        """
        return self._values.get('api_key_required')

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGateway::Method.AuthorizationScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizationscopes
        """
        return self._values.get('authorization_scopes')

    @builtins.property
    def authorization_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.AuthorizationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizationtype
        """
        return self._values.get('authorization_type')

    @builtins.property
    def authorizer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.AuthorizerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizerid
        """
        return self._values.get('authorizer_id')

    @builtins.property
    def integration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnMethod.IntegrationProperty"]]]:
        """``AWS::ApiGateway::Method.Integration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-integration
        """
        return self._values.get('integration')

    @builtins.property
    def method_responses(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMethod.MethodResponseProperty"]]]]]:
        """``AWS::ApiGateway::Method.MethodResponses``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-methodresponses
        """
        return self._values.get('method_responses')

    @builtins.property
    def operation_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.OperationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-operationname
        """
        return self._values.get('operation_name')

    @builtins.property
    def request_models(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::Method.RequestModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestmodels
        """
        return self._values.get('request_models')

    @builtins.property
    def request_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[bool, aws_cdk.core.IResolvable]]]]]:
        """``AWS::ApiGateway::Method.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestparameters
        """
        return self._values.get('request_parameters')

    @builtins.property
    def request_validator_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Method.RequestValidatorId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestvalidatorid
        """
        return self._values.get('request_validator_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMethodProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModel(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnModel"):
    """A CloudFormation ``AWS::ApiGateway::Model``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Model
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api_id: str, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, schema: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGateway::Model``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rest_api_id: ``AWS::ApiGateway::Model.RestApiId``.
        :param content_type: ``AWS::ApiGateway::Model.ContentType``.
        :param description: ``AWS::ApiGateway::Model.Description``.
        :param name: ``AWS::ApiGateway::Model.Name``.
        :param schema: ``AWS::ApiGateway::Model.Schema``.
        """
        props = CfnModelProps(rest_api_id=rest_api_id, content_type=content_type, description=description, name=name, schema=schema)

        jsii.create(CfnModel, self, [scope, id, props])

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
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Model.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Any:
        """``AWS::ApiGateway::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-schema
        """
        return jsii.get(self, "schema")

    @schema.setter
    def schema(self, value: typing.Any):
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Model.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-contenttype
        """
        return jsii.get(self, "contentType")

    @content_type.setter
    def content_type(self, value: typing.Optional[str]):
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Model.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnModelProps", jsii_struct_bases=[], name_mapping={'rest_api_id': 'restApiId', 'content_type': 'contentType', 'description': 'description', 'name': 'name', 'schema': 'schema'})
class CfnModelProps():
    def __init__(self, *, rest_api_id: str, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, schema: typing.Any=None):
        """Properties for defining a ``AWS::ApiGateway::Model``.

        :param rest_api_id: ``AWS::ApiGateway::Model.RestApiId``.
        :param content_type: ``AWS::ApiGateway::Model.ContentType``.
        :param description: ``AWS::ApiGateway::Model.Description``.
        :param name: ``AWS::ApiGateway::Model.Name``.
        :param schema: ``AWS::ApiGateway::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html
        """
        self._values = {
            'rest_api_id': rest_api_id,
        }
        if content_type is not None: self._values["content_type"] = content_type
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name
        if schema is not None: self._values["schema"] = schema

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Model.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Model.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-contenttype
        """
        return self._values.get('content_type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-description
        """
        return self._values.get('description')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Model.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-name
        """
        return self._values.get('name')

    @builtins.property
    def schema(self) -> typing.Any:
        """``AWS::ApiGateway::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-schema
        """
        return self._values.get('schema')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnModelProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModelV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnModelV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Model``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Model
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, name: str, schema: typing.Any, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Model``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Model.ApiId``.
        :param name: ``AWS::ApiGatewayV2::Model.Name``.
        :param schema: ``AWS::ApiGatewayV2::Model.Schema``.
        :param content_type: ``AWS::ApiGatewayV2::Model.ContentType``.
        :param description: ``AWS::ApiGatewayV2::Model.Description``.

        stability
        :stability: deprecated
        """
        props = CfnModelV2Props(api_id=api_id, name=name, schema=schema, content_type=content_type, description=description)

        jsii.create(CfnModelV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Model.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Model.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        stability
        :stability: deprecated
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        stability
        :stability: deprecated
        """
        return jsii.get(self, "schema")

    @schema.setter
    def schema(self, value: typing.Any):
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        stability
        :stability: deprecated
        """
        return jsii.get(self, "contentType")

    @content_type.setter
    def content_type(self, value: typing.Optional[str]):
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        stability
        :stability: deprecated
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnModelV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'name': 'name', 'schema': 'schema', 'content_type': 'contentType', 'description': 'description'})
class CfnModelV2Props():
    def __init__(self, *, api_id: str, name: str, schema: typing.Any, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Model``.

        :param api_id: ``AWS::ApiGatewayV2::Model.ApiId``.
        :param name: ``AWS::ApiGatewayV2::Model.Name``.
        :param schema: ``AWS::ApiGatewayV2::Model.Schema``.
        :param content_type: ``AWS::ApiGatewayV2::Model.ContentType``.
        :param description: ``AWS::ApiGatewayV2::Model.Description``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'name': name,
            'schema': schema,
        }
        if content_type is not None: self._values["content_type"] = content_type
        if description is not None: self._values["description"] = description

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Model.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Model.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        stability
        :stability: deprecated
        """
        return self._values.get('name')

    @builtins.property
    def schema(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        stability
        :stability: deprecated
        """
        return self._values.get('schema')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        stability
        :stability: deprecated
        """
        return self._values.get('content_type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        stability
        :stability: deprecated
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnModelV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRequestValidator(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRequestValidator"):
    """A CloudFormation ``AWS::ApiGateway::RequestValidator``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::RequestValidator
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api_id: str, name: typing.Optional[str]=None, validate_request_body: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, validate_request_parameters: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
        """Create a new ``AWS::ApiGateway::RequestValidator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rest_api_id: ``AWS::ApiGateway::RequestValidator.RestApiId``.
        :param name: ``AWS::ApiGateway::RequestValidator.Name``.
        :param validate_request_body: ``AWS::ApiGateway::RequestValidator.ValidateRequestBody``.
        :param validate_request_parameters: ``AWS::ApiGateway::RequestValidator.ValidateRequestParameters``.
        """
        props = CfnRequestValidatorProps(rest_api_id=rest_api_id, name=name, validate_request_body=validate_request_body, validate_request_parameters=validate_request_parameters)

        jsii.create(CfnRequestValidator, self, [scope, id, props])

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
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::RequestValidator.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RequestValidator.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="validateRequestBody")
    def validate_request_body(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::RequestValidator.ValidateRequestBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-validaterequestbody
        """
        return jsii.get(self, "validateRequestBody")

    @validate_request_body.setter
    def validate_request_body(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "validateRequestBody", value)

    @builtins.property
    @jsii.member(jsii_name="validateRequestParameters")
    def validate_request_parameters(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::RequestValidator.ValidateRequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-validaterequestparameters
        """
        return jsii.get(self, "validateRequestParameters")

    @validate_request_parameters.setter
    def validate_request_parameters(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "validateRequestParameters", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRequestValidatorProps", jsii_struct_bases=[], name_mapping={'rest_api_id': 'restApiId', 'name': 'name', 'validate_request_body': 'validateRequestBody', 'validate_request_parameters': 'validateRequestParameters'})
class CfnRequestValidatorProps():
    def __init__(self, *, rest_api_id: str, name: typing.Optional[str]=None, validate_request_body: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, validate_request_parameters: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
        """Properties for defining a ``AWS::ApiGateway::RequestValidator``.

        :param rest_api_id: ``AWS::ApiGateway::RequestValidator.RestApiId``.
        :param name: ``AWS::ApiGateway::RequestValidator.Name``.
        :param validate_request_body: ``AWS::ApiGateway::RequestValidator.ValidateRequestBody``.
        :param validate_request_parameters: ``AWS::ApiGateway::RequestValidator.ValidateRequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html
        """
        self._values = {
            'rest_api_id': rest_api_id,
        }
        if name is not None: self._values["name"] = name
        if validate_request_body is not None: self._values["validate_request_body"] = validate_request_body
        if validate_request_parameters is not None: self._values["validate_request_parameters"] = validate_request_parameters

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::RequestValidator.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RequestValidator.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-name
        """
        return self._values.get('name')

    @builtins.property
    def validate_request_body(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::RequestValidator.ValidateRequestBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-validaterequestbody
        """
        return self._values.get('validate_request_body')

    @builtins.property
    def validate_request_parameters(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::RequestValidator.ValidateRequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-validaterequestparameters
        """
        return self._values.get('validate_request_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRequestValidatorProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResource(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnResource"):
    """A CloudFormation ``AWS::ApiGateway::Resource``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Resource
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, parent_id: str, path_part: str, rest_api_id: str) -> None:
        """Create a new ``AWS::ApiGateway::Resource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param parent_id: ``AWS::ApiGateway::Resource.ParentId``.
        :param path_part: ``AWS::ApiGateway::Resource.PathPart``.
        :param rest_api_id: ``AWS::ApiGateway::Resource.RestApiId``.
        """
        props = CfnResourceProps(parent_id=parent_id, path_part=path_part, rest_api_id=rest_api_id)

        jsii.create(CfnResource, self, [scope, id, props])

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
    @jsii.member(jsii_name="parentId")
    def parent_id(self) -> str:
        """``AWS::ApiGateway::Resource.ParentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-parentid
        """
        return jsii.get(self, "parentId")

    @parent_id.setter
    def parent_id(self, value: str):
        jsii.set(self, "parentId", value)

    @builtins.property
    @jsii.member(jsii_name="pathPart")
    def path_part(self) -> str:
        """``AWS::ApiGateway::Resource.PathPart``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-pathpart
        """
        return jsii.get(self, "pathPart")

    @path_part.setter
    def path_part(self, value: str):
        jsii.set(self, "pathPart", value)

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Resource.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnResourceProps", jsii_struct_bases=[], name_mapping={'parent_id': 'parentId', 'path_part': 'pathPart', 'rest_api_id': 'restApiId'})
class CfnResourceProps():
    def __init__(self, *, parent_id: str, path_part: str, rest_api_id: str):
        """Properties for defining a ``AWS::ApiGateway::Resource``.

        :param parent_id: ``AWS::ApiGateway::Resource.ParentId``.
        :param path_part: ``AWS::ApiGateway::Resource.PathPart``.
        :param rest_api_id: ``AWS::ApiGateway::Resource.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html
        """
        self._values = {
            'parent_id': parent_id,
            'path_part': path_part,
            'rest_api_id': rest_api_id,
        }

    @builtins.property
    def parent_id(self) -> str:
        """``AWS::ApiGateway::Resource.ParentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-parentid
        """
        return self._values.get('parent_id')

    @builtins.property
    def path_part(self) -> str:
        """``AWS::ApiGateway::Resource.PathPart``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-pathpart
        """
        return self._values.get('path_part')

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Resource.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-restapiid
        """
        return self._values.get('rest_api_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRestApi(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRestApi"):
    """A CloudFormation ``AWS::ApiGateway::RestApi``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::RestApi
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key_source_type: typing.Optional[str]=None, binary_media_types: typing.Optional[typing.List[str]]=None, body: typing.Any=None, body_s3_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["S3LocationProperty"]]]=None, clone_from: typing.Optional[str]=None, description: typing.Optional[str]=None, endpoint_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EndpointConfigurationProperty"]]]=None, fail_on_warnings: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None, parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, policy: typing.Any=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ApiGateway::RestApi``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key_source_type: ``AWS::ApiGateway::RestApi.ApiKeySourceType``.
        :param binary_media_types: ``AWS::ApiGateway::RestApi.BinaryMediaTypes``.
        :param body: ``AWS::ApiGateway::RestApi.Body``.
        :param body_s3_location: ``AWS::ApiGateway::RestApi.BodyS3Location``.
        :param clone_from: ``AWS::ApiGateway::RestApi.CloneFrom``.
        :param description: ``AWS::ApiGateway::RestApi.Description``.
        :param endpoint_configuration: ``AWS::ApiGateway::RestApi.EndpointConfiguration``.
        :param fail_on_warnings: ``AWS::ApiGateway::RestApi.FailOnWarnings``.
        :param minimum_compression_size: ``AWS::ApiGateway::RestApi.MinimumCompressionSize``.
        :param name: ``AWS::ApiGateway::RestApi.Name``.
        :param parameters: ``AWS::ApiGateway::RestApi.Parameters``.
        :param policy: ``AWS::ApiGateway::RestApi.Policy``.
        :param tags: ``AWS::ApiGateway::RestApi.Tags``.
        """
        props = CfnRestApiProps(api_key_source_type=api_key_source_type, binary_media_types=binary_media_types, body=body, body_s3_location=body_s3_location, clone_from=clone_from, description=description, endpoint_configuration=endpoint_configuration, fail_on_warnings=fail_on_warnings, minimum_compression_size=minimum_compression_size, name=name, parameters=parameters, policy=policy, tags=tags)

        jsii.create(CfnRestApi, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrRootResourceId")
    def attr_root_resource_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RootResourceId
        """
        return jsii.get(self, "attrRootResourceId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGateway::RestApi.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Any:
        """``AWS::ApiGateway::RestApi.Body``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-body
        """
        return jsii.get(self, "body")

    @body.setter
    def body(self, value: typing.Any):
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        """``AWS::ApiGateway::RestApi.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-policy
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Any):
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeySourceType")
    def api_key_source_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.ApiKeySourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-apikeysourcetype
        """
        return jsii.get(self, "apiKeySourceType")

    @api_key_source_type.setter
    def api_key_source_type(self, value: typing.Optional[str]):
        jsii.set(self, "apiKeySourceType", value)

    @builtins.property
    @jsii.member(jsii_name="binaryMediaTypes")
    def binary_media_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGateway::RestApi.BinaryMediaTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-binarymediatypes
        """
        return jsii.get(self, "binaryMediaTypes")

    @binary_media_types.setter
    def binary_media_types(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "binaryMediaTypes", value)

    @builtins.property
    @jsii.member(jsii_name="bodyS3Location")
    def body_s3_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["S3LocationProperty"]]]:
        """``AWS::ApiGateway::RestApi.BodyS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-bodys3location
        """
        return jsii.get(self, "bodyS3Location")

    @body_s3_location.setter
    def body_s3_location(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["S3LocationProperty"]]]):
        jsii.set(self, "bodyS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="cloneFrom")
    def clone_from(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.CloneFrom``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-clonefrom
        """
        return jsii.get(self, "cloneFrom")

    @clone_from.setter
    def clone_from(self, value: typing.Optional[str]):
        jsii.set(self, "cloneFrom", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EndpointConfigurationProperty"]]]:
        """``AWS::ApiGateway::RestApi.EndpointConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-endpointconfiguration
        """
        return jsii.get(self, "endpointConfiguration")

    @endpoint_configuration.setter
    def endpoint_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EndpointConfigurationProperty"]]]):
        jsii.set(self, "endpointConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::RestApi.FailOnWarnings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-failonwarnings
        """
        return jsii.get(self, "failOnWarnings")

    @fail_on_warnings.setter
    def fail_on_warnings(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "failOnWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="minimumCompressionSize")
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGateway::RestApi.MinimumCompressionSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-minimumcompressionsize
        """
        return jsii.get(self, "minimumCompressionSize")

    @minimum_compression_size.setter
    def minimum_compression_size(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "minimumCompressionSize", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::RestApi.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        jsii.set(self, "parameters", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRestApi.EndpointConfigurationProperty", jsii_struct_bases=[], name_mapping={'types': 'types', 'vpc_endpoint_ids': 'vpcEndpointIds'})
    class EndpointConfigurationProperty():
        def __init__(self, *, types: typing.Optional[typing.List[str]]=None, vpc_endpoint_ids: typing.Optional[typing.List[str]]=None):
            """
            :param types: ``CfnRestApi.EndpointConfigurationProperty.Types``.
            :param vpc_endpoint_ids: ``CfnRestApi.EndpointConfigurationProperty.VpcEndpointIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html
            """
            self._values = {
            }
            if types is not None: self._values["types"] = types
            if vpc_endpoint_ids is not None: self._values["vpc_endpoint_ids"] = vpc_endpoint_ids

        @builtins.property
        def types(self) -> typing.Optional[typing.List[str]]:
            """``CfnRestApi.EndpointConfigurationProperty.Types``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html#cfn-apigateway-restapi-endpointconfiguration-types
            """
            return self._values.get('types')

        @builtins.property
        def vpc_endpoint_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnRestApi.EndpointConfigurationProperty.VpcEndpointIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html#cfn-apigateway-restapi-endpointconfiguration-vpcendpointids
            """
            return self._values.get('vpc_endpoint_ids')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EndpointConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRestApi.S3LocationProperty", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'e_tag': 'eTag', 'key': 'key', 'version': 'version'})
    class S3LocationProperty():
        def __init__(self, *, bucket: typing.Optional[str]=None, e_tag: typing.Optional[str]=None, key: typing.Optional[str]=None, version: typing.Optional[str]=None):
            """
            :param bucket: ``CfnRestApi.S3LocationProperty.Bucket``.
            :param e_tag: ``CfnRestApi.S3LocationProperty.ETag``.
            :param key: ``CfnRestApi.S3LocationProperty.Key``.
            :param version: ``CfnRestApi.S3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html
            """
            self._values = {
            }
            if bucket is not None: self._values["bucket"] = bucket
            if e_tag is not None: self._values["e_tag"] = e_tag
            if key is not None: self._values["key"] = key
            if version is not None: self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[str]:
            """``CfnRestApi.S3LocationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-bucket
            """
            return self._values.get('bucket')

        @builtins.property
        def e_tag(self) -> typing.Optional[str]:
            """``CfnRestApi.S3LocationProperty.ETag``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-etag
            """
            return self._values.get('e_tag')

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnRestApi.S3LocationProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-key
            """
            return self._values.get('key')

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """``CfnRestApi.S3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRestApiProps", jsii_struct_bases=[], name_mapping={'api_key_source_type': 'apiKeySourceType', 'binary_media_types': 'binaryMediaTypes', 'body': 'body', 'body_s3_location': 'bodyS3Location', 'clone_from': 'cloneFrom', 'description': 'description', 'endpoint_configuration': 'endpointConfiguration', 'fail_on_warnings': 'failOnWarnings', 'minimum_compression_size': 'minimumCompressionSize', 'name': 'name', 'parameters': 'parameters', 'policy': 'policy', 'tags': 'tags'})
class CfnRestApiProps():
    def __init__(self, *, api_key_source_type: typing.Optional[str]=None, binary_media_types: typing.Optional[typing.List[str]]=None, body: typing.Any=None, body_s3_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRestApi.S3LocationProperty"]]]=None, clone_from: typing.Optional[str]=None, description: typing.Optional[str]=None, endpoint_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRestApi.EndpointConfigurationProperty"]]]=None, fail_on_warnings: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None, parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, policy: typing.Any=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ApiGateway::RestApi``.

        :param api_key_source_type: ``AWS::ApiGateway::RestApi.ApiKeySourceType``.
        :param binary_media_types: ``AWS::ApiGateway::RestApi.BinaryMediaTypes``.
        :param body: ``AWS::ApiGateway::RestApi.Body``.
        :param body_s3_location: ``AWS::ApiGateway::RestApi.BodyS3Location``.
        :param clone_from: ``AWS::ApiGateway::RestApi.CloneFrom``.
        :param description: ``AWS::ApiGateway::RestApi.Description``.
        :param endpoint_configuration: ``AWS::ApiGateway::RestApi.EndpointConfiguration``.
        :param fail_on_warnings: ``AWS::ApiGateway::RestApi.FailOnWarnings``.
        :param minimum_compression_size: ``AWS::ApiGateway::RestApi.MinimumCompressionSize``.
        :param name: ``AWS::ApiGateway::RestApi.Name``.
        :param parameters: ``AWS::ApiGateway::RestApi.Parameters``.
        :param policy: ``AWS::ApiGateway::RestApi.Policy``.
        :param tags: ``AWS::ApiGateway::RestApi.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html
        """
        self._values = {
        }
        if api_key_source_type is not None: self._values["api_key_source_type"] = api_key_source_type
        if binary_media_types is not None: self._values["binary_media_types"] = binary_media_types
        if body is not None: self._values["body"] = body
        if body_s3_location is not None: self._values["body_s3_location"] = body_s3_location
        if clone_from is not None: self._values["clone_from"] = clone_from
        if description is not None: self._values["description"] = description
        if endpoint_configuration is not None: self._values["endpoint_configuration"] = endpoint_configuration
        if fail_on_warnings is not None: self._values["fail_on_warnings"] = fail_on_warnings
        if minimum_compression_size is not None: self._values["minimum_compression_size"] = minimum_compression_size
        if name is not None: self._values["name"] = name
        if parameters is not None: self._values["parameters"] = parameters
        if policy is not None: self._values["policy"] = policy
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def api_key_source_type(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.ApiKeySourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-apikeysourcetype
        """
        return self._values.get('api_key_source_type')

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGateway::RestApi.BinaryMediaTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-binarymediatypes
        """
        return self._values.get('binary_media_types')

    @builtins.property
    def body(self) -> typing.Any:
        """``AWS::ApiGateway::RestApi.Body``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-body
        """
        return self._values.get('body')

    @builtins.property
    def body_s3_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRestApi.S3LocationProperty"]]]:
        """``AWS::ApiGateway::RestApi.BodyS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-bodys3location
        """
        return self._values.get('body_s3_location')

    @builtins.property
    def clone_from(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.CloneFrom``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-clonefrom
        """
        return self._values.get('clone_from')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-description
        """
        return self._values.get('description')

    @builtins.property
    def endpoint_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRestApi.EndpointConfigurationProperty"]]]:
        """``AWS::ApiGateway::RestApi.EndpointConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-endpointconfiguration
        """
        return self._values.get('endpoint_configuration')

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::RestApi.FailOnWarnings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-failonwarnings
        """
        return self._values.get('fail_on_warnings')

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGateway::RestApi.MinimumCompressionSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-minimumcompressionsize
        """
        return self._values.get('minimum_compression_size')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::RestApi.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-name
        """
        return self._values.get('name')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::RestApi.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def policy(self) -> typing.Any:
        """``AWS::ApiGateway::RestApi.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-policy
        """
        return self._values.get('policy')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApiGateway::RestApi.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRestApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRouteResponseV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRouteResponseV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::RouteResponse``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::RouteResponse
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, route_id: str, route_response_key: str, model_selection_expression: typing.Optional[str]=None, response_models: typing.Any=None, response_parameters: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::RouteResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::RouteResponse.ApiId``.
        :param route_id: ``AWS::ApiGatewayV2::RouteResponse.RouteId``.
        :param route_response_key: ``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.
        :param response_models: ``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.
        :param response_parameters: ``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        stability
        :stability: deprecated
        """
        props = CfnRouteResponseV2Props(api_id=api_id, route_id=route_id, route_response_key=route_response_key, model_selection_expression=model_selection_expression, response_models=response_models, response_parameters=response_parameters)

        jsii.create(CfnRouteResponseV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="responseModels")
    def response_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        stability
        :stability: deprecated
        """
        return jsii.get(self, "responseModels")

    @response_models.setter
    def response_models(self, value: typing.Any):
        jsii.set(self, "responseModels", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        stability
        :stability: deprecated
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter
    def response_parameters(self, value: typing.Any):
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeId")

    @route_id.setter
    def route_id(self, value: str):
        jsii.set(self, "routeId", value)

    @builtins.property
    @jsii.member(jsii_name="routeResponseKey")
    def route_response_key(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeResponseKey")

    @route_response_key.setter
    def route_response_key(self, value: str):
        jsii.set(self, "routeResponseKey", value)

    @builtins.property
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "modelSelectionExpression")

    @model_selection_expression.setter
    def model_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "modelSelectionExpression", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteResponseV2.ParameterConstraintsProperty", jsii_struct_bases=[], name_mapping={'required': 'required'})
    class ParameterConstraintsProperty():
        def __init__(self, *, required: typing.Union[bool, aws_cdk.core.IResolvable]):
            """
            :param required: ``CfnRouteResponseV2.ParameterConstraintsProperty.Required``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html
            stability
            :stability: deprecated
            """
            self._values = {
                'required': required,
            }

        @builtins.property
        def required(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnRouteResponseV2.ParameterConstraintsProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html#cfn-apigatewayv2-routeresponse-parameterconstraints-required
            stability
            :stability: deprecated
            """
            return self._values.get('required')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteResponseV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'route_id': 'routeId', 'route_response_key': 'routeResponseKey', 'model_selection_expression': 'modelSelectionExpression', 'response_models': 'responseModels', 'response_parameters': 'responseParameters'})
class CfnRouteResponseV2Props():
    def __init__(self, *, api_id: str, route_id: str, route_response_key: str, model_selection_expression: typing.Optional[str]=None, response_models: typing.Any=None, response_parameters: typing.Any=None):
        """Properties for defining a ``AWS::ApiGatewayV2::RouteResponse``.

        :param api_id: ``AWS::ApiGatewayV2::RouteResponse.ApiId``.
        :param route_id: ``AWS::ApiGatewayV2::RouteResponse.RouteId``.
        :param route_response_key: ``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.
        :param response_models: ``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.
        :param response_parameters: ``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'route_id': route_id,
            'route_response_key': route_response_key,
        }
        if model_selection_expression is not None: self._values["model_selection_expression"] = model_selection_expression
        if response_models is not None: self._values["response_models"] = response_models
        if response_parameters is not None: self._values["response_parameters"] = response_parameters

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def route_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        stability
        :stability: deprecated
        """
        return self._values.get('route_id')

    @builtins.property
    def route_response_key(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        stability
        :stability: deprecated
        """
        return self._values.get('route_response_key')

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('model_selection_expression')

    @builtins.property
    def response_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        stability
        :stability: deprecated
        """
        return self._values.get('response_models')

    @builtins.property
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        stability
        :stability: deprecated
        """
        return self._values.get('response_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRouteResponseV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRouteV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnRouteV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Route``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Route
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, route_key: str, api_key_required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, model_selection_expression: typing.Optional[str]=None, operation_name: typing.Optional[str]=None, request_models: typing.Any=None, request_parameters: typing.Any=None, route_response_selection_expression: typing.Optional[str]=None, target: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Route.ApiId``.
        :param route_key: ``AWS::ApiGatewayV2::Route.RouteKey``.
        :param api_key_required: ``AWS::ApiGatewayV2::Route.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGatewayV2::Route.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGatewayV2::Route.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGatewayV2::Route.AuthorizerId``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.
        :param operation_name: ``AWS::ApiGatewayV2::Route.OperationName``.
        :param request_models: ``AWS::ApiGatewayV2::Route.RequestModels``.
        :param request_parameters: ``AWS::ApiGatewayV2::Route.RequestParameters``.
        :param route_response_selection_expression: ``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.
        :param target: ``AWS::ApiGatewayV2::Route.Target``.

        stability
        :stability: deprecated
        """
        props = CfnRouteV2Props(api_id=api_id, route_key=route_key, api_key_required=api_key_required, authorization_scopes=authorization_scopes, authorization_type=authorization_type, authorizer_id=authorizer_id, model_selection_expression=model_selection_expression, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, route_response_selection_expression=route_response_selection_expression, target=target)

        jsii.create(CfnRouteV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Route.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="requestModels")
    def request_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        stability
        :stability: deprecated
        """
        return jsii.get(self, "requestModels")

    @request_models.setter
    def request_models(self, value: typing.Any):
        jsii.set(self, "requestModels", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        stability
        :stability: deprecated
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter
    def request_parameters(self, value: typing.Any):
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> str:
        """``AWS::ApiGatewayV2::Route.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeKey")

    @route_key.setter
    def route_key(self, value: str):
        jsii.set(self, "routeKey", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeyRequired")
    def api_key_required(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Route.ApiKeyRequired``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiKeyRequired")

    @api_key_required.setter
    def api_key_required(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "apiKeyRequired", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationScopes")
    def authorization_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGatewayV2::Route.AuthorizationScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizationScopes")

    @authorization_scopes.setter
    def authorization_scopes(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "authorizationScopes", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizationType")

    @authorization_type.setter
    def authorization_type(self, value: typing.Optional[str]):
        jsii.set(self, "authorizationType", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "authorizerId")

    @authorizer_id.setter
    def authorizer_id(self, value: typing.Optional[str]):
        jsii.set(self, "authorizerId", value)

    @builtins.property
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "modelSelectionExpression")

    @model_selection_expression.setter
    def model_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "modelSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.OperationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        stability
        :stability: deprecated
        """
        return jsii.get(self, "operationName")

    @operation_name.setter
    def operation_name(self, value: typing.Optional[str]):
        jsii.set(self, "operationName", value)

    @builtins.property
    @jsii.member(jsii_name="routeResponseSelectionExpression")
    def route_response_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeResponseSelectionExpression")

    @route_response_selection_expression.setter
    def route_response_selection_expression(self, value: typing.Optional[str]):
        jsii.set(self, "routeResponseSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        stability
        :stability: deprecated
        """
        return jsii.get(self, "target")

    @target.setter
    def target(self, value: typing.Optional[str]):
        jsii.set(self, "target", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteV2.ParameterConstraintsProperty", jsii_struct_bases=[], name_mapping={'required': 'required'})
    class ParameterConstraintsProperty():
        def __init__(self, *, required: typing.Union[bool, aws_cdk.core.IResolvable]):
            """
            :param required: ``CfnRouteV2.ParameterConstraintsProperty.Required``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html
            stability
            :stability: deprecated
            """
            self._values = {
                'required': required,
            }

        @builtins.property
        def required(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnRouteV2.ParameterConstraintsProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html#cfn-apigatewayv2-route-parameterconstraints-required
            stability
            :stability: deprecated
            """
            return self._values.get('required')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnRouteV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'route_key': 'routeKey', 'api_key_required': 'apiKeyRequired', 'authorization_scopes': 'authorizationScopes', 'authorization_type': 'authorizationType', 'authorizer_id': 'authorizerId', 'model_selection_expression': 'modelSelectionExpression', 'operation_name': 'operationName', 'request_models': 'requestModels', 'request_parameters': 'requestParameters', 'route_response_selection_expression': 'routeResponseSelectionExpression', 'target': 'target'})
class CfnRouteV2Props():
    def __init__(self, *, api_id: str, route_key: str, api_key_required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, model_selection_expression: typing.Optional[str]=None, operation_name: typing.Optional[str]=None, request_models: typing.Any=None, request_parameters: typing.Any=None, route_response_selection_expression: typing.Optional[str]=None, target: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Route``.

        :param api_id: ``AWS::ApiGatewayV2::Route.ApiId``.
        :param route_key: ``AWS::ApiGatewayV2::Route.RouteKey``.
        :param api_key_required: ``AWS::ApiGatewayV2::Route.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGatewayV2::Route.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGatewayV2::Route.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGatewayV2::Route.AuthorizerId``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.
        :param operation_name: ``AWS::ApiGatewayV2::Route.OperationName``.
        :param request_models: ``AWS::ApiGatewayV2::Route.RequestModels``.
        :param request_parameters: ``AWS::ApiGatewayV2::Route.RequestParameters``.
        :param route_response_selection_expression: ``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.
        :param target: ``AWS::ApiGatewayV2::Route.Target``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'route_key': route_key,
        }
        if api_key_required is not None: self._values["api_key_required"] = api_key_required
        if authorization_scopes is not None: self._values["authorization_scopes"] = authorization_scopes
        if authorization_type is not None: self._values["authorization_type"] = authorization_type
        if authorizer_id is not None: self._values["authorizer_id"] = authorizer_id
        if model_selection_expression is not None: self._values["model_selection_expression"] = model_selection_expression
        if operation_name is not None: self._values["operation_name"] = operation_name
        if request_models is not None: self._values["request_models"] = request_models
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if route_response_selection_expression is not None: self._values["route_response_selection_expression"] = route_response_selection_expression
        if target is not None: self._values["target"] = target

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Route.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def route_key(self) -> str:
        """``AWS::ApiGatewayV2::Route.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        stability
        :stability: deprecated
        """
        return self._values.get('route_key')

    @builtins.property
    def api_key_required(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Route.ApiKeyRequired``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        stability
        :stability: deprecated
        """
        return self._values.get('api_key_required')

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGatewayV2::Route.AuthorizationScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        stability
        :stability: deprecated
        """
        return self._values.get('authorization_scopes')

    @builtins.property
    def authorization_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        stability
        :stability: deprecated
        """
        return self._values.get('authorization_type')

    @builtins.property
    def authorizer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        stability
        :stability: deprecated
        """
        return self._values.get('authorizer_id')

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('model_selection_expression')

    @builtins.property
    def operation_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.OperationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        stability
        :stability: deprecated
        """
        return self._values.get('operation_name')

    @builtins.property
    def request_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        stability
        :stability: deprecated
        """
        return self._values.get('request_models')

    @builtins.property
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        stability
        :stability: deprecated
        """
        return self._values.get('request_parameters')

    @builtins.property
    def route_response_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        stability
        :stability: deprecated
        """
        return self._values.get('route_response_selection_expression')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        stability
        :stability: deprecated
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRouteV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStage(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnStage"):
    """A CloudFormation ``AWS::ApiGateway::Stage``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::Stage
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api_id: str, access_log_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLogSettingProperty"]]]=None, cache_cluster_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache_cluster_size: typing.Optional[str]=None, canary_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CanarySettingProperty"]]]=None, client_certificate_id: typing.Optional[str]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MethodSettingProperty"]]]]]=None, stage_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, tracing_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, variables: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None) -> None:
        """Create a new ``AWS::ApiGateway::Stage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rest_api_id: ``AWS::ApiGateway::Stage.RestApiId``.
        :param access_log_setting: ``AWS::ApiGateway::Stage.AccessLogSetting``.
        :param cache_cluster_enabled: ``AWS::ApiGateway::Stage.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::ApiGateway::Stage.CacheClusterSize``.
        :param canary_setting: ``AWS::ApiGateway::Stage.CanarySetting``.
        :param client_certificate_id: ``AWS::ApiGateway::Stage.ClientCertificateId``.
        :param deployment_id: ``AWS::ApiGateway::Stage.DeploymentId``.
        :param description: ``AWS::ApiGateway::Stage.Description``.
        :param documentation_version: ``AWS::ApiGateway::Stage.DocumentationVersion``.
        :param method_settings: ``AWS::ApiGateway::Stage.MethodSettings``.
        :param stage_name: ``AWS::ApiGateway::Stage.StageName``.
        :param tags: ``AWS::ApiGateway::Stage.Tags``.
        :param tracing_enabled: ``AWS::ApiGateway::Stage.TracingEnabled``.
        :param variables: ``AWS::ApiGateway::Stage.Variables``.
        """
        props = CfnStageProps(rest_api_id=rest_api_id, access_log_setting=access_log_setting, cache_cluster_enabled=cache_cluster_enabled, cache_cluster_size=cache_cluster_size, canary_setting=canary_setting, client_certificate_id=client_certificate_id, deployment_id=deployment_id, description=description, documentation_version=documentation_version, method_settings=method_settings, stage_name=stage_name, tags=tags, tracing_enabled=tracing_enabled, variables=variables)

        jsii.create(CfnStage, self, [scope, id, props])

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
        """``AWS::ApiGateway::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Stage.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-restapiid
        """
        return jsii.get(self, "restApiId")

    @rest_api_id.setter
    def rest_api_id(self, value: str):
        jsii.set(self, "restApiId", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSetting")
    def access_log_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLogSettingProperty"]]]:
        """``AWS::ApiGateway::Stage.AccessLogSetting``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-accesslogsetting
        """
        return jsii.get(self, "accessLogSetting")

    @access_log_setting.setter
    def access_log_setting(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLogSettingProperty"]]]):
        jsii.set(self, "accessLogSetting", value)

    @builtins.property
    @jsii.member(jsii_name="cacheClusterEnabled")
    def cache_cluster_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::Stage.CacheClusterEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-cacheclusterenabled
        """
        return jsii.get(self, "cacheClusterEnabled")

    @cache_cluster_enabled.setter
    def cache_cluster_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "cacheClusterEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cacheClusterSize")
    def cache_cluster_size(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.CacheClusterSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-cacheclustersize
        """
        return jsii.get(self, "cacheClusterSize")

    @cache_cluster_size.setter
    def cache_cluster_size(self, value: typing.Optional[str]):
        jsii.set(self, "cacheClusterSize", value)

    @builtins.property
    @jsii.member(jsii_name="canarySetting")
    def canary_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CanarySettingProperty"]]]:
        """``AWS::ApiGateway::Stage.CanarySetting``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-canarysetting
        """
        return jsii.get(self, "canarySetting")

    @canary_setting.setter
    def canary_setting(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CanarySettingProperty"]]]):
        jsii.set(self, "canarySetting", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateId")
    def client_certificate_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.ClientCertificateId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-clientcertificateid
        """
        return jsii.get(self, "clientCertificateId")

    @client_certificate_id.setter
    def client_certificate_id(self, value: typing.Optional[str]):
        jsii.set(self, "clientCertificateId", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.DeploymentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-deploymentid
        """
        return jsii.get(self, "deploymentId")

    @deployment_id.setter
    def deployment_id(self, value: typing.Optional[str]):
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="documentationVersion")
    def documentation_version(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.DocumentationVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-documentationversion
        """
        return jsii.get(self, "documentationVersion")

    @documentation_version.setter
    def documentation_version(self, value: typing.Optional[str]):
        jsii.set(self, "documentationVersion", value)

    @builtins.property
    @jsii.member(jsii_name="methodSettings")
    def method_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MethodSettingProperty"]]]]]:
        """``AWS::ApiGateway::Stage.MethodSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-methodsettings
        """
        return jsii.get(self, "methodSettings")

    @method_settings.setter
    def method_settings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MethodSettingProperty"]]]]]):
        jsii.set(self, "methodSettings", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-stagename
        """
        return jsii.get(self, "stageName")

    @stage_name.setter
    def stage_name(self, value: typing.Optional[str]):
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="tracingEnabled")
    def tracing_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::Stage.TracingEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tracingenabled
        """
        return jsii.get(self, "tracingEnabled")

    @tracing_enabled.setter
    def tracing_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "tracingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::Stage.Variables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-variables
        """
        return jsii.get(self, "variables")

    @variables.setter
    def variables(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        jsii.set(self, "variables", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStage.AccessLogSettingProperty", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'format': 'format'})
    class AccessLogSettingProperty():
        def __init__(self, *, destination_arn: typing.Optional[str]=None, format: typing.Optional[str]=None):
            """
            :param destination_arn: ``CfnStage.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnStage.AccessLogSettingProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            """
            self._values = {
            }
            if destination_arn is not None: self._values["destination_arn"] = destination_arn
            if format is not None: self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[str]:
            """``CfnStage.AccessLogSettingProperty.DestinationArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            """
            return self._values.get('destination_arn')

        @builtins.property
        def format(self) -> typing.Optional[str]:
            """``CfnStage.AccessLogSettingProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            """
            return self._values.get('format')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessLogSettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStage.CanarySettingProperty", jsii_struct_bases=[], name_mapping={'deployment_id': 'deploymentId', 'percent_traffic': 'percentTraffic', 'stage_variable_overrides': 'stageVariableOverrides', 'use_stage_cache': 'useStageCache'})
    class CanarySettingProperty():
        def __init__(self, *, deployment_id: typing.Optional[str]=None, percent_traffic: typing.Optional[jsii.Number]=None, stage_variable_overrides: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, use_stage_cache: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param deployment_id: ``CfnStage.CanarySettingProperty.DeploymentId``.
            :param percent_traffic: ``CfnStage.CanarySettingProperty.PercentTraffic``.
            :param stage_variable_overrides: ``CfnStage.CanarySettingProperty.StageVariableOverrides``.
            :param use_stage_cache: ``CfnStage.CanarySettingProperty.UseStageCache``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html
            """
            self._values = {
            }
            if deployment_id is not None: self._values["deployment_id"] = deployment_id
            if percent_traffic is not None: self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None: self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None: self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def deployment_id(self) -> typing.Optional[str]:
            """``CfnStage.CanarySettingProperty.DeploymentId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-deploymentid
            """
            return self._values.get('deployment_id')

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.CanarySettingProperty.PercentTraffic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-percenttraffic
            """
            return self._values.get('percent_traffic')

        @builtins.property
        def stage_variable_overrides(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnStage.CanarySettingProperty.StageVariableOverrides``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-stagevariableoverrides
            """
            return self._values.get('stage_variable_overrides')

        @builtins.property
        def use_stage_cache(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStage.CanarySettingProperty.UseStageCache``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-usestagecache
            """
            return self._values.get('use_stage_cache')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CanarySettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStage.MethodSettingProperty", jsii_struct_bases=[], name_mapping={'cache_data_encrypted': 'cacheDataEncrypted', 'cache_ttl_in_seconds': 'cacheTtlInSeconds', 'caching_enabled': 'cachingEnabled', 'data_trace_enabled': 'dataTraceEnabled', 'http_method': 'httpMethod', 'logging_level': 'loggingLevel', 'metrics_enabled': 'metricsEnabled', 'resource_path': 'resourcePath', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit'})
    class MethodSettingProperty():
        def __init__(self, *, cache_data_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache_ttl_in_seconds: typing.Optional[jsii.Number]=None, caching_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, data_trace_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, http_method: typing.Optional[str]=None, logging_level: typing.Optional[str]=None, metrics_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, resource_path: typing.Optional[str]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None):
            """
            :param cache_data_encrypted: ``CfnStage.MethodSettingProperty.CacheDataEncrypted``.
            :param cache_ttl_in_seconds: ``CfnStage.MethodSettingProperty.CacheTtlInSeconds``.
            :param caching_enabled: ``CfnStage.MethodSettingProperty.CachingEnabled``.
            :param data_trace_enabled: ``CfnStage.MethodSettingProperty.DataTraceEnabled``.
            :param http_method: ``CfnStage.MethodSettingProperty.HttpMethod``.
            :param logging_level: ``CfnStage.MethodSettingProperty.LoggingLevel``.
            :param metrics_enabled: ``CfnStage.MethodSettingProperty.MetricsEnabled``.
            :param resource_path: ``CfnStage.MethodSettingProperty.ResourcePath``.
            :param throttling_burst_limit: ``CfnStage.MethodSettingProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnStage.MethodSettingProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html
            """
            self._values = {
            }
            if cache_data_encrypted is not None: self._values["cache_data_encrypted"] = cache_data_encrypted
            if cache_ttl_in_seconds is not None: self._values["cache_ttl_in_seconds"] = cache_ttl_in_seconds
            if caching_enabled is not None: self._values["caching_enabled"] = caching_enabled
            if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
            if http_method is not None: self._values["http_method"] = http_method
            if logging_level is not None: self._values["logging_level"] = logging_level
            if metrics_enabled is not None: self._values["metrics_enabled"] = metrics_enabled
            if resource_path is not None: self._values["resource_path"] = resource_path
            if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def cache_data_encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStage.MethodSettingProperty.CacheDataEncrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-cachedataencrypted
            """
            return self._values.get('cache_data_encrypted')

        @builtins.property
        def cache_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.MethodSettingProperty.CacheTtlInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-cachettlinseconds
            """
            return self._values.get('cache_ttl_in_seconds')

        @builtins.property
        def caching_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStage.MethodSettingProperty.CachingEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-cachingenabled
            """
            return self._values.get('caching_enabled')

        @builtins.property
        def data_trace_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStage.MethodSettingProperty.DataTraceEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-datatraceenabled
            """
            return self._values.get('data_trace_enabled')

        @builtins.property
        def http_method(self) -> typing.Optional[str]:
            """``CfnStage.MethodSettingProperty.HttpMethod``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-httpmethod
            """
            return self._values.get('http_method')

        @builtins.property
        def logging_level(self) -> typing.Optional[str]:
            """``CfnStage.MethodSettingProperty.LoggingLevel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-logginglevel
            """
            return self._values.get('logging_level')

        @builtins.property
        def metrics_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStage.MethodSettingProperty.MetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-metricsenabled
            """
            return self._values.get('metrics_enabled')

        @builtins.property
        def resource_path(self) -> typing.Optional[str]:
            """``CfnStage.MethodSettingProperty.ResourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-resourcepath
            """
            return self._values.get('resource_path')

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.MethodSettingProperty.ThrottlingBurstLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-throttlingburstlimit
            """
            return self._values.get('throttling_burst_limit')

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.MethodSettingProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-throttlingratelimit
            """
            return self._values.get('throttling_rate_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MethodSettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageProps", jsii_struct_bases=[], name_mapping={'rest_api_id': 'restApiId', 'access_log_setting': 'accessLogSetting', 'cache_cluster_enabled': 'cacheClusterEnabled', 'cache_cluster_size': 'cacheClusterSize', 'canary_setting': 'canarySetting', 'client_certificate_id': 'clientCertificateId', 'deployment_id': 'deploymentId', 'description': 'description', 'documentation_version': 'documentationVersion', 'method_settings': 'methodSettings', 'stage_name': 'stageName', 'tags': 'tags', 'tracing_enabled': 'tracingEnabled', 'variables': 'variables'})
class CfnStageProps():
    def __init__(self, *, rest_api_id: str, access_log_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStage.AccessLogSettingProperty"]]]=None, cache_cluster_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache_cluster_size: typing.Optional[str]=None, canary_setting: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStage.CanarySettingProperty"]]]=None, client_certificate_id: typing.Optional[str]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStage.MethodSettingProperty"]]]]]=None, stage_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, tracing_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, variables: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None):
        """Properties for defining a ``AWS::ApiGateway::Stage``.

        :param rest_api_id: ``AWS::ApiGateway::Stage.RestApiId``.
        :param access_log_setting: ``AWS::ApiGateway::Stage.AccessLogSetting``.
        :param cache_cluster_enabled: ``AWS::ApiGateway::Stage.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::ApiGateway::Stage.CacheClusterSize``.
        :param canary_setting: ``AWS::ApiGateway::Stage.CanarySetting``.
        :param client_certificate_id: ``AWS::ApiGateway::Stage.ClientCertificateId``.
        :param deployment_id: ``AWS::ApiGateway::Stage.DeploymentId``.
        :param description: ``AWS::ApiGateway::Stage.Description``.
        :param documentation_version: ``AWS::ApiGateway::Stage.DocumentationVersion``.
        :param method_settings: ``AWS::ApiGateway::Stage.MethodSettings``.
        :param stage_name: ``AWS::ApiGateway::Stage.StageName``.
        :param tags: ``AWS::ApiGateway::Stage.Tags``.
        :param tracing_enabled: ``AWS::ApiGateway::Stage.TracingEnabled``.
        :param variables: ``AWS::ApiGateway::Stage.Variables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html
        """
        self._values = {
            'rest_api_id': rest_api_id,
        }
        if access_log_setting is not None: self._values["access_log_setting"] = access_log_setting
        if cache_cluster_enabled is not None: self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None: self._values["cache_cluster_size"] = cache_cluster_size
        if canary_setting is not None: self._values["canary_setting"] = canary_setting
        if client_certificate_id is not None: self._values["client_certificate_id"] = client_certificate_id
        if deployment_id is not None: self._values["deployment_id"] = deployment_id
        if description is not None: self._values["description"] = description
        if documentation_version is not None: self._values["documentation_version"] = documentation_version
        if method_settings is not None: self._values["method_settings"] = method_settings
        if stage_name is not None: self._values["stage_name"] = stage_name
        if tags is not None: self._values["tags"] = tags
        if tracing_enabled is not None: self._values["tracing_enabled"] = tracing_enabled
        if variables is not None: self._values["variables"] = variables

    @builtins.property
    def rest_api_id(self) -> str:
        """``AWS::ApiGateway::Stage.RestApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-restapiid
        """
        return self._values.get('rest_api_id')

    @builtins.property
    def access_log_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStage.AccessLogSettingProperty"]]]:
        """``AWS::ApiGateway::Stage.AccessLogSetting``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-accesslogsetting
        """
        return self._values.get('access_log_setting')

    @builtins.property
    def cache_cluster_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::Stage.CacheClusterEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-cacheclusterenabled
        """
        return self._values.get('cache_cluster_enabled')

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.CacheClusterSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-cacheclustersize
        """
        return self._values.get('cache_cluster_size')

    @builtins.property
    def canary_setting(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStage.CanarySettingProperty"]]]:
        """``AWS::ApiGateway::Stage.CanarySetting``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-canarysetting
        """
        return self._values.get('canary_setting')

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.ClientCertificateId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-clientcertificateid
        """
        return self._values.get('client_certificate_id')

    @builtins.property
    def deployment_id(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.DeploymentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-deploymentid
        """
        return self._values.get('deployment_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-description
        """
        return self._values.get('description')

    @builtins.property
    def documentation_version(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.DocumentationVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-documentationversion
        """
        return self._values.get('documentation_version')

    @builtins.property
    def method_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStage.MethodSettingProperty"]]]]]:
        """``AWS::ApiGateway::Stage.MethodSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-methodsettings
        """
        return self._values.get('method_settings')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::Stage.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-stagename
        """
        return self._values.get('stage_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApiGateway::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tags
        """
        return self._values.get('tags')

    @builtins.property
    def tracing_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGateway::Stage.TracingEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tracingenabled
        """
        return self._values.get('tracing_enabled')

    @builtins.property
    def variables(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::ApiGateway::Stage.Variables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-variables
        """
        return self._values.get('variables')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnStageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStageV2(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnStageV2"):
    """A CloudFormation ``AWS::ApiGatewayV2::Stage``.

    deprecated
    :deprecated: moved to package aws-apigatewayv2

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
    stability
    :stability: deprecated
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Stage
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, stage_name: str, access_log_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLogSettingsProperty"]]]=None, auto_deploy: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, client_certificate_id: typing.Optional[str]=None, default_route_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RouteSettingsProperty"]]]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, route_settings: typing.Any=None, stage_variables: typing.Any=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Stage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Stage.ApiId``.
        :param stage_name: ``AWS::ApiGatewayV2::Stage.StageName``.
        :param access_log_settings: ``AWS::ApiGatewayV2::Stage.AccessLogSettings``.
        :param auto_deploy: ``AWS::ApiGatewayV2::Stage.AutoDeploy``.
        :param client_certificate_id: ``AWS::ApiGatewayV2::Stage.ClientCertificateId``.
        :param default_route_settings: ``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.
        :param deployment_id: ``AWS::ApiGatewayV2::Stage.DeploymentId``.
        :param description: ``AWS::ApiGatewayV2::Stage.Description``.
        :param route_settings: ``AWS::ApiGatewayV2::Stage.RouteSettings``.
        :param stage_variables: ``AWS::ApiGatewayV2::Stage.StageVariables``.
        :param tags: ``AWS::ApiGatewayV2::Stage.Tags``.

        stability
        :stability: deprecated
        """
        props = CfnStageV2Props(api_id=api_id, stage_name=stage_name, access_log_settings=access_log_settings, auto_deploy=auto_deploy, client_certificate_id=client_certificate_id, default_route_settings=default_route_settings, deployment_id=deployment_id, description=description, route_settings=route_settings, stage_variables=stage_variables, tags=tags)

        jsii.create(CfnStageV2, self, [scope, id, props])

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

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        stability
        :stability: deprecated
        """
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        stability
        :stability: deprecated
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Stage.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str):
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="routeSettings")
    def route_settings(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.RouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        stability
        :stability: deprecated
        """
        return jsii.get(self, "routeSettings")

    @route_settings.setter
    def route_settings(self, value: typing.Any):
        jsii.set(self, "routeSettings", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """``AWS::ApiGatewayV2::Stage.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        stability
        :stability: deprecated
        """
        return jsii.get(self, "stageName")

    @stage_name.setter
    def stage_name(self, value: str):
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="stageVariables")
    def stage_variables(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.StageVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        stability
        :stability: deprecated
        """
        return jsii.get(self, "stageVariables")

    @stage_variables.setter
    def stage_variables(self, value: typing.Any):
        jsii.set(self, "stageVariables", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSettings")
    def access_log_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLogSettingsProperty"]]]:
        """``AWS::ApiGatewayV2::Stage.AccessLogSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        stability
        :stability: deprecated
        """
        return jsii.get(self, "accessLogSettings")

    @access_log_settings.setter
    def access_log_settings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLogSettingsProperty"]]]):
        jsii.set(self, "accessLogSettings", value)

    @builtins.property
    @jsii.member(jsii_name="autoDeploy")
    def auto_deploy(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Stage.AutoDeploy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        stability
        :stability: deprecated
        """
        return jsii.get(self, "autoDeploy")

    @auto_deploy.setter
    def auto_deploy(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "autoDeploy", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateId")
    def client_certificate_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.ClientCertificateId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "clientCertificateId")

    @client_certificate_id.setter
    def client_certificate_id(self, value: typing.Optional[str]):
        jsii.set(self, "clientCertificateId", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRouteSettings")
    def default_route_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RouteSettingsProperty"]]]:
        """``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        stability
        :stability: deprecated
        """
        return jsii.get(self, "defaultRouteSettings")

    @default_route_settings.setter
    def default_route_settings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RouteSettingsProperty"]]]):
        jsii.set(self, "defaultRouteSettings", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.DeploymentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        stability
        :stability: deprecated
        """
        return jsii.get(self, "deploymentId")

    @deployment_id.setter
    def deployment_id(self, value: typing.Optional[str]):
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        stability
        :stability: deprecated
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageV2.AccessLogSettingsProperty", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'format': 'format'})
    class AccessLogSettingsProperty():
        def __init__(self, *, destination_arn: typing.Optional[str]=None, format: typing.Optional[str]=None):
            """
            :param destination_arn: ``CfnStageV2.AccessLogSettingsProperty.DestinationArn``.
            :param format: ``CfnStageV2.AccessLogSettingsProperty.Format``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html
            stability
            :stability: deprecated
            """
            self._values = {
            }
            if destination_arn is not None: self._values["destination_arn"] = destination_arn
            if format is not None: self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[str]:
            """``CfnStageV2.AccessLogSettingsProperty.DestinationArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-destinationarn
            stability
            :stability: deprecated
            """
            return self._values.get('destination_arn')

        @builtins.property
        def format(self) -> typing.Optional[str]:
            """``CfnStageV2.AccessLogSettingsProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-format
            stability
            :stability: deprecated
            """
            return self._values.get('format')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessLogSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageV2.RouteSettingsProperty", jsii_struct_bases=[], name_mapping={'data_trace_enabled': 'dataTraceEnabled', 'detailed_metrics_enabled': 'detailedMetricsEnabled', 'logging_level': 'loggingLevel', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit'})
    class RouteSettingsProperty():
        def __init__(self, *, data_trace_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, detailed_metrics_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, logging_level: typing.Optional[str]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None):
            """
            :param data_trace_enabled: ``CfnStageV2.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnStageV2.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnStageV2.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnStageV2.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnStageV2.RouteSettingsProperty.ThrottlingRateLimit``.

            deprecated
            :deprecated: moved to package aws-apigatewayv2

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            stability
            :stability: deprecated
            """
            self._values = {
            }
            if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None: self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None: self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStageV2.RouteSettingsProperty.DataTraceEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            stability
            :stability: deprecated
            """
            return self._values.get('data_trace_enabled')

        @builtins.property
        def detailed_metrics_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStageV2.RouteSettingsProperty.DetailedMetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            stability
            :stability: deprecated
            """
            return self._values.get('detailed_metrics_enabled')

        @builtins.property
        def logging_level(self) -> typing.Optional[str]:
            """``CfnStageV2.RouteSettingsProperty.LoggingLevel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            stability
            :stability: deprecated
            """
            return self._values.get('logging_level')

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStageV2.RouteSettingsProperty.ThrottlingBurstLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            stability
            :stability: deprecated
            """
            return self._values.get('throttling_burst_limit')

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStageV2.RouteSettingsProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            stability
            :stability: deprecated
            """
            return self._values.get('throttling_rate_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RouteSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnStageV2Props", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'stage_name': 'stageName', 'access_log_settings': 'accessLogSettings', 'auto_deploy': 'autoDeploy', 'client_certificate_id': 'clientCertificateId', 'default_route_settings': 'defaultRouteSettings', 'deployment_id': 'deploymentId', 'description': 'description', 'route_settings': 'routeSettings', 'stage_variables': 'stageVariables', 'tags': 'tags'})
class CfnStageV2Props():
    def __init__(self, *, api_id: str, stage_name: str, access_log_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStageV2.AccessLogSettingsProperty"]]]=None, auto_deploy: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, client_certificate_id: typing.Optional[str]=None, default_route_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStageV2.RouteSettingsProperty"]]]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, route_settings: typing.Any=None, stage_variables: typing.Any=None, tags: typing.Any=None):
        """Properties for defining a ``AWS::ApiGatewayV2::Stage``.

        :param api_id: ``AWS::ApiGatewayV2::Stage.ApiId``.
        :param stage_name: ``AWS::ApiGatewayV2::Stage.StageName``.
        :param access_log_settings: ``AWS::ApiGatewayV2::Stage.AccessLogSettings``.
        :param auto_deploy: ``AWS::ApiGatewayV2::Stage.AutoDeploy``.
        :param client_certificate_id: ``AWS::ApiGatewayV2::Stage.ClientCertificateId``.
        :param default_route_settings: ``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.
        :param deployment_id: ``AWS::ApiGatewayV2::Stage.DeploymentId``.
        :param description: ``AWS::ApiGatewayV2::Stage.Description``.
        :param route_settings: ``AWS::ApiGatewayV2::Stage.RouteSettings``.
        :param stage_variables: ``AWS::ApiGatewayV2::Stage.StageVariables``.
        :param tags: ``AWS::ApiGatewayV2::Stage.Tags``.

        deprecated
        :deprecated: moved to package aws-apigatewayv2

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
        stability
        :stability: deprecated
        """
        self._values = {
            'api_id': api_id,
            'stage_name': stage_name,
        }
        if access_log_settings is not None: self._values["access_log_settings"] = access_log_settings
        if auto_deploy is not None: self._values["auto_deploy"] = auto_deploy
        if client_certificate_id is not None: self._values["client_certificate_id"] = client_certificate_id
        if default_route_settings is not None: self._values["default_route_settings"] = default_route_settings
        if deployment_id is not None: self._values["deployment_id"] = deployment_id
        if description is not None: self._values["description"] = description
        if route_settings is not None: self._values["route_settings"] = route_settings
        if stage_variables is not None: self._values["stage_variables"] = stage_variables
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Stage.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        stability
        :stability: deprecated
        """
        return self._values.get('api_id')

    @builtins.property
    def stage_name(self) -> str:
        """``AWS::ApiGatewayV2::Stage.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        stability
        :stability: deprecated
        """
        return self._values.get('stage_name')

    @builtins.property
    def access_log_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStageV2.AccessLogSettingsProperty"]]]:
        """``AWS::ApiGatewayV2::Stage.AccessLogSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        stability
        :stability: deprecated
        """
        return self._values.get('access_log_settings')

    @builtins.property
    def auto_deploy(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ApiGatewayV2::Stage.AutoDeploy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        stability
        :stability: deprecated
        """
        return self._values.get('auto_deploy')

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.ClientCertificateId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        stability
        :stability: deprecated
        """
        return self._values.get('client_certificate_id')

    @builtins.property
    def default_route_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStageV2.RouteSettingsProperty"]]]:
        """``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        stability
        :stability: deprecated
        """
        return self._values.get('default_route_settings')

    @builtins.property
    def deployment_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.DeploymentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        stability
        :stability: deprecated
        """
        return self._values.get('deployment_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        stability
        :stability: deprecated
        """
        return self._values.get('description')

    @builtins.property
    def route_settings(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.RouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        stability
        :stability: deprecated
        """
        return self._values.get('route_settings')

    @builtins.property
    def stage_variables(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.StageVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        stability
        :stability: deprecated
        """
        return self._values.get('stage_variables')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        stability
        :stability: deprecated
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnStageV2Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUsagePlan(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan"):
    """A CloudFormation ``AWS::ApiGateway::UsagePlan``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::UsagePlan
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_stages: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ApiStageProperty"]]]]]=None, description: typing.Optional[str]=None, quota: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["QuotaSettingsProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, throttle: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ThrottleSettingsProperty"]]]=None, usage_plan_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::UsagePlan``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_stages: ``AWS::ApiGateway::UsagePlan.ApiStages``.
        :param description: ``AWS::ApiGateway::UsagePlan.Description``.
        :param quota: ``AWS::ApiGateway::UsagePlan.Quota``.
        :param tags: ``AWS::ApiGateway::UsagePlan.Tags``.
        :param throttle: ``AWS::ApiGateway::UsagePlan.Throttle``.
        :param usage_plan_name: ``AWS::ApiGateway::UsagePlan.UsagePlanName``.
        """
        props = CfnUsagePlanProps(api_stages=api_stages, description=description, quota=quota, tags=tags, throttle=throttle, usage_plan_name=usage_plan_name)

        jsii.create(CfnUsagePlan, self, [scope, id, props])

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
        """``AWS::ApiGateway::UsagePlan.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="apiStages")
    def api_stages(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ApiStageProperty"]]]]]:
        """``AWS::ApiGateway::UsagePlan.ApiStages``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-apistages
        """
        return jsii.get(self, "apiStages")

    @api_stages.setter
    def api_stages(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ApiStageProperty"]]]]]):
        jsii.set(self, "apiStages", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::UsagePlan.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["QuotaSettingsProperty"]]]:
        """``AWS::ApiGateway::UsagePlan.Quota``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-quota
        """
        return jsii.get(self, "quota")

    @quota.setter
    def quota(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["QuotaSettingsProperty"]]]):
        jsii.set(self, "quota", value)

    @builtins.property
    @jsii.member(jsii_name="throttle")
    def throttle(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ThrottleSettingsProperty"]]]:
        """``AWS::ApiGateway::UsagePlan.Throttle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-throttle
        """
        return jsii.get(self, "throttle")

    @throttle.setter
    def throttle(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ThrottleSettingsProperty"]]]):
        jsii.set(self, "throttle", value)

    @builtins.property
    @jsii.member(jsii_name="usagePlanName")
    def usage_plan_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::UsagePlan.UsagePlanName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-usageplanname
        """
        return jsii.get(self, "usagePlanName")

    @usage_plan_name.setter
    def usage_plan_name(self, value: typing.Optional[str]):
        jsii.set(self, "usagePlanName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan.ApiStageProperty", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'stage': 'stage', 'throttle': 'throttle'})
    class ApiStageProperty():
        def __init__(self, *, api_id: typing.Optional[str]=None, stage: typing.Optional[str]=None, throttle: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[aws_cdk.core.IResolvable, "CfnUsagePlan.ThrottleSettingsProperty"]]]]]=None):
            """
            :param api_id: ``CfnUsagePlan.ApiStageProperty.ApiId``.
            :param stage: ``CfnUsagePlan.ApiStageProperty.Stage``.
            :param throttle: ``CfnUsagePlan.ApiStageProperty.Throttle``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html
            """
            self._values = {
            }
            if api_id is not None: self._values["api_id"] = api_id
            if stage is not None: self._values["stage"] = stage
            if throttle is not None: self._values["throttle"] = throttle

        @builtins.property
        def api_id(self) -> typing.Optional[str]:
            """``CfnUsagePlan.ApiStageProperty.ApiId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html#cfn-apigateway-usageplan-apistage-apiid
            """
            return self._values.get('api_id')

        @builtins.property
        def stage(self) -> typing.Optional[str]:
            """``CfnUsagePlan.ApiStageProperty.Stage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html#cfn-apigateway-usageplan-apistage-stage
            """
            return self._values.get('stage')

        @builtins.property
        def throttle(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,typing.Union[aws_cdk.core.IResolvable, "CfnUsagePlan.ThrottleSettingsProperty"]]]]]:
            """``CfnUsagePlan.ApiStageProperty.Throttle``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html#cfn-apigateway-usageplan-apistage-throttle
            """
            return self._values.get('throttle')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ApiStageProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan.QuotaSettingsProperty", jsii_struct_bases=[], name_mapping={'limit': 'limit', 'offset': 'offset', 'period': 'period'})
    class QuotaSettingsProperty():
        def __init__(self, *, limit: typing.Optional[jsii.Number]=None, offset: typing.Optional[jsii.Number]=None, period: typing.Optional[str]=None):
            """
            :param limit: ``CfnUsagePlan.QuotaSettingsProperty.Limit``.
            :param offset: ``CfnUsagePlan.QuotaSettingsProperty.Offset``.
            :param period: ``CfnUsagePlan.QuotaSettingsProperty.Period``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html
            """
            self._values = {
            }
            if limit is not None: self._values["limit"] = limit
            if offset is not None: self._values["offset"] = offset
            if period is not None: self._values["period"] = period

        @builtins.property
        def limit(self) -> typing.Optional[jsii.Number]:
            """``CfnUsagePlan.QuotaSettingsProperty.Limit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html#cfn-apigateway-usageplan-quotasettings-limit
            """
            return self._values.get('limit')

        @builtins.property
        def offset(self) -> typing.Optional[jsii.Number]:
            """``CfnUsagePlan.QuotaSettingsProperty.Offset``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html#cfn-apigateway-usageplan-quotasettings-offset
            """
            return self._values.get('offset')

        @builtins.property
        def period(self) -> typing.Optional[str]:
            """``CfnUsagePlan.QuotaSettingsProperty.Period``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html#cfn-apigateway-usageplan-quotasettings-period
            """
            return self._values.get('period')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'QuotaSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlan.ThrottleSettingsProperty", jsii_struct_bases=[], name_mapping={'burst_limit': 'burstLimit', 'rate_limit': 'rateLimit'})
    class ThrottleSettingsProperty():
        def __init__(self, *, burst_limit: typing.Optional[jsii.Number]=None, rate_limit: typing.Optional[jsii.Number]=None):
            """
            :param burst_limit: ``CfnUsagePlan.ThrottleSettingsProperty.BurstLimit``.
            :param rate_limit: ``CfnUsagePlan.ThrottleSettingsProperty.RateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-throttlesettings.html
            """
            self._values = {
            }
            if burst_limit is not None: self._values["burst_limit"] = burst_limit
            if rate_limit is not None: self._values["rate_limit"] = rate_limit

        @builtins.property
        def burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnUsagePlan.ThrottleSettingsProperty.BurstLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-throttlesettings.html#cfn-apigateway-usageplan-throttlesettings-burstlimit
            """
            return self._values.get('burst_limit')

        @builtins.property
        def rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnUsagePlan.ThrottleSettingsProperty.RateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-throttlesettings.html#cfn-apigateway-usageplan-throttlesettings-ratelimit
            """
            return self._values.get('rate_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ThrottleSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnUsagePlanKey(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlanKey"):
    """A CloudFormation ``AWS::ApiGateway::UsagePlanKey``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::UsagePlanKey
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, key_id: str, key_type: str, usage_plan_id: str) -> None:
        """Create a new ``AWS::ApiGateway::UsagePlanKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_id: ``AWS::ApiGateway::UsagePlanKey.KeyId``.
        :param key_type: ``AWS::ApiGateway::UsagePlanKey.KeyType``.
        :param usage_plan_id: ``AWS::ApiGateway::UsagePlanKey.UsagePlanId``.
        """
        props = CfnUsagePlanKeyProps(key_id=key_id, key_type=key_type, usage_plan_id=usage_plan_id)

        jsii.create(CfnUsagePlanKey, self, [scope, id, props])

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
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        """``AWS::ApiGateway::UsagePlanKey.KeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-keyid
        """
        return jsii.get(self, "keyId")

    @key_id.setter
    def key_id(self, value: str):
        jsii.set(self, "keyId", value)

    @builtins.property
    @jsii.member(jsii_name="keyType")
    def key_type(self) -> str:
        """``AWS::ApiGateway::UsagePlanKey.KeyType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-keytype
        """
        return jsii.get(self, "keyType")

    @key_type.setter
    def key_type(self, value: str):
        jsii.set(self, "keyType", value)

    @builtins.property
    @jsii.member(jsii_name="usagePlanId")
    def usage_plan_id(self) -> str:
        """``AWS::ApiGateway::UsagePlanKey.UsagePlanId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-usageplanid
        """
        return jsii.get(self, "usagePlanId")

    @usage_plan_id.setter
    def usage_plan_id(self, value: str):
        jsii.set(self, "usagePlanId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlanKeyProps", jsii_struct_bases=[], name_mapping={'key_id': 'keyId', 'key_type': 'keyType', 'usage_plan_id': 'usagePlanId'})
class CfnUsagePlanKeyProps():
    def __init__(self, *, key_id: str, key_type: str, usage_plan_id: str):
        """Properties for defining a ``AWS::ApiGateway::UsagePlanKey``.

        :param key_id: ``AWS::ApiGateway::UsagePlanKey.KeyId``.
        :param key_type: ``AWS::ApiGateway::UsagePlanKey.KeyType``.
        :param usage_plan_id: ``AWS::ApiGateway::UsagePlanKey.UsagePlanId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html
        """
        self._values = {
            'key_id': key_id,
            'key_type': key_type,
            'usage_plan_id': usage_plan_id,
        }

    @builtins.property
    def key_id(self) -> str:
        """``AWS::ApiGateway::UsagePlanKey.KeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-keyid
        """
        return self._values.get('key_id')

    @builtins.property
    def key_type(self) -> str:
        """``AWS::ApiGateway::UsagePlanKey.KeyType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-keytype
        """
        return self._values.get('key_type')

    @builtins.property
    def usage_plan_id(self) -> str:
        """``AWS::ApiGateway::UsagePlanKey.UsagePlanId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-usageplanid
        """
        return self._values.get('usage_plan_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUsagePlanKeyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnUsagePlanProps", jsii_struct_bases=[], name_mapping={'api_stages': 'apiStages', 'description': 'description', 'quota': 'quota', 'tags': 'tags', 'throttle': 'throttle', 'usage_plan_name': 'usagePlanName'})
class CfnUsagePlanProps():
    def __init__(self, *, api_stages: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUsagePlan.ApiStageProperty"]]]]]=None, description: typing.Optional[str]=None, quota: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUsagePlan.QuotaSettingsProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, throttle: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUsagePlan.ThrottleSettingsProperty"]]]=None, usage_plan_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::UsagePlan``.

        :param api_stages: ``AWS::ApiGateway::UsagePlan.ApiStages``.
        :param description: ``AWS::ApiGateway::UsagePlan.Description``.
        :param quota: ``AWS::ApiGateway::UsagePlan.Quota``.
        :param tags: ``AWS::ApiGateway::UsagePlan.Tags``.
        :param throttle: ``AWS::ApiGateway::UsagePlan.Throttle``.
        :param usage_plan_name: ``AWS::ApiGateway::UsagePlan.UsagePlanName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html
        """
        self._values = {
        }
        if api_stages is not None: self._values["api_stages"] = api_stages
        if description is not None: self._values["description"] = description
        if quota is not None: self._values["quota"] = quota
        if tags is not None: self._values["tags"] = tags
        if throttle is not None: self._values["throttle"] = throttle
        if usage_plan_name is not None: self._values["usage_plan_name"] = usage_plan_name

    @builtins.property
    def api_stages(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUsagePlan.ApiStageProperty"]]]]]:
        """``AWS::ApiGateway::UsagePlan.ApiStages``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-apistages
        """
        return self._values.get('api_stages')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::UsagePlan.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-description
        """
        return self._values.get('description')

    @builtins.property
    def quota(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUsagePlan.QuotaSettingsProperty"]]]:
        """``AWS::ApiGateway::UsagePlan.Quota``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-quota
        """
        return self._values.get('quota')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApiGateway::UsagePlan.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-tags
        """
        return self._values.get('tags')

    @builtins.property
    def throttle(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnUsagePlan.ThrottleSettingsProperty"]]]:
        """``AWS::ApiGateway::UsagePlan.Throttle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-throttle
        """
        return self._values.get('throttle')

    @builtins.property
    def usage_plan_name(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::UsagePlan.UsagePlanName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-usageplanname
        """
        return self._values.get('usage_plan_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUsagePlanProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVpcLink(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.CfnVpcLink"):
    """A CloudFormation ``AWS::ApiGateway::VpcLink``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGateway::VpcLink
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, target_arns: typing.List[str], description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGateway::VpcLink``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::ApiGateway::VpcLink.Name``.
        :param target_arns: ``AWS::ApiGateway::VpcLink.TargetArns``.
        :param description: ``AWS::ApiGateway::VpcLink.Description``.
        """
        props = CfnVpcLinkProps(name=name, target_arns=target_arns, description=description)

        jsii.create(CfnVpcLink, self, [scope, id, props])

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
        """``AWS::ApiGateway::VpcLink.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="targetArns")
    def target_arns(self) -> typing.List[str]:
        """``AWS::ApiGateway::VpcLink.TargetArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-targetarns
        """
        return jsii.get(self, "targetArns")

    @target_arns.setter
    def target_arns(self, value: typing.List[str]):
        jsii.set(self, "targetArns", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::VpcLink.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CfnVpcLinkProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'target_arns': 'targetArns', 'description': 'description'})
class CfnVpcLinkProps():
    def __init__(self, *, name: str, target_arns: typing.List[str], description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ApiGateway::VpcLink``.

        :param name: ``AWS::ApiGateway::VpcLink.Name``.
        :param target_arns: ``AWS::ApiGateway::VpcLink.TargetArns``.
        :param description: ``AWS::ApiGateway::VpcLink.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html
        """
        self._values = {
            'name': name,
            'target_arns': target_arns,
        }
        if description is not None: self._values["description"] = description

    @builtins.property
    def name(self) -> str:
        """``AWS::ApiGateway::VpcLink.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-name
        """
        return self._values.get('name')

    @builtins.property
    def target_arns(self) -> typing.List[str]:
        """``AWS::ApiGateway::VpcLink.TargetArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-targetarns
        """
        return self._values.get('target_arns')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGateway::VpcLink.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnVpcLinkProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.ConnectionType")
class ConnectionType(enum.Enum):
    INTERNET = "INTERNET"
    """For connections through the public routable internet."""
    VPC_LINK = "VPC_LINK"
    """For private connections between API Gateway and a network load balancer in a VPC."""

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.ContentHandling")
class ContentHandling(enum.Enum):
    CONVERT_TO_BINARY = "CONVERT_TO_BINARY"
    """Converts a request payload from a base64-encoded string to a binary blob."""
    CONVERT_TO_TEXT = "CONVERT_TO_TEXT"
    """Converts a request payload from a binary blob to a base64-encoded string."""

class Cors(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Cors"):
    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_METHODS")
    def ALL_METHODS(cls) -> typing.List[str]:
        """All HTTP methods."""
        return jsii.sget(cls, "ALL_METHODS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_ORIGINS")
    def ALL_ORIGINS(cls) -> typing.List[str]:
        """All origins."""
        return jsii.sget(cls, "ALL_ORIGINS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_HEADERS")
    def DEFAULT_HEADERS(cls) -> typing.List[str]:
        """The set of default headers allowed for CORS and useful for API Gateway."""
        return jsii.sget(cls, "DEFAULT_HEADERS")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.CorsOptions", jsii_struct_bases=[], name_mapping={'allow_origins': 'allowOrigins', 'allow_credentials': 'allowCredentials', 'allow_headers': 'allowHeaders', 'allow_methods': 'allowMethods', 'disable_cache': 'disableCache', 'expose_headers': 'exposeHeaders', 'max_age': 'maxAge', 'status_code': 'statusCode'})
class CorsOptions():
    def __init__(self, *, allow_origins: typing.List[str], allow_credentials: typing.Optional[bool]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List[str]]=None, disable_cache: typing.Optional[bool]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[aws_cdk.core.Duration]=None, status_code: typing.Optional[jsii.Number]=None):
        """
        :param allow_origins: Specifies the list of origins that are allowed to make requests to this resource. If you wish to allow all origins, specify ``Cors.ALL_ORIGINS`` or ``[ * ]``. Responses will include the ``Access-Control-Allow-Origin`` response header. If ``Cors.ALL_ORIGINS`` is specified, the ``Vary: Origin`` response header will also be included.
        :param allow_credentials: The Access-Control-Allow-Credentials response header tells browsers whether to expose the response to frontend JavaScript code when the request's credentials mode (Request.credentials) is "include". When a request's credentials mode (Request.credentials) is "include", browsers will only expose the response to frontend JavaScript code if the Access-Control-Allow-Credentials value is true. Credentials are cookies, authorization headers or TLS client certificates. Default: false
        :param allow_headers: The Access-Control-Allow-Headers response header is used in response to a preflight request which includes the Access-Control-Request-Headers to indicate which HTTP headers can be used during the actual request. Default: Cors.DEFAULT_HEADERS
        :param allow_methods: The Access-Control-Allow-Methods response header specifies the method or methods allowed when accessing the resource in response to a preflight request. If ``ANY`` is specified, it will be expanded to ``Cors.ALL_METHODS``. Default: Cors.ALL_METHODS
        :param disable_cache: Sets Access-Control-Max-Age to -1, which means that caching is disabled. This option cannot be used with ``maxAge``. Default: - cache is enabled
        :param expose_headers: The Access-Control-Expose-Headers response header indicates which headers can be exposed as part of the response by listing their names. If you want clients to be able to access other headers, you have to list them using the Access-Control-Expose-Headers header. Default: - only the 6 CORS-safelisted response headers are exposed: Cache-Control, Content-Language, Content-Type, Expires, Last-Modified, Pragma
        :param max_age: The Access-Control-Max-Age response header indicates how long the results of a preflight request (that is the information contained in the Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can be cached. To disable caching altogther use ``disableCache: true``. Default: - browser-specific (see reference)
        :param status_code: Specifies the response status code returned from the OPTIONS method. Default: 204
        """
        self._values = {
            'allow_origins': allow_origins,
        }
        if allow_credentials is not None: self._values["allow_credentials"] = allow_credentials
        if allow_headers is not None: self._values["allow_headers"] = allow_headers
        if allow_methods is not None: self._values["allow_methods"] = allow_methods
        if disable_cache is not None: self._values["disable_cache"] = disable_cache
        if expose_headers is not None: self._values["expose_headers"] = expose_headers
        if max_age is not None: self._values["max_age"] = max_age
        if status_code is not None: self._values["status_code"] = status_code

    @builtins.property
    def allow_origins(self) -> typing.List[str]:
        """Specifies the list of origins that are allowed to make requests to this resource.

        If you wish to allow all origins, specify ``Cors.ALL_ORIGINS`` or
        ``[ * ]``.

        Responses will include the ``Access-Control-Allow-Origin`` response header.
        If ``Cors.ALL_ORIGINS`` is specified, the ``Vary: Origin`` response header will
        also be included.

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
        """
        return self._values.get('allow_origins')

    @builtins.property
    def allow_credentials(self) -> typing.Optional[bool]:
        """The Access-Control-Allow-Credentials response header tells browsers whether to expose the response to frontend JavaScript code when the request's credentials mode (Request.credentials) is "include".

        When a request's credentials mode (Request.credentials) is "include",
        browsers will only expose the response to frontend JavaScript code if the
        Access-Control-Allow-Credentials value is true.

        Credentials are cookies, authorization headers or TLS client certificates.

        default
        :default: false

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials
        """
        return self._values.get('allow_credentials')

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[str]]:
        """The Access-Control-Allow-Headers response header is used in response to a preflight request which includes the Access-Control-Request-Headers to indicate which HTTP headers can be used during the actual request.

        default
        :default: Cors.DEFAULT_HEADERS

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
        """
        return self._values.get('allow_headers')

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List[str]]:
        """The Access-Control-Allow-Methods response header specifies the method or methods allowed when accessing the resource in response to a preflight request.

        If ``ANY`` is specified, it will be expanded to ``Cors.ALL_METHODS``.

        default
        :default: Cors.ALL_METHODS

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods
        """
        return self._values.get('allow_methods')

    @builtins.property
    def disable_cache(self) -> typing.Optional[bool]:
        """Sets Access-Control-Max-Age to -1, which means that caching is disabled.

        This option cannot be used with ``maxAge``.

        default
        :default: - cache is enabled
        """
        return self._values.get('disable_cache')

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[str]]:
        """The Access-Control-Expose-Headers response header indicates which headers can be exposed as part of the response by listing their names.

        If you want clients to be able to access other headers, you have to list
        them using the Access-Control-Expose-Headers header.

        default
        :default:

        - only the 6 CORS-safelisted response headers are exposed:
          Cache-Control, Content-Language, Content-Type, Expires, Last-Modified,
          Pragma

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Expose-Headers
        """
        return self._values.get('expose_headers')

    @builtins.property
    def max_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The Access-Control-Max-Age response header indicates how long the results of a preflight request (that is the information contained in the Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can be cached.

        To disable caching altogther use ``disableCache: true``.

        default
        :default: - browser-specific (see reference)

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Max-Age
        """
        return self._values.get('max_age')

    @builtins.property
    def status_code(self) -> typing.Optional[jsii.Number]:
        """Specifies the response status code returned from the OPTIONS method.

        default
        :default: 204
        """
        return self._values.get('status_code')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CorsOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Deployment(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Deployment"):
    """A Deployment of a REST API.

    An immutable representation of a RestApi resource that can be called by users
    using Stages. A deployment must be associated with a Stage for it to be
    callable over the Internet.

    Normally, you don't need to define deployments manually. The RestApi
    construct manages a Deployment resource that represents the latest model. It
    can be accessed through ``restApi.latestDeployment`` (unless ``deploy: false`` is
    set when defining the ``RestApi``).

    If you manually define this resource, you will need to know that since
    deployments are immutable, as long as the resource's logical ID doesn't
    change, the deployment will represent the snapshot in time in which the
    resource was created. This means that if you modify the RestApi model (i.e.
    add methods or resources), these changes will not be reflected unless a new
    deployment resource is created.

    To achieve this behavior, the method ``addToLogicalId(data)`` can be used to
    augment the logical ID generated for the deployment resource such that it
    will include arbitrary data. This is done automatically for the
    ``restApi.latestDeployment`` deployment.

    Furthermore, since a deployment does not reference any of the REST API
    resources and methods, CloudFormation will likely provision it before these
    resources are created, which means that it will represent a "half-baked"
    model. Use the ``node.addDependency(dep)`` method to circumvent that. This is done
    automatically for the ``restApi.latestDeployment`` deployment.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api: "IRestApi", description: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param api: The Rest API to deploy.
        :param description: A description of the purpose of the API Gateway deployment. Default: - No description.
        :param retain_deployments: When an API Gateway model is updated, a new deployment will automatically be created. If this is true (default), the old API Gateway Deployment resource will not be deleted. This will allow manually reverting back to a previous deployment in case for example Default: false
        """
        props = DeploymentProps(api=api, description=description, retain_deployments=retain_deployments)

        jsii.create(Deployment, self, [scope, id, props])

    @jsii.member(jsii_name="addToLogicalId")
    def add_to_logical_id(self, data: typing.Any) -> None:
        """Adds a component to the hash that determines this Deployment resource's logical ID.

        This should be called by constructs of the API Gateway model that want to
        invalidate the deployment when their settings change. The component will
        be resolve()ed during synthesis so tokens are welcome.

        :param data: -
        """
        return jsii.invoke(self, "addToLogicalId", [data])

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> "IRestApi":
        return jsii.get(self, "api")

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.DeploymentProps", jsii_struct_bases=[], name_mapping={'api': 'api', 'description': 'description', 'retain_deployments': 'retainDeployments'})
class DeploymentProps():
    def __init__(self, *, api: "IRestApi", description: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None):
        """
        :param api: The Rest API to deploy.
        :param description: A description of the purpose of the API Gateway deployment. Default: - No description.
        :param retain_deployments: When an API Gateway model is updated, a new deployment will automatically be created. If this is true (default), the old API Gateway Deployment resource will not be deleted. This will allow manually reverting back to a previous deployment in case for example Default: false
        """
        self._values = {
            'api': api,
        }
        if description is not None: self._values["description"] = description
        if retain_deployments is not None: self._values["retain_deployments"] = retain_deployments

    @builtins.property
    def api(self) -> "IRestApi":
        """The Rest API to deploy."""
        return self._values.get('api')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the purpose of the API Gateway deployment.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def retain_deployments(self) -> typing.Optional[bool]:
        """When an API Gateway model is updated, a new deployment will automatically be created.

        If this is true (default), the old API Gateway Deployment resource will not be deleted.
        This will allow manually reverting back to a previous deployment in case for example

        default
        :default: false
        """
        return self._values.get('retain_deployments')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.DomainNameAttributes", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'domain_name_alias_hosted_zone_id': 'domainNameAliasHostedZoneId', 'domain_name_alias_target': 'domainNameAliasTarget'})
class DomainNameAttributes():
    def __init__(self, *, domain_name: str, domain_name_alias_hosted_zone_id: str, domain_name_alias_target: str):
        """
        :param domain_name: The domain name (e.g. ``example.com``).
        :param domain_name_alias_hosted_zone_id: Thje Route53 hosted zone ID to use in order to connect a record set to this domain through an alias.
        :param domain_name_alias_target: The Route53 alias target to use in order to connect a record set to this domain through an alias.
        """
        self._values = {
            'domain_name': domain_name,
            'domain_name_alias_hosted_zone_id': domain_name_alias_hosted_zone_id,
            'domain_name_alias_target': domain_name_alias_target,
        }

    @builtins.property
    def domain_name(self) -> str:
        """The domain name (e.g. ``example.com``)."""
        return self._values.get('domain_name')

    @builtins.property
    def domain_name_alias_hosted_zone_id(self) -> str:
        """Thje Route53 hosted zone ID to use in order to connect a record set to this domain through an alias."""
        return self._values.get('domain_name_alias_hosted_zone_id')

    @builtins.property
    def domain_name_alias_target(self) -> str:
        """The Route53 alias target to use in order to connect a record set to this domain through an alias."""
        return self._values.get('domain_name_alias_target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DomainNameAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.DomainNameOptions", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'domain_name': 'domainName', 'endpoint_type': 'endpointType'})
class DomainNameOptions():
    def __init__(self, *, certificate: aws_cdk.aws_certificatemanager.ICertificate, domain_name: str, endpoint_type: typing.Optional["EndpointType"]=None):
        """
        :param certificate: The reference to an AWS-managed certificate for use by the edge-optimized endpoint for the domain name. For "EDGE" domain names, the certificate needs to be in the US East (N. Virginia) region.
        :param domain_name: The custom domain name for your API. Uppercase letters are not supported.
        :param endpoint_type: The type of endpoint for this DomainName. Default: REGIONAL
        """
        self._values = {
            'certificate': certificate,
            'domain_name': domain_name,
        }
        if endpoint_type is not None: self._values["endpoint_type"] = endpoint_type

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        """The reference to an AWS-managed certificate for use by the edge-optimized endpoint for the domain name.

        For "EDGE" domain names, the certificate
        needs to be in the US East (N. Virginia) region.
        """
        return self._values.get('certificate')

    @builtins.property
    def domain_name(self) -> str:
        """The custom domain name for your API.

        Uppercase letters are not supported.
        """
        return self._values.get('domain_name')

    @builtins.property
    def endpoint_type(self) -> typing.Optional["EndpointType"]:
        """The type of endpoint for this DomainName.

        default
        :default: REGIONAL
        """
        return self._values.get('endpoint_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DomainNameOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.DomainNameProps", jsii_struct_bases=[DomainNameOptions], name_mapping={'certificate': 'certificate', 'domain_name': 'domainName', 'endpoint_type': 'endpointType', 'mapping': 'mapping'})
class DomainNameProps(DomainNameOptions):
    def __init__(self, *, certificate: aws_cdk.aws_certificatemanager.ICertificate, domain_name: str, endpoint_type: typing.Optional["EndpointType"]=None, mapping: typing.Optional["IRestApi"]=None):
        """
        :param certificate: The reference to an AWS-managed certificate for use by the edge-optimized endpoint for the domain name. For "EDGE" domain names, the certificate needs to be in the US East (N. Virginia) region.
        :param domain_name: The custom domain name for your API. Uppercase letters are not supported.
        :param endpoint_type: The type of endpoint for this DomainName. Default: REGIONAL
        :param mapping: If specified, all requests to this domain will be mapped to the production deployment of this API. If you wish to map this domain to multiple APIs with different base paths, don't specify this option and use ``addBasePathMapping``. Default: - you will have to call ``addBasePathMapping`` to map this domain to API endpoints.
        """
        self._values = {
            'certificate': certificate,
            'domain_name': domain_name,
        }
        if endpoint_type is not None: self._values["endpoint_type"] = endpoint_type
        if mapping is not None: self._values["mapping"] = mapping

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        """The reference to an AWS-managed certificate for use by the edge-optimized endpoint for the domain name.

        For "EDGE" domain names, the certificate
        needs to be in the US East (N. Virginia) region.
        """
        return self._values.get('certificate')

    @builtins.property
    def domain_name(self) -> str:
        """The custom domain name for your API.

        Uppercase letters are not supported.
        """
        return self._values.get('domain_name')

    @builtins.property
    def endpoint_type(self) -> typing.Optional["EndpointType"]:
        """The type of endpoint for this DomainName.

        default
        :default: REGIONAL
        """
        return self._values.get('endpoint_type')

    @builtins.property
    def mapping(self) -> typing.Optional["IRestApi"]:
        """If specified, all requests to this domain will be mapped to the production deployment of this API.

        If you wish to map this domain to multiple APIs
        with different base paths, don't specify this option and use
        ``addBasePathMapping``.

        default
        :default:

        - you will have to call ``addBasePathMapping`` to map this domain to
          API endpoints.
        """
        return self._values.get('mapping')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DomainNameProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.EndpointType")
class EndpointType(enum.Enum):
    EDGE = "EDGE"
    """For an edge-optimized API and its custom domain name."""
    REGIONAL = "REGIONAL"
    """For a regional API and its custom domain name."""
    PRIVATE = "PRIVATE"
    """For a private API and its custom domain name."""

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.HttpIntegrationProps", jsii_struct_bases=[], name_mapping={'http_method': 'httpMethod', 'options': 'options', 'proxy': 'proxy'})
class HttpIntegrationProps():
    def __init__(self, *, http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, proxy: typing.Optional[bool]=None):
        """
        :param http_method: HTTP method to use when invoking the backend URL. Default: GET
        :param options: Integration options, such as request/resopnse mapping, content handling, etc. Default: defaults based on ``IntegrationOptions`` defaults
        :param proxy: Determines whether to use proxy integration or custom integration. Default: true
        """
        if isinstance(options, dict): options = IntegrationOptions(**options)
        self._values = {
        }
        if http_method is not None: self._values["http_method"] = http_method
        if options is not None: self._values["options"] = options
        if proxy is not None: self._values["proxy"] = proxy

    @builtins.property
    def http_method(self) -> typing.Optional[str]:
        """HTTP method to use when invoking the backend URL.

        default
        :default: GET
        """
        return self._values.get('http_method')

    @builtins.property
    def options(self) -> typing.Optional["IntegrationOptions"]:
        """Integration options, such as request/resopnse mapping, content handling, etc.

        default
        :default: defaults based on ``IntegrationOptions`` defaults
        """
        return self._values.get('options')

    @builtins.property
    def proxy(self) -> typing.Optional[bool]:
        """Determines whether to use proxy integration or custom integration.

        default
        :default: true
        """
        return self._values.get('proxy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpIntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IApiKey")
class IApiKey(aws_cdk.core.IResource, jsii.compat.Protocol):
    """API keys are alphanumeric string values that you distribute to app developer customers to grant access to your API."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApiKeyProxy

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        """The API key ID.

        attribute:
        :attribute:: true
        """
        ...


class _IApiKeyProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """API keys are alphanumeric string values that you distribute to app developer customers to grant access to your API."""
    __jsii_type__ = "@aws-cdk/aws-apigateway.IApiKey"
    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        """The API key ID.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "keyId")


@jsii.implements(IApiKey)
class ApiKey(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.ApiKey"):
    """An API Gateway ApiKey.

    An ApiKey can be distributed to API clients that are executing requests
    for Method resources that require an Api Key.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key_name: typing.Optional[str]=None, customer_id: typing.Optional[str]=None, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, generate_distinct_id: typing.Optional[bool]=None, resources: typing.Optional[typing.List["RestApi"]]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param api_key_name: A name for the API key. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the API key name. Default: automically generated name
        :param customer_id: An AWS Marketplace customer identifier to use when integrating with the AWS SaaS Marketplace. Default: none
        :param description: A description of the purpose of the API key. Default: none
        :param enabled: Indicates whether the API key can be used by clients. Default: true
        :param generate_distinct_id: Specifies whether the key identifier is distinct from the created API key value. Default: false
        :param resources: A list of resources this api key is associated with. Default: none
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        props = ApiKeyProps(api_key_name=api_key_name, customer_id=customer_id, description=description, enabled=enabled, generate_distinct_id=generate_distinct_id, resources=resources, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        jsii.create(ApiKey, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        """The API key ID."""
        return jsii.get(self, "keyId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IAuthorizer")
class IAuthorizer(jsii.compat.Protocol):
    """Represents an API Gateway authorizer."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAuthorizerProxy

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> str:
        """The authorizer ID.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional["AuthorizationType"]:
        """The authorization type of this authorizer."""
        ...


class _IAuthorizerProxy():
    """Represents an API Gateway authorizer."""
    __jsii_type__ = "@aws-cdk/aws-apigateway.IAuthorizer"
    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> str:
        """The authorizer ID.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "authorizerId")

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional["AuthorizationType"]:
        """The authorization type of this authorizer."""
        return jsii.get(self, "authorizationType")


@jsii.implements(IAuthorizer)
class Authorizer(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-apigateway.Authorizer"):
    """Base class for all custom authorizers."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _AuthorizerProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = aws_cdk.core.ResourceProps(physical_name=physical_name)

        jsii.create(Authorizer, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    @abc.abstractmethod
    def authorizer_id(self) -> str:
        """The authorizer ID."""
        ...

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional["AuthorizationType"]:
        """The authorization type of this authorizer."""
        return jsii.get(self, "authorizationType")


class _AuthorizerProxy(Authorizer, jsii.proxy_for(aws_cdk.core.Resource)):
    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> str:
        """The authorizer ID."""
        return jsii.get(self, "authorizerId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IDomainName")
class IDomainName(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDomainNameProxy

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name (e.g. ``example.com``).

        attribute:
        :attribute:: DomainName
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="domainNameAliasDomainName")
    def domain_name_alias_domain_name(self) -> str:
        """The Route53 alias target to use in order to connect a record set to this domain through an alias.

        attribute:
        :attribute:: DistributionDomainName,RegionalDomainName
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="domainNameAliasHostedZoneId")
    def domain_name_alias_hosted_zone_id(self) -> str:
        """The Route53 hosted zone ID to use in order to connect a record set to this domain through an alias.

        attribute:
        :attribute:: DistributionHostedZoneId,RegionalHostedZoneId
        """
        ...


class _IDomainNameProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-apigateway.IDomainName"
    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name (e.g. ``example.com``).

        attribute:
        :attribute:: DomainName
        """
        return jsii.get(self, "domainName")

    @builtins.property
    @jsii.member(jsii_name="domainNameAliasDomainName")
    def domain_name_alias_domain_name(self) -> str:
        """The Route53 alias target to use in order to connect a record set to this domain through an alias.

        attribute:
        :attribute:: DistributionDomainName,RegionalDomainName
        """
        return jsii.get(self, "domainNameAliasDomainName")

    @builtins.property
    @jsii.member(jsii_name="domainNameAliasHostedZoneId")
    def domain_name_alias_hosted_zone_id(self) -> str:
        """The Route53 hosted zone ID to use in order to connect a record set to this domain through an alias.

        attribute:
        :attribute:: DistributionHostedZoneId,RegionalHostedZoneId
        """
        return jsii.get(self, "domainNameAliasHostedZoneId")


@jsii.implements(IDomainName)
class DomainName(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.DomainName"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, mapping: typing.Optional["IRestApi"]=None, certificate: aws_cdk.aws_certificatemanager.ICertificate, domain_name: str, endpoint_type: typing.Optional["EndpointType"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mapping: If specified, all requests to this domain will be mapped to the production deployment of this API. If you wish to map this domain to multiple APIs with different base paths, don't specify this option and use ``addBasePathMapping``. Default: - you will have to call ``addBasePathMapping`` to map this domain to API endpoints.
        :param certificate: The reference to an AWS-managed certificate for use by the edge-optimized endpoint for the domain name. For "EDGE" domain names, the certificate needs to be in the US East (N. Virginia) region.
        :param domain_name: The custom domain name for your API. Uppercase letters are not supported.
        :param endpoint_type: The type of endpoint for this DomainName. Default: REGIONAL
        """
        props = DomainNameProps(mapping=mapping, certificate=certificate, domain_name=domain_name, endpoint_type=endpoint_type)

        jsii.create(DomainName, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainNameAttributes")
    @builtins.classmethod
    def from_domain_name_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, domain_name_alias_hosted_zone_id: str, domain_name_alias_target: str) -> "IDomainName":
        """Imports an existing domain name.

        :param scope: -
        :param id: -
        :param domain_name: The domain name (e.g. ``example.com``).
        :param domain_name_alias_hosted_zone_id: Thje Route53 hosted zone ID to use in order to connect a record set to this domain through an alias.
        :param domain_name_alias_target: The Route53 alias target to use in order to connect a record set to this domain through an alias.
        """
        attrs = DomainNameAttributes(domain_name=domain_name, domain_name_alias_hosted_zone_id=domain_name_alias_hosted_zone_id, domain_name_alias_target=domain_name_alias_target)

        return jsii.sinvoke(cls, "fromDomainNameAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addBasePathMapping")
    def add_base_path_mapping(self, target_api: "IRestApi", *, base_path: typing.Optional[str]=None) -> "BasePathMapping":
        """Maps this domain to an API endpoint.

        :param target_api: That target API endpoint, requests will be mapped to the deployment stage.
        :param base_path: The base path name that callers of the API must provide in the URL after the domain name (e.g. ``example.com/base-path``). If you specify this property, it can't be an empty string. Default: - map requests from the domain root (e.g. ``example.com``). If this is undefined, no additional mappings will be allowed on this domain name.
        """
        options = BasePathMappingOptions(base_path=base_path)

        return jsii.invoke(self, "addBasePathMapping", [target_api, options])

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name (e.g. ``example.com``)."""
        return jsii.get(self, "domainName")

    @builtins.property
    @jsii.member(jsii_name="domainNameAliasDomainName")
    def domain_name_alias_domain_name(self) -> str:
        """The Route53 alias target to use in order to connect a record set to this domain through an alias."""
        return jsii.get(self, "domainNameAliasDomainName")

    @builtins.property
    @jsii.member(jsii_name="domainNameAliasHostedZoneId")
    def domain_name_alias_hosted_zone_id(self) -> str:
        """The Route53 hosted zone ID to use in order to connect a record set to this domain through an alias."""
        return jsii.get(self, "domainNameAliasHostedZoneId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IModel")
class IModel(jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IModelProxy

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        """Returns the model name, such as 'myModel'.

        attribute:
        :attribute:: true
        """
        ...


class _IModelProxy():
    __jsii_type__ = "@aws-cdk/aws-apigateway.IModel"
    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        """Returns the model name, such as 'myModel'.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "modelId")


@jsii.implements(IModel)
class EmptyModel(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.EmptyModel"):
    """Represents a reference to a REST API's Empty model, which is available as part of the model collection by default.

    This can be used for mapping
    JSON responses from an integration to what is returned to a client,
    where strong typing is not required. In the absence of any defined
    model, the Empty model will be used to return the response payload
    unmapped.

    Definition
    {
    "$schema" : "http://json-schema.org/draft-04/schema#",
    "title" : "Empty Schema",
    "type" : "object"
    }

    deprecated
    :deprecated: You should use

    see
    :see: Model.EMPTY_MODEL
    stability
    :stability: deprecated
    """
    def __init__(self) -> None:
        jsii.create(EmptyModel, self, [])

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        """Returns the model name, such as 'myModel'.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "modelId")


@jsii.implements(IModel)
class ErrorModel(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.ErrorModel"):
    """Represents a reference to a REST API's Error model, which is available as part of the model collection by default.

    This can be used for mapping
    error JSON responses from an integration to a client, where a simple
    generic message field is sufficient to map and return an error payload.

    Definition
    {
    "$schema" : "http://json-schema.org/draft-04/schema#",
    "title" : "Error Schema",
    "type" : "object",
    "properties" : {
    "message" : { "type" : "string" }
    }
    }

    deprecated
    :deprecated: You should use

    see
    :see: Model.ERROR_MODEL
    stability
    :stability: deprecated
    """
    def __init__(self) -> None:
        jsii.create(ErrorModel, self, [])

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        """Returns the model name, such as 'myModel'.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "modelId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IRequestValidator")
class IRequestValidator(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRequestValidatorProxy

    @builtins.property
    @jsii.member(jsii_name="requestValidatorId")
    def request_validator_id(self) -> str:
        """ID of the request validator, such as abc123.

        attribute:
        :attribute:: true
        """
        ...


class _IRequestValidatorProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-apigateway.IRequestValidator"
    @builtins.property
    @jsii.member(jsii_name="requestValidatorId")
    def request_validator_id(self) -> str:
        """ID of the request validator, such as abc123.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "requestValidatorId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IResource")
class IResource(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourceProxy

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The full path of this resuorce."""
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        """The ID of the resource.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "RestApi":
        """The rest API that this resource is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultCorsPreflightOptions")
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Default options for CORS preflight OPTIONS method."""
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified."""
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified."""
        ...

    @builtins.property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IResource"]:
        """The parent of this resource or undefined for the root resource."""
        ...

    @jsii.member(jsii_name="addCorsPreflight")
    def add_cors_preflight(self, *, allow_origins: typing.List[str], allow_credentials: typing.Optional[bool]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List[str]]=None, disable_cache: typing.Optional[bool]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[aws_cdk.core.Duration]=None, status_code: typing.Optional[jsii.Number]=None) -> "Method":
        """Adds an OPTIONS method to this resource which responds to Cross-Origin Resource Sharing (CORS) preflight requests.

        Cross-Origin Resource Sharing (CORS) is a mechanism that uses additional
        HTTP headers to tell browsers to give a web application running at one
        origin, access to selected resources from a different origin. A web
        application executes a cross-origin HTTP request when it requests a
        resource that has a different origin (domain, protocol, or port) from its
        own.

        :param allow_origins: Specifies the list of origins that are allowed to make requests to this resource. If you wish to allow all origins, specify ``Cors.ALL_ORIGINS`` or ``[ * ]``. Responses will include the ``Access-Control-Allow-Origin`` response header. If ``Cors.ALL_ORIGINS`` is specified, the ``Vary: Origin`` response header will also be included.
        :param allow_credentials: The Access-Control-Allow-Credentials response header tells browsers whether to expose the response to frontend JavaScript code when the request's credentials mode (Request.credentials) is "include". When a request's credentials mode (Request.credentials) is "include", browsers will only expose the response to frontend JavaScript code if the Access-Control-Allow-Credentials value is true. Credentials are cookies, authorization headers or TLS client certificates. Default: false
        :param allow_headers: The Access-Control-Allow-Headers response header is used in response to a preflight request which includes the Access-Control-Request-Headers to indicate which HTTP headers can be used during the actual request. Default: Cors.DEFAULT_HEADERS
        :param allow_methods: The Access-Control-Allow-Methods response header specifies the method or methods allowed when accessing the resource in response to a preflight request. If ``ANY`` is specified, it will be expanded to ``Cors.ALL_METHODS``. Default: Cors.ALL_METHODS
        :param disable_cache: Sets Access-Control-Max-Age to -1, which means that caching is disabled. This option cannot be used with ``maxAge``. Default: - cache is enabled
        :param expose_headers: The Access-Control-Expose-Headers response header indicates which headers can be exposed as part of the response by listing their names. If you want clients to be able to access other headers, you have to list them using the Access-Control-Expose-Headers header. Default: - only the 6 CORS-safelisted response headers are exposed: Cache-Control, Content-Language, Content-Type, Expires, Last-Modified, Pragma
        :param max_age: The Access-Control-Max-Age response header indicates how long the results of a preflight request (that is the information contained in the Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can be cached. To disable caching altogther use ``disableCache: true``. Default: - browser-specific (see reference)
        :param status_code: Specifies the response status code returned from the OPTIONS method. Default: 204

        return
        :return: a ``Method`` object

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
        """
        ...

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, target: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer: typing.Optional["IAuthorizer"]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str,"IModel"]]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None, request_validator: typing.Optional["IRequestValidator"]=None) -> "Method":
        """Defines a new method for this resource.

        :param http_method: The HTTP method.
        :param target: The target backend integration for this method.
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The resources that are used for the response's content type. Specify request models as key-value pairs (string-to-string mapping), with a content type as the key and a Model resource name as the value
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator.

        return
        :return: The newly created ``Method`` object.
        """
        ...

    @jsii.member(jsii_name="addProxy")
    def add_proxy(self, *, any_method: typing.Optional[bool]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "ProxyResource":
        """Adds a greedy proxy resource ("{proxy+}") and an ANY method to this route.

        :param any_method: Adds an "ANY" method to this resource. If set to ``false``, you will have to explicitly add methods to this resource after it's created. Default: true
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        ...

    @jsii.member(jsii_name="addResource")
    def add_resource(self, path_part: str, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "Resource":
        """Defines a new child resource where this resource is the parent.

        :param path_part: The path part for the child resource.
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.

        return
        :return: A Resource object
        """
        ...

    @jsii.member(jsii_name="getResource")
    def get_resource(self, path_part: str) -> typing.Optional["IResource"]:
        """Retrieves a child resource by path part.

        :param path_part: The path part of the child resource.

        return
        :return: the child resource or undefined if not found
        """
        ...

    @jsii.member(jsii_name="resourceForPath")
    def resource_for_path(self, path: str) -> "Resource":
        """Gets or create all resources leading up to the specified path.

        - Path may only start with "/" if this method is called on the root resource.
        - All resources are created using default options.

        :param path: The relative path.

        return
        :return: a new or existing resource.
        """
        ...


class _IResourceProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-apigateway.IResource"
    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The full path of this resuorce."""
        return jsii.get(self, "path")

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        """The ID of the resource.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "resourceId")

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "RestApi":
        """The rest API that this resource is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        return jsii.get(self, "restApi")

    @builtins.property
    @jsii.member(jsii_name="defaultCorsPreflightOptions")
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Default options for CORS preflight OPTIONS method."""
        return jsii.get(self, "defaultCorsPreflightOptions")

    @builtins.property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified."""
        return jsii.get(self, "defaultIntegration")

    @builtins.property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified."""
        return jsii.get(self, "defaultMethodOptions")

    @builtins.property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IResource"]:
        """The parent of this resource or undefined for the root resource."""
        return jsii.get(self, "parentResource")

    @jsii.member(jsii_name="addCorsPreflight")
    def add_cors_preflight(self, *, allow_origins: typing.List[str], allow_credentials: typing.Optional[bool]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List[str]]=None, disable_cache: typing.Optional[bool]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[aws_cdk.core.Duration]=None, status_code: typing.Optional[jsii.Number]=None) -> "Method":
        """Adds an OPTIONS method to this resource which responds to Cross-Origin Resource Sharing (CORS) preflight requests.

        Cross-Origin Resource Sharing (CORS) is a mechanism that uses additional
        HTTP headers to tell browsers to give a web application running at one
        origin, access to selected resources from a different origin. A web
        application executes a cross-origin HTTP request when it requests a
        resource that has a different origin (domain, protocol, or port) from its
        own.

        :param allow_origins: Specifies the list of origins that are allowed to make requests to this resource. If you wish to allow all origins, specify ``Cors.ALL_ORIGINS`` or ``[ * ]``. Responses will include the ``Access-Control-Allow-Origin`` response header. If ``Cors.ALL_ORIGINS`` is specified, the ``Vary: Origin`` response header will also be included.
        :param allow_credentials: The Access-Control-Allow-Credentials response header tells browsers whether to expose the response to frontend JavaScript code when the request's credentials mode (Request.credentials) is "include". When a request's credentials mode (Request.credentials) is "include", browsers will only expose the response to frontend JavaScript code if the Access-Control-Allow-Credentials value is true. Credentials are cookies, authorization headers or TLS client certificates. Default: false
        :param allow_headers: The Access-Control-Allow-Headers response header is used in response to a preflight request which includes the Access-Control-Request-Headers to indicate which HTTP headers can be used during the actual request. Default: Cors.DEFAULT_HEADERS
        :param allow_methods: The Access-Control-Allow-Methods response header specifies the method or methods allowed when accessing the resource in response to a preflight request. If ``ANY`` is specified, it will be expanded to ``Cors.ALL_METHODS``. Default: Cors.ALL_METHODS
        :param disable_cache: Sets Access-Control-Max-Age to -1, which means that caching is disabled. This option cannot be used with ``maxAge``. Default: - cache is enabled
        :param expose_headers: The Access-Control-Expose-Headers response header indicates which headers can be exposed as part of the response by listing their names. If you want clients to be able to access other headers, you have to list them using the Access-Control-Expose-Headers header. Default: - only the 6 CORS-safelisted response headers are exposed: Cache-Control, Content-Language, Content-Type, Expires, Last-Modified, Pragma
        :param max_age: The Access-Control-Max-Age response header indicates how long the results of a preflight request (that is the information contained in the Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can be cached. To disable caching altogther use ``disableCache: true``. Default: - browser-specific (see reference)
        :param status_code: Specifies the response status code returned from the OPTIONS method. Default: 204

        return
        :return: a ``Method`` object

        see
        :see: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
        """
        options = CorsOptions(allow_origins=allow_origins, allow_credentials=allow_credentials, allow_headers=allow_headers, allow_methods=allow_methods, disable_cache=disable_cache, expose_headers=expose_headers, max_age=max_age, status_code=status_code)

        return jsii.invoke(self, "addCorsPreflight", [options])

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, target: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer: typing.Optional["IAuthorizer"]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str,"IModel"]]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None, request_validator: typing.Optional["IRequestValidator"]=None) -> "Method":
        """Defines a new method for this resource.

        :param http_method: The HTTP method.
        :param target: The target backend integration for this method.
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The resources that are used for the response's content type. Specify request models as key-value pairs (string-to-string mapping), with a content type as the key and a Model resource name as the value
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator.

        return
        :return: The newly created ``Method`` object.
        """
        options = MethodOptions(api_key_required=api_key_required, authorization_type=authorization_type, authorizer=authorizer, method_responses=method_responses, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, request_validator=request_validator)

        return jsii.invoke(self, "addMethod", [http_method, target, options])

    @jsii.member(jsii_name="addProxy")
    def add_proxy(self, *, any_method: typing.Optional[bool]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "ProxyResource":
        """Adds a greedy proxy resource ("{proxy+}") and an ANY method to this route.

        :param any_method: Adds an "ANY" method to this resource. If set to ``false``, you will have to explicitly add methods to this resource after it's created. Default: true
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        options = ProxyResourceOptions(any_method=any_method, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        return jsii.invoke(self, "addProxy", [options])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, path_part: str, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "Resource":
        """Defines a new child resource where this resource is the parent.

        :param path_part: The path part for the child resource.
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.

        return
        :return: A Resource object
        """
        options = ResourceOptions(default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        return jsii.invoke(self, "addResource", [path_part, options])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, path_part: str) -> typing.Optional["IResource"]:
        """Retrieves a child resource by path part.

        :param path_part: The path part of the child resource.

        return
        :return: the child resource or undefined if not found
        """
        return jsii.invoke(self, "getResource", [path_part])

    @jsii.member(jsii_name="resourceForPath")
    def resource_for_path(self, path: str) -> "Resource":
        """Gets or create all resources leading up to the specified path.

        - Path may only start with "/" if this method is called on the root resource.
        - All resources are created using default options.

        :param path: The relative path.

        return
        :return: a new or existing resource.
        """
        return jsii.invoke(self, "resourceForPath", [path])


@jsii.interface(jsii_type="@aws-cdk/aws-apigateway.IRestApi")
class IRestApi(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRestApiProxy

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """The ID of this API Gateway RestApi.

        attribute:
        :attribute:: true
        """
        ...


class _IRestApiProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-apigateway.IRestApi"
    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """The ID of this API Gateway RestApi.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "restApiId")


class Integration(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Integration"):
    """Base class for backend integrations for an API Gateway method.

    Use one of the concrete classes such as ``MockIntegration``, ``AwsIntegration``, ``LambdaIntegration``
    or implement on your own by specifying the set of props.
    """
    def __init__(self, *, type: "IntegrationType", integration_http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, uri: typing.Any=None) -> None:
        """
        :param type: Specifies an API method integration type.
        :param integration_http_method: The integration's HTTP method type. Required unless you use a MOCK integration.
        :param options: Integration options.
        :param uri: The Uniform Resource Identifier (URI) for the integration. - If you specify HTTP for the ``type`` property, specify the API endpoint URL. - If you specify MOCK for the ``type`` property, don't specify this property. - If you specify AWS for the ``type`` property, specify an AWS service that follows this form: ``arn:aws:apigateway:region:subdomain.service|service:path|action/service_api.`` For example, a Lambda function URI follows this form: arn:aws:apigateway:region:lambda:path/path. The path is usually in the form /2015-03-31/functions/LambdaFunctionARN/invocations.
        """
        props = IntegrationProps(type=type, integration_http_method=integration_http_method, options=options, uri=uri)

        jsii.create(Integration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _method: "Method") -> None:
        """Can be overridden by subclasses to allow the integration to interact with the method being integrated, access the REST API object, method ARNs, etc.

        :param _method: -
        """
        return jsii.invoke(self, "bind", [_method])


class AwsIntegration(Integration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.AwsIntegration"):
    """This type of integration lets an API expose AWS service actions.

    It is
    intended for calling all AWS service actions, but is not recommended for
    calling a Lambda function, because the Lambda custom integration is a legacy
    technology.
    """
    def __init__(self, *, service: str, action: typing.Optional[str]=None, action_parameters: typing.Optional[typing.Mapping[str,str]]=None, integration_http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, path: typing.Optional[str]=None, proxy: typing.Optional[bool]=None, subdomain: typing.Optional[str]=None) -> None:
        """
        :param service: The name of the integrated AWS service (e.g. ``s3``).
        :param action: The AWS action to perform in the integration. Use ``actionParams`` to specify key-value params for the action. Mutually exclusive with ``path``.
        :param action_parameters: Parameters for the action. ``action`` must be set, and ``path`` must be undefined. The action params will be URL encoded.
        :param integration_http_method: The integration's HTTP method type. Default: POST
        :param options: Integration options, such as content handling, request/response mapping, etc.
        :param path: The path to use for path-base APIs. For example, for S3 GET, you can set path to ``bucket/key``. For lambda, you can set path to ``2015-03-31/functions/${function-arn}/invocations`` Mutually exclusive with the ``action`` options.
        :param proxy: Use AWS_PROXY integration. Default: false
        :param subdomain: A designated subdomain supported by certain AWS service for fast host-name lookup.
        """
        props = AwsIntegrationProps(service=service, action=action, action_parameters=action_parameters, integration_http_method=integration_http_method, options=options, path=path, proxy=proxy, subdomain=subdomain)

        jsii.create(AwsIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, method: "Method") -> None:
        """Can be overridden by subclasses to allow the integration to interact with the method being integrated, access the REST API object, method ARNs, etc.

        :param method: -
        """
        return jsii.invoke(self, "bind", [method])


class HttpIntegration(Integration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.HttpIntegration"):
    """You can integrate an API method with an HTTP endpoint using the HTTP proxy integration or the HTTP custom integration,.

    With the proxy integration, the setup is simple. You only need to set the
    HTTP method and the HTTP endpoint URI, according to the backend requirements,
    if you are not concerned with content encoding or caching.

    With the custom integration, the setup is more involved. In addition to the
    proxy integration setup steps, you need to specify how the incoming request
    data is mapped to the integration request and how the resulting integration
    response data is mapped to the method response.
    """
    def __init__(self, url: str, *, http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, proxy: typing.Optional[bool]=None) -> None:
        """
        :param url: -
        :param http_method: HTTP method to use when invoking the backend URL. Default: GET
        :param options: Integration options, such as request/resopnse mapping, content handling, etc. Default: defaults based on ``IntegrationOptions`` defaults
        :param proxy: Determines whether to use proxy integration or custom integration. Default: true
        """
        props = HttpIntegrationProps(http_method=http_method, options=options, proxy=proxy)

        jsii.create(HttpIntegration, self, [url, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.IntegrationOptions", jsii_struct_bases=[], name_mapping={'cache_key_parameters': 'cacheKeyParameters', 'cache_namespace': 'cacheNamespace', 'connection_type': 'connectionType', 'content_handling': 'contentHandling', 'credentials_passthrough': 'credentialsPassthrough', 'credentials_role': 'credentialsRole', 'integration_responses': 'integrationResponses', 'passthrough_behavior': 'passthroughBehavior', 'request_parameters': 'requestParameters', 'request_templates': 'requestTemplates', 'vpc_link': 'vpcLink'})
class IntegrationOptions():
    def __init__(self, *, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_type: typing.Optional["ConnectionType"]=None, content_handling: typing.Optional["ContentHandling"]=None, credentials_passthrough: typing.Optional[bool]=None, credentials_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, integration_responses: typing.Optional[typing.List["IntegrationResponse"]]=None, passthrough_behavior: typing.Optional["PassthroughBehavior"]=None, request_parameters: typing.Optional[typing.Mapping[str,str]]=None, request_templates: typing.Optional[typing.Mapping[str,str]]=None, vpc_link: typing.Optional["VpcLink"]=None):
        """
        :param cache_key_parameters: A list of request parameters whose values are to be cached. It determines request parameters that will make it into the cache key.
        :param cache_namespace: An API-specific tag group of related cached parameters.
        :param connection_type: The type of network connection to the integration endpoint. Default: ConnectionType.Internet
        :param content_handling: Specifies how to handle request payload content type conversions. Default: none if this property isn't defined, the request payload is passed through from the method request to the integration request without modification, provided that the ``passthroughBehaviors`` property is configured to support payload pass-through.
        :param credentials_passthrough: Requires that the caller's identity be passed through from the request. Default: Caller identity is not passed through
        :param credentials_role: An IAM role that API Gateway assumes. Mutually exclusive with ``credentialsPassThrough``. Default: A role is not assumed
        :param integration_responses: The response that API Gateway provides after a method's backend completes processing a request. API Gateway intercepts the response from the backend so that you can control how API Gateway surfaces backend responses. For example, you can map the backend status codes to codes that you define.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER.
        :param request_parameters: The request parameters that API Gateway sends with the backend request. Specify request parameters as key-value pairs (string-to-string mappings), with a destination as the key and a source as the value. Specify the destination by using the following pattern integration.request.location.name, where location is querystring, path, or header, and name is a valid, unique parameter name. The source must be an existing method request parameter or a static value. You must enclose static values in single quotation marks and pre-encode these values based on their destination in the request.
        :param request_templates: A map of Apache Velocity templates that are applied on the request payload. The template that API Gateway uses is based on the value of the Content-Type header that's sent by the client. The content type value is the key, and the template is the value (specified as a string), such as the following snippet: { "application/json": "{\n "statusCode": "200"\n}" }
        :param vpc_link: The VpcLink used for the integration. Required if connectionType is VPC_LINK
        """
        self._values = {
        }
        if cache_key_parameters is not None: self._values["cache_key_parameters"] = cache_key_parameters
        if cache_namespace is not None: self._values["cache_namespace"] = cache_namespace
        if connection_type is not None: self._values["connection_type"] = connection_type
        if content_handling is not None: self._values["content_handling"] = content_handling
        if credentials_passthrough is not None: self._values["credentials_passthrough"] = credentials_passthrough
        if credentials_role is not None: self._values["credentials_role"] = credentials_role
        if integration_responses is not None: self._values["integration_responses"] = integration_responses
        if passthrough_behavior is not None: self._values["passthrough_behavior"] = passthrough_behavior
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if request_templates is not None: self._values["request_templates"] = request_templates
        if vpc_link is not None: self._values["vpc_link"] = vpc_link

    @builtins.property
    def cache_key_parameters(self) -> typing.Optional[typing.List[str]]:
        """A list of request parameters whose values are to be cached.

        It determines
        request parameters that will make it into the cache key.
        """
        return self._values.get('cache_key_parameters')

    @builtins.property
    def cache_namespace(self) -> typing.Optional[str]:
        """An API-specific tag group of related cached parameters."""
        return self._values.get('cache_namespace')

    @builtins.property
    def connection_type(self) -> typing.Optional["ConnectionType"]:
        """The type of network connection to the integration endpoint.

        default
        :default: ConnectionType.Internet
        """
        return self._values.get('connection_type')

    @builtins.property
    def content_handling(self) -> typing.Optional["ContentHandling"]:
        """Specifies how to handle request payload content type conversions.

        default
        :default:

        none if this property isn't defined, the request payload is passed
        through from the method request to the integration request without
        modification, provided that the ``passthroughBehaviors`` property is
        configured to support payload pass-through.
        """
        return self._values.get('content_handling')

    @builtins.property
    def credentials_passthrough(self) -> typing.Optional[bool]:
        """Requires that the caller's identity be passed through from the request.

        default
        :default: Caller identity is not passed through
        """
        return self._values.get('credentials_passthrough')

    @builtins.property
    def credentials_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role that API Gateway assumes.

        Mutually exclusive with ``credentialsPassThrough``.

        default
        :default: A role is not assumed
        """
        return self._values.get('credentials_role')

    @builtins.property
    def integration_responses(self) -> typing.Optional[typing.List["IntegrationResponse"]]:
        """The response that API Gateway provides after a method's backend completes processing a request.

        API Gateway intercepts the response from the
        backend so that you can control how API Gateway surfaces backend
        responses. For example, you can map the backend status codes to codes
        that you define.
        """
        return self._values.get('integration_responses')

    @builtins.property
    def passthrough_behavior(self) -> typing.Optional["PassthroughBehavior"]:
        """Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource.

        There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and
        NEVER.
        """
        return self._values.get('passthrough_behavior')

    @builtins.property
    def request_parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The request parameters that API Gateway sends with the backend request.

        Specify request parameters as key-value pairs (string-to-string
        mappings), with a destination as the key and a source as the value.

        Specify the destination by using the following pattern
        integration.request.location.name, where location is querystring, path,
        or header, and name is a valid, unique parameter name.

        The source must be an existing method request parameter or a static
        value. You must enclose static values in single quotation marks and
        pre-encode these values based on their destination in the request.
        """
        return self._values.get('request_parameters')

    @builtins.property
    def request_templates(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A map of Apache Velocity templates that are applied on the request payload.

        The template that API Gateway uses is based on the value of the
        Content-Type header that's sent by the client. The content type value is
        the key, and the template is the value (specified as a string), such as
        the following snippet:

        { "application/json": "{\n  "statusCode": "200"\n}" }

        see
        :see: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        """
        return self._values.get('request_templates')

    @builtins.property
    def vpc_link(self) -> typing.Optional["VpcLink"]:
        """The VpcLink used for the integration.

        Required if connectionType is VPC_LINK
        """
        return self._values.get('vpc_link')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'IntegrationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.IntegrationProps", jsii_struct_bases=[], name_mapping={'type': 'type', 'integration_http_method': 'integrationHttpMethod', 'options': 'options', 'uri': 'uri'})
class IntegrationProps():
    def __init__(self, *, type: "IntegrationType", integration_http_method: typing.Optional[str]=None, options: typing.Optional["IntegrationOptions"]=None, uri: typing.Any=None):
        """
        :param type: Specifies an API method integration type.
        :param integration_http_method: The integration's HTTP method type. Required unless you use a MOCK integration.
        :param options: Integration options.
        :param uri: The Uniform Resource Identifier (URI) for the integration. - If you specify HTTP for the ``type`` property, specify the API endpoint URL. - If you specify MOCK for the ``type`` property, don't specify this property. - If you specify AWS for the ``type`` property, specify an AWS service that follows this form: ``arn:aws:apigateway:region:subdomain.service|service:path|action/service_api.`` For example, a Lambda function URI follows this form: arn:aws:apigateway:region:lambda:path/path. The path is usually in the form /2015-03-31/functions/LambdaFunctionARN/invocations.
        """
        if isinstance(options, dict): options = IntegrationOptions(**options)
        self._values = {
            'type': type,
        }
        if integration_http_method is not None: self._values["integration_http_method"] = integration_http_method
        if options is not None: self._values["options"] = options
        if uri is not None: self._values["uri"] = uri

    @builtins.property
    def type(self) -> "IntegrationType":
        """Specifies an API method integration type."""
        return self._values.get('type')

    @builtins.property
    def integration_http_method(self) -> typing.Optional[str]:
        """The integration's HTTP method type.

        Required unless you use a MOCK integration.
        """
        return self._values.get('integration_http_method')

    @builtins.property
    def options(self) -> typing.Optional["IntegrationOptions"]:
        """Integration options."""
        return self._values.get('options')

    @builtins.property
    def uri(self) -> typing.Any:
        """The Uniform Resource Identifier (URI) for the integration.

        - If you specify HTTP for the ``type`` property, specify the API endpoint URL.
        - If you specify MOCK for the ``type`` property, don't specify this property.
        - If you specify AWS for the ``type`` property, specify an AWS service that
          follows this form: ``arn:aws:apigateway:region:subdomain.service|service:path|action/service_api.``
          For example, a Lambda function URI follows this form:
          arn:aws:apigateway:region:lambda:path/path. The path is usually in the
          form /2015-03-31/functions/LambdaFunctionARN/invocations.

        see
        :see: https://docs.aws.amazon.com/apigateway/api-reference/resource/integration/#uri
        """
        return self._values.get('uri')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'IntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.IntegrationResponse", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'content_handling': 'contentHandling', 'response_parameters': 'responseParameters', 'response_templates': 'responseTemplates', 'selection_pattern': 'selectionPattern'})
class IntegrationResponse():
    def __init__(self, *, status_code: str, content_handling: typing.Optional["ContentHandling"]=None, response_parameters: typing.Optional[typing.Mapping[str,str]]=None, response_templates: typing.Optional[typing.Mapping[str,str]]=None, selection_pattern: typing.Optional[str]=None):
        """
        :param status_code: The status code that API Gateway uses to map the integration response to a MethodResponse status code.
        :param content_handling: Specifies how to handle request payload content type conversions. Default: none the request payload is passed through from the method request to the integration request without modification.
        :param response_parameters: The response parameters from the backend response that API Gateway sends to the method response. Use the destination as the key and the source as the value: - The destination must be an existing response parameter in the MethodResponse property. - The source must be an existing method request parameter or a static value. You must enclose static values in single quotation marks and pre-encode these values based on the destination specified in the request.
        :param response_templates: The templates that are used to transform the integration response body. Specify templates as key-value pairs, with a content type as the key and a template as the value.
        :param selection_pattern: Specifies the regular expression (regex) pattern used to choose an integration response based on the response from the back end. For example, if the success response returns nothing and the error response returns some string, you could use the ``.+`` regex to match error response. However, make sure that the error response does not contain any newline (``\n``) character in such cases. If the back end is an AWS Lambda function, the AWS Lambda function error header is matched. For all other HTTP and AWS back ends, the HTTP status code is matched.
        """
        self._values = {
            'status_code': status_code,
        }
        if content_handling is not None: self._values["content_handling"] = content_handling
        if response_parameters is not None: self._values["response_parameters"] = response_parameters
        if response_templates is not None: self._values["response_templates"] = response_templates
        if selection_pattern is not None: self._values["selection_pattern"] = selection_pattern

    @builtins.property
    def status_code(self) -> str:
        """The status code that API Gateway uses to map the integration response to a MethodResponse status code."""
        return self._values.get('status_code')

    @builtins.property
    def content_handling(self) -> typing.Optional["ContentHandling"]:
        """Specifies how to handle request payload content type conversions.

        default
        :default:

        none the request payload is passed through from the method
        request to the integration request without modification.
        """
        return self._values.get('content_handling')

    @builtins.property
    def response_parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The response parameters from the backend response that API Gateway sends to the method response.

        Use the destination as the key and the source as the value:

        - The destination must be an existing response parameter in the
          MethodResponse property.
        - The source must be an existing method request parameter or a static
          value. You must enclose static values in single quotation marks and
          pre-encode these values based on the destination specified in the
          request.

        see
        :see: http://docs.aws.amazon.com/apigateway/latest/developerguide/request-response-data-mappings.html
        """
        return self._values.get('response_parameters')

    @builtins.property
    def response_templates(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The templates that are used to transform the integration response body.

        Specify templates as key-value pairs, with a content type as the key and
        a template as the value.

        see
        :see: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        """
        return self._values.get('response_templates')

    @builtins.property
    def selection_pattern(self) -> typing.Optional[str]:
        """Specifies the regular expression (regex) pattern used to choose an integration response based on the response from the back end.

        For example, if the success response returns nothing and the error response returns some string, you
        could use the ``.+`` regex to match error response. However, make sure that the error response does not contain any
        newline (``\n``) character in such cases. If the back end is an AWS Lambda function, the AWS Lambda function error
        header is matched. For all other HTTP and AWS back ends, the HTTP status code is matched.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-integration-settings-integration-response.html
        """
        return self._values.get('selection_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'IntegrationResponse(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.IntegrationType")
class IntegrationType(enum.Enum):
    AWS = "AWS"
    """For integrating the API method request with an AWS service action, including the Lambda function-invoking action.

    With the Lambda
    function-invoking action, this is referred to as the Lambda custom
    integration. With any other AWS service action, this is known as AWS
    integration.
    """
    AWS_PROXY = "AWS_PROXY"
    """For integrating the API method request with the Lambda function-invoking action with the client request passed through as-is.

    This integration is
    also referred to as the Lambda proxy integration
    """
    HTTP = "HTTP"
    """For integrating the API method request with an HTTP endpoint, including a private HTTP endpoint within a VPC.

    This integration is also referred to
    as the HTTP custom integration.
    """
    HTTP_PROXY = "HTTP_PROXY"
    """For integrating the API method request with an HTTP endpoint, including a private HTTP endpoint within a VPC, with the client request passed through as-is.

    This is also referred to as the HTTP proxy integration
    """
    MOCK = "MOCK"
    """For integrating the API method request with API Gateway as a "loop-back" endpoint without invoking any backend."""

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.JsonSchema", jsii_struct_bases=[], name_mapping={'additional_items': 'additionalItems', 'additional_properties': 'additionalProperties', 'all_of': 'allOf', 'any_of': 'anyOf', 'contains': 'contains', 'definitions': 'definitions', 'dependencies': 'dependencies', 'description': 'description', 'enum': 'enum', 'exclusive_maximum': 'exclusiveMaximum', 'exclusive_minimum': 'exclusiveMinimum', 'format': 'format', 'id': 'id', 'items': 'items', 'maximum': 'maximum', 'max_items': 'maxItems', 'max_length': 'maxLength', 'max_properties': 'maxProperties', 'minimum': 'minimum', 'min_items': 'minItems', 'min_length': 'minLength', 'min_properties': 'minProperties', 'multiple_of': 'multipleOf', 'not_': 'not', 'one_of': 'oneOf', 'pattern': 'pattern', 'pattern_properties': 'patternProperties', 'properties': 'properties', 'property_names': 'propertyNames', 'ref': 'ref', 'required': 'required', 'schema': 'schema', 'title': 'title', 'type': 'type', 'unique_items': 'uniqueItems'})
class JsonSchema():
    def __init__(self, *, additional_items: typing.Optional[typing.List["JsonSchema"]]=None, additional_properties: typing.Optional[bool]=None, all_of: typing.Optional[typing.List["JsonSchema"]]=None, any_of: typing.Optional[typing.List["JsonSchema"]]=None, contains: typing.Optional[typing.Union[typing.Optional["JsonSchema"], typing.Optional[typing.List["JsonSchema"]]]]=None, definitions: typing.Optional[typing.Mapping[str,"JsonSchema"]]=None, dependencies: typing.Optional[typing.Mapping[str,typing.Union["JsonSchema", typing.List[str]]]]=None, description: typing.Optional[str]=None, enum: typing.Optional[typing.List[typing.Any]]=None, exclusive_maximum: typing.Optional[bool]=None, exclusive_minimum: typing.Optional[bool]=None, format: typing.Optional[str]=None, id: typing.Optional[str]=None, items: typing.Optional[typing.Union[typing.Optional["JsonSchema"], typing.Optional[typing.List["JsonSchema"]]]]=None, maximum: typing.Optional[jsii.Number]=None, max_items: typing.Optional[jsii.Number]=None, max_length: typing.Optional[jsii.Number]=None, max_properties: typing.Optional[jsii.Number]=None, minimum: typing.Optional[jsii.Number]=None, min_items: typing.Optional[jsii.Number]=None, min_length: typing.Optional[jsii.Number]=None, min_properties: typing.Optional[jsii.Number]=None, multiple_of: typing.Optional[jsii.Number]=None, not_: typing.Optional["JsonSchema"]=None, one_of: typing.Optional[typing.List["JsonSchema"]]=None, pattern: typing.Optional[str]=None, pattern_properties: typing.Optional[typing.Mapping[str,"JsonSchema"]]=None, properties: typing.Optional[typing.Mapping[str,"JsonSchema"]]=None, property_names: typing.Optional["JsonSchema"]=None, ref: typing.Optional[str]=None, required: typing.Optional[typing.List[str]]=None, schema: typing.Optional["JsonSchemaVersion"]=None, title: typing.Optional[str]=None, type: typing.Optional[typing.Union[typing.Optional["JsonSchemaType"], typing.Optional[typing.List["JsonSchemaType"]]]]=None, unique_items: typing.Optional[bool]=None):
        """Represents a JSON schema definition of the structure of a REST API model.

        Copied from npm module jsonschema.

        :param additional_items: 
        :param additional_properties: 
        :param all_of: 
        :param any_of: 
        :param contains: 
        :param definitions: 
        :param dependencies: 
        :param description: 
        :param enum: 
        :param exclusive_maximum: 
        :param exclusive_minimum: 
        :param format: 
        :param id: 
        :param items: 
        :param maximum: 
        :param max_items: 
        :param max_length: 
        :param max_properties: 
        :param minimum: 
        :param min_items: 
        :param min_length: 
        :param min_properties: 
        :param multiple_of: 
        :param not_: 
        :param one_of: 
        :param pattern: 
        :param pattern_properties: 
        :param properties: 
        :param property_names: 
        :param ref: 
        :param required: 
        :param schema: 
        :param title: 
        :param type: 
        :param unique_items: 

        see
        :see: https://github.com/tdegrunt/jsonschema
        """
        if isinstance(not_, dict): not_ = JsonSchema(**not_)
        if isinstance(property_names, dict): property_names = JsonSchema(**property_names)
        self._values = {
        }
        if additional_items is not None: self._values["additional_items"] = additional_items
        if additional_properties is not None: self._values["additional_properties"] = additional_properties
        if all_of is not None: self._values["all_of"] = all_of
        if any_of is not None: self._values["any_of"] = any_of
        if contains is not None: self._values["contains"] = contains
        if definitions is not None: self._values["definitions"] = definitions
        if dependencies is not None: self._values["dependencies"] = dependencies
        if description is not None: self._values["description"] = description
        if enum is not None: self._values["enum"] = enum
        if exclusive_maximum is not None: self._values["exclusive_maximum"] = exclusive_maximum
        if exclusive_minimum is not None: self._values["exclusive_minimum"] = exclusive_minimum
        if format is not None: self._values["format"] = format
        if id is not None: self._values["id"] = id
        if items is not None: self._values["items"] = items
        if maximum is not None: self._values["maximum"] = maximum
        if max_items is not None: self._values["max_items"] = max_items
        if max_length is not None: self._values["max_length"] = max_length
        if max_properties is not None: self._values["max_properties"] = max_properties
        if minimum is not None: self._values["minimum"] = minimum
        if min_items is not None: self._values["min_items"] = min_items
        if min_length is not None: self._values["min_length"] = min_length
        if min_properties is not None: self._values["min_properties"] = min_properties
        if multiple_of is not None: self._values["multiple_of"] = multiple_of
        if not_ is not None: self._values["not_"] = not_
        if one_of is not None: self._values["one_of"] = one_of
        if pattern is not None: self._values["pattern"] = pattern
        if pattern_properties is not None: self._values["pattern_properties"] = pattern_properties
        if properties is not None: self._values["properties"] = properties
        if property_names is not None: self._values["property_names"] = property_names
        if ref is not None: self._values["ref"] = ref
        if required is not None: self._values["required"] = required
        if schema is not None: self._values["schema"] = schema
        if title is not None: self._values["title"] = title
        if type is not None: self._values["type"] = type
        if unique_items is not None: self._values["unique_items"] = unique_items

    @builtins.property
    def additional_items(self) -> typing.Optional[typing.List["JsonSchema"]]:
        return self._values.get('additional_items')

    @builtins.property
    def additional_properties(self) -> typing.Optional[bool]:
        return self._values.get('additional_properties')

    @builtins.property
    def all_of(self) -> typing.Optional[typing.List["JsonSchema"]]:
        return self._values.get('all_of')

    @builtins.property
    def any_of(self) -> typing.Optional[typing.List["JsonSchema"]]:
        return self._values.get('any_of')

    @builtins.property
    def contains(self) -> typing.Optional[typing.Union[typing.Optional["JsonSchema"], typing.Optional[typing.List["JsonSchema"]]]]:
        return self._values.get('contains')

    @builtins.property
    def definitions(self) -> typing.Optional[typing.Mapping[str,"JsonSchema"]]:
        return self._values.get('definitions')

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.Mapping[str,typing.Union["JsonSchema", typing.List[str]]]]:
        return self._values.get('dependencies')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        return self._values.get('description')

    @builtins.property
    def enum(self) -> typing.Optional[typing.List[typing.Any]]:
        return self._values.get('enum')

    @builtins.property
    def exclusive_maximum(self) -> typing.Optional[bool]:
        return self._values.get('exclusive_maximum')

    @builtins.property
    def exclusive_minimum(self) -> typing.Optional[bool]:
        return self._values.get('exclusive_minimum')

    @builtins.property
    def format(self) -> typing.Optional[str]:
        return self._values.get('format')

    @builtins.property
    def id(self) -> typing.Optional[str]:
        return self._values.get('id')

    @builtins.property
    def items(self) -> typing.Optional[typing.Union[typing.Optional["JsonSchema"], typing.Optional[typing.List["JsonSchema"]]]]:
        return self._values.get('items')

    @builtins.property
    def maximum(self) -> typing.Optional[jsii.Number]:
        return self._values.get('maximum')

    @builtins.property
    def max_items(self) -> typing.Optional[jsii.Number]:
        return self._values.get('max_items')

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        return self._values.get('max_length')

    @builtins.property
    def max_properties(self) -> typing.Optional[jsii.Number]:
        return self._values.get('max_properties')

    @builtins.property
    def minimum(self) -> typing.Optional[jsii.Number]:
        return self._values.get('minimum')

    @builtins.property
    def min_items(self) -> typing.Optional[jsii.Number]:
        return self._values.get('min_items')

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        return self._values.get('min_length')

    @builtins.property
    def min_properties(self) -> typing.Optional[jsii.Number]:
        return self._values.get('min_properties')

    @builtins.property
    def multiple_of(self) -> typing.Optional[jsii.Number]:
        return self._values.get('multiple_of')

    @builtins.property
    def not_(self) -> typing.Optional["JsonSchema"]:
        return self._values.get('not_')

    @builtins.property
    def one_of(self) -> typing.Optional[typing.List["JsonSchema"]]:
        return self._values.get('one_of')

    @builtins.property
    def pattern(self) -> typing.Optional[str]:
        return self._values.get('pattern')

    @builtins.property
    def pattern_properties(self) -> typing.Optional[typing.Mapping[str,"JsonSchema"]]:
        return self._values.get('pattern_properties')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[str,"JsonSchema"]]:
        return self._values.get('properties')

    @builtins.property
    def property_names(self) -> typing.Optional["JsonSchema"]:
        return self._values.get('property_names')

    @builtins.property
    def ref(self) -> typing.Optional[str]:
        return self._values.get('ref')

    @builtins.property
    def required(self) -> typing.Optional[typing.List[str]]:
        return self._values.get('required')

    @builtins.property
    def schema(self) -> typing.Optional["JsonSchemaVersion"]:
        return self._values.get('schema')

    @builtins.property
    def title(self) -> typing.Optional[str]:
        return self._values.get('title')

    @builtins.property
    def type(self) -> typing.Optional[typing.Union[typing.Optional["JsonSchemaType"], typing.Optional[typing.List["JsonSchemaType"]]]]:
        return self._values.get('type')

    @builtins.property
    def unique_items(self) -> typing.Optional[bool]:
        return self._values.get('unique_items')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JsonSchema(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.JsonSchemaType")
class JsonSchemaType(enum.Enum):
    NULL = "NULL"
    BOOLEAN = "BOOLEAN"
    OBJECT = "OBJECT"
    ARRAY = "ARRAY"
    NUMBER = "NUMBER"
    INTEGER = "INTEGER"
    STRING = "STRING"

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.JsonSchemaVersion")
class JsonSchemaVersion(enum.Enum):
    DRAFT4 = "DRAFT4"
    """In API Gateway models are defined using the JSON schema draft 4.

    see
    :see: https://tools.ietf.org/html/draft-zyp-json-schema-04
    """
    DRAFT7 = "DRAFT7"

class LambdaIntegration(AwsIntegration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.LambdaIntegration"):
    """Integrates an AWS Lambda function to an API Gateway method.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        handler = lambda.Function(self, "MyFunction", ...)
        api.add_method("GET", LambdaIntegration(handler))
    """
    def __init__(self, handler: aws_cdk.aws_lambda.IFunction, *, allow_test_invoke: typing.Optional[bool]=None, proxy: typing.Optional[bool]=None, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_type: typing.Optional["ConnectionType"]=None, content_handling: typing.Optional["ContentHandling"]=None, credentials_passthrough: typing.Optional[bool]=None, credentials_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, integration_responses: typing.Optional[typing.List["IntegrationResponse"]]=None, passthrough_behavior: typing.Optional["PassthroughBehavior"]=None, request_parameters: typing.Optional[typing.Mapping[str,str]]=None, request_templates: typing.Optional[typing.Mapping[str,str]]=None, vpc_link: typing.Optional["VpcLink"]=None) -> None:
        """
        :param handler: -
        :param allow_test_invoke: Allow invoking method from AWS Console UI (for testing purposes). This will add another permission to the AWS Lambda resource policy which will allow the ``test-invoke-stage`` stage to invoke this handler. If this is set to ``false``, the function will only be usable from the deployment endpoint. Default: true
        :param proxy: Use proxy integration or normal (request/response mapping) integration. Default: true
        :param cache_key_parameters: A list of request parameters whose values are to be cached. It determines request parameters that will make it into the cache key.
        :param cache_namespace: An API-specific tag group of related cached parameters.
        :param connection_type: The type of network connection to the integration endpoint. Default: ConnectionType.Internet
        :param content_handling: Specifies how to handle request payload content type conversions. Default: none if this property isn't defined, the request payload is passed through from the method request to the integration request without modification, provided that the ``passthroughBehaviors`` property is configured to support payload pass-through.
        :param credentials_passthrough: Requires that the caller's identity be passed through from the request. Default: Caller identity is not passed through
        :param credentials_role: An IAM role that API Gateway assumes. Mutually exclusive with ``credentialsPassThrough``. Default: A role is not assumed
        :param integration_responses: The response that API Gateway provides after a method's backend completes processing a request. API Gateway intercepts the response from the backend so that you can control how API Gateway surfaces backend responses. For example, you can map the backend status codes to codes that you define.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER.
        :param request_parameters: The request parameters that API Gateway sends with the backend request. Specify request parameters as key-value pairs (string-to-string mappings), with a destination as the key and a source as the value. Specify the destination by using the following pattern integration.request.location.name, where location is querystring, path, or header, and name is a valid, unique parameter name. The source must be an existing method request parameter or a static value. You must enclose static values in single quotation marks and pre-encode these values based on their destination in the request.
        :param request_templates: A map of Apache Velocity templates that are applied on the request payload. The template that API Gateway uses is based on the value of the Content-Type header that's sent by the client. The content type value is the key, and the template is the value (specified as a string), such as the following snippet: { "application/json": "{\n "statusCode": "200"\n}" }
        :param vpc_link: The VpcLink used for the integration. Required if connectionType is VPC_LINK
        """
        options = LambdaIntegrationOptions(allow_test_invoke=allow_test_invoke, proxy=proxy, cache_key_parameters=cache_key_parameters, cache_namespace=cache_namespace, connection_type=connection_type, content_handling=content_handling, credentials_passthrough=credentials_passthrough, credentials_role=credentials_role, integration_responses=integration_responses, passthrough_behavior=passthrough_behavior, request_parameters=request_parameters, request_templates=request_templates, vpc_link=vpc_link)

        jsii.create(LambdaIntegration, self, [handler, options])

    @jsii.member(jsii_name="bind")
    def bind(self, method: "Method") -> None:
        """Can be overridden by subclasses to allow the integration to interact with the method being integrated, access the REST API object, method ARNs, etc.

        :param method: -
        """
        return jsii.invoke(self, "bind", [method])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.LambdaIntegrationOptions", jsii_struct_bases=[IntegrationOptions], name_mapping={'cache_key_parameters': 'cacheKeyParameters', 'cache_namespace': 'cacheNamespace', 'connection_type': 'connectionType', 'content_handling': 'contentHandling', 'credentials_passthrough': 'credentialsPassthrough', 'credentials_role': 'credentialsRole', 'integration_responses': 'integrationResponses', 'passthrough_behavior': 'passthroughBehavior', 'request_parameters': 'requestParameters', 'request_templates': 'requestTemplates', 'vpc_link': 'vpcLink', 'allow_test_invoke': 'allowTestInvoke', 'proxy': 'proxy'})
class LambdaIntegrationOptions(IntegrationOptions):
    def __init__(self, *, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_type: typing.Optional["ConnectionType"]=None, content_handling: typing.Optional["ContentHandling"]=None, credentials_passthrough: typing.Optional[bool]=None, credentials_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, integration_responses: typing.Optional[typing.List["IntegrationResponse"]]=None, passthrough_behavior: typing.Optional["PassthroughBehavior"]=None, request_parameters: typing.Optional[typing.Mapping[str,str]]=None, request_templates: typing.Optional[typing.Mapping[str,str]]=None, vpc_link: typing.Optional["VpcLink"]=None, allow_test_invoke: typing.Optional[bool]=None, proxy: typing.Optional[bool]=None):
        """
        :param cache_key_parameters: A list of request parameters whose values are to be cached. It determines request parameters that will make it into the cache key.
        :param cache_namespace: An API-specific tag group of related cached parameters.
        :param connection_type: The type of network connection to the integration endpoint. Default: ConnectionType.Internet
        :param content_handling: Specifies how to handle request payload content type conversions. Default: none if this property isn't defined, the request payload is passed through from the method request to the integration request without modification, provided that the ``passthroughBehaviors`` property is configured to support payload pass-through.
        :param credentials_passthrough: Requires that the caller's identity be passed through from the request. Default: Caller identity is not passed through
        :param credentials_role: An IAM role that API Gateway assumes. Mutually exclusive with ``credentialsPassThrough``. Default: A role is not assumed
        :param integration_responses: The response that API Gateway provides after a method's backend completes processing a request. API Gateway intercepts the response from the backend so that you can control how API Gateway surfaces backend responses. For example, you can map the backend status codes to codes that you define.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER.
        :param request_parameters: The request parameters that API Gateway sends with the backend request. Specify request parameters as key-value pairs (string-to-string mappings), with a destination as the key and a source as the value. Specify the destination by using the following pattern integration.request.location.name, where location is querystring, path, or header, and name is a valid, unique parameter name. The source must be an existing method request parameter or a static value. You must enclose static values in single quotation marks and pre-encode these values based on their destination in the request.
        :param request_templates: A map of Apache Velocity templates that are applied on the request payload. The template that API Gateway uses is based on the value of the Content-Type header that's sent by the client. The content type value is the key, and the template is the value (specified as a string), such as the following snippet: { "application/json": "{\n "statusCode": "200"\n}" }
        :param vpc_link: The VpcLink used for the integration. Required if connectionType is VPC_LINK
        :param allow_test_invoke: Allow invoking method from AWS Console UI (for testing purposes). This will add another permission to the AWS Lambda resource policy which will allow the ``test-invoke-stage`` stage to invoke this handler. If this is set to ``false``, the function will only be usable from the deployment endpoint. Default: true
        :param proxy: Use proxy integration or normal (request/response mapping) integration. Default: true
        """
        self._values = {
        }
        if cache_key_parameters is not None: self._values["cache_key_parameters"] = cache_key_parameters
        if cache_namespace is not None: self._values["cache_namespace"] = cache_namespace
        if connection_type is not None: self._values["connection_type"] = connection_type
        if content_handling is not None: self._values["content_handling"] = content_handling
        if credentials_passthrough is not None: self._values["credentials_passthrough"] = credentials_passthrough
        if credentials_role is not None: self._values["credentials_role"] = credentials_role
        if integration_responses is not None: self._values["integration_responses"] = integration_responses
        if passthrough_behavior is not None: self._values["passthrough_behavior"] = passthrough_behavior
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if request_templates is not None: self._values["request_templates"] = request_templates
        if vpc_link is not None: self._values["vpc_link"] = vpc_link
        if allow_test_invoke is not None: self._values["allow_test_invoke"] = allow_test_invoke
        if proxy is not None: self._values["proxy"] = proxy

    @builtins.property
    def cache_key_parameters(self) -> typing.Optional[typing.List[str]]:
        """A list of request parameters whose values are to be cached.

        It determines
        request parameters that will make it into the cache key.
        """
        return self._values.get('cache_key_parameters')

    @builtins.property
    def cache_namespace(self) -> typing.Optional[str]:
        """An API-specific tag group of related cached parameters."""
        return self._values.get('cache_namespace')

    @builtins.property
    def connection_type(self) -> typing.Optional["ConnectionType"]:
        """The type of network connection to the integration endpoint.

        default
        :default: ConnectionType.Internet
        """
        return self._values.get('connection_type')

    @builtins.property
    def content_handling(self) -> typing.Optional["ContentHandling"]:
        """Specifies how to handle request payload content type conversions.

        default
        :default:

        none if this property isn't defined, the request payload is passed
        through from the method request to the integration request without
        modification, provided that the ``passthroughBehaviors`` property is
        configured to support payload pass-through.
        """
        return self._values.get('content_handling')

    @builtins.property
    def credentials_passthrough(self) -> typing.Optional[bool]:
        """Requires that the caller's identity be passed through from the request.

        default
        :default: Caller identity is not passed through
        """
        return self._values.get('credentials_passthrough')

    @builtins.property
    def credentials_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role that API Gateway assumes.

        Mutually exclusive with ``credentialsPassThrough``.

        default
        :default: A role is not assumed
        """
        return self._values.get('credentials_role')

    @builtins.property
    def integration_responses(self) -> typing.Optional[typing.List["IntegrationResponse"]]:
        """The response that API Gateway provides after a method's backend completes processing a request.

        API Gateway intercepts the response from the
        backend so that you can control how API Gateway surfaces backend
        responses. For example, you can map the backend status codes to codes
        that you define.
        """
        return self._values.get('integration_responses')

    @builtins.property
    def passthrough_behavior(self) -> typing.Optional["PassthroughBehavior"]:
        """Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource.

        There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and
        NEVER.
        """
        return self._values.get('passthrough_behavior')

    @builtins.property
    def request_parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The request parameters that API Gateway sends with the backend request.

        Specify request parameters as key-value pairs (string-to-string
        mappings), with a destination as the key and a source as the value.

        Specify the destination by using the following pattern
        integration.request.location.name, where location is querystring, path,
        or header, and name is a valid, unique parameter name.

        The source must be an existing method request parameter or a static
        value. You must enclose static values in single quotation marks and
        pre-encode these values based on their destination in the request.
        """
        return self._values.get('request_parameters')

    @builtins.property
    def request_templates(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A map of Apache Velocity templates that are applied on the request payload.

        The template that API Gateway uses is based on the value of the
        Content-Type header that's sent by the client. The content type value is
        the key, and the template is the value (specified as a string), such as
        the following snippet:

        { "application/json": "{\n  "statusCode": "200"\n}" }

        see
        :see: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        """
        return self._values.get('request_templates')

    @builtins.property
    def vpc_link(self) -> typing.Optional["VpcLink"]:
        """The VpcLink used for the integration.

        Required if connectionType is VPC_LINK
        """
        return self._values.get('vpc_link')

    @builtins.property
    def allow_test_invoke(self) -> typing.Optional[bool]:
        """Allow invoking method from AWS Console UI (for testing purposes).

        This will add another permission to the AWS Lambda resource policy which
        will allow the ``test-invoke-stage`` stage to invoke this handler. If this
        is set to ``false``, the function will only be usable from the deployment
        endpoint.

        default
        :default: true
        """
        return self._values.get('allow_test_invoke')

    @builtins.property
    def proxy(self) -> typing.Optional[bool]:
        """Use proxy integration or normal (request/response mapping) integration.

        default
        :default: true
        """
        return self._values.get('proxy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaIntegrationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Method(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Method"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, http_method: str, resource: "IResource", integration: typing.Optional["Integration"]=None, options: typing.Optional["MethodOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param http_method: The HTTP method ("GET", "POST", "PUT", ...) that clients use to call this method.
        :param resource: The resource this method is associated with. For root resource methods, specify the ``RestApi`` object.
        :param integration: The backend system that the method calls when it receives a request. Default: - a new ``MockIntegration``.
        :param options: Method options. Default: - No options.
        """
        props = MethodProps(http_method=http_method, resource=resource, integration=integration, options=options)

        jsii.create(Method, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> str:
        return jsii.get(self, "httpMethod")

    @builtins.property
    @jsii.member(jsii_name="methodArn")
    def method_arn(self) -> str:
        """Returns an execute-api ARN for this method:.

        arn:aws:execute-api:{region}:{account}:{restApiId}/{stage}/{method}/{path}

        NOTE: {stage} will refer to the ``restApi.deploymentStage``, which will
        automatically set if auto-deploy is enabled.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "methodArn")

    @builtins.property
    @jsii.member(jsii_name="methodId")
    def method_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "methodId")

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "IResource":
        return jsii.get(self, "resource")

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "RestApi":
        return jsii.get(self, "restApi")

    @builtins.property
    @jsii.member(jsii_name="testMethodArn")
    def test_method_arn(self) -> str:
        """Returns an execute-api ARN for this method's "test-invoke-stage" stage.

        This stage is used by the AWS Console UI when testing the method.
        """
        return jsii.get(self, "testMethodArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodDeploymentOptions", jsii_struct_bases=[], name_mapping={'cache_data_encrypted': 'cacheDataEncrypted', 'cache_ttl': 'cacheTtl', 'caching_enabled': 'cachingEnabled', 'data_trace_enabled': 'dataTraceEnabled', 'logging_level': 'loggingLevel', 'metrics_enabled': 'metricsEnabled', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit'})
class MethodDeploymentOptions():
    def __init__(self, *, cache_data_encrypted: typing.Optional[bool]=None, cache_ttl: typing.Optional[aws_cdk.core.Duration]=None, caching_enabled: typing.Optional[bool]=None, data_trace_enabled: typing.Optional[bool]=None, logging_level: typing.Optional["MethodLoggingLevel"]=None, metrics_enabled: typing.Optional[bool]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None):
        """
        :param cache_data_encrypted: Indicates whether the cached responses are encrypted. Default: false
        :param cache_ttl: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached. Default: Duration.minutes(5)
        :param caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached. Default: - Caching is Disabled.
        :param data_trace_enabled: Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: false
        :param logging_level: Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: - Off
        :param metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method. Default: false
        :param throttling_burst_limit: Specifies the throttling burst limit. The total rate of all requests in your AWS account is limited to 5,000 requests. Default: - No additional restriction.
        :param throttling_rate_limit: Specifies the throttling rate limit. The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps). Default: - No additional restriction.
        """
        self._values = {
        }
        if cache_data_encrypted is not None: self._values["cache_data_encrypted"] = cache_data_encrypted
        if cache_ttl is not None: self._values["cache_ttl"] = cache_ttl
        if caching_enabled is not None: self._values["caching_enabled"] = caching_enabled
        if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
        if logging_level is not None: self._values["logging_level"] = logging_level
        if metrics_enabled is not None: self._values["metrics_enabled"] = metrics_enabled
        if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
        if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit

    @builtins.property
    def cache_data_encrypted(self) -> typing.Optional[bool]:
        """Indicates whether the cached responses are encrypted.

        default
        :default: false
        """
        return self._values.get('cache_data_encrypted')

    @builtins.property
    def cache_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the time to live (TTL), in seconds, for cached responses.

        The
        higher the TTL, the longer the response will be cached.

        default
        :default: Duration.minutes(5)

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html
        """
        return self._values.get('cache_ttl')

    @builtins.property
    def caching_enabled(self) -> typing.Optional[bool]:
        """Specifies whether responses should be cached and returned for requests.

        A
        cache cluster must be enabled on the stage for responses to be cached.

        default
        :default: - Caching is Disabled.
        """
        return self._values.get('caching_enabled')

    @builtins.property
    def data_trace_enabled(self) -> typing.Optional[bool]:
        """Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: false
        """
        return self._values.get('data_trace_enabled')

    @builtins.property
    def logging_level(self) -> typing.Optional["MethodLoggingLevel"]:
        """Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: - Off
        """
        return self._values.get('logging_level')

    @builtins.property
    def metrics_enabled(self) -> typing.Optional[bool]:
        """Specifies whether Amazon CloudWatch metrics are enabled for this method.

        default
        :default: false
        """
        return self._values.get('metrics_enabled')

    @builtins.property
    def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
        """Specifies the throttling burst limit.

        The total rate of all requests in your AWS account is limited to 5,000 requests.

        default
        :default: - No additional restriction.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        return self._values.get('throttling_burst_limit')

    @builtins.property
    def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
        """Specifies the throttling rate limit.

        The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps).

        default
        :default: - No additional restriction.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        return self._values.get('throttling_rate_limit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MethodDeploymentOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.MethodLoggingLevel")
class MethodLoggingLevel(enum.Enum):
    OFF = "OFF"
    ERROR = "ERROR"
    INFO = "INFO"

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodOptions", jsii_struct_bases=[], name_mapping={'api_key_required': 'apiKeyRequired', 'authorization_type': 'authorizationType', 'authorizer': 'authorizer', 'method_responses': 'methodResponses', 'operation_name': 'operationName', 'request_models': 'requestModels', 'request_parameters': 'requestParameters', 'request_validator': 'requestValidator'})
class MethodOptions():
    def __init__(self, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer: typing.Optional["IAuthorizer"]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str,"IModel"]]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None, request_validator: typing.Optional["IRequestValidator"]=None):
        """
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The resources that are used for the response's content type. Specify request models as key-value pairs (string-to-string mapping), with a content type as the key and a Model resource name as the value
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator.
        """
        self._values = {
        }
        if api_key_required is not None: self._values["api_key_required"] = api_key_required
        if authorization_type is not None: self._values["authorization_type"] = authorization_type
        if authorizer is not None: self._values["authorizer"] = authorizer
        if method_responses is not None: self._values["method_responses"] = method_responses
        if operation_name is not None: self._values["operation_name"] = operation_name
        if request_models is not None: self._values["request_models"] = request_models
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if request_validator is not None: self._values["request_validator"] = request_validator

    @builtins.property
    def api_key_required(self) -> typing.Optional[bool]:
        """Indicates whether the method requires clients to submit a valid API key.

        default
        :default: false
        """
        return self._values.get('api_key_required')

    @builtins.property
    def authorization_type(self) -> typing.Optional["AuthorizationType"]:
        """Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified.

        If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()},
        it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type.
        However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer}
        will result in an error.

        default
        :default: - open access unless ``authorizer`` is specified
        """
        return self._values.get('authorization_type')

    @builtins.property
    def authorizer(self) -> typing.Optional["IAuthorizer"]:
        """If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource.

        If specified, the value of ``authorizationType`` must be set to ``Custom``
        """
        return self._values.get('authorizer')

    @builtins.property
    def method_responses(self) -> typing.Optional[typing.List["MethodResponse"]]:
        """The responses that can be sent to the client who calls the method.

        default
        :default:

        None

        This property is not required, but if these are not supplied for a Lambda
        proxy integration, the Lambda function must return a value of the correct format,
        for the integration response to be correctly mapped to a response to the client.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-settings-method-response.html
        """
        return self._values.get('method_responses')

    @builtins.property
    def operation_name(self) -> typing.Optional[str]:
        """A friendly operation name for the method.

        For example, you can assign the
        OperationName of ListPets for the GET /pets method.
        """
        return self._values.get('operation_name')

    @builtins.property
    def request_models(self) -> typing.Optional[typing.Mapping[str,"IModel"]]:
        """The resources that are used for the response's content type.

        Specify request
        models as key-value pairs (string-to-string mapping), with a content type
        as the key and a Model resource name as the value
        """
        return self._values.get('request_models')

    @builtins.property
    def request_parameters(self) -> typing.Optional[typing.Mapping[str,bool]]:
        """The request parameters that API Gateway accepts.

        Specify request parameters
        as key-value pairs (string-to-Boolean mapping), with a source as the key and
        a Boolean as the value. The Boolean specifies whether a parameter is required.
        A source must match the format method.request.location.name, where the location
        is querystring, path, or header, and name is a valid, unique parameter name.

        default
        :default: None
        """
        return self._values.get('request_parameters')

    @builtins.property
    def request_validator(self) -> typing.Optional["IRequestValidator"]:
        """The ID of the associated request validator."""
        return self._values.get('request_validator')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MethodOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodProps", jsii_struct_bases=[], name_mapping={'http_method': 'httpMethod', 'resource': 'resource', 'integration': 'integration', 'options': 'options'})
class MethodProps():
    def __init__(self, *, http_method: str, resource: "IResource", integration: typing.Optional["Integration"]=None, options: typing.Optional["MethodOptions"]=None):
        """
        :param http_method: The HTTP method ("GET", "POST", "PUT", ...) that clients use to call this method.
        :param resource: The resource this method is associated with. For root resource methods, specify the ``RestApi`` object.
        :param integration: The backend system that the method calls when it receives a request. Default: - a new ``MockIntegration``.
        :param options: Method options. Default: - No options.
        """
        if isinstance(options, dict): options = MethodOptions(**options)
        self._values = {
            'http_method': http_method,
            'resource': resource,
        }
        if integration is not None: self._values["integration"] = integration
        if options is not None: self._values["options"] = options

    @builtins.property
    def http_method(self) -> str:
        """The HTTP method ("GET", "POST", "PUT", ...) that clients use to call this method."""
        return self._values.get('http_method')

    @builtins.property
    def resource(self) -> "IResource":
        """The resource this method is associated with.

        For root resource methods,
        specify the ``RestApi`` object.
        """
        return self._values.get('resource')

    @builtins.property
    def integration(self) -> typing.Optional["Integration"]:
        """The backend system that the method calls when it receives a request.

        default
        :default: - a new ``MockIntegration``.
        """
        return self._values.get('integration')

    @builtins.property
    def options(self) -> typing.Optional["MethodOptions"]:
        """Method options.

        default
        :default: - No options.
        """
        return self._values.get('options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MethodProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.MethodResponse", jsii_struct_bases=[], name_mapping={'status_code': 'statusCode', 'response_models': 'responseModels', 'response_parameters': 'responseParameters'})
class MethodResponse():
    def __init__(self, *, status_code: str, response_models: typing.Optional[typing.Mapping[str,"IModel"]]=None, response_parameters: typing.Optional[typing.Mapping[str,bool]]=None):
        """
        :param status_code: The method response's status code, which you map to an IntegrationResponse. Required.
        :param response_models: The resources used for the response's content type. Specify response models as key-value pairs (string-to-string maps), with a content type as the key and a Model resource name as the value. Default: None
        :param response_parameters: Response parameters that API Gateway sends to the client that called a method. Specify response parameters as key-value pairs (string-to-Boolean maps), with a destination as the key and a Boolean as the value. Specify the destination using the following pattern: method.response.header.name, where the name is a valid, unique header name. The Boolean specifies whether a parameter is required. Default: None
        """
        self._values = {
            'status_code': status_code,
        }
        if response_models is not None: self._values["response_models"] = response_models
        if response_parameters is not None: self._values["response_parameters"] = response_parameters

    @builtins.property
    def status_code(self) -> str:
        """The method response's status code, which you map to an IntegrationResponse.

        Required.
        """
        return self._values.get('status_code')

    @builtins.property
    def response_models(self) -> typing.Optional[typing.Mapping[str,"IModel"]]:
        """The resources used for the response's content type.

        Specify response models as
        key-value pairs (string-to-string maps), with a content type as the key and a Model
        resource name as the value.

        default
        :default: None
        """
        return self._values.get('response_models')

    @builtins.property
    def response_parameters(self) -> typing.Optional[typing.Mapping[str,bool]]:
        """Response parameters that API Gateway sends to the client that called a method.

        Specify response parameters as key-value pairs (string-to-Boolean maps), with
        a destination as the key and a Boolean as the value. Specify the destination
        using the following pattern: method.response.header.name, where the name is a
        valid, unique header name. The Boolean specifies whether a parameter is required.

        default
        :default: None
        """
        return self._values.get('response_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MethodResponse(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class MockIntegration(Integration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.MockIntegration"):
    """This type of integration lets API Gateway return a response without sending the request further to the backend.

    This is useful for API testing because it
    can be used to test the integration set up without incurring charges for
    using the backend and to enable collaborative development of an API. In
    collaborative development, a team can isolate their development effort by
    setting up simulations of API components owned by other teams by using the
    MOCK integrations. It is also used to return CORS-related headers to ensure
    that the API method permits CORS access. In fact, the API Gateway console
    integrates the OPTIONS method to support CORS with a mock integration.
    Gateway responses are other examples of mock integrations.
    """
    def __init__(self, *, cache_key_parameters: typing.Optional[typing.List[str]]=None, cache_namespace: typing.Optional[str]=None, connection_type: typing.Optional["ConnectionType"]=None, content_handling: typing.Optional["ContentHandling"]=None, credentials_passthrough: typing.Optional[bool]=None, credentials_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, integration_responses: typing.Optional[typing.List["IntegrationResponse"]]=None, passthrough_behavior: typing.Optional["PassthroughBehavior"]=None, request_parameters: typing.Optional[typing.Mapping[str,str]]=None, request_templates: typing.Optional[typing.Mapping[str,str]]=None, vpc_link: typing.Optional["VpcLink"]=None) -> None:
        """
        :param cache_key_parameters: A list of request parameters whose values are to be cached. It determines request parameters that will make it into the cache key.
        :param cache_namespace: An API-specific tag group of related cached parameters.
        :param connection_type: The type of network connection to the integration endpoint. Default: ConnectionType.Internet
        :param content_handling: Specifies how to handle request payload content type conversions. Default: none if this property isn't defined, the request payload is passed through from the method request to the integration request without modification, provided that the ``passthroughBehaviors`` property is configured to support payload pass-through.
        :param credentials_passthrough: Requires that the caller's identity be passed through from the request. Default: Caller identity is not passed through
        :param credentials_role: An IAM role that API Gateway assumes. Mutually exclusive with ``credentialsPassThrough``. Default: A role is not assumed
        :param integration_responses: The response that API Gateway provides after a method's backend completes processing a request. API Gateway intercepts the response from the backend so that you can control how API Gateway surfaces backend responses. For example, you can map the backend status codes to codes that you define.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER.
        :param request_parameters: The request parameters that API Gateway sends with the backend request. Specify request parameters as key-value pairs (string-to-string mappings), with a destination as the key and a source as the value. Specify the destination by using the following pattern integration.request.location.name, where location is querystring, path, or header, and name is a valid, unique parameter name. The source must be an existing method request parameter or a static value. You must enclose static values in single quotation marks and pre-encode these values based on their destination in the request.
        :param request_templates: A map of Apache Velocity templates that are applied on the request payload. The template that API Gateway uses is based on the value of the Content-Type header that's sent by the client. The content type value is the key, and the template is the value (specified as a string), such as the following snippet: { "application/json": "{\n "statusCode": "200"\n}" }
        :param vpc_link: The VpcLink used for the integration. Required if connectionType is VPC_LINK
        """
        options = IntegrationOptions(cache_key_parameters=cache_key_parameters, cache_namespace=cache_namespace, connection_type=connection_type, content_handling=content_handling, credentials_passthrough=credentials_passthrough, credentials_role=credentials_role, integration_responses=integration_responses, passthrough_behavior=passthrough_behavior, request_parameters=request_parameters, request_templates=request_templates, vpc_link=vpc_link)

        jsii.create(MockIntegration, self, [options])


@jsii.implements(IModel)
class Model(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Model"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api: "IRestApi", schema: "JsonSchema", content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, model_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param rest_api: The rest API that this model is part of. The reason we need the RestApi object itself and not just the ID is because the model is being tracked by the top-level RestApi object for the purpose of calculating it's hash to determine the ID of the deployment. This allows us to automatically update the deployment when the model of the REST API changes.
        :param schema: The schema to use to transform data to one or more output formats. Specify null ({}) if you don't want to specify a schema.
        :param content_type: The content type for the model. You can also force a content type in the request or response model mapping. Default: -
        :param description: A description that identifies this model. Default: None
        :param model_name: A name for the model. Important If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. Default: If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the model name. For more information, see Name Type.
        """
        props = ModelProps(rest_api=rest_api, schema=schema, content_type=content_type, description=description, model_name=model_name)

        jsii.create(Model, self, [scope, id, props])

    @jsii.member(jsii_name="fromModelName")
    @builtins.classmethod
    def from_model_name(cls, scope: aws_cdk.core.Construct, id: str, model_name: str) -> "IModel":
        """
        :param scope: -
        :param id: -
        :param model_name: -
        """
        return jsii.sinvoke(cls, "fromModelName", [scope, id, model_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="EMPTY_MODEL")
    def EMPTY_MODEL(cls) -> "IModel":
        """Represents a reference to a REST API's Empty model, which is available as part of the model collection by default.

        This can be used for mapping
        JSON responses from an integration to what is returned to a client,
        where strong typing is not required. In the absence of any defined
        model, the Empty model will be used to return the response payload
        unmapped.

        Definition
        {
        "$schema" : "http://json-schema.org/draft-04/schema#",
        "title" : "Empty Schema",
        "type" : "object"
        }

        see
        :see: https://docs.amazonaws.cn/en_us/apigateway/latest/developerguide/models-mappings.html#models-mappings-models
        """
        return jsii.sget(cls, "EMPTY_MODEL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ERROR_MODEL")
    def ERROR_MODEL(cls) -> "IModel":
        """Represents a reference to a REST API's Error model, which is available as part of the model collection by default.

        This can be used for mapping
        error JSON responses from an integration to a client, where a simple
        generic message field is sufficient to map and return an error payload.

        Definition
        {
        "$schema" : "http://json-schema.org/draft-04/schema#",
        "title" : "Error Schema",
        "type" : "object",
        "properties" : {
        "message" : { "type" : "string" }
        }
        }
        """
        return jsii.sget(cls, "ERROR_MODEL")

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> str:
        """Returns the model name, such as 'myModel'.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "modelId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ModelOptions", jsii_struct_bases=[], name_mapping={'schema': 'schema', 'content_type': 'contentType', 'description': 'description', 'model_name': 'modelName'})
class ModelOptions():
    def __init__(self, *, schema: "JsonSchema", content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, model_name: typing.Optional[str]=None):
        """
        :param schema: The schema to use to transform data to one or more output formats. Specify null ({}) if you don't want to specify a schema.
        :param content_type: The content type for the model. You can also force a content type in the request or response model mapping. Default: -
        :param description: A description that identifies this model. Default: None
        :param model_name: A name for the model. Important If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. Default: If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the model name. For more information, see Name Type.
        """
        if isinstance(schema, dict): schema = JsonSchema(**schema)
        self._values = {
            'schema': schema,
        }
        if content_type is not None: self._values["content_type"] = content_type
        if description is not None: self._values["description"] = description
        if model_name is not None: self._values["model_name"] = model_name

    @builtins.property
    def schema(self) -> "JsonSchema":
        """The schema to use to transform data to one or more output formats.

        Specify null ({}) if you don't want to specify a schema.
        """
        return self._values.get('schema')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """The content type for the model.

        You can also force a
        content type in the request or response model mapping.

        default
        :default: -
        """
        return self._values.get('content_type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description that identifies this model.

        default
        :default: None
        """
        return self._values.get('description')

    @builtins.property
    def model_name(self) -> typing.Optional[str]:
        """A name for the model.

        Important
        If you specify a name, you cannot perform updates that
        require replacement of this resource. You can perform
        updates that require no or some interruption. If you
        must replace the resource, specify a new name.

        default
        :default:

         If you don't specify a name,
        AWS CloudFormation generates a unique physical ID and
        uses that ID for the model name. For more information,
        see Name Type.
        """
        return self._values.get('model_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ModelOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ModelProps", jsii_struct_bases=[ModelOptions], name_mapping={'schema': 'schema', 'content_type': 'contentType', 'description': 'description', 'model_name': 'modelName', 'rest_api': 'restApi'})
class ModelProps(ModelOptions):
    def __init__(self, *, schema: "JsonSchema", content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, model_name: typing.Optional[str]=None, rest_api: "IRestApi"):
        """
        :param schema: The schema to use to transform data to one or more output formats. Specify null ({}) if you don't want to specify a schema.
        :param content_type: The content type for the model. You can also force a content type in the request or response model mapping. Default: -
        :param description: A description that identifies this model. Default: None
        :param model_name: A name for the model. Important If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. Default: If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the model name. For more information, see Name Type.
        :param rest_api: The rest API that this model is part of. The reason we need the RestApi object itself and not just the ID is because the model is being tracked by the top-level RestApi object for the purpose of calculating it's hash to determine the ID of the deployment. This allows us to automatically update the deployment when the model of the REST API changes.
        """
        if isinstance(schema, dict): schema = JsonSchema(**schema)
        self._values = {
            'schema': schema,
            'rest_api': rest_api,
        }
        if content_type is not None: self._values["content_type"] = content_type
        if description is not None: self._values["description"] = description
        if model_name is not None: self._values["model_name"] = model_name

    @builtins.property
    def schema(self) -> "JsonSchema":
        """The schema to use to transform data to one or more output formats.

        Specify null ({}) if you don't want to specify a schema.
        """
        return self._values.get('schema')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """The content type for the model.

        You can also force a
        content type in the request or response model mapping.

        default
        :default: -
        """
        return self._values.get('content_type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description that identifies this model.

        default
        :default: None
        """
        return self._values.get('description')

    @builtins.property
    def model_name(self) -> typing.Optional[str]:
        """A name for the model.

        Important
        If you specify a name, you cannot perform updates that
        require replacement of this resource. You can perform
        updates that require no or some interruption. If you
        must replace the resource, specify a new name.

        default
        :default:

         If you don't specify a name,
        AWS CloudFormation generates a unique physical ID and
        uses that ID for the model name. For more information,
        see Name Type.
        """
        return self._values.get('model_name')

    @builtins.property
    def rest_api(self) -> "IRestApi":
        """The rest API that this model is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        return self._values.get('rest_api')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ModelProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.PassthroughBehavior")
class PassthroughBehavior(enum.Enum):
    WHEN_NO_MATCH = "WHEN_NO_MATCH"
    """Passes the request body for unmapped content types through to the integration back end without transformation."""
    NEVER = "NEVER"
    """Rejects unmapped content types with an HTTP 415 'Unsupported Media Type' response."""
    WHEN_NO_TEMPLATES = "WHEN_NO_TEMPLATES"
    """Allows pass-through when the integration has NO content types mapped to templates.

    However if there is at least one content type defined,
    unmapped content types will be rejected with the same 415 response.
    """

@jsii.enum(jsii_type="@aws-cdk/aws-apigateway.Period")
class Period(enum.Enum):
    """Time period for which quota settings apply."""
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.QuotaSettings", jsii_struct_bases=[], name_mapping={'limit': 'limit', 'offset': 'offset', 'period': 'period'})
class QuotaSettings():
    def __init__(self, *, limit: typing.Optional[jsii.Number]=None, offset: typing.Optional[jsii.Number]=None, period: typing.Optional["Period"]=None):
        """Specifies the maximum number of requests that clients can make to API Gateway APIs.

        :param limit: The maximum number of requests that users can make within the specified time period. Default: none
        :param offset: For the initial time period, the number of requests to subtract from the specified limit. Default: none
        :param period: The time period for which the maximum limit of requests applies. Default: none
        """
        self._values = {
        }
        if limit is not None: self._values["limit"] = limit
        if offset is not None: self._values["offset"] = offset
        if period is not None: self._values["period"] = period

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        """The maximum number of requests that users can make within the specified time period.

        default
        :default: none
        """
        return self._values.get('limit')

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        """For the initial time period, the number of requests to subtract from the specified limit.

        default
        :default: none
        """
        return self._values.get('offset')

    @builtins.property
    def period(self) -> typing.Optional["Period"]:
        """The time period for which the maximum limit of requests applies.

        default
        :default: none
        """
        return self._values.get('period')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QuotaSettings(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IRequestValidator)
class RequestValidator(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.RequestValidator"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api: "IRestApi", request_validator_name: typing.Optional[str]=None, validate_request_body: typing.Optional[bool]=None, validate_request_parameters: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param rest_api: The rest API that this model is part of. The reason we need the RestApi object itself and not just the ID is because the model is being tracked by the top-level RestApi object for the purpose of calculating it's hash to determine the ID of the deployment. This allows us to automatically update the deployment when the model of the REST API changes.
        :param request_validator_name: The name of this request validator. Default: None
        :param validate_request_body: Indicates whether to validate the request body according to the configured schema for the targeted API and method. Default: false
        :param validate_request_parameters: Indicates whether to validate request parameters. Default: false
        """
        props = RequestValidatorProps(rest_api=rest_api, request_validator_name=request_validator_name, validate_request_body=validate_request_body, validate_request_parameters=validate_request_parameters)

        jsii.create(RequestValidator, self, [scope, id, props])

    @jsii.member(jsii_name="fromRequestValidatorId")
    @builtins.classmethod
    def from_request_validator_id(cls, scope: aws_cdk.core.Construct, id: str, request_validator_id: str) -> "IRequestValidator":
        """
        :param scope: -
        :param id: -
        :param request_validator_id: -
        """
        return jsii.sinvoke(cls, "fromRequestValidatorId", [scope, id, request_validator_id])

    @builtins.property
    @jsii.member(jsii_name="requestValidatorId")
    def request_validator_id(self) -> str:
        """ID of the request validator, such as abc123.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "requestValidatorId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.RequestValidatorOptions", jsii_struct_bases=[], name_mapping={'request_validator_name': 'requestValidatorName', 'validate_request_body': 'validateRequestBody', 'validate_request_parameters': 'validateRequestParameters'})
class RequestValidatorOptions():
    def __init__(self, *, request_validator_name: typing.Optional[str]=None, validate_request_body: typing.Optional[bool]=None, validate_request_parameters: typing.Optional[bool]=None):
        """
        :param request_validator_name: The name of this request validator. Default: None
        :param validate_request_body: Indicates whether to validate the request body according to the configured schema for the targeted API and method. Default: false
        :param validate_request_parameters: Indicates whether to validate request parameters. Default: false
        """
        self._values = {
        }
        if request_validator_name is not None: self._values["request_validator_name"] = request_validator_name
        if validate_request_body is not None: self._values["validate_request_body"] = validate_request_body
        if validate_request_parameters is not None: self._values["validate_request_parameters"] = validate_request_parameters

    @builtins.property
    def request_validator_name(self) -> typing.Optional[str]:
        """The name of this request validator.

        default
        :default: None
        """
        return self._values.get('request_validator_name')

    @builtins.property
    def validate_request_body(self) -> typing.Optional[bool]:
        """Indicates whether to validate the request body according to the configured schema for the targeted API and method.

        default
        :default: false
        """
        return self._values.get('validate_request_body')

    @builtins.property
    def validate_request_parameters(self) -> typing.Optional[bool]:
        """Indicates whether to validate request parameters.

        default
        :default: false
        """
        return self._values.get('validate_request_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RequestValidatorOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.RequestValidatorProps", jsii_struct_bases=[RequestValidatorOptions], name_mapping={'request_validator_name': 'requestValidatorName', 'validate_request_body': 'validateRequestBody', 'validate_request_parameters': 'validateRequestParameters', 'rest_api': 'restApi'})
class RequestValidatorProps(RequestValidatorOptions):
    def __init__(self, *, request_validator_name: typing.Optional[str]=None, validate_request_body: typing.Optional[bool]=None, validate_request_parameters: typing.Optional[bool]=None, rest_api: "IRestApi"):
        """
        :param request_validator_name: The name of this request validator. Default: None
        :param validate_request_body: Indicates whether to validate the request body according to the configured schema for the targeted API and method. Default: false
        :param validate_request_parameters: Indicates whether to validate request parameters. Default: false
        :param rest_api: The rest API that this model is part of. The reason we need the RestApi object itself and not just the ID is because the model is being tracked by the top-level RestApi object for the purpose of calculating it's hash to determine the ID of the deployment. This allows us to automatically update the deployment when the model of the REST API changes.
        """
        self._values = {
            'rest_api': rest_api,
        }
        if request_validator_name is not None: self._values["request_validator_name"] = request_validator_name
        if validate_request_body is not None: self._values["validate_request_body"] = validate_request_body
        if validate_request_parameters is not None: self._values["validate_request_parameters"] = validate_request_parameters

    @builtins.property
    def request_validator_name(self) -> typing.Optional[str]:
        """The name of this request validator.

        default
        :default: None
        """
        return self._values.get('request_validator_name')

    @builtins.property
    def validate_request_body(self) -> typing.Optional[bool]:
        """Indicates whether to validate the request body according to the configured schema for the targeted API and method.

        default
        :default: false
        """
        return self._values.get('validate_request_body')

    @builtins.property
    def validate_request_parameters(self) -> typing.Optional[bool]:
        """Indicates whether to validate request parameters.

        default
        :default: false
        """
        return self._values.get('validate_request_parameters')

    @builtins.property
    def rest_api(self) -> "IRestApi":
        """The rest API that this model is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        return self._values.get('rest_api')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RequestValidatorProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IResource)
class ResourceBase(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-apigateway.ResourceBase"):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ResourceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -
        """
        jsii.create(ResourceBase, self, [scope, id])

    @jsii.member(jsii_name="addCorsPreflight")
    def add_cors_preflight(self, *, allow_origins: typing.List[str], allow_credentials: typing.Optional[bool]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List[str]]=None, disable_cache: typing.Optional[bool]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[aws_cdk.core.Duration]=None, status_code: typing.Optional[jsii.Number]=None) -> "Method":
        """Adds an OPTIONS method to this resource which responds to Cross-Origin Resource Sharing (CORS) preflight requests.

        Cross-Origin Resource Sharing (CORS) is a mechanism that uses additional
        HTTP headers to tell browsers to give a web application running at one
        origin, access to selected resources from a different origin. A web
        application executes a cross-origin HTTP request when it requests a
        resource that has a different origin (domain, protocol, or port) from its
        own.

        :param allow_origins: Specifies the list of origins that are allowed to make requests to this resource. If you wish to allow all origins, specify ``Cors.ALL_ORIGINS`` or ``[ * ]``. Responses will include the ``Access-Control-Allow-Origin`` response header. If ``Cors.ALL_ORIGINS`` is specified, the ``Vary: Origin`` response header will also be included.
        :param allow_credentials: The Access-Control-Allow-Credentials response header tells browsers whether to expose the response to frontend JavaScript code when the request's credentials mode (Request.credentials) is "include". When a request's credentials mode (Request.credentials) is "include", browsers will only expose the response to frontend JavaScript code if the Access-Control-Allow-Credentials value is true. Credentials are cookies, authorization headers or TLS client certificates. Default: false
        :param allow_headers: The Access-Control-Allow-Headers response header is used in response to a preflight request which includes the Access-Control-Request-Headers to indicate which HTTP headers can be used during the actual request. Default: Cors.DEFAULT_HEADERS
        :param allow_methods: The Access-Control-Allow-Methods response header specifies the method or methods allowed when accessing the resource in response to a preflight request. If ``ANY`` is specified, it will be expanded to ``Cors.ALL_METHODS``. Default: Cors.ALL_METHODS
        :param disable_cache: Sets Access-Control-Max-Age to -1, which means that caching is disabled. This option cannot be used with ``maxAge``. Default: - cache is enabled
        :param expose_headers: The Access-Control-Expose-Headers response header indicates which headers can be exposed as part of the response by listing their names. If you want clients to be able to access other headers, you have to list them using the Access-Control-Expose-Headers header. Default: - only the 6 CORS-safelisted response headers are exposed: Cache-Control, Content-Language, Content-Type, Expires, Last-Modified, Pragma
        :param max_age: The Access-Control-Max-Age response header indicates how long the results of a preflight request (that is the information contained in the Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can be cached. To disable caching altogther use ``disableCache: true``. Default: - browser-specific (see reference)
        :param status_code: Specifies the response status code returned from the OPTIONS method. Default: 204
        """
        options = CorsOptions(allow_origins=allow_origins, allow_credentials=allow_credentials, allow_headers=allow_headers, allow_methods=allow_methods, disable_cache=disable_cache, expose_headers=expose_headers, max_age=max_age, status_code=status_code)

        return jsii.invoke(self, "addCorsPreflight", [options])

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, integration: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer: typing.Optional["IAuthorizer"]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str,"IModel"]]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None, request_validator: typing.Optional["IRequestValidator"]=None) -> "Method":
        """Defines a new method for this resource.

        :param http_method: -
        :param integration: -
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The resources that are used for the response's content type. Specify request models as key-value pairs (string-to-string mapping), with a content type as the key and a Model resource name as the value
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator.
        """
        options = MethodOptions(api_key_required=api_key_required, authorization_type=authorization_type, authorizer=authorizer, method_responses=method_responses, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, request_validator=request_validator)

        return jsii.invoke(self, "addMethod", [http_method, integration, options])

    @jsii.member(jsii_name="addProxy")
    def add_proxy(self, *, any_method: typing.Optional[bool]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "ProxyResource":
        """Adds a greedy proxy resource ("{proxy+}") and an ANY method to this route.

        :param any_method: Adds an "ANY" method to this resource. If set to ``false``, you will have to explicitly add methods to this resource after it's created. Default: true
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        options = ProxyResourceOptions(any_method=any_method, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        return jsii.invoke(self, "addProxy", [options])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, path_part: str, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> "Resource":
        """Defines a new child resource where this resource is the parent.

        :param path_part: -
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        options = ResourceOptions(default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        return jsii.invoke(self, "addResource", [path_part, options])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, path_part: str) -> typing.Optional["IResource"]:
        """Retrieves a child resource by path part.

        :param path_part: -
        """
        return jsii.invoke(self, "getResource", [path_part])

    @jsii.member(jsii_name="resourceForPath")
    def resource_for_path(self, path: str) -> "Resource":
        """Gets or create all resources leading up to the specified path.

        - Path may only start with "/" if this method is called on the root resource.
        - All resources are created using default options.

        :param path: -
        """
        return jsii.invoke(self, "resourceForPath", [path])

    @builtins.property
    @jsii.member(jsii_name="path")
    @abc.abstractmethod
    def path(self) -> str:
        """The full path of this resuorce."""
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    @abc.abstractmethod
    def resource_id(self) -> str:
        """The ID of the resource."""
        ...

    @builtins.property
    @jsii.member(jsii_name="restApi")
    @abc.abstractmethod
    def rest_api(self) -> "RestApi":
        """The rest API that this resource is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="defaultCorsPreflightOptions")
    @abc.abstractmethod
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Default options for CORS preflight OPTIONS method."""
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultIntegration")
    @abc.abstractmethod
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified."""
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultMethodOptions")
    @abc.abstractmethod
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified."""
        ...

    @builtins.property
    @jsii.member(jsii_name="parentResource")
    @abc.abstractmethod
    def parent_resource(self) -> typing.Optional["IResource"]:
        """The parent of this resource or undefined for the root resource."""
        ...


class _ResourceBaseProxy(ResourceBase, jsii.proxy_for(aws_cdk.core.Resource)):
    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The full path of this resuorce."""
        return jsii.get(self, "path")

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        """The ID of the resource."""
        return jsii.get(self, "resourceId")

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "RestApi":
        """The rest API that this resource is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        return jsii.get(self, "restApi")

    @builtins.property
    @jsii.member(jsii_name="defaultCorsPreflightOptions")
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Default options for CORS preflight OPTIONS method."""
        return jsii.get(self, "defaultCorsPreflightOptions")

    @builtins.property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified."""
        return jsii.get(self, "defaultIntegration")

    @builtins.property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified."""
        return jsii.get(self, "defaultMethodOptions")

    @builtins.property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IResource"]:
        """The parent of this resource or undefined for the root resource."""
        return jsii.get(self, "parentResource")


class Resource(ResourceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Resource"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, parent: "IResource", path_part: str, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param parent: The parent resource of this resource. You can either pass another ``Resource`` object or a ``RestApi`` object here.
        :param path_part: A path name for the resource.
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        props = ResourceProps(parent=parent, path_part=path_part, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        jsii.create(Resource, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The full path of this resuorce."""
        return jsii.get(self, "path")

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> str:
        """The ID of the resource."""
        return jsii.get(self, "resourceId")

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "RestApi":
        """The rest API that this resource is part of.

        The reason we need the RestApi object itself and not just the ID is because the model
        is being tracked by the top-level RestApi object for the purpose of calculating it's
        hash to determine the ID of the deployment. This allows us to automatically update
        the deployment when the model of the REST API changes.
        """
        return jsii.get(self, "restApi")

    @builtins.property
    @jsii.member(jsii_name="defaultCorsPreflightOptions")
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Default options for CORS preflight OPTIONS method."""
        return jsii.get(self, "defaultCorsPreflightOptions")

    @builtins.property
    @jsii.member(jsii_name="defaultIntegration")
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified."""
        return jsii.get(self, "defaultIntegration")

    @builtins.property
    @jsii.member(jsii_name="defaultMethodOptions")
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified."""
        return jsii.get(self, "defaultMethodOptions")

    @builtins.property
    @jsii.member(jsii_name="parentResource")
    def parent_resource(self) -> typing.Optional["IResource"]:
        """The parent of this resource or undefined for the root resource."""
        return jsii.get(self, "parentResource")


class ProxyResource(Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.ProxyResource"):
    """Defines a {proxy+} greedy resource and an ANY method on a route.

    see
    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, parent: "IResource", any_method: typing.Optional[bool]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param parent: The parent resource of this resource. You can either pass another ``Resource`` object or a ``RestApi`` object here.
        :param any_method: Adds an "ANY" method to this resource. If set to ``false``, you will have to explicitly add methods to this resource after it's created. Default: true
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        props = ProxyResourceProps(parent=parent, any_method=any_method, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        jsii.create(ProxyResource, self, [scope, id, props])

    @jsii.member(jsii_name="addMethod")
    def add_method(self, http_method: str, integration: typing.Optional["Integration"]=None, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional["AuthorizationType"]=None, authorizer: typing.Optional["IAuthorizer"]=None, method_responses: typing.Optional[typing.List["MethodResponse"]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str,"IModel"]]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None, request_validator: typing.Optional["IRequestValidator"]=None) -> "Method":
        """Defines a new method for this resource.

        :param http_method: -
        :param integration: -
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The resources that are used for the response's content type. Specify request models as key-value pairs (string-to-string mapping), with a content type as the key and a Model resource name as the value
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator.
        """
        options = MethodOptions(api_key_required=api_key_required, authorization_type=authorization_type, authorizer=authorizer, method_responses=method_responses, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, request_validator=request_validator)

        return jsii.invoke(self, "addMethod", [http_method, integration, options])

    @builtins.property
    @jsii.member(jsii_name="anyMethod")
    def any_method(self) -> typing.Optional["Method"]:
        """If ``props.anyMethod`` is ``true``, this will be the reference to the 'ANY' method associated with this proxy resource."""
        return jsii.get(self, "anyMethod")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ResourceOptions", jsii_struct_bases=[], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions'})
class ResourceOptions():
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None):
        """
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        self._values = {
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ApiKeyProps", jsii_struct_bases=[ResourceOptions], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions', 'api_key_name': 'apiKeyName', 'customer_id': 'customerId', 'description': 'description', 'enabled': 'enabled', 'generate_distinct_id': 'generateDistinctId', 'resources': 'resources'})
class ApiKeyProps(ResourceOptions):
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, api_key_name: typing.Optional[str]=None, customer_id: typing.Optional[str]=None, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, generate_distinct_id: typing.Optional[bool]=None, resources: typing.Optional[typing.List["RestApi"]]=None):
        """ApiKey Properties.

        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param api_key_name: A name for the API key. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the API key name. Default: automically generated name
        :param customer_id: An AWS Marketplace customer identifier to use when integrating with the AWS SaaS Marketplace. Default: none
        :param description: A description of the purpose of the API key. Default: none
        :param enabled: Indicates whether the API key can be used by clients. Default: true
        :param generate_distinct_id: Specifies whether the key identifier is distinct from the created API key value. Default: false
        :param resources: A list of resources this api key is associated with. Default: none
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        self._values = {
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options
        if api_key_name is not None: self._values["api_key_name"] = api_key_name
        if customer_id is not None: self._values["customer_id"] = customer_id
        if description is not None: self._values["description"] = description
        if enabled is not None: self._values["enabled"] = enabled
        if generate_distinct_id is not None: self._values["generate_distinct_id"] = generate_distinct_id
        if resources is not None: self._values["resources"] = resources

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    @builtins.property
    def api_key_name(self) -> typing.Optional[str]:
        """A name for the API key.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the API key name.

        default
        :default: automically generated name

        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-name
        """
        return self._values.get('api_key_name')

    @builtins.property
    def customer_id(self) -> typing.Optional[str]:
        """An AWS Marketplace customer identifier to use when integrating with the AWS SaaS Marketplace.

        default
        :default: none

        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-customerid
        """
        return self._values.get('customer_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the purpose of the API key.

        default
        :default: none

        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-description
        """
        return self._values.get('description')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """Indicates whether the API key can be used by clients.

        default
        :default: true

        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-enabled
        """
        return self._values.get('enabled')

    @builtins.property
    def generate_distinct_id(self) -> typing.Optional[bool]:
        """Specifies whether the key identifier is distinct from the created API key value.

        default
        :default: false

        link:
        :link:: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-generatedistinctid
        """
        return self._values.get('generate_distinct_id')

    @builtins.property
    def resources(self) -> typing.Optional[typing.List["RestApi"]]:
        """A list of resources this api key is associated with.

        default
        :default: none
        """
        return self._values.get('resources')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApiKeyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ProxyResourceOptions", jsii_struct_bases=[ResourceOptions], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions', 'any_method': 'anyMethod'})
class ProxyResourceOptions(ResourceOptions):
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, any_method: typing.Optional[bool]=None):
        """
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param any_method: Adds an "ANY" method to this resource. If set to ``false``, you will have to explicitly add methods to this resource after it's created. Default: true
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        self._values = {
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options
        if any_method is not None: self._values["any_method"] = any_method

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    @builtins.property
    def any_method(self) -> typing.Optional[bool]:
        """Adds an "ANY" method to this resource.

        If set to ``false``, you will have to explicitly
        add methods to this resource after it's created.

        default
        :default: true
        """
        return self._values.get('any_method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ProxyResourceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ProxyResourceProps", jsii_struct_bases=[ProxyResourceOptions], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions', 'any_method': 'anyMethod', 'parent': 'parent'})
class ProxyResourceProps(ProxyResourceOptions):
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, any_method: typing.Optional[bool]=None, parent: "IResource"):
        """
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param any_method: Adds an "ANY" method to this resource. If set to ``false``, you will have to explicitly add methods to this resource after it's created. Default: true
        :param parent: The parent resource of this resource. You can either pass another ``Resource`` object or a ``RestApi`` object here.
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        self._values = {
            'parent': parent,
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options
        if any_method is not None: self._values["any_method"] = any_method

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    @builtins.property
    def any_method(self) -> typing.Optional[bool]:
        """Adds an "ANY" method to this resource.

        If set to ``false``, you will have to explicitly
        add methods to this resource after it's created.

        default
        :default: true
        """
        return self._values.get('any_method')

    @builtins.property
    def parent(self) -> "IResource":
        """The parent resource of this resource.

        You can either pass another
        ``Resource`` object or a ``RestApi`` object here.
        """
        return self._values.get('parent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ProxyResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ResourceProps", jsii_struct_bases=[ResourceOptions], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions', 'parent': 'parent', 'path_part': 'pathPart'})
class ResourceProps(ResourceOptions):
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, parent: "IResource", path_part: str):
        """
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param parent: The parent resource of this resource. You can either pass another ``Resource`` object or a ``RestApi`` object here.
        :param path_part: A path name for the resource.
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        self._values = {
            'parent': parent,
            'path_part': path_part,
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    @builtins.property
    def parent(self) -> "IResource":
        """The parent resource of this resource.

        You can either pass another
        ``Resource`` object or a ``RestApi`` object here.
        """
        return self._values.get('parent')

    @builtins.property
    def path_part(self) -> str:
        """A path name for the resource."""
        return self._values.get('path_part')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IRestApi)
class RestApi(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.RestApi"):
    """Represents a REST API in Amazon API Gateway.

    Use ``addResource`` and ``addMethod`` to configure the API model.

    By default, the API will automatically be deployed and accessible from a
    public endpoint.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key_source_type: typing.Optional["ApiKeySourceType"]=None, binary_media_types: typing.Optional[typing.List[str]]=None, clone_from: typing.Optional["IRestApi"]=None, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, domain_name: typing.Optional["DomainNameOptions"]=None, endpoint_export_name: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: true
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployStageOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the purpose of this API Gateway RestApi resource. Default: - No description.
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: - No endpoint types.
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param minimum_compression_size: A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        props = RestApiProps(api_key_source_type=api_key_source_type, binary_media_types=binary_media_types, clone_from=clone_from, cloud_watch_role=cloud_watch_role, deploy=deploy, deploy_options=deploy_options, description=description, domain_name=domain_name, endpoint_export_name=endpoint_export_name, endpoint_types=endpoint_types, fail_on_warnings=fail_on_warnings, minimum_compression_size=minimum_compression_size, parameters=parameters, policy=policy, rest_api_name=rest_api_name, retain_deployments=retain_deployments, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        jsii.create(RestApi, self, [scope, id, props])

    @jsii.member(jsii_name="fromRestApiId")
    @builtins.classmethod
    def from_rest_api_id(cls, scope: aws_cdk.core.Construct, id: str, rest_api_id: str) -> "IRestApi":
        """
        :param scope: -
        :param id: -
        :param rest_api_id: -
        """
        return jsii.sinvoke(cls, "fromRestApiId", [scope, id, rest_api_id])

    @jsii.member(jsii_name="addApiKey")
    def add_api_key(self, id: str) -> "IApiKey":
        """Add an ApiKey.

        :param id: -
        """
        return jsii.invoke(self, "addApiKey", [id])

    @jsii.member(jsii_name="addDomainName")
    def add_domain_name(self, id: str, *, certificate: aws_cdk.aws_certificatemanager.ICertificate, domain_name: str, endpoint_type: typing.Optional["EndpointType"]=None) -> "DomainName":
        """Defines an API Gateway domain name and maps it to this API.

        :param id: The construct id.
        :param certificate: The reference to an AWS-managed certificate for use by the edge-optimized endpoint for the domain name. For "EDGE" domain names, the certificate needs to be in the US East (N. Virginia) region.
        :param domain_name: The custom domain name for your API. Uppercase letters are not supported.
        :param endpoint_type: The type of endpoint for this DomainName. Default: REGIONAL
        """
        options = DomainNameOptions(certificate=certificate, domain_name=domain_name, endpoint_type=endpoint_type)

        return jsii.invoke(self, "addDomainName", [id, options])

    @jsii.member(jsii_name="addModel")
    def add_model(self, id: str, *, schema: "JsonSchema", content_type: typing.Optional[str]=None, description: typing.Optional[str]=None, model_name: typing.Optional[str]=None) -> "Model":
        """Adds a new model.

        :param id: -
        :param schema: The schema to use to transform data to one or more output formats. Specify null ({}) if you don't want to specify a schema.
        :param content_type: The content type for the model. You can also force a content type in the request or response model mapping. Default: -
        :param description: A description that identifies this model. Default: None
        :param model_name: A name for the model. Important If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. Default: If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the model name. For more information, see Name Type.
        """
        props = ModelOptions(schema=schema, content_type=content_type, description=description, model_name=model_name)

        return jsii.invoke(self, "addModel", [id, props])

    @jsii.member(jsii_name="addRequestValidator")
    def add_request_validator(self, id: str, *, request_validator_name: typing.Optional[str]=None, validate_request_body: typing.Optional[bool]=None, validate_request_parameters: typing.Optional[bool]=None) -> "RequestValidator":
        """Adds a new request validator.

        :param id: -
        :param request_validator_name: The name of this request validator. Default: None
        :param validate_request_body: Indicates whether to validate the request body according to the configured schema for the targeted API and method. Default: false
        :param validate_request_parameters: Indicates whether to validate request parameters. Default: false
        """
        props = RequestValidatorOptions(request_validator_name=request_validator_name, validate_request_body=validate_request_body, validate_request_parameters=validate_request_parameters)

        return jsii.invoke(self, "addRequestValidator", [id, props])

    @jsii.member(jsii_name="addUsagePlan")
    def add_usage_plan(self, id: str, *, api_key: typing.Optional["IApiKey"]=None, api_stages: typing.Optional[typing.List["UsagePlanPerApiStage"]]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, quota: typing.Optional["QuotaSettings"]=None, throttle: typing.Optional["ThrottleSettings"]=None) -> "UsagePlan":
        """Adds a usage plan.

        :param id: -
        :param api_key: ApiKey to be associated with the usage plan. Default: none
        :param api_stages: API Stages to be associated which the usage plan. Default: none
        :param description: Represents usage plan purpose. Default: none
        :param name: Name for this usage plan. Default: none
        :param quota: Number of requests clients can make in a given time period. Default: none
        :param throttle: Overall throttle settings for the API. Default: none
        """
        props = UsagePlanProps(api_key=api_key, api_stages=api_stages, description=description, name=name, quota=quota, throttle=throttle)

        return jsii.invoke(self, "addUsagePlan", [id, props])

    @jsii.member(jsii_name="arnForExecuteApi")
    def arn_for_execute_api(self, method: typing.Optional[str]=None, path: typing.Optional[str]=None, stage: typing.Optional[str]=None) -> str:
        """
        :param method: The method (default ``*``).
        :param path: The resource path. Must start with '/' (default ``*``)
        :param stage: The stage (default ``*``).

        default
        :default:

        "*" returns the execute API ARN for all methods/resources in
        this API.

        return
        :return: The "execute-api" ARN.
        """
        return jsii.invoke(self, "arnForExecuteApi", [method, path, stage])

    @jsii.member(jsii_name="urlForPath")
    def url_for_path(self, path: typing.Optional[str]=None) -> str:
        """Returns the URL for an HTTP path.

        Fails if ``deploymentStage`` is not set either by ``deploy`` or explicitly.

        :param path: -
        """
        return jsii.invoke(self, "urlForPath", [path])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Performs validation of the REST API."""
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="restApiId")
    def rest_api_id(self) -> str:
        """The ID of this API Gateway RestApi."""
        return jsii.get(self, "restApiId")

    @builtins.property
    @jsii.member(jsii_name="restApiRootResourceId")
    def rest_api_root_resource_id(self) -> str:
        """The resource ID of the root resource.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "restApiRootResourceId")

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "IResource":
        """Represents the root resource ("/") of this API. Use it to define the API model:.

        api.root.addMethod('ANY', redirectToHomePage); // "ANY /"
        api.root.addResource('friends').addMethod('GET', getFriendsHandler); // "GET /friends"
        """
        return jsii.get(self, "root")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        """The deployed root URL of this REST API."""
        return jsii.get(self, "url")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional["DomainName"]:
        """The first domain name mapped to this API, if defined through the ``domainName`` configuration prop, or added via ``addDomainName``."""
        return jsii.get(self, "domainName")

    @builtins.property
    @jsii.member(jsii_name="latestDeployment")
    def latest_deployment(self) -> typing.Optional["Deployment"]:
        """API Gateway deployment that represents the latest changes of the API.

        This resource will be automatically updated every time the REST API model changes.
        This will be undefined if ``deploy`` is false.
        """
        return jsii.get(self, "latestDeployment")

    @builtins.property
    @jsii.member(jsii_name="deploymentStage")
    def deployment_stage(self) -> "Stage":
        """API Gateway stage that points to the latest deployment (if defined).

        If ``deploy`` is disabled, you will need to explicitly assign this value in order to
        set up integrations.
        """
        return jsii.get(self, "deploymentStage")

    @deployment_stage.setter
    def deployment_stage(self, value: "Stage"):
        jsii.set(self, "deploymentStage", value)


class LambdaRestApi(RestApi, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.LambdaRestApi"):
    """Defines an API Gateway REST API with AWS Lambda proxy integration.

    Use the ``proxyPath`` property to define a greedy proxy ("{proxy+}") and "ANY"
    method from the specified path. If not defined, you will need to explicity
    add resources and methods to the API.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, handler: aws_cdk.aws_lambda.IFunction, options: typing.Optional["RestApiProps"]=None, proxy: typing.Optional[bool]=None, api_key_source_type: typing.Optional["ApiKeySourceType"]=None, binary_media_types: typing.Optional[typing.List[str]]=None, clone_from: typing.Optional["IRestApi"]=None, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, domain_name: typing.Optional["DomainNameOptions"]=None, endpoint_export_name: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param handler: The default Lambda function that handles all requests from this API. This handler will be used as a the default integration for all methods in this API, unless specified otherwise in ``addMethod``.
        :param options: Default: - no options.
        :param proxy: If true, route all requests to the Lambda Function. If set to false, you will need to explicitly define the API model using ``addResource`` and ``addMethod`` (or ``addProxy``). Default: true
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: true
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployStageOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the purpose of this API Gateway RestApi resource. Default: - No description.
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: - No endpoint types.
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param minimum_compression_size: A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        """
        props = LambdaRestApiProps(handler=handler, options=options, proxy=proxy, api_key_source_type=api_key_source_type, binary_media_types=binary_media_types, clone_from=clone_from, cloud_watch_role=cloud_watch_role, deploy=deploy, deploy_options=deploy_options, description=description, domain_name=domain_name, endpoint_export_name=endpoint_export_name, endpoint_types=endpoint_types, fail_on_warnings=fail_on_warnings, minimum_compression_size=minimum_compression_size, parameters=parameters, policy=policy, rest_api_name=rest_api_name, retain_deployments=retain_deployments, default_cors_preflight_options=default_cors_preflight_options, default_integration=default_integration, default_method_options=default_method_options)

        jsii.create(LambdaRestApi, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.RestApiProps", jsii_struct_bases=[ResourceOptions], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions', 'api_key_source_type': 'apiKeySourceType', 'binary_media_types': 'binaryMediaTypes', 'clone_from': 'cloneFrom', 'cloud_watch_role': 'cloudWatchRole', 'deploy': 'deploy', 'deploy_options': 'deployOptions', 'description': 'description', 'domain_name': 'domainName', 'endpoint_export_name': 'endpointExportName', 'endpoint_types': 'endpointTypes', 'fail_on_warnings': 'failOnWarnings', 'minimum_compression_size': 'minimumCompressionSize', 'parameters': 'parameters', 'policy': 'policy', 'rest_api_name': 'restApiName', 'retain_deployments': 'retainDeployments'})
class RestApiProps(ResourceOptions):
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, api_key_source_type: typing.Optional["ApiKeySourceType"]=None, binary_media_types: typing.Optional[typing.List[str]]=None, clone_from: typing.Optional["IRestApi"]=None, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, domain_name: typing.Optional["DomainNameOptions"]=None, endpoint_export_name: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None):
        """
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: true
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployStageOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the purpose of this API Gateway RestApi resource. Default: - No description.
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: - No endpoint types.
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param minimum_compression_size: A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        if isinstance(deploy_options, dict): deploy_options = StageOptions(**deploy_options)
        if isinstance(domain_name, dict): domain_name = DomainNameOptions(**domain_name)
        self._values = {
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options
        if api_key_source_type is not None: self._values["api_key_source_type"] = api_key_source_type
        if binary_media_types is not None: self._values["binary_media_types"] = binary_media_types
        if clone_from is not None: self._values["clone_from"] = clone_from
        if cloud_watch_role is not None: self._values["cloud_watch_role"] = cloud_watch_role
        if deploy is not None: self._values["deploy"] = deploy
        if deploy_options is not None: self._values["deploy_options"] = deploy_options
        if description is not None: self._values["description"] = description
        if domain_name is not None: self._values["domain_name"] = domain_name
        if endpoint_export_name is not None: self._values["endpoint_export_name"] = endpoint_export_name
        if endpoint_types is not None: self._values["endpoint_types"] = endpoint_types
        if fail_on_warnings is not None: self._values["fail_on_warnings"] = fail_on_warnings
        if minimum_compression_size is not None: self._values["minimum_compression_size"] = minimum_compression_size
        if parameters is not None: self._values["parameters"] = parameters
        if policy is not None: self._values["policy"] = policy
        if rest_api_name is not None: self._values["rest_api_name"] = rest_api_name
        if retain_deployments is not None: self._values["retain_deployments"] = retain_deployments

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    @builtins.property
    def api_key_source_type(self) -> typing.Optional["ApiKeySourceType"]:
        """The source of the API key for metering requests according to a usage plan.

        default
        :default: - Metering is disabled.
        """
        return self._values.get('api_key_source_type')

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[str]]:
        """The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream".

        default
        :default: - RestApi supports only UTF-8-encoded text payloads.
        """
        return self._values.get('binary_media_types')

    @builtins.property
    def clone_from(self) -> typing.Optional["IRestApi"]:
        """The ID of the API Gateway RestApi resource that you want to clone.

        default
        :default: - None.
        """
        return self._values.get('clone_from')

    @builtins.property
    def cloud_watch_role(self) -> typing.Optional[bool]:
        """Automatically configure an AWS CloudWatch role for API Gateway.

        default
        :default: true
        """
        return self._values.get('cloud_watch_role')

    @builtins.property
    def deploy(self) -> typing.Optional[bool]:
        """Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes.

        Since API Gateway deployments are immutable, When this option is enabled
        (by default), an AWS::ApiGateway::Deployment resource will automatically
        created with a logical ID that hashes the API model (methods, resources
        and options). This means that when the model changes, the logical ID of
        this CloudFormation resource will change, and a new deployment will be
        created.

        If this is set, ``latestDeployment`` will refer to the ``Deployment`` object
        and ``deploymentStage`` will refer to a ``Stage`` that points to this
        deployment. To customize the stage options, use the ``deployStageOptions``
        property.

        A CloudFormation Output will also be defined with the root URL endpoint
        of this REST API.

        default
        :default: true
        """
        return self._values.get('deploy')

    @builtins.property
    def deploy_options(self) -> typing.Optional["StageOptions"]:
        """Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled.

        If ``deploy`` is disabled,
        this value cannot be set.

        default
        :default: - Based on defaults of ``StageOptions``.
        """
        return self._values.get('deploy_options')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the purpose of this API Gateway RestApi resource.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def domain_name(self) -> typing.Optional["DomainNameOptions"]:
        """Configure a custom domain name and map it to this API.

        default
        :default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        """
        return self._values.get('domain_name')

    @builtins.property
    def endpoint_export_name(self) -> typing.Optional[str]:
        """Export name for the CfnOutput containing the API endpoint.

        default
        :default: - when no export name is given, output will be created without export
        """
        return self._values.get('endpoint_export_name')

    @builtins.property
    def endpoint_types(self) -> typing.Optional[typing.List["EndpointType"]]:
        """A list of the endpoint types of the API.

        Use this property when creating
        an API.

        default
        :default: - No endpoint types.
        """
        return self._values.get('endpoint_types')

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[bool]:
        """Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource.

        default
        :default: false
        """
        return self._values.get('fail_on_warnings')

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        """A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API.

        When compression is enabled, compression or
        decompression is not applied on the payload if the payload size is
        smaller than this value. Setting it to zero allows compression for any
        payload size.

        default
        :default: - Compression is disabled.
        """
        return self._values.get('minimum_compression_size')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom header parameters for the request.

        default
        :default: - No parameters.

        see
        :see: https://docs.aws.amazon.com/cli/latest/reference/apigateway/import-rest-api.html
        """
        return self._values.get('parameters')

    @builtins.property
    def policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        """A policy document that contains the permissions for this RestApi.

        default
        :default: - No policy.
        """
        return self._values.get('policy')

    @builtins.property
    def rest_api_name(self) -> typing.Optional[str]:
        """A name for the API Gateway RestApi resource.

        default
        :default: - ID of the RestApi construct.
        """
        return self._values.get('rest_api_name')

    @builtins.property
    def retain_deployments(self) -> typing.Optional[bool]:
        """Retains old deployment resources when the API changes.

        This allows
        manually reverting stages to point to old deployments via the AWS
        Console.

        default
        :default: false
        """
        return self._values.get('retain_deployments')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RestApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.LambdaRestApiProps", jsii_struct_bases=[RestApiProps], name_mapping={'default_cors_preflight_options': 'defaultCorsPreflightOptions', 'default_integration': 'defaultIntegration', 'default_method_options': 'defaultMethodOptions', 'api_key_source_type': 'apiKeySourceType', 'binary_media_types': 'binaryMediaTypes', 'clone_from': 'cloneFrom', 'cloud_watch_role': 'cloudWatchRole', 'deploy': 'deploy', 'deploy_options': 'deployOptions', 'description': 'description', 'domain_name': 'domainName', 'endpoint_export_name': 'endpointExportName', 'endpoint_types': 'endpointTypes', 'fail_on_warnings': 'failOnWarnings', 'minimum_compression_size': 'minimumCompressionSize', 'parameters': 'parameters', 'policy': 'policy', 'rest_api_name': 'restApiName', 'retain_deployments': 'retainDeployments', 'handler': 'handler', 'options': 'options', 'proxy': 'proxy'})
class LambdaRestApiProps(RestApiProps):
    def __init__(self, *, default_cors_preflight_options: typing.Optional["CorsOptions"]=None, default_integration: typing.Optional["Integration"]=None, default_method_options: typing.Optional["MethodOptions"]=None, api_key_source_type: typing.Optional["ApiKeySourceType"]=None, binary_media_types: typing.Optional[typing.List[str]]=None, clone_from: typing.Optional["IRestApi"]=None, cloud_watch_role: typing.Optional[bool]=None, deploy: typing.Optional[bool]=None, deploy_options: typing.Optional["StageOptions"]=None, description: typing.Optional[str]=None, domain_name: typing.Optional["DomainNameOptions"]=None, endpoint_export_name: typing.Optional[str]=None, endpoint_types: typing.Optional[typing.List["EndpointType"]]=None, fail_on_warnings: typing.Optional[bool]=None, minimum_compression_size: typing.Optional[jsii.Number]=None, parameters: typing.Optional[typing.Mapping[str,str]]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, rest_api_name: typing.Optional[str]=None, retain_deployments: typing.Optional[bool]=None, handler: aws_cdk.aws_lambda.IFunction, options: typing.Optional["RestApiProps"]=None, proxy: typing.Optional[bool]=None):
        """
        :param default_cors_preflight_options: Adds a CORS preflight OPTIONS method to this resource and all child resources. You can add CORS at the resource-level using ``addCorsPreflight``. Default: - CORS is disabled
        :param default_integration: An integration to use as a default for all methods created within this API unless an integration is specified. Default: - Inherited from parent.
        :param default_method_options: Method options to use as a default for all methods created within this API unless custom options are specified. Default: - Inherited from parent.
        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Default: - Metering is disabled.
        :param binary_media_types: The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream". Default: - RestApi supports only UTF-8-encoded text payloads.
        :param clone_from: The ID of the API Gateway RestApi resource that you want to clone. Default: - None.
        :param cloud_watch_role: Automatically configure an AWS CloudWatch role for API Gateway. Default: true
        :param deploy: Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes. Since API Gateway deployments are immutable, When this option is enabled (by default), an AWS::ApiGateway::Deployment resource will automatically created with a logical ID that hashes the API model (methods, resources and options). This means that when the model changes, the logical ID of this CloudFormation resource will change, and a new deployment will be created. If this is set, ``latestDeployment`` will refer to the ``Deployment`` object and ``deploymentStage`` will refer to a ``Stage`` that points to this deployment. To customize the stage options, use the ``deployStageOptions`` property. A CloudFormation Output will also be defined with the root URL endpoint of this REST API. Default: true
        :param deploy_options: Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled. If ``deploy`` is disabled, this value cannot be set. Default: - Based on defaults of ``StageOptions``.
        :param description: A description of the purpose of this API Gateway RestApi resource. Default: - No description.
        :param domain_name: Configure a custom domain name and map it to this API. Default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        :param endpoint_export_name: Export name for the CfnOutput containing the API endpoint. Default: - when no export name is given, output will be created without export
        :param endpoint_types: A list of the endpoint types of the API. Use this property when creating an API. Default: - No endpoint types.
        :param fail_on_warnings: Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource. Default: false
        :param minimum_compression_size: A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size. Default: - Compression is disabled.
        :param parameters: Custom header parameters for the request. Default: - No parameters.
        :param policy: A policy document that contains the permissions for this RestApi. Default: - No policy.
        :param rest_api_name: A name for the API Gateway RestApi resource. Default: - ID of the RestApi construct.
        :param retain_deployments: Retains old deployment resources when the API changes. This allows manually reverting stages to point to old deployments via the AWS Console. Default: false
        :param handler: The default Lambda function that handles all requests from this API. This handler will be used as a the default integration for all methods in this API, unless specified otherwise in ``addMethod``.
        :param options: Default: - no options.
        :param proxy: If true, route all requests to the Lambda Function. If set to false, you will need to explicitly define the API model using ``addResource`` and ``addMethod`` (or ``addProxy``). Default: true
        """
        if isinstance(default_cors_preflight_options, dict): default_cors_preflight_options = CorsOptions(**default_cors_preflight_options)
        if isinstance(default_method_options, dict): default_method_options = MethodOptions(**default_method_options)
        if isinstance(deploy_options, dict): deploy_options = StageOptions(**deploy_options)
        if isinstance(domain_name, dict): domain_name = DomainNameOptions(**domain_name)
        if isinstance(options, dict): options = RestApiProps(**options)
        self._values = {
            'handler': handler,
        }
        if default_cors_preflight_options is not None: self._values["default_cors_preflight_options"] = default_cors_preflight_options
        if default_integration is not None: self._values["default_integration"] = default_integration
        if default_method_options is not None: self._values["default_method_options"] = default_method_options
        if api_key_source_type is not None: self._values["api_key_source_type"] = api_key_source_type
        if binary_media_types is not None: self._values["binary_media_types"] = binary_media_types
        if clone_from is not None: self._values["clone_from"] = clone_from
        if cloud_watch_role is not None: self._values["cloud_watch_role"] = cloud_watch_role
        if deploy is not None: self._values["deploy"] = deploy
        if deploy_options is not None: self._values["deploy_options"] = deploy_options
        if description is not None: self._values["description"] = description
        if domain_name is not None: self._values["domain_name"] = domain_name
        if endpoint_export_name is not None: self._values["endpoint_export_name"] = endpoint_export_name
        if endpoint_types is not None: self._values["endpoint_types"] = endpoint_types
        if fail_on_warnings is not None: self._values["fail_on_warnings"] = fail_on_warnings
        if minimum_compression_size is not None: self._values["minimum_compression_size"] = minimum_compression_size
        if parameters is not None: self._values["parameters"] = parameters
        if policy is not None: self._values["policy"] = policy
        if rest_api_name is not None: self._values["rest_api_name"] = rest_api_name
        if retain_deployments is not None: self._values["retain_deployments"] = retain_deployments
        if options is not None: self._values["options"] = options
        if proxy is not None: self._values["proxy"] = proxy

    @builtins.property
    def default_cors_preflight_options(self) -> typing.Optional["CorsOptions"]:
        """Adds a CORS preflight OPTIONS method to this resource and all child resources.

        You can add CORS at the resource-level using ``addCorsPreflight``.

        default
        :default: - CORS is disabled
        """
        return self._values.get('default_cors_preflight_options')

    @builtins.property
    def default_integration(self) -> typing.Optional["Integration"]:
        """An integration to use as a default for all methods created within this API unless an integration is specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_integration')

    @builtins.property
    def default_method_options(self) -> typing.Optional["MethodOptions"]:
        """Method options to use as a default for all methods created within this API unless custom options are specified.

        default
        :default: - Inherited from parent.
        """
        return self._values.get('default_method_options')

    @builtins.property
    def api_key_source_type(self) -> typing.Optional["ApiKeySourceType"]:
        """The source of the API key for metering requests according to a usage plan.

        default
        :default: - Metering is disabled.
        """
        return self._values.get('api_key_source_type')

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[str]]:
        """The list of binary media mime-types that are supported by the RestApi resource, such as "image/png" or "application/octet-stream".

        default
        :default: - RestApi supports only UTF-8-encoded text payloads.
        """
        return self._values.get('binary_media_types')

    @builtins.property
    def clone_from(self) -> typing.Optional["IRestApi"]:
        """The ID of the API Gateway RestApi resource that you want to clone.

        default
        :default: - None.
        """
        return self._values.get('clone_from')

    @builtins.property
    def cloud_watch_role(self) -> typing.Optional[bool]:
        """Automatically configure an AWS CloudWatch role for API Gateway.

        default
        :default: true
        """
        return self._values.get('cloud_watch_role')

    @builtins.property
    def deploy(self) -> typing.Optional[bool]:
        """Indicates if a Deployment should be automatically created for this API, and recreated when the API model (resources, methods) changes.

        Since API Gateway deployments are immutable, When this option is enabled
        (by default), an AWS::ApiGateway::Deployment resource will automatically
        created with a logical ID that hashes the API model (methods, resources
        and options). This means that when the model changes, the logical ID of
        this CloudFormation resource will change, and a new deployment will be
        created.

        If this is set, ``latestDeployment`` will refer to the ``Deployment`` object
        and ``deploymentStage`` will refer to a ``Stage`` that points to this
        deployment. To customize the stage options, use the ``deployStageOptions``
        property.

        A CloudFormation Output will also be defined with the root URL endpoint
        of this REST API.

        default
        :default: true
        """
        return self._values.get('deploy')

    @builtins.property
    def deploy_options(self) -> typing.Optional["StageOptions"]:
        """Options for the API Gateway stage that will always point to the latest deployment when ``deploy`` is enabled.

        If ``deploy`` is disabled,
        this value cannot be set.

        default
        :default: - Based on defaults of ``StageOptions``.
        """
        return self._values.get('deploy_options')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the purpose of this API Gateway RestApi resource.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def domain_name(self) -> typing.Optional["DomainNameOptions"]:
        """Configure a custom domain name and map it to this API.

        default
        :default: - no domain name is defined, use ``addDomainName`` or directly define a ``DomainName``.
        """
        return self._values.get('domain_name')

    @builtins.property
    def endpoint_export_name(self) -> typing.Optional[str]:
        """Export name for the CfnOutput containing the API endpoint.

        default
        :default: - when no export name is given, output will be created without export
        """
        return self._values.get('endpoint_export_name')

    @builtins.property
    def endpoint_types(self) -> typing.Optional[typing.List["EndpointType"]]:
        """A list of the endpoint types of the API.

        Use this property when creating
        an API.

        default
        :default: - No endpoint types.
        """
        return self._values.get('endpoint_types')

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[bool]:
        """Indicates whether to roll back the resource if a warning occurs while API Gateway is creating the RestApi resource.

        default
        :default: false
        """
        return self._values.get('fail_on_warnings')

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        """A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (when undefined) on an API.

        When compression is enabled, compression or
        decompression is not applied on the payload if the payload size is
        smaller than this value. Setting it to zero allows compression for any
        payload size.

        default
        :default: - Compression is disabled.
        """
        return self._values.get('minimum_compression_size')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom header parameters for the request.

        default
        :default: - No parameters.

        see
        :see: https://docs.aws.amazon.com/cli/latest/reference/apigateway/import-rest-api.html
        """
        return self._values.get('parameters')

    @builtins.property
    def policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        """A policy document that contains the permissions for this RestApi.

        default
        :default: - No policy.
        """
        return self._values.get('policy')

    @builtins.property
    def rest_api_name(self) -> typing.Optional[str]:
        """A name for the API Gateway RestApi resource.

        default
        :default: - ID of the RestApi construct.
        """
        return self._values.get('rest_api_name')

    @builtins.property
    def retain_deployments(self) -> typing.Optional[bool]:
        """Retains old deployment resources when the API changes.

        This allows
        manually reverting stages to point to old deployments via the AWS
        Console.

        default
        :default: false
        """
        return self._values.get('retain_deployments')

    @builtins.property
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The default Lambda function that handles all requests from this API.

        This handler will be used as a the default integration for all methods in
        this API, unless specified otherwise in ``addMethod``.
        """
        return self._values.get('handler')

    @builtins.property
    def options(self) -> typing.Optional["RestApiProps"]:
        """
        default
        :default: - no options.

        deprecated
        :deprecated:

        the ``LambdaRestApiProps`` now extends ``RestApiProps``, so all
        options are just available here. Note that the options specified in
        ``options`` will be overridden by any props specified at the root level.

        stability
        :stability: deprecated
        """
        return self._values.get('options')

    @builtins.property
    def proxy(self) -> typing.Optional[bool]:
        """If true, route all requests to the Lambda Function.

        If set to false, you will need to explicitly define the API model using
        ``addResource`` and ``addMethod`` (or ``addProxy``).

        default
        :default: true
        """
        return self._values.get('proxy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaRestApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Stage(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.Stage"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deployment: "Deployment", cache_cluster_enabled: typing.Optional[bool]=None, cache_cluster_size: typing.Optional[str]=None, client_certificate_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_options: typing.Optional[typing.Mapping[str,"MethodDeploymentOptions"]]=None, stage_name: typing.Optional[str]=None, tracing_enabled: typing.Optional[bool]=None, variables: typing.Optional[typing.Mapping[str,str]]=None, cache_data_encrypted: typing.Optional[bool]=None, cache_ttl: typing.Optional[aws_cdk.core.Duration]=None, caching_enabled: typing.Optional[bool]=None, data_trace_enabled: typing.Optional[bool]=None, logging_level: typing.Optional["MethodLoggingLevel"]=None, metrics_enabled: typing.Optional[bool]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param deployment: The deployment that this stage points to [disable-awslint:ref-via-interface].
        :param cache_cluster_enabled: Indicates whether cache clustering is enabled for the stage. Default: - Disabled for the stage.
        :param cache_cluster_size: The stage's cache cluster size. Default: 0.5
        :param client_certificate_id: The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage. Default: - None.
        :param description: A description of the purpose of the stage. Default: - No description.
        :param documentation_version: The version identifier of the API documentation snapshot. Default: - No documentation version.
        :param method_options: Method deployment options for specific resources/methods. These will override common options defined in ``StageOptions#methodOptions``. Default: - Common options will be used.
        :param stage_name: The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI). Default: - "prod"
        :param tracing_enabled: Specifies whether Amazon X-Ray tracing is enabled for this method. Default: false
        :param variables: A map that defines the stage variables. Variable names must consist of alphanumeric characters, and the values must match the following regular expression: [A-Za-z0-9-._~:/?#&=,]+. Default: - No stage variables.
        :param cache_data_encrypted: Indicates whether the cached responses are encrypted. Default: false
        :param cache_ttl: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached. Default: Duration.minutes(5)
        :param caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached. Default: - Caching is Disabled.
        :param data_trace_enabled: Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: false
        :param logging_level: Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: - Off
        :param metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method. Default: false
        :param throttling_burst_limit: Specifies the throttling burst limit. The total rate of all requests in your AWS account is limited to 5,000 requests. Default: - No additional restriction.
        :param throttling_rate_limit: Specifies the throttling rate limit. The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps). Default: - No additional restriction.
        """
        props = StageProps(deployment=deployment, cache_cluster_enabled=cache_cluster_enabled, cache_cluster_size=cache_cluster_size, client_certificate_id=client_certificate_id, description=description, documentation_version=documentation_version, method_options=method_options, stage_name=stage_name, tracing_enabled=tracing_enabled, variables=variables, cache_data_encrypted=cache_data_encrypted, cache_ttl=cache_ttl, caching_enabled=caching_enabled, data_trace_enabled=data_trace_enabled, logging_level=logging_level, metrics_enabled=metrics_enabled, throttling_burst_limit=throttling_burst_limit, throttling_rate_limit=throttling_rate_limit)

        jsii.create(Stage, self, [scope, id, props])

    @jsii.member(jsii_name="urlForPath")
    def url_for_path(self, path: typing.Optional[str]=None) -> str:
        """Returns the invoke URL for a certain path.

        :param path: The resource path.
        """
        return jsii.invoke(self, "urlForPath", [path])

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> "IRestApi":
        return jsii.get(self, "restApi")

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "stageName")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.StageOptions", jsii_struct_bases=[MethodDeploymentOptions], name_mapping={'cache_data_encrypted': 'cacheDataEncrypted', 'cache_ttl': 'cacheTtl', 'caching_enabled': 'cachingEnabled', 'data_trace_enabled': 'dataTraceEnabled', 'logging_level': 'loggingLevel', 'metrics_enabled': 'metricsEnabled', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit', 'cache_cluster_enabled': 'cacheClusterEnabled', 'cache_cluster_size': 'cacheClusterSize', 'client_certificate_id': 'clientCertificateId', 'description': 'description', 'documentation_version': 'documentationVersion', 'method_options': 'methodOptions', 'stage_name': 'stageName', 'tracing_enabled': 'tracingEnabled', 'variables': 'variables'})
class StageOptions(MethodDeploymentOptions):
    def __init__(self, *, cache_data_encrypted: typing.Optional[bool]=None, cache_ttl: typing.Optional[aws_cdk.core.Duration]=None, caching_enabled: typing.Optional[bool]=None, data_trace_enabled: typing.Optional[bool]=None, logging_level: typing.Optional["MethodLoggingLevel"]=None, metrics_enabled: typing.Optional[bool]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None, cache_cluster_enabled: typing.Optional[bool]=None, cache_cluster_size: typing.Optional[str]=None, client_certificate_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_options: typing.Optional[typing.Mapping[str,"MethodDeploymentOptions"]]=None, stage_name: typing.Optional[str]=None, tracing_enabled: typing.Optional[bool]=None, variables: typing.Optional[typing.Mapping[str,str]]=None):
        """
        :param cache_data_encrypted: Indicates whether the cached responses are encrypted. Default: false
        :param cache_ttl: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached. Default: Duration.minutes(5)
        :param caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached. Default: - Caching is Disabled.
        :param data_trace_enabled: Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: false
        :param logging_level: Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: - Off
        :param metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method. Default: false
        :param throttling_burst_limit: Specifies the throttling burst limit. The total rate of all requests in your AWS account is limited to 5,000 requests. Default: - No additional restriction.
        :param throttling_rate_limit: Specifies the throttling rate limit. The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps). Default: - No additional restriction.
        :param cache_cluster_enabled: Indicates whether cache clustering is enabled for the stage. Default: - Disabled for the stage.
        :param cache_cluster_size: The stage's cache cluster size. Default: 0.5
        :param client_certificate_id: The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage. Default: - None.
        :param description: A description of the purpose of the stage. Default: - No description.
        :param documentation_version: The version identifier of the API documentation snapshot. Default: - No documentation version.
        :param method_options: Method deployment options for specific resources/methods. These will override common options defined in ``StageOptions#methodOptions``. Default: - Common options will be used.
        :param stage_name: The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI). Default: - "prod"
        :param tracing_enabled: Specifies whether Amazon X-Ray tracing is enabled for this method. Default: false
        :param variables: A map that defines the stage variables. Variable names must consist of alphanumeric characters, and the values must match the following regular expression: [A-Za-z0-9-._~:/?#&=,]+. Default: - No stage variables.
        """
        self._values = {
        }
        if cache_data_encrypted is not None: self._values["cache_data_encrypted"] = cache_data_encrypted
        if cache_ttl is not None: self._values["cache_ttl"] = cache_ttl
        if caching_enabled is not None: self._values["caching_enabled"] = caching_enabled
        if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
        if logging_level is not None: self._values["logging_level"] = logging_level
        if metrics_enabled is not None: self._values["metrics_enabled"] = metrics_enabled
        if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
        if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit
        if cache_cluster_enabled is not None: self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None: self._values["cache_cluster_size"] = cache_cluster_size
        if client_certificate_id is not None: self._values["client_certificate_id"] = client_certificate_id
        if description is not None: self._values["description"] = description
        if documentation_version is not None: self._values["documentation_version"] = documentation_version
        if method_options is not None: self._values["method_options"] = method_options
        if stage_name is not None: self._values["stage_name"] = stage_name
        if tracing_enabled is not None: self._values["tracing_enabled"] = tracing_enabled
        if variables is not None: self._values["variables"] = variables

    @builtins.property
    def cache_data_encrypted(self) -> typing.Optional[bool]:
        """Indicates whether the cached responses are encrypted.

        default
        :default: false
        """
        return self._values.get('cache_data_encrypted')

    @builtins.property
    def cache_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the time to live (TTL), in seconds, for cached responses.

        The
        higher the TTL, the longer the response will be cached.

        default
        :default: Duration.minutes(5)

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html
        """
        return self._values.get('cache_ttl')

    @builtins.property
    def caching_enabled(self) -> typing.Optional[bool]:
        """Specifies whether responses should be cached and returned for requests.

        A
        cache cluster must be enabled on the stage for responses to be cached.

        default
        :default: - Caching is Disabled.
        """
        return self._values.get('caching_enabled')

    @builtins.property
    def data_trace_enabled(self) -> typing.Optional[bool]:
        """Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: false
        """
        return self._values.get('data_trace_enabled')

    @builtins.property
    def logging_level(self) -> typing.Optional["MethodLoggingLevel"]:
        """Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: - Off
        """
        return self._values.get('logging_level')

    @builtins.property
    def metrics_enabled(self) -> typing.Optional[bool]:
        """Specifies whether Amazon CloudWatch metrics are enabled for this method.

        default
        :default: false
        """
        return self._values.get('metrics_enabled')

    @builtins.property
    def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
        """Specifies the throttling burst limit.

        The total rate of all requests in your AWS account is limited to 5,000 requests.

        default
        :default: - No additional restriction.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        return self._values.get('throttling_burst_limit')

    @builtins.property
    def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
        """Specifies the throttling rate limit.

        The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps).

        default
        :default: - No additional restriction.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        return self._values.get('throttling_rate_limit')

    @builtins.property
    def cache_cluster_enabled(self) -> typing.Optional[bool]:
        """Indicates whether cache clustering is enabled for the stage.

        default
        :default: - Disabled for the stage.
        """
        return self._values.get('cache_cluster_enabled')

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[str]:
        """The stage's cache cluster size.

        default
        :default: 0.5
        """
        return self._values.get('cache_cluster_size')

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[str]:
        """The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage.

        default
        :default: - None.
        """
        return self._values.get('client_certificate_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the purpose of the stage.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def documentation_version(self) -> typing.Optional[str]:
        """The version identifier of the API documentation snapshot.

        default
        :default: - No documentation version.
        """
        return self._values.get('documentation_version')

    @builtins.property
    def method_options(self) -> typing.Optional[typing.Mapping[str,"MethodDeploymentOptions"]]:
        """Method deployment options for specific resources/methods.

        These will
        override common options defined in ``StageOptions#methodOptions``.

        default
        :default: - Common options will be used.
        """
        return self._values.get('method_options')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI).

        default
        :default: - "prod"
        """
        return self._values.get('stage_name')

    @builtins.property
    def tracing_enabled(self) -> typing.Optional[bool]:
        """Specifies whether Amazon X-Ray tracing is enabled for this method.

        default
        :default: false
        """
        return self._values.get('tracing_enabled')

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A map that defines the stage variables.

        Variable names must consist of
        alphanumeric characters, and the values must match the following regular
        expression: [A-Za-z0-9-._~:/?#&=,]+.

        default
        :default: - No stage variables.
        """
        return self._values.get('variables')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.StageProps", jsii_struct_bases=[StageOptions], name_mapping={'cache_data_encrypted': 'cacheDataEncrypted', 'cache_ttl': 'cacheTtl', 'caching_enabled': 'cachingEnabled', 'data_trace_enabled': 'dataTraceEnabled', 'logging_level': 'loggingLevel', 'metrics_enabled': 'metricsEnabled', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit', 'cache_cluster_enabled': 'cacheClusterEnabled', 'cache_cluster_size': 'cacheClusterSize', 'client_certificate_id': 'clientCertificateId', 'description': 'description', 'documentation_version': 'documentationVersion', 'method_options': 'methodOptions', 'stage_name': 'stageName', 'tracing_enabled': 'tracingEnabled', 'variables': 'variables', 'deployment': 'deployment'})
class StageProps(StageOptions):
    def __init__(self, *, cache_data_encrypted: typing.Optional[bool]=None, cache_ttl: typing.Optional[aws_cdk.core.Duration]=None, caching_enabled: typing.Optional[bool]=None, data_trace_enabled: typing.Optional[bool]=None, logging_level: typing.Optional["MethodLoggingLevel"]=None, metrics_enabled: typing.Optional[bool]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None, cache_cluster_enabled: typing.Optional[bool]=None, cache_cluster_size: typing.Optional[str]=None, client_certificate_id: typing.Optional[str]=None, description: typing.Optional[str]=None, documentation_version: typing.Optional[str]=None, method_options: typing.Optional[typing.Mapping[str,"MethodDeploymentOptions"]]=None, stage_name: typing.Optional[str]=None, tracing_enabled: typing.Optional[bool]=None, variables: typing.Optional[typing.Mapping[str,str]]=None, deployment: "Deployment"):
        """
        :param cache_data_encrypted: Indicates whether the cached responses are encrypted. Default: false
        :param cache_ttl: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached. Default: Duration.minutes(5)
        :param caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached. Default: - Caching is Disabled.
        :param data_trace_enabled: Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: false
        :param logging_level: Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. Default: - Off
        :param metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method. Default: false
        :param throttling_burst_limit: Specifies the throttling burst limit. The total rate of all requests in your AWS account is limited to 5,000 requests. Default: - No additional restriction.
        :param throttling_rate_limit: Specifies the throttling rate limit. The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps). Default: - No additional restriction.
        :param cache_cluster_enabled: Indicates whether cache clustering is enabled for the stage. Default: - Disabled for the stage.
        :param cache_cluster_size: The stage's cache cluster size. Default: 0.5
        :param client_certificate_id: The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage. Default: - None.
        :param description: A description of the purpose of the stage. Default: - No description.
        :param documentation_version: The version identifier of the API documentation snapshot. Default: - No documentation version.
        :param method_options: Method deployment options for specific resources/methods. These will override common options defined in ``StageOptions#methodOptions``. Default: - Common options will be used.
        :param stage_name: The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI). Default: - "prod"
        :param tracing_enabled: Specifies whether Amazon X-Ray tracing is enabled for this method. Default: false
        :param variables: A map that defines the stage variables. Variable names must consist of alphanumeric characters, and the values must match the following regular expression: [A-Za-z0-9-._~:/?#&=,]+. Default: - No stage variables.
        :param deployment: The deployment that this stage points to [disable-awslint:ref-via-interface].
        """
        self._values = {
            'deployment': deployment,
        }
        if cache_data_encrypted is not None: self._values["cache_data_encrypted"] = cache_data_encrypted
        if cache_ttl is not None: self._values["cache_ttl"] = cache_ttl
        if caching_enabled is not None: self._values["caching_enabled"] = caching_enabled
        if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
        if logging_level is not None: self._values["logging_level"] = logging_level
        if metrics_enabled is not None: self._values["metrics_enabled"] = metrics_enabled
        if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
        if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit
        if cache_cluster_enabled is not None: self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None: self._values["cache_cluster_size"] = cache_cluster_size
        if client_certificate_id is not None: self._values["client_certificate_id"] = client_certificate_id
        if description is not None: self._values["description"] = description
        if documentation_version is not None: self._values["documentation_version"] = documentation_version
        if method_options is not None: self._values["method_options"] = method_options
        if stage_name is not None: self._values["stage_name"] = stage_name
        if tracing_enabled is not None: self._values["tracing_enabled"] = tracing_enabled
        if variables is not None: self._values["variables"] = variables

    @builtins.property
    def cache_data_encrypted(self) -> typing.Optional[bool]:
        """Indicates whether the cached responses are encrypted.

        default
        :default: false
        """
        return self._values.get('cache_data_encrypted')

    @builtins.property
    def cache_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the time to live (TTL), in seconds, for cached responses.

        The
        higher the TTL, the longer the response will be cached.

        default
        :default: Duration.minutes(5)

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html
        """
        return self._values.get('cache_ttl')

    @builtins.property
    def caching_enabled(self) -> typing.Optional[bool]:
        """Specifies whether responses should be cached and returned for requests.

        A
        cache cluster must be enabled on the stage for responses to be cached.

        default
        :default: - Caching is Disabled.
        """
        return self._values.get('caching_enabled')

    @builtins.property
    def data_trace_enabled(self) -> typing.Optional[bool]:
        """Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: false
        """
        return self._values.get('data_trace_enabled')

    @builtins.property
    def logging_level(self) -> typing.Optional["MethodLoggingLevel"]:
        """Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: - Off
        """
        return self._values.get('logging_level')

    @builtins.property
    def metrics_enabled(self) -> typing.Optional[bool]:
        """Specifies whether Amazon CloudWatch metrics are enabled for this method.

        default
        :default: false
        """
        return self._values.get('metrics_enabled')

    @builtins.property
    def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
        """Specifies the throttling burst limit.

        The total rate of all requests in your AWS account is limited to 5,000 requests.

        default
        :default: - No additional restriction.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        return self._values.get('throttling_burst_limit')

    @builtins.property
    def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
        """Specifies the throttling rate limit.

        The total rate of all requests in your AWS account is limited to 10,000 requests per second (rps).

        default
        :default: - No additional restriction.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        return self._values.get('throttling_rate_limit')

    @builtins.property
    def cache_cluster_enabled(self) -> typing.Optional[bool]:
        """Indicates whether cache clustering is enabled for the stage.

        default
        :default: - Disabled for the stage.
        """
        return self._values.get('cache_cluster_enabled')

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[str]:
        """The stage's cache cluster size.

        default
        :default: 0.5
        """
        return self._values.get('cache_cluster_size')

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[str]:
        """The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage.

        default
        :default: - None.
        """
        return self._values.get('client_certificate_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the purpose of the stage.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def documentation_version(self) -> typing.Optional[str]:
        """The version identifier of the API documentation snapshot.

        default
        :default: - No documentation version.
        """
        return self._values.get('documentation_version')

    @builtins.property
    def method_options(self) -> typing.Optional[typing.Mapping[str,"MethodDeploymentOptions"]]:
        """Method deployment options for specific resources/methods.

        These will
        override common options defined in ``StageOptions#methodOptions``.

        default
        :default: - Common options will be used.
        """
        return self._values.get('method_options')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """The name of the stage, which API Gateway uses as the first path segment in the invoked Uniform Resource Identifier (URI).

        default
        :default: - "prod"
        """
        return self._values.get('stage_name')

    @builtins.property
    def tracing_enabled(self) -> typing.Optional[bool]:
        """Specifies whether Amazon X-Ray tracing is enabled for this method.

        default
        :default: false
        """
        return self._values.get('tracing_enabled')

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A map that defines the stage variables.

        Variable names must consist of
        alphanumeric characters, and the values must match the following regular
        expression: [A-Za-z0-9-._~:/?#&=,]+.

        default
        :default: - No stage variables.
        """
        return self._values.get('variables')

    @builtins.property
    def deployment(self) -> "Deployment":
        """The deployment that this stage points to [disable-awslint:ref-via-interface]."""
        return self._values.get('deployment')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ThrottleSettings", jsii_struct_bases=[], name_mapping={'burst_limit': 'burstLimit', 'rate_limit': 'rateLimit'})
class ThrottleSettings():
    def __init__(self, *, burst_limit: typing.Optional[jsii.Number]=None, rate_limit: typing.Optional[jsii.Number]=None):
        """Container for defining throttling parameters to API stages or methods.

        :param burst_limit: The maximum API request rate limit over a time ranging from one to a few seconds. Default: none
        :param rate_limit: The API request steady-state rate limit (average requests per second over an extended period of time). Default: none

        link:
        :link:: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
        """
        self._values = {
        }
        if burst_limit is not None: self._values["burst_limit"] = burst_limit
        if rate_limit is not None: self._values["rate_limit"] = rate_limit

    @builtins.property
    def burst_limit(self) -> typing.Optional[jsii.Number]:
        """The maximum API request rate limit over a time ranging from one to a few seconds.

        default
        :default: none
        """
        return self._values.get('burst_limit')

    @builtins.property
    def rate_limit(self) -> typing.Optional[jsii.Number]:
        """The API request steady-state rate limit (average requests per second over an extended period of time).

        default
        :default: none
        """
        return self._values.get('rate_limit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ThrottleSettings(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.ThrottlingPerMethod", jsii_struct_bases=[], name_mapping={'method': 'method', 'throttle': 'throttle'})
class ThrottlingPerMethod():
    def __init__(self, *, method: "Method", throttle: "ThrottleSettings"):
        """Represents per-method throttling for a resource.

        :param method: [disable-awslint:ref-via-interface] The method for which you specify the throttling settings. Default: none
        :param throttle: Specifies the overall request rate (average requests per second) and burst capacity. Default: none
        """
        if isinstance(throttle, dict): throttle = ThrottleSettings(**throttle)
        self._values = {
            'method': method,
            'throttle': throttle,
        }

    @builtins.property
    def method(self) -> "Method":
        """[disable-awslint:ref-via-interface] The method for which you specify the throttling settings.

        default
        :default: none
        """
        return self._values.get('method')

    @builtins.property
    def throttle(self) -> "ThrottleSettings":
        """Specifies the overall request rate (average requests per second) and burst capacity.

        default
        :default: none
        """
        return self._values.get('throttle')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ThrottlingPerMethod(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IAuthorizer)
class TokenAuthorizer(Authorizer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.TokenAuthorizer"):
    """Token based lambda authorizer that recognizes the caller's identity as a bearer token, such as a JSON Web Token (JWT) or an OAuth token.

    Based on the token, authorization is performed by a lambda function.

    resource:
    :resource:: AWS::ApiGateway::Authorizer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, handler: aws_cdk.aws_lambda.IFunction, assume_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, authorizer_name: typing.Optional[str]=None, identity_source: typing.Optional[str]=None, results_cache_ttl: typing.Optional[aws_cdk.core.Duration]=None, validation_regex: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param handler: The handler for the authorizer lambda function. The handler must follow a very specific protocol on the input it receives and the output it needs to produce. API Gateway has documented the handler's input specification {@link https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-input.html | here} and output specification {@link https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html | here}.
        :param assume_role: An optional IAM role for APIGateway to assume before calling the Lambda-based authorizer. The IAM role must be assumable by 'apigateway.amazonaws.com'. Default: - A resource policy is added to the Lambda function allowing apigateway.amazonaws.com to invoke the function.
        :param authorizer_name: An optional human friendly name for the authorizer. Note that, this is not the primary identifier of the authorizer. Default: this.node.uniqueId
        :param identity_source: The request header mapping expression for the bearer token. This is typically passed as part of the header, in which case this should be ``method.request.header.Authorizer`` where Authorizer is the header containing the bearer token. Default: 'method.request.header.Authorization'
        :param results_cache_ttl: How long APIGateway should cache the results. Max 1 hour. Disable caching by setting this to 0. Default: Duration.minutes(5)
        :param validation_regex: An optional regex to be matched against the authorization token. When matched the authorizer lambda is invoked, otherwise a 401 Unauthorized is returned to the client. Default: - no regex filter will be applied.
        """
        props = TokenAuthorizerProps(handler=handler, assume_role=assume_role, authorizer_name=authorizer_name, identity_source=identity_source, results_cache_ttl=results_cache_ttl, validation_regex=validation_regex)

        jsii.create(TokenAuthorizer, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="authorizerArn")
    def authorizer_arn(self) -> str:
        """The ARN of the authorizer to be used in permission policies, such as IAM and resource-based grants."""
        return jsii.get(self, "authorizerArn")

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> str:
        """The id of the authorizer.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "authorizerId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.TokenAuthorizerProps", jsii_struct_bases=[], name_mapping={'handler': 'handler', 'assume_role': 'assumeRole', 'authorizer_name': 'authorizerName', 'identity_source': 'identitySource', 'results_cache_ttl': 'resultsCacheTtl', 'validation_regex': 'validationRegex'})
class TokenAuthorizerProps():
    def __init__(self, *, handler: aws_cdk.aws_lambda.IFunction, assume_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, authorizer_name: typing.Optional[str]=None, identity_source: typing.Optional[str]=None, results_cache_ttl: typing.Optional[aws_cdk.core.Duration]=None, validation_regex: typing.Optional[str]=None):
        """Properties for TokenAuthorizer.

        :param handler: The handler for the authorizer lambda function. The handler must follow a very specific protocol on the input it receives and the output it needs to produce. API Gateway has documented the handler's input specification {@link https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-input.html | here} and output specification {@link https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html | here}.
        :param assume_role: An optional IAM role for APIGateway to assume before calling the Lambda-based authorizer. The IAM role must be assumable by 'apigateway.amazonaws.com'. Default: - A resource policy is added to the Lambda function allowing apigateway.amazonaws.com to invoke the function.
        :param authorizer_name: An optional human friendly name for the authorizer. Note that, this is not the primary identifier of the authorizer. Default: this.node.uniqueId
        :param identity_source: The request header mapping expression for the bearer token. This is typically passed as part of the header, in which case this should be ``method.request.header.Authorizer`` where Authorizer is the header containing the bearer token. Default: 'method.request.header.Authorization'
        :param results_cache_ttl: How long APIGateway should cache the results. Max 1 hour. Disable caching by setting this to 0. Default: Duration.minutes(5)
        :param validation_regex: An optional regex to be matched against the authorization token. When matched the authorizer lambda is invoked, otherwise a 401 Unauthorized is returned to the client. Default: - no regex filter will be applied.
        """
        self._values = {
            'handler': handler,
        }
        if assume_role is not None: self._values["assume_role"] = assume_role
        if authorizer_name is not None: self._values["authorizer_name"] = authorizer_name
        if identity_source is not None: self._values["identity_source"] = identity_source
        if results_cache_ttl is not None: self._values["results_cache_ttl"] = results_cache_ttl
        if validation_regex is not None: self._values["validation_regex"] = validation_regex

    @builtins.property
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The handler for the authorizer lambda function.

        The handler must follow a very specific protocol on the input it receives and the output it needs to produce.
        API Gateway has documented the handler's input specification
        {@link https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-input.html | here} and output specification
        {@link https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html | here}.
        """
        return self._values.get('handler')

    @builtins.property
    def assume_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An optional IAM role for APIGateway to assume before calling the Lambda-based authorizer.

        The IAM role must be
        assumable by 'apigateway.amazonaws.com'.

        default
        :default: - A resource policy is added to the Lambda function allowing apigateway.amazonaws.com to invoke the function.
        """
        return self._values.get('assume_role')

    @builtins.property
    def authorizer_name(self) -> typing.Optional[str]:
        """An optional human friendly name for the authorizer.

        Note that, this is not the primary identifier of the authorizer.

        default
        :default: this.node.uniqueId
        """
        return self._values.get('authorizer_name')

    @builtins.property
    def identity_source(self) -> typing.Optional[str]:
        """The request header mapping expression for the bearer token.

        This is typically passed as part of the header, in which case
        this should be ``method.request.header.Authorizer`` where Authorizer is the header containing the bearer token.

        default
        :default: 'method.request.header.Authorization'

        see
        :see: https://docs.aws.amazon.com/apigateway/api-reference/link-relation/authorizer-create/#identitySource
        """
        return self._values.get('identity_source')

    @builtins.property
    def results_cache_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """How long APIGateway should cache the results.

        Max 1 hour.
        Disable caching by setting this to 0.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('results_cache_ttl')

    @builtins.property
    def validation_regex(self) -> typing.Optional[str]:
        """An optional regex to be matched against the authorization token.

        When matched the authorizer lambda is invoked,
        otherwise a 401 Unauthorized is returned to the client.

        default
        :default: - no regex filter will be applied.
        """
        return self._values.get('validation_regex')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TokenAuthorizerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class UsagePlan(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.UsagePlan"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key: typing.Optional["IApiKey"]=None, api_stages: typing.Optional[typing.List["UsagePlanPerApiStage"]]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, quota: typing.Optional["QuotaSettings"]=None, throttle: typing.Optional["ThrottleSettings"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param api_key: ApiKey to be associated with the usage plan. Default: none
        :param api_stages: API Stages to be associated which the usage plan. Default: none
        :param description: Represents usage plan purpose. Default: none
        :param name: Name for this usage plan. Default: none
        :param quota: Number of requests clients can make in a given time period. Default: none
        :param throttle: Overall throttle settings for the API. Default: none
        """
        props = UsagePlanProps(api_key=api_key, api_stages=api_stages, description=description, name=name, quota=quota, throttle=throttle)

        jsii.create(UsagePlan, self, [scope, id, props])

    @jsii.member(jsii_name="addApiKey")
    def add_api_key(self, api_key: "IApiKey") -> None:
        """Adds an ApiKey.

        :param api_key: -
        """
        return jsii.invoke(self, "addApiKey", [api_key])

    @jsii.member(jsii_name="addApiStage")
    def add_api_stage(self, *, api: typing.Optional["IRestApi"]=None, stage: typing.Optional["Stage"]=None, throttle: typing.Optional[typing.List["ThrottlingPerMethod"]]=None) -> None:
        """Adds an apiStage.

        :param api: Default: none
        :param stage: [disable-awslint:ref-via-interface]. Default: none
        :param throttle: Default: none
        """
        api_stage = UsagePlanPerApiStage(api=api, stage=stage, throttle=throttle)

        return jsii.invoke(self, "addApiStage", [api_stage])

    @builtins.property
    @jsii.member(jsii_name="usagePlanId")
    def usage_plan_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "usagePlanId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.UsagePlanPerApiStage", jsii_struct_bases=[], name_mapping={'api': 'api', 'stage': 'stage', 'throttle': 'throttle'})
class UsagePlanPerApiStage():
    def __init__(self, *, api: typing.Optional["IRestApi"]=None, stage: typing.Optional["Stage"]=None, throttle: typing.Optional[typing.List["ThrottlingPerMethod"]]=None):
        """Represents the API stages that a usage plan applies to.

        :param api: Default: none
        :param stage: [disable-awslint:ref-via-interface]. Default: none
        :param throttle: Default: none
        """
        self._values = {
        }
        if api is not None: self._values["api"] = api
        if stage is not None: self._values["stage"] = stage
        if throttle is not None: self._values["throttle"] = throttle

    @builtins.property
    def api(self) -> typing.Optional["IRestApi"]:
        """
        default
        :default: none
        """
        return self._values.get('api')

    @builtins.property
    def stage(self) -> typing.Optional["Stage"]:
        """[disable-awslint:ref-via-interface].

        default
        :default: none
        """
        return self._values.get('stage')

    @builtins.property
    def throttle(self) -> typing.Optional[typing.List["ThrottlingPerMethod"]]:
        """
        default
        :default: none
        """
        return self._values.get('throttle')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UsagePlanPerApiStage(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.UsagePlanProps", jsii_struct_bases=[], name_mapping={'api_key': 'apiKey', 'api_stages': 'apiStages', 'description': 'description', 'name': 'name', 'quota': 'quota', 'throttle': 'throttle'})
class UsagePlanProps():
    def __init__(self, *, api_key: typing.Optional["IApiKey"]=None, api_stages: typing.Optional[typing.List["UsagePlanPerApiStage"]]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, quota: typing.Optional["QuotaSettings"]=None, throttle: typing.Optional["ThrottleSettings"]=None):
        """
        :param api_key: ApiKey to be associated with the usage plan. Default: none
        :param api_stages: API Stages to be associated which the usage plan. Default: none
        :param description: Represents usage plan purpose. Default: none
        :param name: Name for this usage plan. Default: none
        :param quota: Number of requests clients can make in a given time period. Default: none
        :param throttle: Overall throttle settings for the API. Default: none
        """
        if isinstance(quota, dict): quota = QuotaSettings(**quota)
        if isinstance(throttle, dict): throttle = ThrottleSettings(**throttle)
        self._values = {
        }
        if api_key is not None: self._values["api_key"] = api_key
        if api_stages is not None: self._values["api_stages"] = api_stages
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name
        if quota is not None: self._values["quota"] = quota
        if throttle is not None: self._values["throttle"] = throttle

    @builtins.property
    def api_key(self) -> typing.Optional["IApiKey"]:
        """ApiKey to be associated with the usage plan.

        default
        :default: none
        """
        return self._values.get('api_key')

    @builtins.property
    def api_stages(self) -> typing.Optional[typing.List["UsagePlanPerApiStage"]]:
        """API Stages to be associated which the usage plan.

        default
        :default: none
        """
        return self._values.get('api_stages')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Represents usage plan purpose.

        default
        :default: none
        """
        return self._values.get('description')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """Name for this usage plan.

        default
        :default: none
        """
        return self._values.get('name')

    @builtins.property
    def quota(self) -> typing.Optional["QuotaSettings"]:
        """Number of requests clients can make in a given time period.

        default
        :default: none
        """
        return self._values.get('quota')

    @builtins.property
    def throttle(self) -> typing.Optional["ThrottleSettings"]:
        """Overall throttle settings for the API.

        default
        :default: none
        """
        return self._values.get('throttle')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UsagePlanProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class VpcLink(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigateway.VpcLink"):
    """Define a new VPC Link Specifies an API Gateway VPC link for a RestApi to access resources in an Amazon Virtual Private Cloud (VPC)."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancer]]=None, vpc_link_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param description: The description of the VPC link. Default: no description
        :param targets: The network load balancers of the VPC targeted by the VPC link. The network load balancers must be owned by the same AWS account of the API owner. Default: - no targets. Use ``addTargets`` to add targets
        :param vpc_link_name: The name used to label and identify the VPC link. Default: - automatically generated name
        """
        props = VpcLinkProps(description=description, targets=targets, vpc_link_name=vpc_link_name)

        jsii.create(VpcLink, self, [scope, id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, *targets: aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancer) -> None:
        """
        :param targets: -
        """
        return jsii.invoke(self, "addTargets", [*targets])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> str:
        """Physical ID of the VpcLink resource.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "vpcLinkId")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigateway.VpcLinkProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'targets': 'targets', 'vpc_link_name': 'vpcLinkName'})
class VpcLinkProps():
    def __init__(self, *, description: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancer]]=None, vpc_link_name: typing.Optional[str]=None):
        """Properties for a VpcLink.

        :param description: The description of the VPC link. Default: no description
        :param targets: The network load balancers of the VPC targeted by the VPC link. The network load balancers must be owned by the same AWS account of the API owner. Default: - no targets. Use ``addTargets`` to add targets
        :param vpc_link_name: The name used to label and identify the VPC link. Default: - automatically generated name
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if targets is not None: self._values["targets"] = targets
        if vpc_link_name is not None: self._values["vpc_link_name"] = vpc_link_name

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """The description of the VPC link.

        default
        :default: no description
        """
        return self._values.get('description')

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancer]]:
        """The network load balancers of the VPC targeted by the VPC link.

        The network load balancers must be owned by the same AWS account of the API owner.

        default
        :default: - no targets. Use ``addTargets`` to add targets
        """
        return self._values.get('targets')

    @builtins.property
    def vpc_link_name(self) -> typing.Optional[str]:
        """The name used to label and identify the VPC link.

        default
        :default: - automatically generated name
        """
        return self._values.get('vpc_link_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcLinkProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["ApiKey", "ApiKeyProps", "ApiKeySourceType", "AuthorizationType", "Authorizer", "AwsIntegration", "AwsIntegrationProps", "BasePathMapping", "BasePathMappingOptions", "BasePathMappingProps", "CfnAccount", "CfnAccountProps", "CfnApiKey", "CfnApiKeyProps", "CfnApiMappingV2", "CfnApiMappingV2Props", "CfnApiV2", "CfnApiV2Props", "CfnAuthorizer", "CfnAuthorizerProps", "CfnAuthorizerV2", "CfnAuthorizerV2Props", "CfnBasePathMapping", "CfnBasePathMappingProps", "CfnClientCertificate", "CfnClientCertificateProps", "CfnDeployment", "CfnDeploymentProps", "CfnDeploymentV2", "CfnDeploymentV2Props", "CfnDocumentationPart", "CfnDocumentationPartProps", "CfnDocumentationVersion", "CfnDocumentationVersionProps", "CfnDomainName", "CfnDomainNameProps", "CfnDomainNameV2", "CfnDomainNameV2Props", "CfnGatewayResponse", "CfnGatewayResponseProps", "CfnIntegrationResponseV2", "CfnIntegrationResponseV2Props", "CfnIntegrationV2", "CfnIntegrationV2Props", "CfnMethod", "CfnMethodProps", "CfnModel", "CfnModelProps", "CfnModelV2", "CfnModelV2Props", "CfnRequestValidator", "CfnRequestValidatorProps", "CfnResource", "CfnResourceProps", "CfnRestApi", "CfnRestApiProps", "CfnRouteResponseV2", "CfnRouteResponseV2Props", "CfnRouteV2", "CfnRouteV2Props", "CfnStage", "CfnStageProps", "CfnStageV2", "CfnStageV2Props", "CfnUsagePlan", "CfnUsagePlanKey", "CfnUsagePlanKeyProps", "CfnUsagePlanProps", "CfnVpcLink", "CfnVpcLinkProps", "ConnectionType", "ContentHandling", "Cors", "CorsOptions", "Deployment", "DeploymentProps", "DomainName", "DomainNameAttributes", "DomainNameOptions", "DomainNameProps", "EmptyModel", "EndpointType", "ErrorModel", "HttpIntegration", "HttpIntegrationProps", "IApiKey", "IAuthorizer", "IDomainName", "IModel", "IRequestValidator", "IResource", "IRestApi", "Integration", "IntegrationOptions", "IntegrationProps", "IntegrationResponse", "IntegrationType", "JsonSchema", "JsonSchemaType", "JsonSchemaVersion", "LambdaIntegration", "LambdaIntegrationOptions", "LambdaRestApi", "LambdaRestApiProps", "Method", "MethodDeploymentOptions", "MethodLoggingLevel", "MethodOptions", "MethodProps", "MethodResponse", "MockIntegration", "Model", "ModelOptions", "ModelProps", "PassthroughBehavior", "Period", "ProxyResource", "ProxyResourceOptions", "ProxyResourceProps", "QuotaSettings", "RequestValidator", "RequestValidatorOptions", "RequestValidatorProps", "Resource", "ResourceBase", "ResourceOptions", "ResourceProps", "RestApi", "RestApiProps", "Stage", "StageOptions", "StageProps", "ThrottleSettings", "ThrottlingPerMethod", "TokenAuthorizer", "TokenAuthorizerProps", "UsagePlan", "UsagePlanPerApiStage", "UsagePlanProps", "VpcLink", "VpcLinkProps", "__jsii_assembly__"]

publication.publish()
