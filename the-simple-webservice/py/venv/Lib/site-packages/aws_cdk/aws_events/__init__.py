"""
## Amazon CloudWatch Events Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Amazon CloudWatch Events delivers a near real-time stream of system events that
describe changes in AWS resources. For example, an AWS CodePipeline emits the
[State
Change](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#codepipeline_event_type)
event when the pipeline changes it's state.

* **Events**: An event indicates a change in your AWS environment. AWS resources
  can generate events when their state changes. For example, Amazon EC2
  generates an event when the state of an EC2 instance changes from pending to
  running, and Amazon EC2 Auto Scaling generates events when it launches or
  terminates instances. AWS CloudTrail publishes events when you make API calls.
  You can generate custom application-level events and publish them to
  CloudWatch Events. You can also set up scheduled events that are generated on
  a periodic basis. For a list of services that generate events, and sample
  events from each service, see [CloudWatch Events Event Examples From Each
  Supported
  Service](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html).
* **Targets**: A target processes events. Targets can include Amazon EC2
  instances, AWS Lambda functions, Kinesis streams, Amazon ECS tasks, Step
  Functions state machines, Amazon SNS topics, Amazon SQS queues, and built-in
  targets. A target receives events in JSON format.
* **Rules**: A rule matches incoming events and routes them to targets for
  processing. A single rule can route to multiple targets, all of which are
  processed in parallel. Rules are not processed in a particular order. This
  enables different parts of an organization to look for and process the events
  that are of interest to them. A rule can customize the JSON sent to the
  target, by passing only certain parts or by overwriting it with a constant.
* **EventBuses**: An event bus can receive events from your own custom applications
  or it can receive events from applications and services created by AWS SaaS partners.
  See [Creating an Event Bus](https://docs.aws.amazon.com/eventbridge/latest/userguide/create-event-bus.html).

## Rule

The `Rule` construct defines a CloudWatch events rule which monitors an
event based on an [event
pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html)
and invoke **event targets** when the pattern is matched against a triggered
event. Event targets are objects that implement the `IRuleTarget` interface.

Normally, you will use one of the `source.onXxx(name[, target[, options]]) -> Rule` methods on the event source to define an event rule associated with
the specific activity. You can targets either via props, or add targets using
`rule.addTarget`.

For example, to define an rule that triggers a CodeBuild project build when a
commit is pushed to the "master" branch of a CodeCommit repository:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
on_commit_rule = repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project),
    branches=["master"]
)
```

You can add additional targets, with optional [input
transformer](https://docs.aws.amazon.com/AmazonCloudWatchEvents/latest/APIReference/API_InputTransformer.html)
using `eventRule.addTarget(target[, input])`. For example, we can add a SNS
topic target which formats a human-readable message for the commit.

For example, this adds an SNS topic as a target:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
on_commit_rule.add_target(targets.SnsTopic(topic,
    message=events.RuleTargetInput.from_text(f"A commit was pushed to the repository {codecommit.ReferenceEvent.repositoryName} on branch {codecommit.ReferenceEvent.referenceName}")
))
```

## Scheduling

You can configure a Rule to run on a schedule (cron or rate).

The following example runs a task every day at 4am:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import EcsTask

ecs_task_target = EcsTask(cluster=cluster, task_definition=task_definition)

Rule(self, "ScheduleRule",
    schedule=Schedule.cron(minute="0", hour="4"),
    targets=[ecs_task_target]
)
```

More details in [ScheduledEvents](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html) documentation page.

## Event Targets

The `@aws-cdk/aws-events-targets` module includes classes that implement the `IRuleTarget`
interface for various AWS services.

The following targets are supported:

* `targets.CodeBuildProject`: Start an AWS CodeBuild build
* `targets.CodePipeline`: Start an AWS CodePipeline pipeline execution
* `targets.EcsTask`: Start a task on an Amazon ECS cluster
* `targets.LambdaFunction`: Invoke an AWS Lambda function
* `targets.SnsTopic`: Publish into an SNS topic
* `targets.SqsQueue`: Send a message to an Amazon SQS Queue
* `targets.SfnStateMachine`: Trigger an AWS Step Functions state machine
* `targets.AwsApi`: Make an AWS API call

### Cross-account targets

It's possible to have the source of the event and a target in separate AWS accounts:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import App, Stack
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codecommit as codecommit
import aws_cdk.aws_events_targets as targets

app = App()

stack1 = Stack(app, "Stack1", env=Environment(account=account1, region="us-east-1"))
repo = codecommit.Repository(stack1, "Repository")

stack2 = Stack(app, "Stack2", env=Environment(account=account2, region="us-east-1"))
project = codebuild.Project(stack2, "Project")

repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project)
)
```

In this situation, the CDK will wire the 2 accounts together:

* It will generate a rule in the source stack with the event bus of the target account as the target
* It will generate a rule in the target stack, with the provided target
* It will generate a separate stack that gives the source account permissions to publish events
  to the event bus of the target account in the given region,
  and make sure its deployed before the source stack

**Note**: while events can span multiple accounts, they *cannot* span different regions
(that is a CloudWatch, not CDK, limitation).

For more information, see the
[AWS documentation on cross-account events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEvents-CrossAccountEventDelivery.html).
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

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-events", "1.23.0", __name__, "aws-events@1.23.0.jsii.tgz")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEventBus(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnEventBus"):
    """A CloudFormation ``AWS::Events::EventBus``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html
    cloudformationResource:
    :cloudformationResource:: AWS::Events::EventBus
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, event_source_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Events::EventBus``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Events::EventBus.Name``.
        :param event_source_name: ``AWS::Events::EventBus.EventSourceName``.
        """
        props = CfnEventBusProps(name=name, event_source_name=event_source_name)

        jsii.create(CfnEventBus, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="attrPolicy")
    def attr_policy(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Policy
        """
        return jsii.get(self, "attrPolicy")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Events::EventBus.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[str]:
        """``AWS::Events::EventBus.EventSourceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return jsii.get(self, "eventSourceName")

    @event_source_name.setter
    def event_source_name(self, value: typing.Optional[str]):
        jsii.set(self, "eventSourceName", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEventBusPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy"):
    """A CloudFormation ``AWS::Events::EventBusPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::Events::EventBusPolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, action: str, principal: str, statement_id: str, condition: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConditionProperty"]]]=None, event_bus_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Events::EventBusPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: ``AWS::Events::EventBusPolicy.Action``.
        :param principal: ``AWS::Events::EventBusPolicy.Principal``.
        :param statement_id: ``AWS::Events::EventBusPolicy.StatementId``.
        :param condition: ``AWS::Events::EventBusPolicy.Condition``.
        :param event_bus_name: ``AWS::Events::EventBusPolicy.EventBusName``.
        """
        props = CfnEventBusPolicyProps(action=action, principal=principal, statement_id=statement_id, condition=condition, event_bus_name=event_bus_name)

        jsii.create(CfnEventBusPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="action")
    def action(self) -> str:
        """``AWS::Events::EventBusPolicy.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
        """
        return jsii.get(self, "action")

    @action.setter
    def action(self, value: str):
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> str:
        """``AWS::Events::EventBusPolicy.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
        """
        return jsii.get(self, "principal")

    @principal.setter
    def principal(self, value: str):
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="statementId")
    def statement_id(self) -> str:
        """``AWS::Events::EventBusPolicy.StatementId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
        """
        return jsii.get(self, "statementId")

    @statement_id.setter
    def statement_id(self, value: str):
        jsii.set(self, "statementId", value)

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConditionProperty"]]]:
        """``AWS::Events::EventBusPolicy.Condition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
        """
        return jsii.get(self, "condition")

    @condition.setter
    def condition(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConditionProperty"]]]):
        jsii.set(self, "condition", value)

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> typing.Optional[str]:
        """``AWS::Events::EventBusPolicy.EventBusName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-eventbusname
        """
        return jsii.get(self, "eventBusName")

    @event_bus_name.setter
    def event_bus_name(self, value: typing.Optional[str]):
        jsii.set(self, "eventBusName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy.ConditionProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'type': 'type', 'value': 'value'})
    class ConditionProperty():
        def __init__(self, *, key: typing.Optional[str]=None, type: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param key: ``CfnEventBusPolicy.ConditionProperty.Key``.
            :param type: ``CfnEventBusPolicy.ConditionProperty.Type``.
            :param value: ``CfnEventBusPolicy.ConditionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if type is not None: self._values["type"] = type
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnEventBusPolicy.ConditionProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-key
            """
            return self._values.get('key')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnEventBusPolicy.ConditionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnEventBusPolicy.ConditionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConditionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusPolicyProps", jsii_struct_bases=[], name_mapping={'action': 'action', 'principal': 'principal', 'statement_id': 'statementId', 'condition': 'condition', 'event_bus_name': 'eventBusName'})
class CfnEventBusPolicyProps():
    def __init__(self, *, action: str, principal: str, statement_id: str, condition: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnEventBusPolicy.ConditionProperty"]]]=None, event_bus_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Events::EventBusPolicy``.

        :param action: ``AWS::Events::EventBusPolicy.Action``.
        :param principal: ``AWS::Events::EventBusPolicy.Principal``.
        :param statement_id: ``AWS::Events::EventBusPolicy.StatementId``.
        :param condition: ``AWS::Events::EventBusPolicy.Condition``.
        :param event_bus_name: ``AWS::Events::EventBusPolicy.EventBusName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
        """
        self._values = {
            'action': action,
            'principal': principal,
            'statement_id': statement_id,
        }
        if condition is not None: self._values["condition"] = condition
        if event_bus_name is not None: self._values["event_bus_name"] = event_bus_name

    @builtins.property
    def action(self) -> str:
        """``AWS::Events::EventBusPolicy.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
        """
        return self._values.get('action')

    @builtins.property
    def principal(self) -> str:
        """``AWS::Events::EventBusPolicy.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
        """
        return self._values.get('principal')

    @builtins.property
    def statement_id(self) -> str:
        """``AWS::Events::EventBusPolicy.StatementId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
        """
        return self._values.get('statement_id')

    @builtins.property
    def condition(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnEventBusPolicy.ConditionProperty"]]]:
        """``AWS::Events::EventBusPolicy.Condition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
        """
        return self._values.get('condition')

    @builtins.property
    def event_bus_name(self) -> typing.Optional[str]:
        """``AWS::Events::EventBusPolicy.EventBusName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-eventbusname
        """
        return self._values.get('event_bus_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEventBusPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'event_source_name': 'eventSourceName'})
class CfnEventBusProps():
    def __init__(self, *, name: str, event_source_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Events::EventBus``.

        :param name: ``AWS::Events::EventBus.Name``.
        :param event_source_name: ``AWS::Events::EventBus.EventSourceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html
        """
        self._values = {
            'name': name,
        }
        if event_source_name is not None: self._values["event_source_name"] = event_source_name

    @builtins.property
    def name(self) -> str:
        """``AWS::Events::EventBus.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return self._values.get('name')

    @builtins.property
    def event_source_name(self) -> typing.Optional[str]:
        """``AWS::Events::EventBus.EventSourceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return self._values.get('event_source_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEventBusProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRule(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnRule"):
    """A CloudFormation ``AWS::Events::Rule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
    cloudformationResource:
    :cloudformationResource:: AWS::Events::Rule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, event_bus_name: typing.Optional[str]=None, event_pattern: typing.Any=None, name: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, state: typing.Optional[str]=None, targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Events::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Events::Rule.Description``.
        :param event_bus_name: ``AWS::Events::Rule.EventBusName``.
        :param event_pattern: ``AWS::Events::Rule.EventPattern``.
        :param name: ``AWS::Events::Rule.Name``.
        :param role_arn: ``AWS::Events::Rule.RoleArn``.
        :param schedule_expression: ``AWS::Events::Rule.ScheduleExpression``.
        :param state: ``AWS::Events::Rule.State``.
        :param targets: ``AWS::Events::Rule.Targets``.
        """
        props = CfnRuleProps(description=description, event_bus_name=event_bus_name, event_pattern=event_pattern, name=name, role_arn=role_arn, schedule_expression=schedule_expression, state=state, targets=targets)

        jsii.create(CfnRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> typing.Any:
        """``AWS::Events::Rule.EventPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
        """
        return jsii.get(self, "eventPattern")

    @event_pattern.setter
    def event_pattern(self, value: typing.Any):
        jsii.set(self, "eventPattern", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.EventBusName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventbusname
        """
        return jsii.get(self, "eventBusName")

    @event_bus_name.setter
    def event_bus_name(self, value: typing.Optional[str]):
        jsii.set(self, "eventBusName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]):
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.ScheduleExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
        """
        return jsii.get(self, "scheduleExpression")

    @schedule_expression.setter
    def schedule_expression(self, value: typing.Optional[str]):
        jsii.set(self, "scheduleExpression", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
        """
        return jsii.get(self, "state")

    @state.setter
    def state(self, value: typing.Optional[str]):
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetProperty"]]]]]:
        """``AWS::Events::Rule.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
        """
        return jsii.get(self, "targets")

    @targets.setter
    def targets(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TargetProperty"]]]]]):
        jsii.set(self, "targets", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.AwsVpcConfigurationProperty", jsii_struct_bases=[], name_mapping={'subnets': 'subnets', 'assign_public_ip': 'assignPublicIp', 'security_groups': 'securityGroups'})
    class AwsVpcConfigurationProperty():
        def __init__(self, *, subnets: typing.List[str], assign_public_ip: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None):
            """
            :param subnets: ``CfnRule.AwsVpcConfigurationProperty.Subnets``.
            :param assign_public_ip: ``CfnRule.AwsVpcConfigurationProperty.AssignPublicIp``.
            :param security_groups: ``CfnRule.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html
            """
            self._values = {
                'subnets': subnets,
            }
            if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None: self._values["security_groups"] = security_groups

        @builtins.property
        def subnets(self) -> typing.List[str]:
            """``CfnRule.AwsVpcConfigurationProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-subnets
            """
            return self._values.get('subnets')

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[str]:
            """``CfnRule.AwsVpcConfigurationProperty.AssignPublicIp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-assignpublicip
            """
            return self._values.get('assign_public_ip')

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnRule.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-securitygroups
            """
            return self._values.get('security_groups')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AwsVpcConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.BatchArrayPropertiesProperty", jsii_struct_bases=[], name_mapping={'size': 'size'})
    class BatchArrayPropertiesProperty():
        def __init__(self, *, size: typing.Optional[jsii.Number]=None):
            """
            :param size: ``CfnRule.BatchArrayPropertiesProperty.Size``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batcharrayproperties.html
            """
            self._values = {
            }
            if size is not None: self._values["size"] = size

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.BatchArrayPropertiesProperty.Size``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batcharrayproperties.html#cfn-events-rule-batcharrayproperties-size
            """
            return self._values.get('size')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BatchArrayPropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.BatchParametersProperty", jsii_struct_bases=[], name_mapping={'job_definition': 'jobDefinition', 'job_name': 'jobName', 'array_properties': 'arrayProperties', 'retry_strategy': 'retryStrategy'})
    class BatchParametersProperty():
        def __init__(self, *, job_definition: str, job_name: str, array_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.BatchArrayPropertiesProperty"]]]=None, retry_strategy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.BatchRetryStrategyProperty"]]]=None):
            """
            :param job_definition: ``CfnRule.BatchParametersProperty.JobDefinition``.
            :param job_name: ``CfnRule.BatchParametersProperty.JobName``.
            :param array_properties: ``CfnRule.BatchParametersProperty.ArrayProperties``.
            :param retry_strategy: ``CfnRule.BatchParametersProperty.RetryStrategy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html
            """
            self._values = {
                'job_definition': job_definition,
                'job_name': job_name,
            }
            if array_properties is not None: self._values["array_properties"] = array_properties
            if retry_strategy is not None: self._values["retry_strategy"] = retry_strategy

        @builtins.property
        def job_definition(self) -> str:
            """``CfnRule.BatchParametersProperty.JobDefinition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-jobdefinition
            """
            return self._values.get('job_definition')

        @builtins.property
        def job_name(self) -> str:
            """``CfnRule.BatchParametersProperty.JobName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-jobname
            """
            return self._values.get('job_name')

        @builtins.property
        def array_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.BatchArrayPropertiesProperty"]]]:
            """``CfnRule.BatchParametersProperty.ArrayProperties``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-arrayproperties
            """
            return self._values.get('array_properties')

        @builtins.property
        def retry_strategy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.BatchRetryStrategyProperty"]]]:
            """``CfnRule.BatchParametersProperty.RetryStrategy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-retrystrategy
            """
            return self._values.get('retry_strategy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BatchParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.BatchRetryStrategyProperty", jsii_struct_bases=[], name_mapping={'attempts': 'attempts'})
    class BatchRetryStrategyProperty():
        def __init__(self, *, attempts: typing.Optional[jsii.Number]=None):
            """
            :param attempts: ``CfnRule.BatchRetryStrategyProperty.Attempts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchretrystrategy.html
            """
            self._values = {
            }
            if attempts is not None: self._values["attempts"] = attempts

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.BatchRetryStrategyProperty.Attempts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchretrystrategy.html#cfn-events-rule-batchretrystrategy-attempts
            """
            return self._values.get('attempts')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BatchRetryStrategyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.EcsParametersProperty", jsii_struct_bases=[], name_mapping={'task_definition_arn': 'taskDefinitionArn', 'group': 'group', 'launch_type': 'launchType', 'network_configuration': 'networkConfiguration', 'platform_version': 'platformVersion', 'task_count': 'taskCount'})
    class EcsParametersProperty():
        def __init__(self, *, task_definition_arn: str, group: typing.Optional[str]=None, launch_type: typing.Optional[str]=None, network_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.NetworkConfigurationProperty"]]]=None, platform_version: typing.Optional[str]=None, task_count: typing.Optional[jsii.Number]=None):
            """
            :param task_definition_arn: ``CfnRule.EcsParametersProperty.TaskDefinitionArn``.
            :param group: ``CfnRule.EcsParametersProperty.Group``.
            :param launch_type: ``CfnRule.EcsParametersProperty.LaunchType``.
            :param network_configuration: ``CfnRule.EcsParametersProperty.NetworkConfiguration``.
            :param platform_version: ``CfnRule.EcsParametersProperty.PlatformVersion``.
            :param task_count: ``CfnRule.EcsParametersProperty.TaskCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html
            """
            self._values = {
                'task_definition_arn': task_definition_arn,
            }
            if group is not None: self._values["group"] = group
            if launch_type is not None: self._values["launch_type"] = launch_type
            if network_configuration is not None: self._values["network_configuration"] = network_configuration
            if platform_version is not None: self._values["platform_version"] = platform_version
            if task_count is not None: self._values["task_count"] = task_count

        @builtins.property
        def task_definition_arn(self) -> str:
            """``CfnRule.EcsParametersProperty.TaskDefinitionArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskdefinitionarn
            """
            return self._values.get('task_definition_arn')

        @builtins.property
        def group(self) -> typing.Optional[str]:
            """``CfnRule.EcsParametersProperty.Group``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-group
            """
            return self._values.get('group')

        @builtins.property
        def launch_type(self) -> typing.Optional[str]:
            """``CfnRule.EcsParametersProperty.LaunchType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-launchtype
            """
            return self._values.get('launch_type')

        @builtins.property
        def network_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.NetworkConfigurationProperty"]]]:
            """``CfnRule.EcsParametersProperty.NetworkConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-networkconfiguration
            """
            return self._values.get('network_configuration')

        @builtins.property
        def platform_version(self) -> typing.Optional[str]:
            """``CfnRule.EcsParametersProperty.PlatformVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-platformversion
            """
            return self._values.get('platform_version')

        @builtins.property
        def task_count(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.EcsParametersProperty.TaskCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskcount
            """
            return self._values.get('task_count')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EcsParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.InputTransformerProperty", jsii_struct_bases=[], name_mapping={'input_template': 'inputTemplate', 'input_paths_map': 'inputPathsMap'})
    class InputTransformerProperty():
        def __init__(self, *, input_template: str, input_paths_map: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None):
            """
            :param input_template: ``CfnRule.InputTransformerProperty.InputTemplate``.
            :param input_paths_map: ``CfnRule.InputTransformerProperty.InputPathsMap``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html
            """
            self._values = {
                'input_template': input_template,
            }
            if input_paths_map is not None: self._values["input_paths_map"] = input_paths_map

        @builtins.property
        def input_template(self) -> str:
            """``CfnRule.InputTransformerProperty.InputTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputtemplate
            """
            return self._values.get('input_template')

        @builtins.property
        def input_paths_map(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnRule.InputTransformerProperty.InputPathsMap``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputpathsmap
            """
            return self._values.get('input_paths_map')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InputTransformerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.KinesisParametersProperty", jsii_struct_bases=[], name_mapping={'partition_key_path': 'partitionKeyPath'})
    class KinesisParametersProperty():
        def __init__(self, *, partition_key_path: str):
            """
            :param partition_key_path: ``CfnRule.KinesisParametersProperty.PartitionKeyPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html
            """
            self._values = {
                'partition_key_path': partition_key_path,
            }

        @builtins.property
        def partition_key_path(self) -> str:
            """``CfnRule.KinesisParametersProperty.PartitionKeyPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html#cfn-events-rule-kinesisparameters-partitionkeypath
            """
            return self._values.get('partition_key_path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KinesisParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.NetworkConfigurationProperty", jsii_struct_bases=[], name_mapping={'aws_vpc_configuration': 'awsVpcConfiguration'})
    class NetworkConfigurationProperty():
        def __init__(self, *, aws_vpc_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.AwsVpcConfigurationProperty"]]]=None):
            """
            :param aws_vpc_configuration: ``CfnRule.NetworkConfigurationProperty.AwsVpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-networkconfiguration.html
            """
            self._values = {
            }
            if aws_vpc_configuration is not None: self._values["aws_vpc_configuration"] = aws_vpc_configuration

        @builtins.property
        def aws_vpc_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.AwsVpcConfigurationProperty"]]]:
            """``CfnRule.NetworkConfigurationProperty.AwsVpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-networkconfiguration.html#cfn-events-rule-networkconfiguration-awsvpcconfiguration
            """
            return self._values.get('aws_vpc_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NetworkConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandParametersProperty", jsii_struct_bases=[], name_mapping={'run_command_targets': 'runCommandTargets'})
    class RunCommandParametersProperty():
        def __init__(self, *, run_command_targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RunCommandTargetProperty"]]]):
            """
            :param run_command_targets: ``CfnRule.RunCommandParametersProperty.RunCommandTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html
            """
            self._values = {
                'run_command_targets': run_command_targets,
            }

        @builtins.property
        def run_command_targets(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RunCommandTargetProperty"]]]:
            """``CfnRule.RunCommandParametersProperty.RunCommandTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html#cfn-events-rule-runcommandparameters-runcommandtargets
            """
            return self._values.get('run_command_targets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RunCommandParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandTargetProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'values': 'values'})
    class RunCommandTargetProperty():
        def __init__(self, *, key: str, values: typing.List[str]):
            """
            :param key: ``CfnRule.RunCommandTargetProperty.Key``.
            :param values: ``CfnRule.RunCommandTargetProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html
            """
            self._values = {
                'key': key,
                'values': values,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnRule.RunCommandTargetProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-key
            """
            return self._values.get('key')

        @builtins.property
        def values(self) -> typing.List[str]:
            """``CfnRule.RunCommandTargetProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-values
            """
            return self._values.get('values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RunCommandTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.SqsParametersProperty", jsii_struct_bases=[], name_mapping={'message_group_id': 'messageGroupId'})
    class SqsParametersProperty():
        def __init__(self, *, message_group_id: str):
            """
            :param message_group_id: ``CfnRule.SqsParametersProperty.MessageGroupId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html
            """
            self._values = {
                'message_group_id': message_group_id,
            }

        @builtins.property
        def message_group_id(self) -> str:
            """``CfnRule.SqsParametersProperty.MessageGroupId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html#cfn-events-rule-sqsparameters-messagegroupid
            """
            return self._values.get('message_group_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SqsParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.TargetProperty", jsii_struct_bases=[], name_mapping={'arn': 'arn', 'id': 'id', 'batch_parameters': 'batchParameters', 'ecs_parameters': 'ecsParameters', 'input': 'input', 'input_path': 'inputPath', 'input_transformer': 'inputTransformer', 'kinesis_parameters': 'kinesisParameters', 'role_arn': 'roleArn', 'run_command_parameters': 'runCommandParameters', 'sqs_parameters': 'sqsParameters'})
    class TargetProperty():
        def __init__(self, *, arn: str, id: str, batch_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.BatchParametersProperty"]]]=None, ecs_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.EcsParametersProperty"]]]=None, input: typing.Optional[str]=None, input_path: typing.Optional[str]=None, input_transformer: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.InputTransformerProperty"]]]=None, kinesis_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.KinesisParametersProperty"]]]=None, role_arn: typing.Optional[str]=None, run_command_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.RunCommandParametersProperty"]]]=None, sqs_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.SqsParametersProperty"]]]=None):
            """
            :param arn: ``CfnRule.TargetProperty.Arn``.
            :param id: ``CfnRule.TargetProperty.Id``.
            :param batch_parameters: ``CfnRule.TargetProperty.BatchParameters``.
            :param ecs_parameters: ``CfnRule.TargetProperty.EcsParameters``.
            :param input: ``CfnRule.TargetProperty.Input``.
            :param input_path: ``CfnRule.TargetProperty.InputPath``.
            :param input_transformer: ``CfnRule.TargetProperty.InputTransformer``.
            :param kinesis_parameters: ``CfnRule.TargetProperty.KinesisParameters``.
            :param role_arn: ``CfnRule.TargetProperty.RoleArn``.
            :param run_command_parameters: ``CfnRule.TargetProperty.RunCommandParameters``.
            :param sqs_parameters: ``CfnRule.TargetProperty.SqsParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html
            """
            self._values = {
                'arn': arn,
                'id': id,
            }
            if batch_parameters is not None: self._values["batch_parameters"] = batch_parameters
            if ecs_parameters is not None: self._values["ecs_parameters"] = ecs_parameters
            if input is not None: self._values["input"] = input
            if input_path is not None: self._values["input_path"] = input_path
            if input_transformer is not None: self._values["input_transformer"] = input_transformer
            if kinesis_parameters is not None: self._values["kinesis_parameters"] = kinesis_parameters
            if role_arn is not None: self._values["role_arn"] = role_arn
            if run_command_parameters is not None: self._values["run_command_parameters"] = run_command_parameters
            if sqs_parameters is not None: self._values["sqs_parameters"] = sqs_parameters

        @builtins.property
        def arn(self) -> str:
            """``CfnRule.TargetProperty.Arn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-arn
            """
            return self._values.get('arn')

        @builtins.property
        def id(self) -> str:
            """``CfnRule.TargetProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-id
            """
            return self._values.get('id')

        @builtins.property
        def batch_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.BatchParametersProperty"]]]:
            """``CfnRule.TargetProperty.BatchParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-batchparameters
            """
            return self._values.get('batch_parameters')

        @builtins.property
        def ecs_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.EcsParametersProperty"]]]:
            """``CfnRule.TargetProperty.EcsParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-ecsparameters
            """
            return self._values.get('ecs_parameters')

        @builtins.property
        def input(self) -> typing.Optional[str]:
            """``CfnRule.TargetProperty.Input``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-input
            """
            return self._values.get('input')

        @builtins.property
        def input_path(self) -> typing.Optional[str]:
            """``CfnRule.TargetProperty.InputPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputpath
            """
            return self._values.get('input_path')

        @builtins.property
        def input_transformer(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.InputTransformerProperty"]]]:
            """``CfnRule.TargetProperty.InputTransformer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputtransformer
            """
            return self._values.get('input_transformer')

        @builtins.property
        def kinesis_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.KinesisParametersProperty"]]]:
            """``CfnRule.TargetProperty.KinesisParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-kinesisparameters
            """
            return self._values.get('kinesis_parameters')

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnRule.TargetProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def run_command_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.RunCommandParametersProperty"]]]:
            """``CfnRule.TargetProperty.RunCommandParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-runcommandparameters
            """
            return self._values.get('run_command_parameters')

        @builtins.property
        def sqs_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRule.SqsParametersProperty"]]]:
            """``CfnRule.TargetProperty.SqsParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-sqsparameters
            """
            return self._values.get('sqs_parameters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRuleProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'event_bus_name': 'eventBusName', 'event_pattern': 'eventPattern', 'name': 'name', 'role_arn': 'roleArn', 'schedule_expression': 'scheduleExpression', 'state': 'state', 'targets': 'targets'})
class CfnRuleProps():
    def __init__(self, *, description: typing.Optional[str]=None, event_bus_name: typing.Optional[str]=None, event_pattern: typing.Any=None, name: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, state: typing.Optional[str]=None, targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.TargetProperty"]]]]]=None):
        """Properties for defining a ``AWS::Events::Rule``.

        :param description: ``AWS::Events::Rule.Description``.
        :param event_bus_name: ``AWS::Events::Rule.EventBusName``.
        :param event_pattern: ``AWS::Events::Rule.EventPattern``.
        :param name: ``AWS::Events::Rule.Name``.
        :param role_arn: ``AWS::Events::Rule.RoleArn``.
        :param schedule_expression: ``AWS::Events::Rule.ScheduleExpression``.
        :param state: ``AWS::Events::Rule.State``.
        :param targets: ``AWS::Events::Rule.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if event_bus_name is not None: self._values["event_bus_name"] = event_bus_name
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if name is not None: self._values["name"] = name
        if role_arn is not None: self._values["role_arn"] = role_arn
        if schedule_expression is not None: self._values["schedule_expression"] = schedule_expression
        if state is not None: self._values["state"] = state
        if targets is not None: self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
        """
        return self._values.get('description')

    @builtins.property
    def event_bus_name(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.EventBusName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventbusname
        """
        return self._values.get('event_bus_name')

    @builtins.property
    def event_pattern(self) -> typing.Any:
        """``AWS::Events::Rule.EventPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
        """
        return self._values.get('event_pattern')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
        """
        return self._values.get('name')

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def schedule_expression(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.ScheduleExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
        """
        return self._values.get('schedule_expression')

    @builtins.property
    def state(self) -> typing.Optional[str]:
        """``AWS::Events::Rule.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
        """
        return self._values.get('state')

    @builtins.property
    def targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.TargetProperty"]]]]]:
        """``AWS::Events::Rule.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events.CronOptions", jsii_struct_bases=[], name_mapping={'day': 'day', 'hour': 'hour', 'minute': 'minute', 'month': 'month', 'week_day': 'weekDay', 'year': 'year'})
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


@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventBusAttributes", jsii_struct_bases=[], name_mapping={'event_bus_arn': 'eventBusArn', 'event_bus_name': 'eventBusName', 'event_bus_policy': 'eventBusPolicy', 'event_source_name': 'eventSourceName'})
class EventBusAttributes():
    def __init__(self, *, event_bus_arn: str, event_bus_name: str, event_bus_policy: str, event_source_name: typing.Optional[str]=None):
        """Interface with properties necessary to import a reusable EventBus.

        :param event_bus_arn: The ARN of this event bus resource.
        :param event_bus_name: The physical ID of this event bus resource.
        :param event_bus_policy: The JSON policy of this event bus resource.
        :param event_source_name: The partner event source to associate with this event bus resource. Default: - no partner event source
        """
        self._values = {
            'event_bus_arn': event_bus_arn,
            'event_bus_name': event_bus_name,
            'event_bus_policy': event_bus_policy,
        }
        if event_source_name is not None: self._values["event_source_name"] = event_source_name

    @builtins.property
    def event_bus_arn(self) -> str:
        """The ARN of this event bus resource.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        """
        return self._values.get('event_bus_arn')

    @builtins.property
    def event_bus_name(self) -> str:
        """The physical ID of this event bus resource.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return self._values.get('event_bus_name')

    @builtins.property
    def event_bus_policy(self) -> str:
        """The JSON policy of this event bus resource.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        """
        return self._values.get('event_bus_policy')

    @builtins.property
    def event_source_name(self) -> typing.Optional[str]:
        """The partner event source to associate with this event bus resource.

        default
        :default: - no partner event source

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return self._values.get('event_source_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventBusAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventBusProps", jsii_struct_bases=[], name_mapping={'event_bus_name': 'eventBusName', 'event_source_name': 'eventSourceName'})
class EventBusProps():
    def __init__(self, *, event_bus_name: typing.Optional[str]=None, event_source_name: typing.Optional[str]=None):
        """Properties to define an event bus.

        :param event_bus_name: The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this. Default: - automatically generated name
        :param event_source_name: The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this. Default: - no partner event source
        """
        self._values = {
        }
        if event_bus_name is not None: self._values["event_bus_name"] = event_bus_name
        if event_source_name is not None: self._values["event_source_name"] = event_source_name

    @builtins.property
    def event_bus_name(self) -> typing.Optional[str]:
        """The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this.

        default
        :default: - automatically generated name

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return self._values.get('event_bus_name')

    @builtins.property
    def event_source_name(self) -> typing.Optional[str]:
        """The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this.

        default
        :default: - no partner event source

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return self._values.get('event_source_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventBusProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IResolvable)
class EventField(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.EventField"):
    """Represents a field in the event pattern."""
    @jsii.member(jsii_name="fromPath")
    @builtins.classmethod
    def from_path(cls, path: str) -> str:
        """Extract a custom JSON path from the event.

        :param path: -
        """
        return jsii.sinvoke(cls, "fromPath", [path])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _ctx: aws_cdk.core.IResolveContext) -> typing.Any:
        """Produce the Token's value at resolution time.

        :param _ctx: -
        """
        return jsii.invoke(self, "resolve", [_ctx])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> str:
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.
        """
        return jsii.invoke(self, "toString", [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="account")
    def account(cls) -> str:
        """Extract the account from the event."""
        return jsii.sget(cls, "account")

    @jsii.python.classproperty
    @jsii.member(jsii_name="detailType")
    def detail_type(cls) -> str:
        """Extract the detail type from the event."""
        return jsii.sget(cls, "detailType")

    @jsii.python.classproperty
    @jsii.member(jsii_name="eventId")
    def event_id(cls) -> str:
        """Extract the event ID from the event."""
        return jsii.sget(cls, "eventId")

    @jsii.python.classproperty
    @jsii.member(jsii_name="region")
    def region(cls) -> str:
        """Extract the region from the event."""
        return jsii.sget(cls, "region")

    @jsii.python.classproperty
    @jsii.member(jsii_name="source")
    def source(cls) -> str:
        """Extract the source from the event."""
        return jsii.sget(cls, "source")

    @jsii.python.classproperty
    @jsii.member(jsii_name="time")
    def time(cls) -> str:
        """Extract the time from the event."""
        return jsii.sget(cls, "time")

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.
        """
        return jsii.get(self, "creationStack")

    @builtins.property
    @jsii.member(jsii_name="displayHint")
    def display_hint(self) -> str:
        return jsii.get(self, "displayHint")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        return jsii.get(self, "path")


@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventPattern", jsii_struct_bases=[], name_mapping={'account': 'account', 'detail': 'detail', 'detail_type': 'detailType', 'id': 'id', 'region': 'region', 'resources': 'resources', 'source': 'source', 'time': 'time', 'version': 'version'})
class EventPattern():
    def __init__(self, *, account: typing.Optional[typing.List[str]]=None, detail: typing.Optional[typing.Mapping[str,typing.Any]]=None, detail_type: typing.Optional[typing.List[str]]=None, id: typing.Optional[typing.List[str]]=None, region: typing.Optional[typing.List[str]]=None, resources: typing.Optional[typing.List[str]]=None, source: typing.Optional[typing.List[str]]=None, time: typing.Optional[typing.List[str]]=None, version: typing.Optional[typing.List[str]]=None):
        """Events in Amazon CloudWatch Events are represented as JSON objects. For more information about JSON objects, see RFC 7159.

        Rules use event patterns to select events and route them to targets. A
        pattern either matches an event or it doesn't. Event patterns are represented
        as JSON objects with a structure that is similar to that of events, for
        example:

        It is important to remember the following about event pattern matching:

        - For a pattern to match an event, the event must contain all the field names
          listed in the pattern. The field names must appear in the event with the
          same nesting structure.
        - Other fields of the event not mentioned in the pattern are ignored;
          effectively, there is a ``"*": "*"`` wildcard for fields not mentioned.
        - The matching is exact (character-by-character), without case-folding or any
          other string normalization.
        - The values being matched follow JSON rules: Strings enclosed in quotes,
          numbers, and the unquoted keywords true, false, and null.
        - Number matching is at the string representation level. For example, 300,
          300.0, and 3.0e2 are not considered equal.

        :param account: The 12-digit number identifying an AWS account. Default: - No filtering on account
        :param detail: A JSON object, whose content is at the discretion of the service originating the event. Default: - No filtering on detail
        :param detail_type: Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field. Default: - No filtering on detail type
        :param id: A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed. Default: - No filtering on id
        :param region: Identifies the AWS region where the event originated. Default: - No filtering on region
        :param resources: This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs. Default: - No filtering on resource
        :param source: Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront. Default: - No filtering on source
        :param time: The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received. Default: - No filtering on time
        :param version: By default, this is set to 0 (zero) in all events. Default: - No filtering on version

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
        """
        self._values = {
        }
        if account is not None: self._values["account"] = account
        if detail is not None: self._values["detail"] = detail
        if detail_type is not None: self._values["detail_type"] = detail_type
        if id is not None: self._values["id"] = id
        if region is not None: self._values["region"] = region
        if resources is not None: self._values["resources"] = resources
        if source is not None: self._values["source"] = source
        if time is not None: self._values["time"] = time
        if version is not None: self._values["version"] = version

    @builtins.property
    def account(self) -> typing.Optional[typing.List[str]]:
        """The 12-digit number identifying an AWS account.

        default
        :default: - No filtering on account
        """
        return self._values.get('account')

    @builtins.property
    def detail(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """A JSON object, whose content is at the discretion of the service originating the event.

        default
        :default: - No filtering on detail
        """
        return self._values.get('detail')

    @builtins.property
    def detail_type(self) -> typing.Optional[typing.List[str]]:
        """Identifies, in combination with the source field, the fields and values that appear in the detail field.

        Represents the "detail-type" event field.

        default
        :default: - No filtering on detail type
        """
        return self._values.get('detail_type')

    @builtins.property
    def id(self) -> typing.Optional[typing.List[str]]:
        """A unique value is generated for every event.

        This can be helpful in
        tracing events as they move through rules to targets, and are processed.

        default
        :default: - No filtering on id
        """
        return self._values.get('id')

    @builtins.property
    def region(self) -> typing.Optional[typing.List[str]]:
        """Identifies the AWS region where the event originated.

        default
        :default: - No filtering on region
        """
        return self._values.get('region')

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[str]]:
        """This JSON array contains ARNs that identify resources that are involved in the event.

        Inclusion of these ARNs is at the discretion of the
        service.

        For example, Amazon EC2 instance state-changes include Amazon EC2
        instance ARNs, Auto Scaling events include ARNs for both instances and
        Auto Scaling groups, but API calls with AWS CloudTrail do not include
        resource ARNs.

        default
        :default: - No filtering on resource
        """
        return self._values.get('resources')

    @builtins.property
    def source(self) -> typing.Optional[typing.List[str]]:
        """Identifies the service that sourced the event.

        All events sourced from
        within AWS begin with "aws." Customer-generated events can have any value
        here, as long as it doesn't begin with "aws." We recommend the use of
        Java package-name style reverse domain-name strings.

        To find the correct value for source for an AWS service, see the table in
        AWS Service Namespaces. For example, the source value for Amazon
        CloudFront is aws.cloudfront.

        default
        :default: - No filtering on source

        see
        :see: http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces
        """
        return self._values.get('source')

    @builtins.property
    def time(self) -> typing.Optional[typing.List[str]]:
        """The event timestamp, which can be specified by the service originating the event.

        If the event spans a time interval, the service might choose
        to report the start time, so this value can be noticeably before the time
        the event is actually received.

        default
        :default: - No filtering on time
        """
        return self._values.get('time')

    @builtins.property
    def version(self) -> typing.Optional[typing.List[str]]:
        """By default, this is set to 0 (zero) in all events.

        default
        :default: - No filtering on version
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventPattern(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-events.IEventBus")
class IEventBus(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Interface which all EventBus based classes MUST implement."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEventBusProxy

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> str:
        """The ARN of this event bus resource.

        attribute:
        :attribute:: true
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> str:
        """The physical ID of this event bus resource.

        attribute:
        :attribute:: true
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> str:
        """The JSON policy of this event bus resource.

        attribute:
        :attribute:: true
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[str]:
        """The partner event source to associate with this event bus resource.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        ...


class _IEventBusProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Interface which all EventBus based classes MUST implement."""
    __jsii_type__ = "@aws-cdk/aws-events.IEventBus"
    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> str:
        """The ARN of this event bus resource.

        attribute:
        :attribute:: true
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        """
        return jsii.get(self, "eventBusArn")

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> str:
        """The physical ID of this event bus resource.

        attribute:
        :attribute:: true
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return jsii.get(self, "eventBusName")

    @builtins.property
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> str:
        """The JSON policy of this event bus resource.

        attribute:
        :attribute:: true
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        """
        return jsii.get(self, "eventBusPolicy")

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[str]:
        """The partner event source to associate with this event bus resource.

        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return jsii.get(self, "eventSourceName")


@jsii.implements(IEventBus)
class EventBus(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.EventBus"):
    """Define a CloudWatch EventBus.

    resource:
    :resource:: AWS::Events::EventBus
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, event_bus_name: typing.Optional[str]=None, event_source_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param event_bus_name: The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this. Default: - automatically generated name
        :param event_source_name: The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this. Default: - no partner event source
        """
        props = EventBusProps(event_bus_name=event_bus_name, event_source_name=event_source_name)

        jsii.create(EventBus, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventBusArn")
    @builtins.classmethod
    def from_event_bus_arn(cls, scope: aws_cdk.core.Construct, id: str, event_bus_arn: str) -> "IEventBus":
        """Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_arn: ARN of imported event bus.
        """
        return jsii.sinvoke(cls, "fromEventBusArn", [scope, id, event_bus_arn])

    @jsii.member(jsii_name="fromEventBusAttributes")
    @builtins.classmethod
    def from_event_bus_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, event_bus_arn: str, event_bus_name: str, event_bus_policy: str, event_source_name: typing.Optional[str]=None) -> "IEventBus":
        """Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_arn: The ARN of this event bus resource.
        :param event_bus_name: The physical ID of this event bus resource.
        :param event_bus_policy: The JSON policy of this event bus resource.
        :param event_source_name: The partner event source to associate with this event bus resource. Default: - no partner event source
        """
        attrs = EventBusAttributes(event_bus_arn=event_bus_arn, event_bus_name=event_bus_name, event_bus_policy=event_bus_policy, event_source_name=event_source_name)

        return jsii.sinvoke(cls, "fromEventBusAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="grantPutEvents")
    @builtins.classmethod
    def grant_put_events(cls, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM Principal to send custom events to EventBridge so that they can be matched to rules.

        :param grantee: The principal (no-op if undefined).
        """
        return jsii.sinvoke(cls, "grantPutEvents", [grantee])

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> str:
        """The ARN of the event bus, such as: arn:aws:events:us-east-2:123456789012:event-bus/aws.partner/PartnerName/acct1/repo1."""
        return jsii.get(self, "eventBusArn")

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> str:
        """The physical ID of this event bus resource."""
        return jsii.get(self, "eventBusName")

    @builtins.property
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> str:
        """The policy for the event bus in JSON form."""
        return jsii.get(self, "eventBusPolicy")

    @builtins.property
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[str]:
        """The name of the partner event source."""
        return jsii.get(self, "eventSourceName")


@jsii.interface(jsii_type="@aws-cdk/aws-events.IRule")
class IRule(aws_cdk.core.IResource, jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRuleProxy

    @builtins.property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> str:
        """The name event rule.

        attribute:
        :attribute:: true
        """
        ...


class _IRuleProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-events.IRule"
    @builtins.property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "ruleArn")

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> str:
        """The name event rule.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "ruleName")


@jsii.interface(jsii_type="@aws-cdk/aws-events.IRuleTarget")
class IRuleTarget(jsii.compat.Protocol):
    """An abstract target for EventRules."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRuleTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(self, rule: "IRule", id: typing.Optional[str]=None) -> "RuleTargetConfig":
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: The CloudWatch Event Rule that would trigger this target.
        :param id: The id of the target that will be attached to the rule.
        """
        ...


class _IRuleTargetProxy():
    """An abstract target for EventRules."""
    __jsii_type__ = "@aws-cdk/aws-events.IRuleTarget"
    @jsii.member(jsii_name="bind")
    def bind(self, rule: "IRule", id: typing.Optional[str]=None) -> "RuleTargetConfig":
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: The CloudWatch Event Rule that would trigger this target.
        :param id: The id of the target that will be attached to the rule.
        """
        return jsii.invoke(self, "bind", [rule, id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events.OnEventOptions", jsii_struct_bases=[], name_mapping={'description': 'description', 'event_pattern': 'eventPattern', 'rule_name': 'ruleName', 'target': 'target'})
class OnEventOptions():
    def __init__(self, *, description: typing.Optional[str]=None, event_pattern: typing.Optional["EventPattern"]=None, rule_name: typing.Optional[str]=None, target: typing.Optional["IRuleTarget"]=None):
        """Standard set of options for ``onXxx`` event handlers on construct.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        if isinstance(event_pattern, dict): event_pattern = EventPattern(**event_pattern)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if rule_name is not None: self._values["rule_name"] = rule_name
        if target is not None: self._values["target"] = target

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the rule's purpose.

        default
        :default: - No description
        """
        return self._values.get('description')

    @builtins.property
    def event_pattern(self) -> typing.Optional["EventPattern"]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        default
        :default: - No additional filtering based on an event pattern.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CloudWatchEventsandEventPatterns.html
        """
        return self._values.get('event_pattern')

    @builtins.property
    def rule_name(self) -> typing.Optional[str]:
        """A name for the rule.

        default
        :default: AWS CloudFormation generates a unique physical ID.
        """
        return self._values.get('rule_name')

    @builtins.property
    def target(self) -> typing.Optional["IRuleTarget"]:
        """The target to register for the event.

        default
        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OnEventOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IRule)
class Rule(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.Rule"):
    """Defines a CloudWatch Event Rule in this stack.

    resource:
    :resource:: AWS::Events::Rule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional["IEventBus"]=None, event_pattern: typing.Optional["EventPattern"]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional["Schedule"]=None, targets: typing.Optional[typing.List["IRuleTarget"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        props = RuleProps(description=description, enabled=enabled, event_bus=event_bus, event_pattern=event_pattern, rule_name=rule_name, schedule=schedule, targets=targets)

        jsii.create(Rule, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventRuleArn")
    @builtins.classmethod
    def from_event_rule_arn(cls, scope: aws_cdk.core.Construct, id: str, event_rule_arn: str) -> "IRule":
        """
        :param scope: -
        :param id: -
        :param event_rule_arn: -
        """
        return jsii.sinvoke(cls, "fromEventRuleArn", [scope, id, event_rule_arn])

    @jsii.member(jsii_name="addEventPattern")
    def add_event_pattern(self, *, account: typing.Optional[typing.List[str]]=None, detail: typing.Optional[typing.Mapping[str,typing.Any]]=None, detail_type: typing.Optional[typing.List[str]]=None, id: typing.Optional[typing.List[str]]=None, region: typing.Optional[typing.List[str]]=None, resources: typing.Optional[typing.List[str]]=None, source: typing.Optional[typing.List[str]]=None, time: typing.Optional[typing.List[str]]=None, version: typing.Optional[typing.List[str]]=None) -> None:
        """Adds an event pattern filter to this rule.

        If a pattern was already specified,
        these values are merged into the existing pattern.

        For example, if the rule already contains the pattern::

           {
             "resources": [ "r1" ],
             "detail": {
               "hello": [ 1 ]
             }
           }

        And ``addEventPattern`` is called with the pattern::

           {
             "resources": [ "r2" ],
             "detail": {
               "foo": [ "bar" ]
             }
           }

        The resulting event pattern will be::

           {
             "resources": [ "r1", "r2" ],
             "detail": {
               "hello": [ 1 ],
               "foo": [ "bar" ]
             }
           }

        :param account: The 12-digit number identifying an AWS account. Default: - No filtering on account
        :param detail: A JSON object, whose content is at the discretion of the service originating the event. Default: - No filtering on detail
        :param detail_type: Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field. Default: - No filtering on detail type
        :param id: A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed. Default: - No filtering on id
        :param region: Identifies the AWS region where the event originated. Default: - No filtering on region
        :param resources: This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs. Default: - No filtering on resource
        :param source: Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront. Default: - No filtering on source
        :param time: The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received. Default: - No filtering on time
        :param version: By default, this is set to 0 (zero) in all events. Default: - No filtering on version
        """
        event_pattern = EventPattern(account=account, detail=detail, detail_type=detail_type, id=id, region=region, resources=resources, source=source, time=time, version=version)

        return jsii.invoke(self, "addEventPattern", [event_pattern])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: typing.Optional["IRuleTarget"]=None) -> None:
        """Adds a target to the rule. The abstract class RuleTarget can be extended to define new targets.

        No-op if target is undefined.

        :param target: -
        """
        return jsii.invoke(self, "addTarget", [target])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example."""
        return jsii.get(self, "ruleArn")

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> str:
        """The name event rule."""
        return jsii.get(self, "ruleName")


@jsii.data_type(jsii_type="@aws-cdk/aws-events.RuleProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'enabled': 'enabled', 'event_bus': 'eventBus', 'event_pattern': 'eventPattern', 'rule_name': 'ruleName', 'schedule': 'schedule', 'targets': 'targets'})
class RuleProps():
    def __init__(self, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional["IEventBus"]=None, event_pattern: typing.Optional["EventPattern"]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional["Schedule"]=None, targets: typing.Optional[typing.List["IRuleTarget"]]=None):
        """
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        if isinstance(event_pattern, dict): event_pattern = EventPattern(**event_pattern)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if enabled is not None: self._values["enabled"] = enabled
        if event_bus is not None: self._values["event_bus"] = event_bus
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if rule_name is not None: self._values["rule_name"] = rule_name
        if schedule is not None: self._values["schedule"] = schedule
        if targets is not None: self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the rule's purpose.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """Indicates whether the rule is enabled.

        default
        :default: true
        """
        return self._values.get('enabled')

    @builtins.property
    def event_bus(self) -> typing.Optional["IEventBus"]:
        """The event bus to associate with this rule.

        default
        :default: - The default event bus.
        """
        return self._values.get('event_bus')

    @builtins.property
    def event_pattern(self) -> typing.Optional["EventPattern"]:
        """Describes which events CloudWatch Events routes to the specified target.

        These routed events are matched events. For more information, see Events
        and Event Patterns in the Amazon CloudWatch User Guide.

        default
        :default: - None.

        see
        :see:

        http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CloudWatchEventsandEventPatterns.html

        You must specify this property (either via props or via
        ``addEventPattern``), the ``scheduleExpression`` property, or both. The
        method ``addEventPattern`` can be used to add filter values to the event
        pattern.
        """
        return self._values.get('event_pattern')

    @builtins.property
    def rule_name(self) -> typing.Optional[str]:
        """A name for the rule.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
          for the rule name. For more information, see Name Type.
        """
        return self._values.get('rule_name')

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon CloudWatch User Guide.

        default
        :default: - None.

        see
        :see:

        http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html

        You must specify this property, the ``eventPattern`` property, or both.
        """
        return self._values.get('schedule')

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["IRuleTarget"]]:
        """Targets to invoke when this rule matches an event.

        Input will be the full matched event. If you wish to specify custom
        target input, use ``addTarget(target[, inputOptions])``.

        default
        :default: - No targets.
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-events.RuleTargetConfig", jsii_struct_bases=[], name_mapping={'arn': 'arn', 'id': 'id', 'ecs_parameters': 'ecsParameters', 'input': 'input', 'kinesis_parameters': 'kinesisParameters', 'role': 'role', 'run_command_parameters': 'runCommandParameters', 'sqs_parameters': 'sqsParameters', 'target_resource': 'targetResource'})
class RuleTargetConfig():
    def __init__(self, *, arn: str, id: str, ecs_parameters: typing.Optional["CfnRule.EcsParametersProperty"]=None, input: typing.Optional["RuleTargetInput"]=None, kinesis_parameters: typing.Optional["CfnRule.KinesisParametersProperty"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, run_command_parameters: typing.Optional["CfnRule.RunCommandParametersProperty"]=None, sqs_parameters: typing.Optional["CfnRule.SqsParametersProperty"]=None, target_resource: typing.Optional[aws_cdk.core.IConstruct]=None):
        """Properties for an event rule target.

        :param arn: The Amazon Resource Name (ARN) of the target.
        :param id: A unique, user-defined identifier for the target. Acceptable values include alphanumeric characters, periods (.), hyphens (-), and underscores (_).
        :param ecs_parameters: The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task.
        :param input: What input to send to the event target. Default: the entire event
        :param kinesis_parameters: Settings that control shard assignment, when the target is a Kinesis stream. If you don't include this parameter, eventId is used as the partition key.
        :param role: Role to use to invoke this event target.
        :param run_command_parameters: Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command.
        :param sqs_parameters: Parameters used when the FIFO sqs queue is used an event target by the rule.
        :param target_resource: The resource that is backing this target. This is the resource that will actually have some action performed on it when used as a target (for example, start a build for a CodeBuild project). We need it to determine whether the rule belongs to a different account than the target - if so, we generate a more complex setup, including an additional stack containing the EventBusPolicy. Default: the target is not backed by any resource
        """
        if isinstance(ecs_parameters, dict): ecs_parameters = CfnRule.EcsParametersProperty(**ecs_parameters)
        if isinstance(kinesis_parameters, dict): kinesis_parameters = CfnRule.KinesisParametersProperty(**kinesis_parameters)
        if isinstance(run_command_parameters, dict): run_command_parameters = CfnRule.RunCommandParametersProperty(**run_command_parameters)
        if isinstance(sqs_parameters, dict): sqs_parameters = CfnRule.SqsParametersProperty(**sqs_parameters)
        self._values = {
            'arn': arn,
            'id': id,
        }
        if ecs_parameters is not None: self._values["ecs_parameters"] = ecs_parameters
        if input is not None: self._values["input"] = input
        if kinesis_parameters is not None: self._values["kinesis_parameters"] = kinesis_parameters
        if role is not None: self._values["role"] = role
        if run_command_parameters is not None: self._values["run_command_parameters"] = run_command_parameters
        if sqs_parameters is not None: self._values["sqs_parameters"] = sqs_parameters
        if target_resource is not None: self._values["target_resource"] = target_resource

    @builtins.property
    def arn(self) -> str:
        """The Amazon Resource Name (ARN) of the target."""
        return self._values.get('arn')

    @builtins.property
    def id(self) -> str:
        """A unique, user-defined identifier for the target.

        Acceptable values
        include alphanumeric characters, periods (.), hyphens (-), and
        underscores (_).

        deprecated
        :deprecated: prefer auto-generated id by specifying an empty string

        stability
        :stability: deprecated
        """
        return self._values.get('id')

    @builtins.property
    def ecs_parameters(self) -> typing.Optional["CfnRule.EcsParametersProperty"]:
        """The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task."""
        return self._values.get('ecs_parameters')

    @builtins.property
    def input(self) -> typing.Optional["RuleTargetInput"]:
        """What input to send to the event target.

        default
        :default: the entire event
        """
        return self._values.get('input')

    @builtins.property
    def kinesis_parameters(self) -> typing.Optional["CfnRule.KinesisParametersProperty"]:
        """Settings that control shard assignment, when the target is a Kinesis stream.

        If you don't include this parameter, eventId is used as the
        partition key.
        """
        return self._values.get('kinesis_parameters')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role to use to invoke this event target."""
        return self._values.get('role')

    @builtins.property
    def run_command_parameters(self) -> typing.Optional["CfnRule.RunCommandParametersProperty"]:
        """Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command."""
        return self._values.get('run_command_parameters')

    @builtins.property
    def sqs_parameters(self) -> typing.Optional["CfnRule.SqsParametersProperty"]:
        """Parameters used when the FIFO sqs queue is used an event target by the rule."""
        return self._values.get('sqs_parameters')

    @builtins.property
    def target_resource(self) -> typing.Optional[aws_cdk.core.IConstruct]:
        """The resource that is backing this target.

        This is the resource that will actually have some action performed on it when used as a target
        (for example, start a build for a CodeBuild project).
        We need it to determine whether the rule belongs to a different account than the target -
        if so, we generate a more complex setup,
        including an additional stack containing the EventBusPolicy.

        default
        :default: the target is not backed by any resource

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEvents-CrossAccountEventDelivery.html
        """
        return self._values.get('target_resource')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RuleTargetConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class RuleTargetInput(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-events.RuleTargetInput"):
    """The input to send to the event target."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _RuleTargetInputProxy

    def __init__(self) -> None:
        jsii.create(RuleTargetInput, self, [])

    @jsii.member(jsii_name="fromEventPath")
    @builtins.classmethod
    def from_event_path(cls, path: str) -> "RuleTargetInput":
        """Take the event target input from a path in the event JSON.

        :param path: -
        """
        return jsii.sinvoke(cls, "fromEventPath", [path])

    @jsii.member(jsii_name="fromMultilineText")
    @builtins.classmethod
    def from_multiline_text(cls, text: str) -> "RuleTargetInput":
        """Pass text to the event target, splitting on newlines.

        This is only useful when passing to a target that does not
        take a single argument.

        May contain strings returned by EventField.from() to substitute in parts
        of the matched event.

        :param text: -
        """
        return jsii.sinvoke(cls, "fromMultilineText", [text])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, obj: typing.Any) -> "RuleTargetInput":
        """Pass a JSON object to the event target.

        May contain strings returned by EventField.from() to substitute in parts of the
        matched event.

        :param obj: -
        """
        return jsii.sinvoke(cls, "fromObject", [obj])

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, text: str) -> "RuleTargetInput":
        """Pass text to the event target.

        May contain strings returned by EventField.from() to substitute in parts of the
        matched event.

        :param text: -
        """
        return jsii.sinvoke(cls, "fromText", [text])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, rule: "IRule") -> "RuleTargetInputProperties":
        """Return the input properties for this input object.

        :param rule: -
        """
        ...


class _RuleTargetInputProxy(RuleTargetInput):
    @jsii.member(jsii_name="bind")
    def bind(self, rule: "IRule") -> "RuleTargetInputProperties":
        """Return the input properties for this input object.

        :param rule: -
        """
        return jsii.invoke(self, "bind", [rule])


@jsii.data_type(jsii_type="@aws-cdk/aws-events.RuleTargetInputProperties", jsii_struct_bases=[], name_mapping={'input': 'input', 'input_path': 'inputPath', 'input_paths_map': 'inputPathsMap', 'input_template': 'inputTemplate'})
class RuleTargetInputProperties():
    def __init__(self, *, input: typing.Optional[str]=None, input_path: typing.Optional[str]=None, input_paths_map: typing.Optional[typing.Mapping[str,str]]=None, input_template: typing.Optional[str]=None):
        """The input properties for an event target.

        :param input: Literal input to the target service (must be valid JSON).
        :param input_path: JsonPath to take input from the input event.
        :param input_paths_map: Paths map to extract values from event and insert into ``inputTemplate``.
        :param input_template: Input template to insert paths map into.
        """
        self._values = {
        }
        if input is not None: self._values["input"] = input
        if input_path is not None: self._values["input_path"] = input_path
        if input_paths_map is not None: self._values["input_paths_map"] = input_paths_map
        if input_template is not None: self._values["input_template"] = input_template

    @builtins.property
    def input(self) -> typing.Optional[str]:
        """Literal input to the target service (must be valid JSON)."""
        return self._values.get('input')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JsonPath to take input from the input event."""
        return self._values.get('input_path')

    @builtins.property
    def input_paths_map(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Paths map to extract values from event and insert into ``inputTemplate``."""
        return self._values.get('input_paths_map')

    @builtins.property
    def input_template(self) -> typing.Optional[str]:
        """Input template to insert paths map into."""
        return self._values.get('input_template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RuleTargetInputProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Schedule(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-events.Schedule"):
    """Schedule for scheduled event rules."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ScheduleProxy

    def __init__(self) -> None:
        jsii.create(Schedule, self, [])

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

        :param expression: The expression to use. Must be in a format that Cloudwatch Events will recognize
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


__all__ = ["CfnEventBus", "CfnEventBusPolicy", "CfnEventBusPolicyProps", "CfnEventBusProps", "CfnRule", "CfnRuleProps", "CronOptions", "EventBus", "EventBusAttributes", "EventBusProps", "EventField", "EventPattern", "IEventBus", "IRule", "IRuleTarget", "OnEventOptions", "Rule", "RuleProps", "RuleTargetConfig", "RuleTargetInput", "RuleTargetInputProperties", "Schedule", "__jsii_assembly__"]

publication.publish()
