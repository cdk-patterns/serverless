export {};
var AWSXRay = require('aws-xray-sdk');

exports.handler = function(event:any, context:any, callback:any) {
    AWSXRay.captureFunc('process_message', function(subsegment:any) {
        var message = event.Records[0].Sns.Message;
        subsegment.addAnnotation('message_content', message);
        subsegment.close();
    });
    
    callback(null, "Message received.");
};