export {};
const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));

exports.handler = async function(event:any) {
  const segment = AWSXRay.getSegment(); //returns the facade segment
  const sqsSegment = segment.addNewSubsegment('SQS Logic');
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Create an SQS service object
  var sqs = new AWS.SQS({apiVersion: '2012-11-05'});
  let path = event.Records[0].Sns.Message;

  var params = {
    DelaySeconds: 1,
    MessageBody: "hello from "+path,
    QueueUrl: process.env.SQS_URL,
  };
  sqsSegment.addAnnotation("message", params.MessageBody);
  sqsSegment.addMetadata("params", params)


  await sqs.sendMessage(params, function(err:any, data:any) {
    if (err) {
      console.log("Error", err);
    } else {
      console.log("Success", data.MessageId);
    }
  }).promise();

  
  // return response back to upstream caller
  return {"status": "success"};
};
