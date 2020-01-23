const { DynamoDB, Lambda } = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // return response back to upstream caller
  return sendRes(200, 'You have connected with the Lambda!');
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