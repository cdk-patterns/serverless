export {};
const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));
// Set region
AWS.config.update({region: 'us-east-1'});

exports.handler = async function(event:any) {
  const segment = AWSXRay.getSegment(); //returns the facade segment
  const snsSegment = segment.addNewSubsegment('SNS Publish Logic');
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Create an SNS service object
  var params = {
    Message: 'Simulated Message', 
    TopicArn: process.env.TOPIC_ARN
  };
  var publishResponse = await new AWS.SNS().publish(params).promise();

  snsSegment.addAnnotation("message", params.Message);
  snsSegment.addMetadata("params", params)
  snsSegment.addMetadata("response", publishResponse)

  console.log(publishResponse);
 
  snsSegment.close();
  
  // return response back to upstream caller
  return {"status": "success"};
};
