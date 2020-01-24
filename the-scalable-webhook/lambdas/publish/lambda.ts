var AWS = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Create an SQS service object
  var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

  var params = {
    DelaySeconds: 10,
    MessageAttributes: {
      "Title": {
        DataType: "String",
        StringValue: "The Whistler"
      },
      "Author": {
        DataType: "String",
        StringValue: "John Grisham"
      },
      "WeeksOn": {
        DataType: "Number",
        StringValue: "6"
      }
    },
    MessageBody: "Information about current NY Times fiction bestseller for week of 12/11/2016.",
    // MessageDeduplicationId: "TheWhistler",  // Required for FIFO queues
    // MessageId: "Group1",  // Required for FIFO queues
    QueueUrl: process.env.queueURL
  };

  await sqs.sendMessage(params, function(err:any, data:any) {
    if (err) {
      console.log("Error", err);
    } else {
      console.log("Success", data.MessageId);
    }
  }).promise();

  // return response back to upstream caller
  return sendRes(200, 'You have added a message to the queue!');
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