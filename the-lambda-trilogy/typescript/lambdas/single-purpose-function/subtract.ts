export {};

exports.handler = async (event:any) => {
  console.log(JSON.stringify(event, null, 2));

  // pull firstNum and secondNum from queryparams, default to 0
  let firstNum = event?.queryStringParameters?.firstNum ?? 0;
  let secondNum = event?.queryStringParameters?.secondNum ?? 0;

  let result = firstNum - secondNum;
  console.log(`result of ${firstNum} - ${secondNum} = ${result}`)

  return sendRes(200, result.toString());
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