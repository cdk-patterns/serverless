const AWS = require('aws-sdk')
AWS.config.region = process.env.AWS_REGION || 'us-east-1'
export {};

exports.handler = async (event:any, context:any) => {
  console.log(event) 
  
  // Create the DynamoDB service object
  var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
  
  const secondsSinceEpoch = Math.round(Date.now() / 1000);
  const expirationTime = ''+(secondsSinceEpoch + 60);
  
  var params = {
    TableName: process.env.TABLE_NAME,
    Item: {
      'RequestID' : {S: Math.random().toString(36).substring(2) + Date.now().toString(36)},
      'SiteUrl' : {S: event.detail.siteUrl},
      'ErrorType': {S: event.detail.errorType},
      'ExpirationTime': {N: expirationTime}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await ddb.putItem(params).promise();
  console.log(result);
}
