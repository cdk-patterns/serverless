"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var AWSXRay = require('aws-xray-sdk');

exports.handler = function (event, context, callback) {
    
    AWSXRay.captureFunc('process_message', function (subsegment) {
        var message = event.Records[0].Sns.Message;
        subsegment.addAnnotation('message_content', message);
        subsegment.close();
    });

    callback(null, "Message received.");
};