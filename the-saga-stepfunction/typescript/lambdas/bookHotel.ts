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
  if(event.runType === 'failHotel'){
      throw new Error('Failed to book the hotel');
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params = {
    TableName: process.env.TABLE_NAME,
    Item: {
      'trip_id' : {S: event.trip_id},
      'hotel' : {S: event.hotel},
      'check_in': {S: event.check_in},
      'check_out': {N: event.check_out}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.putItem(params).promise().catch((error: any) => {
    throw new Error(error);
  });

  console.log('inserted hotel booking:');
  console.log(result);

  // return status of ok
  return {status: "ok"}
};