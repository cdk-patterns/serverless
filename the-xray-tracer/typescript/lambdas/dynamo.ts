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
  const segment = AWSXRay.getSegment(); //returns the facade segment
  console.log("request:", JSON.stringify(event, undefined, 2));

  const dynamoSegment = segment.addNewSubsegment('DynamoDB Query');
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

  dynamoSegment.close();
  const subsegment = segment.addNewSubsegment('external HTTP Request');
  
  let response = await new Promise((resolve:any, reject:any) => {
    let dataString = '';
    // Make a call to a webservice
    const req = https.request(options, (res:any) => {
        console.log(`statusCode: ${res.statusCode}`);

        res.on('data', (chunk:any) => {
            dataString += chunk;
        });

        res.on('end', () => {
            resolve({
                data: dataString
            })
        });
    });

    req.on('error', (e:any) => {
        reject(e)
    });
  });

  console.log(response);
  subsegment.close();

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