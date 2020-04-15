const AWS = require('aws-sdk');

const stepFunctions = new AWS.StepFunctions({
region: 'us-east-1'
});

module.exports.handler = (event:any, context:any, callback:any) => {
    // [success, failFlights, failHotel, failRental]
    let runType = 'success';
    let tripID =  "5c12d94a-ee6a-40d9-889b-1d49142248b7";
    
    if(null != event.queryStringParameters){
        if(typeof event.queryStringParameters.runType != 'undefined') {
            runType = event.queryStringParameters.runType;
        }

        if(typeof event.queryStringParameters.tripID != 'undefined') {
            tripID = event.queryStringParameters.tripID;
        }
    }

    let input = {
        "trip_id": tripID,
        "depart": "London",
        "depart_at": "2021-07-10T06:00:00.000Z",
        "arrive": "Dublin",
        "arrive_at": "2021-07-12T08:00:00.000Z",
        "hotel": "holiday inn",
        "check_in": "2021-07-10T12:00:00.000Z",
        "check_out": "2021-07-12T14:00:00.000Z",
        "rental": "Volvo",
        "rental_from": "2021-07-10T00:00:00.000Z",
        "rental_to": "2021-07-12T00:00:00.000Z",
        "run_type": runType
    };
    
    const params = {
        stateMachineArn: process.env.statemachine_arn,
        input: JSON.stringify(input)
    };
    
    stepFunctions.startExecution(params, (err:any, data:any) => {
        if (err) {
            console.log(err);
            const response = {
                statusCode: 500,
                body: JSON.stringify({
                message: 'There was an error'
                })
            };
            callback(null, response);
        } else {
            console.log(data);
            const response = {
                statusCode: 200,
                body: JSON.stringify({
                    message: 'The holiday booking system is processing your order'
                })
            };
            callback(null, response);
        }
    });
};