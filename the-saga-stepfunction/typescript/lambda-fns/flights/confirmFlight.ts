const { DynamoDB } = require('aws-sdk');
export {};

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  // If we passed the parameter to fail this step 
  if(event.run_type === 'failFlightsConfirmation'){
      throw new Error('Failed to book the flights');
  }

  let bookingID = '';
  if (typeof event.ReserveFlightResult !== 'undefined') {
      bookingID = event.ReserveFlightResult.Payload.booking_id;
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params  = {
    TableName: process.env.TABLE_NAME,
    Key: {
      'pk' : {S: event.trip_id},
      'sk' : {S: 'FLIGHT#'+bookingID}
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

  console.log('confirmed flight booking:');
  console.log(result);

  // return status of ok
  return {
    status: "ok",
    booking_id: bookingID
  }
};