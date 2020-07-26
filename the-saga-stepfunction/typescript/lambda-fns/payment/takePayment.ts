const { DynamoDB } = require('aws-sdk');
export {};

/* input example:
 *  { trip_id: some_guid,
 *    depart: london,
 *    depart_at: some_date,
 *    arrive: dublin,
 *    arrive_at: some_date,
 *    hotel: holiday inn,
 *    check_in: some_date,
 *    check_out: some_date,
 *    rental: volvo,
 *    rental_from: some_date,
 *    rental_to: some_date
 *  }
 */
exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let flightBookingID = '';
  if (typeof event.ReserveFlightResult !== 'undefined') {
    flightBookingID = event.ReserveFlightResult.Payload.booking_id;
  }

  let hotelBookingID = '';
  if (typeof event.ReserveHotelResult !== 'undefined') {
    hotelBookingID = event.ReserveHotelResult.Payload.booking_id;
  }

  let paymentID = hashCode(''+event.trip_id+hotelBookingID+flightBookingID);

  // If we passed the parameter to fail this step 
  if(event.run_type === 'failPayment'){
    throw new Error('Failed to book the flights');
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params = {
      TableName: process.env.TABLE_NAME,
      Item: {
        'pk' : {S: event.trip_id},
        'sk' : {S: 'PAYMENT#'+paymentID},
        'type': {S: 'Payment'},
        'trip_id' : {S: event.trip_id},
        'id': {S: paymentID},
        'amount': {S: "450.00"},
        'currency': {S: "USD"},
        'transaction_status': {S: "confirmed"}
      }
    };
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.putItem(params).promise().catch((error: any) => {
    throw new Error(error);
  });

  console.log('Payment Taken Successfully:');
  console.log(result);

  // return status of ok
  return {
    status: "ok",
    payment_id: paymentID
  }
};

function hashCode(s:string) {
  let h:any;

  for(let i = 0; i < s.length; i++){
    h = Math.imul(31, h) + s.charCodeAt(i) | 0;
  }

  return ''+Math.abs(h);
}
