const AWS = require("aws-sdk")
const db = new AWS.DynamoDB.DocumentClient()
import {v4 as uuidv4} from "uuid"

export const handler = async (event: any = {}): Promise<any> => {
  if (!event.body) {
    return {statusCode: 400, body: "invalid request, you are missing the parameter body"}
  }

  //item: {todo_id: '', title: ''}
  const item = {itemId: uuidv4(), todos: [event.body]}

  const params = {
    TableName: process.env.TABLE_NAME || "",
    Item: item,
  }

  try {
    await db.put(params).promise()
    return {statusCode: 200}
  } catch (dbError) {
    return {statusCode: 500, body: JSON.stringify(dbError)}
  }
}
