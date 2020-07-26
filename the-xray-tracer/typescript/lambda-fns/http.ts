export {};
const AWSXRay = require('aws-xray-sdk');
var https = AWSXRay.captureHTTPs(require('https'));

exports.handler = async function(event:any) {
  const segment = AWSXRay.getSegment(); //returns the facade segment
  console.log("request:", JSON.stringify(event, undefined, 2));

  if (Math.random() < 0.4) {
    throw new Error("SSL Cert Exception");
  }

  const subsegment = segment.addNewSubsegment('external HTTP Request');
  
  let response = await new Promise((resolve:any, reject:any) => {
    let dataString = '';
    // Make a call to a webservice
    const req = https.get("https://jsonplaceholder.typicode.com/todos/1", (res:any) => {
        console.log(`statusCode: ${res.statusCode}`);

        res.on('data', (chunk:any) => {
            dataString += chunk;
        });

        res.on('end', () => {
            resolve({
                data: JSON.parse(dataString)
            })
        });
    });

    req.on('error', (e:any) => {
        reject(e)
    });
  });

  console.log(response);
  subsegment.addMetadata("response", response)
  subsegment.close();

  // return response back to upstream caller
  return {response: response};
};