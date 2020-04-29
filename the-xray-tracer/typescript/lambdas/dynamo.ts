const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));
var https = AWSXRay.captureHTTPs(require('https'));

const options = {
  hostname: 'jsonplaceholder.typicode.com',
  port: 443,
  path: '/todos/1',
  method: 'GET'
}

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // create AWS SDK clients
  const dynamo = new AWS.DynamoDB();

  // update dynamo entry for "path" with hits++
  await dynamo.updateItem({
    TableName: process.env.HITS_TABLE_NAME,
    Key: { path: { S: event.path } },
    UpdateExpression: 'ADD hits :incr',
    ExpressionAttributeValues: { ':incr': { N: '1' } }
  }).promise();

  console.log('inserted counter for '+ event.path);

  // Make a call to a webservice
  const req = https.request(options, (res:any) => {
    console.log(`statusCode: ${res.statusCode}`)
  
    res.on('data', (d:any) => {
      console.log(d)
    })
  })

  req.on('error', (error:any) => {
    console.error(error)
  })
  
  req.end()

  // return response back to upstream caller
  return sendRes(200, 'You have connected with the Lambda!');
};

const sendRes = (status:number, body:string) => {
  var response = {
    statusCode: status,
    headers: {
      "Content-Type": "text/html"
    },
    body: body
  };
  return response;
};