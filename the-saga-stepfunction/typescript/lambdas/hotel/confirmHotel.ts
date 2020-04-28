const { DynamoDB } = require('aws-sdk');
export {};

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let bookingID = '';

  // If we passed the parameter to fail this step 
  if(event.run_type === 'failHotelConfirmation'){
    throw new Error('Failed to confirm the hotel booking');
  }

  if (typeof event.ReserveHotelResult !== 'undefined') {
    bookingID = event.ReserveHotelResult.Payload.booking_id;
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params  = {
    TableName: process.env.TABLE_NAME,
    Key: {
      'pk' : {S: event.trip_id},
      'sk' : {S: 'HOTEL#'+bookingID}
    },
    "UpdateExpression": "set transaction_status = :booked",
    "ExpressionAttributeValues": {
        ":booked": {"S": "confirmed"}
    }
  }
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.updateItem(params).promise().catch((error: any) => {
    throw new Error(error);
  });

  console.log('updated hotel booking:');
  console.log(result);

  // return status of ok
  return {
    status: "ok",
    booking_id: bookingID
  }
};