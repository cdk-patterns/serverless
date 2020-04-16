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

  if (Math.random() < 0.4) {
    throw new Error("Internal Server Error");
  }

  let bookingID = '';
  if(typeof event.BookHotelResult !== 'undefined'){
    bookingID = event.BookHotelResult.booking_id;
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params = {
    TableName: process.env.TABLE_NAME,
    Key: {
      ':pk' : {S: event.trip_id},
      ':sk' : {S: 'HOTEL#'+bookingID}
    },
    ConditionExpression: "pk = :pk and sk begins_with(:sk)", 
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