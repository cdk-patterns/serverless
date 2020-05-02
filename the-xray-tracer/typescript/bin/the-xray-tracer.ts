#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { TheXrayTracerStack } from '../lib/the-xray-tracer-stack';
import { TheDynamoFlowStack } from '../lib/the-dynamo-flow-stack';
import { TheHttpFlowStack } from '../lib/the-http-flow-stack';
import { TheSqsFlowStack } from '../lib/the-sqs-flow-stack';
//import { TheSnsFlowStack } from '../lib/the-sns-flow-stack';

const app = new cdk.App();

let xrayStack = new TheXrayTracerStack(app, 'TheXrayTracerStack', {});

let dynamoFlow = new TheDynamoFlowStack(app, 'TheXrayDynamoFlow', {
    snsTopicARN: xrayStack.snsTopicARN
});
let httpFlow = new TheHttpFlowStack(app, 'TheXrayHttpFlow', {
    snsTopicARN: xrayStack.snsTopicARN
});
let sqsFlow = new TheSqsFlowStack(app, 'TheXraySQSFlow', {
    snsTopicARN: xrayStack.snsTopicARN
});
//let snsFlow = new TheSnsFlowStack(app, 'TheXraySnsFlow');

httpFlow.addDependency(xrayStack, 'need to know the topic arn');
dynamoFlow.addDependency(xrayStack, 'need to know the topic arn');
sqsFlow.addDependency(xrayStack, 'need to know the topic arn');

//xrayStack.addDependency(dynamoFlow, 'needs the lambda to trigger the DynamoDB flow');
//xrayStack.addDependency(httpFlow, 'needs the lambda to trigger the http flow');
//xrayStack.addDependency(sqsFlow, 'needs the lambda to trigger the sqs flow');
//xrayStack.addDependency(snsFlow, 'needs the lambda to trigger the sns flow')
