const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.BLOGS_TABLE_NAME || '';
const HEADERS = {
  "Content-Type": "text/html",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
};

export const handler = async () : Promise <any> => {

  const params = {
    TableName: TABLE_NAME
  };

  try {
    const response = await db.scan(params).promise();
    return { statusCode: 200, body: JSON.stringify(response.Items), headers: HEADERS };
  } catch (dbError) {
    return { statusCode: 500, body: JSON.stringify(dbError), headers: HEADERS};
  }
};