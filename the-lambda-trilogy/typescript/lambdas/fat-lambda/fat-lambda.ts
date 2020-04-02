export {};

/**
 * This lambda contains 3 handlers in the same file rather than separating them out
 * 
 * Note that crucially this still ends up 3 lambdas they just have all the code for all 3
 * in each one
 */

exports.add = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));

    // pull firstNum and secondNum from queryparams, default to 0
    let firstNum = event?.queryStringParameters?.firstNum ?? 0;
    let secondNum = event?.queryStringParameters?.secondNum ?? 0;

    let result = Number(firstNum) + Number(secondNum);
    console.log(`result of ${firstNum} + ${secondNum} = ${result}`)

    return sendRes(200, result.toString());
}

exports.subtract = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));

    // pull firstNum and secondNum from queryparams, default to 0
    let firstNum = event?.queryStringParameters?.firstNum ?? 0;
    let secondNum = event?.queryStringParameters?.secondNum ?? 0;

    let result = firstNum - secondNum;
    console.log(`result of ${firstNum} - ${secondNum} = ${result}`)

    return sendRes(200, result.toString());
}

exports.multiply = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));

    // pull firstNum and secondNum from queryparams, default to 0
    let firstNum = event?.queryStringParameters?.firstNum ?? 0;
    let secondNum = event?.queryStringParameters?.secondNum ?? 0;

    let result = firstNum * secondNum;
    console.log(`result of ${firstNum} x ${secondNum} = ${result}`)

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