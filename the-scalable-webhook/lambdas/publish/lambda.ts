var AWS = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Create an SQS service object
  var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

  var params = {
    DelaySeconds: 10,
    MessageAttributes: {
      MessageDeduplicationId: {
        DataType: "String",
        StringValue: event.path + new Date().getTime()
      }
    },
    MessageBody: "hello from "+event.path,
    QueueUrl: process.env.queueURL,
  };

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
  return response;
};

let sendRes = (status:number, body:string) => {
  var response = {
    statusCode: status,
    headers: {
      "Content-Type": "text/html"
    },
    body: body
  };
  return response;
};