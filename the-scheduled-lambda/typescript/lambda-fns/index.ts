const AWS = require('aws-sdk');

exports.handler = (event:object, context:any) => {
    const params = {
        TableName: process.env.TABLE_NAME,
        Item: {
            requestid: context.awsRequestId,
        }
    };

    const documentClient = new AWS.DynamoDB.DocumentClient();

    documentClient.put(params, function(err:{}, data:{}) {
        if (err) {
            console.error("Unable to add item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("Added item:", JSON.stringify(data, null, 2));
        }

    });

}