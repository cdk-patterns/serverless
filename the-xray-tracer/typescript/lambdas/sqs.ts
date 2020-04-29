export {};
const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));

exports.handler = async function(event:any) {
  const segment = AWSXRay.getSegment(); //returns the facade segment
  const sqsSegment = segment.addNewSubsegment('SQS Logic');
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Create an SQS service object
  var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

  var params = {
    DelaySeconds: 1,
    MessageAttributes: {
      MessageDeduplicationId: {
        DataType: "String",
        StringValue: event.path + new Date().getTime()
      }
    },
    MessageBody: "hello from "+event.path,
    QueueUrl: process.env.queueURL,
  };
  sqsSegment.addAnnotation("message", params.MessageBody);
  sqsSegment.addMetadata("params", params)

  let response;

  await sqs.sendMessage(params, function(err:any, data:any) {
    if (err) {
      console.log("Error", err);
      response = sendRes(500, err)
    } else {
      console.log("Success", data.MessageId);
      response = sendRes(200, 'You have added a message to the queue! Message ID is '+data.MessageId)
    }
  }).promise();

  
  // return response back to upstream caller
  return {"status": "success"};
};
