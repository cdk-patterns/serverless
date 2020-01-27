const { DynamoDB } = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let records: any[] = event.Records;
  
  for(let index in records) {
    let payload = records[index].body;
    let id = records[index].messageAttributes.MessageDeduplicationId.stringValue
    console.log('received message ' + payload);
  }
};