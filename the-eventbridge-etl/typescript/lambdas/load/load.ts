const { DynamoDB } = require('aws-sdk');

exports.handler = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));

    // Create the DynamoDB service object
  var ddb = new DynamoDB({apiVersion: '2012-08-10'});
  
  var params = {
    TableName: process.env.TABLE_NAME,
    Item: {
      'id' : {S: event.detail.ID},
      'house_number' : {S: event.detail.HouseNum},
      'street_address': {S: event.detail.Street},
      'town': {S: event.detail.Town},
      'zip': {S: event.detail.Zip}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await ddb.putItem(params).promise();

  console.log(result);
}