const AWS = require('aws-sdk')
AWS.config.region = process.env.AWS_REGION || 'us-east-1'
const eventbridge = new AWS.EventBridge()

exports.handler = async (event:any, context:any) => {

  // create AWS SDK clients
  const dynamo = new AWS.DynamoDB();

  var dynamoParams = {
    ExpressionAttributeValues: {
     ":v1": {
       S: "www.google.com"
      }
    }, 
    KeyConditionExpression: "siteUrl = :v1", 
    IndexName: "UrlIndex",
    TableName: process.env.TABLE_NAME,
   };

  const knownErrors = await dynamo.query(dynamoParams).promise();

  console.log(knownErrors);

  // Hard coding in a failure event
  var params = {
    Entries: [
      {
        DetailType: 'httpcall',
        EventBusName: 'default',
        Source: 'cdkpatterns.eventbridge.circuitbreaker',
        Time: new Date(),
        // Main event body
        Detail: JSON.stringify({
          status: 'fail',
          siteUrl: 'www.google.com',
        })
      }
    ]
  };

  const result = await eventbridge.putEvents(params).promise()

  console.log('--- EventBridge Response ---')
  console.log(result)  

  return sendRes(500, 'Something appears to be wrong with this service, please try again later');
}

const sendRes = (status:any, body:any) => {
  var response = {
      statusCode: status,
      headers: {
          "Content-Type": "text/html"
      },
      body: body
  };
  return response;
};
