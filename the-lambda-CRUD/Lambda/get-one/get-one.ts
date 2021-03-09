const AWS = require("aws-sdk")
const db = new AWS.DynamoDB.DocumentClient()

export const handler = async (event: any = {}): Promise<any> => {
  const requestedItemId = event.pathParameters.id
  if (!requestedItemId) {
    return {statusCode: 400, body: `Error: You are missing the path parameter id`}
  }

  const params = {
    TableName: process.env.TABLE_NAME,
    Key: {
      itemId: requestedItemId,
    },
  }

  try {
    const response = await db.get(params).promise()
    return {statusCode: 200, body: JSON.stringify(response.Item)}
  } catch (dbError) {
    return {statusCode: 500, body: JSON.stringify(dbError)}
  }
}
