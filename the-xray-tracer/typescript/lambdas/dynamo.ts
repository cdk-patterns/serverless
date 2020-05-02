const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));

exports.handler = async function(event:any) {
  const segment = AWSXRay.getSegment(); //returns the facade segment
  console.log("request:", JSON.stringify(event, undefined, 2));

  const dynamoSegment = segment.addNewSubsegment('DynamoDB Query');
  // create AWS SDK clients
  const dynamo = new AWS.DynamoDB();
  let path = event.Records[0].Sns.Message;

  dynamoSegment.addAnnotation("path", path);
  dynamoSegment.addMetadata("event", event)

  // update dynamo entry for "path" with hits++
  await dynamo.updateItem({
    TableName: process.env.HITS_TABLE_NAME,
    Key: { path: { S: path } },
    UpdateExpression: 'ADD hits :incr',
    ExpressionAttributeValues: { ':incr': { N: '1' } }
  }).promise();

  console.log('inserted counter for '+ path);

  dynamoSegment.close();

  // return response back to upstream caller
  return {"status": "success"};
};