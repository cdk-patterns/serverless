const AWS = require("aws-sdk")
const db = new AWS.DynamoDB.DocumentClient()

export const handler = async (event: any = {}): Promise<any> => {
  if (!event.body) {
    return {statusCode: 400, body: "invalid request, you are missing the parameter body"}
  }
  const editedItemId = event.pathParameters.id

  const editedItem: any = {todos: [event.body]}

  const params: any = {
    TableName: process.env.TABLE_NAME,
    Key: {
      itemId: editedItemId,
    },
    UpdateExpression: `set todos = :${editedItem.todos}`,
  }

  try {
    await db.update(params).promise()
    return {statusCode: 200, body: ""}
  } catch (dbError) {
    return {statusCode: 500, body: dbError}
  }
}
