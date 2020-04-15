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
  if(event.runType === 'failRental'){
      throw new Error('Failed to book the rental car');
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params = {
    TableName: process.env.TABLE_NAME,
    Item: {
      'trip_id' : {S: event.trip_id},
      'rental' : {S: event.rental},
      'rental_from': {S: event.rental_from},
      'rental_to': {N: event.rental_to}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.putItem(params).promise();

  console.log('inserted rental booking:');
  console.log(result);

  // return status of ok
  return {status: "ok"}
};