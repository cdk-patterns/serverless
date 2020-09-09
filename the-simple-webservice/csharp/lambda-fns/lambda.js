const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async function (event) {
    console.log("request:", JSON.stringify(event, undefined, 2));

    // update dynamo entry for "path" with hits++
    await dynamo.update({
        TableName: process.env.HITS_TABLE_NAME,
        Key: { path: event.rawPath },
        UpdateExpression: 'ADD hits :incr',
        ExpressionAttributeValues: { ':incr': 1 }
    }).promise();
    console.log('inserted counter for ' + event.rawPath);

    return createResponse(200, 'You have connected with the Lambda!');
};

const createResponse = (statusCode, body) => {
    return response = {
        headers: { 'Content-Type': 'text/html' },
        statusCode,
        body
    };
}