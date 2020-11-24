const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient();
//const {"v4": uuidv4} = require('uuid'); // use this as part of a shipped lambda package instead of the workaround function below.
const TABLE_NAME = process.env.BLOGS_TABLE_NAME || '';
const PRIMARY_KEY = process.env.PRIMARY_KEY || '';
const HEADERS = {
  "Content-Type": "text/html",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
};

const RESERVED_RESPONSE = `Error: You're using AWS reserved keywords as attributes`,
  DYNAMODB_EXECUTION_ERROR = `Error: Execution update, caused a Dynamodb error, please take a look at your CloudWatch Logs.`;

  // Work around to avoid having to ship a full lambda zip packages for the purposes of demonstration. 
  // Donot deploy this to prd. 
  // 
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

export const handler = async (event: any = {}): Promise<any> => {

  if (!event.body) {
    return {
      statusCode: 400,
      body: 'invalid request, you are missing the parameter body',
      headers: HEADERS
    };
  }
  const item = typeof event.body == 'object' ? event.body : JSON.parse(event.body);
  item[PRIMARY_KEY] = uuidv4();
  const params = {
    TableName: TABLE_NAME,
    Item: item
  };

  try {
    await db.put(params).promise();
    return { statusCode: 201, body: '', headers: HEADERS };
  } catch (dbError) {
    const errorResponse = dbError.code === 'ValidationException' && dbError.message.includes('reserved keyword') ?
      DYNAMODB_EXECUTION_ERROR : RESERVED_RESPONSE;
    return { statusCode: 500, body: errorResponse };
  }
};