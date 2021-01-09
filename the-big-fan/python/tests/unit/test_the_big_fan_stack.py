import json
import pytest

from aws_cdk import core
from the_big_fan.the_big_fan_stack import TheBigFanStack

#TODO: replace these with aws-cdk/assert(or similar testing framework) if a python implementation is released
def get_template():
    app = core.App()
    TheBigFanStack(app, "MyTestStack")
    return json.dumps(app.synth().get_stack("MyTestStack").template)


def test_sns_topic_created():
    assert("The Big Fan CDK Pattern Topic" in get_template())


def test_statusCreated_subscriber_sqs_created():
    print(get_template())
    assert("BigFanTopicStatusCreatedSubscriberQueue" in get_template())

def test_anyOtherStatus_subscriber_sqs_created():
    assert("BigFanTopicAnyOtherStatusSubscriberQueue" in get_template())

def test_statusCreated_sns_message_subscription():
    assert('FilterPolicy": {"status": ["created"]}' in get_template())

def test_anyOtherStatus_sns_message_subscription():
    assert('"FilterPolicy": {"status": [{"anything-but": ["created"]}]}' in get_template())

def test_sqs_receiveMessage_iam_policy_created():
    assert(('"PolicyDocument": {'
                '"Statement": ['
                '{"Action": ['
                    '"sqs:ReceiveMessage", '
                    '"sqs:ChangeMessageVisibility", '
                    '"sqs:GetQueueUrl", '
                    '"sqs:DeleteMessage", '
                    '"sqs:GetQueueAttributes"], '
                '"Effect": "Allow"') in get_template())

def test_createdStatus_sqs_subscriber_lambda_created():
    assert('"Handler": "createdStatus.handler"' in get_template())

def test_anyOtherStatus_sqs_subscriber_lambda_created():
    assert('"Handler": "anyOtherStatus.handler"' in get_template())

def test_api_gateway_sendEvent_created():
    assert('"PathPart": "SendEvent"' in get_template())
