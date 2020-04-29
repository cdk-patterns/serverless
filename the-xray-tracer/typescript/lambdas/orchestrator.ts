export {};
const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));

exports.handler = async function(event:any) {
    var lambda = new AWS.Lambda();
    var params = {
        FunctionName: process.env.DYNAMO_FN_ARN, 
        Payload: JSON.stringify({path:"test"}), 
        InvocationType: "Event"
       };
    await lambda.invoke(params, function(err:any, data:any) {
        if (err) console.log(err, err.stack); // an error occurred
        else     console.log(data);           // successful response
    }).promise();

    // return response back to upstream caller
  return sendRes(200, 'You have connected with the Lambda!');
}

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