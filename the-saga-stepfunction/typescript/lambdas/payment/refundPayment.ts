const { DynamoDB } = require('aws-sdk');
export {};

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  if (Math.random() < 0.4) {
    throw new Error("Internal Server Error");
  }

  let paymentID = '';
  if (typeof event.TakePaymentResult !== 'undefined') {
    paymentID = event.TakePaymentResult.Payload.payment_id;
  }

  // create AWS SDK clients
  const dynamo = new DynamoDB();

  var params = {
    TableName: process.env.TABLE_NAME,
    Key: {
      'pk' : {S: event.trip_id},
      'sk' : {S: 'PAYMENT#'+paymentID}
    }
  };
  
  // Call DynamoDB to add the item to the table
  let result = await dynamo.deleteItem(params).promise().catch((error: any) => {
    throw new Error(error);
  });

  console.log('Payment has been refunded:');
  console.log(result);

  // return status of ok
  return {
    status: "ok",
  }
};
