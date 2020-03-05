"use strict";
const { Lambda } = require('aws-sdk');
exports.handler = async function (event) {
    console.log("request:", JSON.stringify(event, undefined, 2));

    var loyaltylevel = "Silver"
    // return response back to upstream caller
    return sendRes(200, loyaltylevel);
};
const sendRes = (status, body) => {
    var response = {
        statusCode: status,
        headers: {
            "Content-Type": "application/json"
        },
        level: loyaltylevel
    };
    return response;
};