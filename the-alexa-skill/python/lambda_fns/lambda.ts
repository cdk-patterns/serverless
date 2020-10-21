import {
    ErrorHandler,
    HandlerInput,
    RequestHandler,
    SkillBuilders,
    Skill,
} from 'ask-sdk-core';
import {
    Response,
    SessionEndedRequest,
    RequestEnvelope,
} from 'ask-sdk-model';
const patterns: string[] = ['The Destined Lambda', 'The S3 React Website', 'The State Machine', 'The Dynamo Streamer', 'The Lambda Trilogy', 'The Big Fan', 'The Eventbridge Circuit Breaker', 'The Scalable Webhook', 'The Cloudwatch Dashboard', 'The Saga Stepfunction', 'The S3 Angular Website', 'this pattern that you\'re testing right now: The Alexa Skill'];
const ddbAdapter = require('ask-sdk-dynamodb-persistence-adapter');
const USERS_TABLE = process.env.USERS_TABLE || '';
function getPattern(min: number, max: number) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min);
}
const LaunchRequestHandler: RequestHandler = {
    canHandle(handlerInput: HandlerInput): boolean {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest' ||
        handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
        handlerInput.requestEnvelope.request.intent.name === 'AMAZON.NavigateHomeIntent';
    },
    async handle(handlerInput: HandlerInput): Promise<Response> {
        const speechText = 'Hey, it\'s Pancakes the CDK Otter here, what would you like to know?';
        const repromptText = 'You can ask what CDK Patterns I have, if you like!';
        const { attributesManager } = handlerInput;
        attributesManager.setPersistentAttributes( {lastAccessedDate: Date.now(), lastAccessedIntent: 'Launch Request or Navigate Home'});
        await attributesManager.savePersistentAttributes();
        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(repromptText)
            .withSimpleCard('Hello World', speechText)
            .getResponse();
    },
};
const PatternListIntentHandler: RequestHandler = {
    canHandle(handlerInput: HandlerInput): boolean {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            handlerInput.requestEnvelope.request.intent.name === 'PatternListIntent';
    },
    async handle(handlerInput: HandlerInput): Promise<Response> {
        const { attributesManager } = handlerInput;
        attributesManager.setPersistentAttributes( {lastAccessedDate: Date.now(), lastAccessedIntent: 'PatternListIntent'});
        await attributesManager.savePersistentAttributes();

        const speechText = 'I have many patterns for you to see! For example, there is ' + patterns[getPattern(0, 3)] + ', ' + patterns[getPattern(4, 7)] + ' or ' + patterns[getPattern(8, 11)] + '!';

        return handlerInput.responseBuilder
            .speak(speechText)
            .withSimpleCard('Hello World', speechText)
            .getResponse();
    },
};
const HelpIntentHandler: RequestHandler = {
    canHandle(handlerInput: HandlerInput): boolean {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent' ||
            handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            handlerInput.requestEnvelope.request.intent.name === 'AMAZON.FallbackIntent';
    },
    async handle(handlerInput: HandlerInput): Promise<Response> {
        const speechText = 'You can say hello to me!';
        const { attributesManager } = handlerInput;
        attributesManager.setPersistentAttributes( {lastAccessedDate: Date.now(), lastAccessedIntent: 'Help or Fallback Intent'});
        await attributesManager.savePersistentAttributes();

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .withSimpleCard('Hello World', speechText)
            .getResponse();
    },
};
const CancelAndStopIntentHandler: RequestHandler = {
    canHandle(handlerInput: HandlerInput): boolean {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent' ||
                handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    async handle(handlerInput: HandlerInput): Promise<Response> {
        const { attributesManager } = handlerInput;
        attributesManager.setPersistentAttributes( {lastAccessedDate: Date.now(), lastAccessedIntent: 'Cancel or Stop Intent'});
        await attributesManager.savePersistentAttributes();
        const speechText = 'Goodbye!';

        return handlerInput.responseBuilder
            .speak(speechText)
            .withSimpleCard('Hello World', speechText)
            .withShouldEndSession(true)
            .getResponse();
    },
};
const SessionEndedRequestHandler: RequestHandler = {
    canHandle(handlerInput: HandlerInput): boolean {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput: HandlerInput): Response {
        console.log(`Session ended with reason: ${(handlerInput.requestEnvelope.request as SessionEndedRequest).reason}`);

        return handlerInput.responseBuilder.getResponse();
    },
};
const ErrorHandler: ErrorHandler = {
    canHandle(handlerInput: HandlerInput, error: Error): boolean {
        return true;
    },
    handle(handlerInput: HandlerInput, error: Error): Response {
        console.log(`Error handled: ${error.message}`);

        return handlerInput.responseBuilder
            .speak('Sorry, I can\'t understand the command. Please say again.')
            .reprompt('Sorry, I can\'t understand the command. Please say again.')
            .getResponse();
    },
};
let skill: Skill;

function getPersistenceAdapter(tableName: string) {
    return new ddbAdapter.DynamoDbPersistenceAdapter({
      tableName: tableName,
      partitionKeyName: "userId"
    });
  }
exports.handler = SkillBuilders.custom()
    .withPersistenceAdapter(getPersistenceAdapter(USERS_TABLE))
    .addRequestHandlers(
        LaunchRequestHandler,
        PatternListIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        SessionEndedRequestHandler,
    )
    .addErrorHandlers(ErrorHandler)
    .lambda();