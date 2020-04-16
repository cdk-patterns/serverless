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

  // If we passed the parameter to fail this step 
  if(event.run_type === 'failHotel'){
      throw new Error('Failed to book the hotel');
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  let hotelBookingID = hashCode(''+event.trip_id+event.hotel+event.check_in);

  var params = {
    TableName: process.env.TABLE_NAME,
    Item: {
      'pk' : {S: event.trip_id},
      'sk' : {S: 'HOTEL#'+hotelBookingID},
      'type': {S: 'Hotel'},
      'hotel_booking_id': {S: hotelBookingID},
      'hotel' : {S: event.hotel},
      'check_in': {S: event.check_in},
      'check_out': {S: event.check_out}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.putItem(params).promise().catch((error: any) => {
    throw new Error(error);
  });

  console.log('inserted hotel booking:');
  console.log(result);

  // return status of ok
  return {
    status: "ok",
    booking_id: hotelBookingID
  }
};

function hashCode(s:string) {
  let h:any;

  for(let i = 0; i < s.length; i++){
    h = Math.imul(31, h) + s.charCodeAt(i) | 0;
  }

  return ''+h;
}