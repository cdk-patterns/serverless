export {};

exports.handler = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));

    return sendRes(200, "4");
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