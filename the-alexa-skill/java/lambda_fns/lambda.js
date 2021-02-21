"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var ask_sdk_core_1 = require("ask-sdk-core");
var patterns = ['The Destined Lambda', 'The S3 React Website', 'The State Machine', 'The Dynamo Streamer', 'The Lambda Trilogy', 'The Big Fan', 'The Eventbridge Circuit Breaker', 'The Scalable Webhook', 'The Cloudwatch Dashboard', 'The Saga Stepfunction', 'The S3 Angular Website', 'this pattern that you\'re testing right now: The Alexa Skill'];
var ddbAdapter = require('ask-sdk-dynamodb-persistence-adapter');
var USERS_TABLE = process.env.USERS_TABLE || '';
function getPattern(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min);
}
var LaunchRequestHandler = {
    canHandle: function (handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest' ||
            handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
                handlerInput.requestEnvelope.request.intent.name === 'AMAZON.NavigateHomeIntent';
    },
    handle: function (handlerInput) {
        return __awaiter(this, void 0, void 0, function () {
            var speechText, repromptText, attributesManager;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        speechText = 'Hey, it\'s Pancakes the CDK Otter here, what would you like to know?';
                        repromptText = 'You can ask what CDK Patterns I have, if you like!';
                        attributesManager = handlerInput.attributesManager;
                        attributesManager.setPersistentAttributes({ lastAccessedDate: Date.now(), lastAccessedIntent: 'Launch Request or Navigate Home' });
                        return [4 /*yield*/, attributesManager.savePersistentAttributes()];
                    case 1:
                        _a.sent();
                        return [2 /*return*/, handlerInput.responseBuilder
                                .speak(speechText)
                                .reprompt(repromptText)
                                .withSimpleCard('Hello World', speechText)
                                .getResponse()];
                }
            });
        });
    }
};
var PatternListIntentHandler = {
    canHandle: function (handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            handlerInput.requestEnvelope.request.intent.name === 'PatternListIntent';
    },
    handle: function (handlerInput) {
        return __awaiter(this, void 0, void 0, function () {
            var attributesManager, speechText;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        attributesManager = handlerInput.attributesManager;
                        attributesManager.setPersistentAttributes({ lastAccessedDate: Date.now(), lastAccessedIntent: 'PatternListIntent' });
                        return [4 /*yield*/, attributesManager.savePersistentAttributes()];
                    case 1:
                        _a.sent();
                        speechText = 'I have many patterns for you to see! For example, there is ' + patterns[getPattern(0, 3)] + ', ' + patterns[getPattern(4, 7)] + ' or ' + patterns[getPattern(8, 11)] + '!';
                        return [2 /*return*/, handlerInput.responseBuilder
                                .speak(speechText)
                                .withSimpleCard('Hello World', speechText)
                                .getResponse()];
                }
            });
        });
    }
};
var HelpIntentHandler = {
    canHandle: function (handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent' ||
            handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
                handlerInput.requestEnvelope.request.intent.name === 'AMAZON.FallbackIntent';
    },
    handle: function (handlerInput) {
        return __awaiter(this, void 0, void 0, function () {
            var speechText, attributesManager;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        speechText = 'You can say hello to me!';
                        attributesManager = handlerInput.attributesManager;
                        attributesManager.setPersistentAttributes({ lastAccessedDate: Date.now(), lastAccessedIntent: 'Help or Fallback Intent' });
                        return [4 /*yield*/, attributesManager.savePersistentAttributes()];
                    case 1:
                        _a.sent();
                        return [2 /*return*/, handlerInput.responseBuilder
                                .speak(speechText)
                                .reprompt(speechText)
                                .withSimpleCard('Hello World', speechText)
                                .getResponse()];
                }
            });
        });
    }
};
var CancelAndStopIntentHandler = {
    canHandle: function (handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
            (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent' ||
                handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle: function (handlerInput) {
        return __awaiter(this, void 0, void 0, function () {
            var attributesManager, speechText;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        attributesManager = handlerInput.attributesManager;
                        attributesManager.setPersistentAttributes({ lastAccessedDate: Date.now(), lastAccessedIntent: 'Cancel or Stop Intent' });
                        return [4 /*yield*/, attributesManager.savePersistentAttributes()];
                    case 1:
                        _a.sent();
                        speechText = 'Goodbye!';
                        return [2 /*return*/, handlerInput.responseBuilder
                                .speak(speechText)
                                .withSimpleCard('Hello World', speechText)
                                .withShouldEndSession(true)
                                .getResponse()];
                }
            });
        });
    }
};
var SessionEndedRequestHandler = {
    canHandle: function (handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle: function (handlerInput) {
        console.log("Session ended with reason: " + handlerInput.requestEnvelope.request.reason);
        return handlerInput.responseBuilder.getResponse();
    }
};
var ErrorHandler = {
    canHandle: function (handlerInput, error) {
        return true;
    },
    handle: function (handlerInput, error) {
        console.log("Error handled: " + error.message);
        return handlerInput.responseBuilder
            .speak('Sorry, I can\'t understand the command. Please say again.')
            .reprompt('Sorry, I can\'t understand the command. Please say again.')
            .getResponse();
    }
};
var skill;
function getPersistenceAdapter(tableName) {
    return new ddbAdapter.DynamoDbPersistenceAdapter({
        tableName: tableName,
        partitionKeyName: "userId"
    });
}
exports.handler = ask_sdk_core_1.SkillBuilders.custom()
    .withPersistenceAdapter(getPersistenceAdapter(USERS_TABLE))
    .addRequestHandlers(LaunchRequestHandler, PatternListIntentHandler, HelpIntentHandler, CancelAndStopIntentHandler, SessionEndedRequestHandler)
    .addErrorHandlers(ErrorHandler)
    .lambda();
