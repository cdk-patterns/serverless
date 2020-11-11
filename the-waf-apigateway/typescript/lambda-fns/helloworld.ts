exports.handler = async function(event:any) {
  // return response back to upstream caller
  return sendRes(200, 'Hello World!');
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