let aws = require('aws-sdk')
exports.handler = async function(event:any) {
    console.log("request:", JSON.stringify(event, undefined, 2));
    var params = {
    stateMachineArn: process.env.statemachine_arn,
    input: JSON.stringify({})
    }
    var stepfunctions = new aws.StepFunctions()
    stepfunctions.startExecution(params, function (err:any, data:any) {
    if (err) {
        console.log('err while executing step function')
    } else {
        console.log('started execution of step function')
    }
    })
}