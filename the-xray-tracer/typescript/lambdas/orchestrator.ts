export {};
const AWSXRay = require('aws-xray-sdk');
const AWS = AWSXRay.captureAWS(require('aws-sdk'));

exports.handler = async function(event:any) {
    var lambda = new AWS.Lambda();
    const segment = AWSXRay.getSegment(); //returns the facade segment

    let lambdaString = process.env.LAMBDA_ARNS_TO_INVOKE;

    if(typeof lambdaString != 'undefined'){
      let lambdasARNsToInvoke:string[] = JSON.parse(lambdaString);

      for(let lambdaARN of lambdasARNsToInvoke){

        // Create a custom X-Ray segment for this Lambda Function Inokation
        let lambdaInvokeSegment = segment.addNewSubsegment(`${lambdaARN} Invoke Logic`);

        let params = {
          FunctionName: lambdaARN, 
          Payload: JSON.stringify({path:event.path}), 
          InvocationType: "Event"
         };

         lambdaInvokeSegment.addAnnotation("functionARN", lambdaARN);
         lambdaInvokeSegment.addMetadata("params", params)

         // Invoke the lambda
         await lambda.invoke(params).promise();

         lambdaInvokeSegment.close();

      }
    }

    // return response back to upstream caller
  return sendRes(200, 'You have kicked off the orchestrator flow!');
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