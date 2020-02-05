const AWS = require('aws-sdk');

const stepFunctions = new AWS.StepFunctions({
region: 'us-east-1'
});

module.exports.handler = (event:any, context:any, callback:any) => {
    let pizzaType = 'pepperoni';
    
    if(null != event.queryStringParameters){
        if(typeof event.queryStringParameters.flavour != 'undefined') {
            pizzaType = event.queryStringParameters.flavour;
        }
    }
    
    const params = {
        stateMachineArn: process.env.statemachine_arn,
        input: JSON.stringify({flavour:pizzaType})
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
            message: 'The Pizzeria is processing your order'
            })
        };
        callback(null, response);
        }
    });
};