const { DynamoDB } = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let records: any[] = event.Records;
  // create AWS SDK clients
  const dynamo = new DynamoDB();
  
  for(let index in records) {
    let payload = records[index].body;
    let id = records[index].messageAttributes.MessageDeduplicationId.stringValue
    console.log('received message ' + payload);
    
    
    var params = {
      TableName: process.env.tableName,
      Item: {
        'id' : {S: id},
        'message' : {S: payload}
      }
    };
    
    // Call DynamoDB to add the item to the table
    await dynamo.putItem(params, function(err:any, data:any) {
      if (err) {
        console.log("Error", err);
      } else {
        console.log("Success", data);
      }
    }).promise();
  }
};