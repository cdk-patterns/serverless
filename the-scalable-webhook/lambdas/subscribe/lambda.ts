exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // return response back to upstream caller
  //return sendRes(200, 'You have connected with the Lambda!');
};