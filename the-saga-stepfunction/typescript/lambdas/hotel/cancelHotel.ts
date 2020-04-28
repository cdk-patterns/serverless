const { DynamoDB } = require('aws-sdk');
export {};

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  if (Math.random() < 0.4) {
    throw new Error("Internal Server Error");
  }

  let bookingID = '';
  if (typeof event.ReserveHotelResult !== 'undefined') {
      bookingID = event.ReserveHotelResult.Payload.booking_id;
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params = {
    TableName: process.env.TABLE_NAME,
    Key: {
      'pk' : {S: event.trip_id},
      'sk' : {S: 'HOTEL#'+bookingID}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.deleteItem(params).promise().catch((error: any) => {
    throw new Error(error);
  });

  console.log('deleted hotel booking:');
  console.log(result);

  // return status of ok
  return {status: "ok"}
};