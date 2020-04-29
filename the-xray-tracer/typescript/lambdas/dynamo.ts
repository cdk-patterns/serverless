const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));

exports.handler = async function(event:any) {
  const segment = AWSXRay.getSegment(); //returns the facade segment
  console.log("request:", JSON.stringify(event, undefined, 2));

  const dynamoSegment = segment.addNewSubsegment('DynamoDB Query');
  // create AWS SDK clients
  const dynamo = new AWS.DynamoDB();

  dynamoSegment.addAnnotation("path", event.path);
  dynamoSegment.addMetadata("event", event)

  // update dynamo entry for "path" with hits++
  await dynamo.updateItem({
    TableName: process.env.HITS_TABLE_NAME,
    Key: { path: { S: event.path } },
    UpdateExpression: 'ADD hits :incr',
    ExpressionAttributeValues: { ':incr': { N: '1' } }
  }).promise();

  console.log('inserted counter for '+ event.path);

  dynamoSegment.close();

  // return response back to upstream caller
  return {"status": "success"};
};