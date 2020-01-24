var AWS = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Create an SQS service object
  var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

  var params = {
    AttributeNames: [
       "SentTimestamp"
    ],
    MaxNumberOfMessages: 10,
    MessageAttributeNames: [
       "All"
    ],
    QueueUrl: process.env.queueURL,
    VisibilityTimeout: 20,
    WaitTimeSeconds: 0
  };

  sqs.receiveMessage(params, function(err:any, data:any) {
    if (err) {
      console.log("Error pulling message from queue", err);
    } else if (data.Messages) {
      var deleteParams = {
        QueueUrl: process.env.queueURL,
        ReceiptHandle: data.Messages[0].ReceiptHandle
      };
      sqs.deleteMessage(deleteParams, function(err:any, data:any) {
        if (err) {
          console.log("Delete Error", err);
        } else {
          console.log("Message Deleted From Queue Successfully", data);
        }
      });
    }
  });
};