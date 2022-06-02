"use strict";
const { Lambda } = require('aws-sdk');
exports.handler = async function (event) {
    console.log("get loyalty request:", JSON.stringify(event, undefined, 2));
    let loyaltylevel = "Silver";
    // return response back to upstream caller
    return sendRes(200, loyaltylevel);
};
const sendRes = (status, loyaltylevel) => {
    var response = {
        statusCode: status,
        headers: {
            "Content-Type": "application/json"
        },
        level: loyaltylevel
    };
    return response;
};