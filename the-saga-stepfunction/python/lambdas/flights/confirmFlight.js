"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const { DynamoDB } = require('aws-sdk');
exports.handler = async function (event) {
    console.log("request:", JSON.stringify(event, undefined, 2));
    // If we passed the parameter to fail this step 
    if (event.run_type === 'failFlightsConfirmation') {
        throw new Error('Failed to book the flights');
    }
    let bookingID = '';
    if (typeof event.ReserveFlightResult !== 'undefined') {
        bookingID = event.ReserveFlightResult.Payload.booking_id;
    }
    // create AWS SDK clients
    const dynamo = new DynamoDB();
    var params = {
        TableName: process.env.TABLE_NAME,
        Key: {
            'pk': { S: event.trip_id },
            'sk': { S: 'FLIGHT#' + bookingID }
        },
        "UpdateExpression": "set transaction_status = :booked",
        "ExpressionAttributeValues": {
            ":booked": { "S": "confirmed" }
        }
    };
    // Call DynamoDB to add the item to the table
    let result = await dynamo.updateItem(params).promise().catch((error) => {
        throw new Error(error);
    });
    console.log('confirmed flight booking:');
    console.log(result);
    // return status of ok
    return {
        status: "ok",
        booking_id: bookingID
    };
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29uZmlybUZsaWdodC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbImNvbmZpcm1GbGlnaHQudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7QUFBQSxNQUFNLEVBQUUsUUFBUSxFQUFFLEdBQUcsT0FBTyxDQUFDLFNBQVMsQ0FBQyxDQUFDO0FBR3hDLE9BQU8sQ0FBQyxPQUFPLEdBQUcsS0FBSyxXQUFVLEtBQVM7SUFDeEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxVQUFVLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLEVBQUUsU0FBUyxFQUFFLENBQUMsQ0FBQyxDQUFDLENBQUM7SUFFN0QsZ0RBQWdEO0lBQ2hELElBQUcsS0FBSyxDQUFDLFFBQVEsS0FBSyx5QkFBeUIsRUFBQztRQUM1QyxNQUFNLElBQUksS0FBSyxDQUFDLDRCQUE0QixDQUFDLENBQUM7S0FDakQ7SUFFRCxJQUFJLFNBQVMsR0FBRyxFQUFFLENBQUM7SUFDbkIsSUFBSSxPQUFPLEtBQUssQ0FBQyxtQkFBbUIsS0FBSyxXQUFXLEVBQUU7UUFDbEQsU0FBUyxHQUFHLEtBQUssQ0FBQyxtQkFBbUIsQ0FBQyxVQUFVLENBQUM7S0FDcEQ7SUFFRCx5QkFBeUI7SUFDekIsTUFBTSxNQUFNLEdBQUcsSUFBSSxRQUFRLEVBQUUsQ0FBQztJQUU5QixJQUFJLE1BQU0sR0FBSTtRQUNaLFNBQVMsRUFBRSxPQUFPLENBQUMsR0FBRyxDQUFDLFVBQVU7UUFDakMsR0FBRyxFQUFFO1lBQ0gsSUFBSSxFQUFHLEVBQUMsQ0FBQyxFQUFFLEtBQUssQ0FBQyxPQUFPLEVBQUM7WUFDekIsSUFBSSxFQUFHLEVBQUMsQ0FBQyxFQUFFLFNBQVMsR0FBQyxTQUFTLEVBQUM7U0FDaEM7UUFDRCxrQkFBa0IsRUFBRSxrQ0FBa0M7UUFDdEQsMkJBQTJCLEVBQUU7WUFDekIsU0FBUyxFQUFFLEVBQUMsR0FBRyxFQUFFLFdBQVcsRUFBQztTQUNoQztLQUNGLENBQUE7SUFFRCw2Q0FBNkM7SUFDN0MsSUFBSSxNQUFNLEdBQUcsTUFBTSxNQUFNLENBQUMsVUFBVSxDQUFDLE1BQU0sQ0FBQyxDQUFDLE9BQU8sRUFBRSxDQUFDLEtBQUssQ0FBQyxDQUFDLEtBQVUsRUFBRSxFQUFFO1FBQzFFLE1BQU0sSUFBSSxLQUFLLENBQUMsS0FBSyxDQUFDLENBQUM7SUFDekIsQ0FBQyxDQUFDLENBQUM7SUFFSCxPQUFPLENBQUMsR0FBRyxDQUFDLDJCQUEyQixDQUFDLENBQUM7SUFDekMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxNQUFNLENBQUMsQ0FBQztJQUVwQixzQkFBc0I7SUFDdEIsT0FBTztRQUNMLE1BQU0sRUFBRSxJQUFJO1FBQ1osVUFBVSxFQUFFLFNBQVM7S0FDdEIsQ0FBQTtBQUNILENBQUMsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbImNvbnN0IHsgRHluYW1vREIgfSA9IHJlcXVpcmUoJ2F3cy1zZGsnKTtcbmV4cG9ydCB7fTtcblxuZXhwb3J0cy5oYW5kbGVyID0gYXN5bmMgZnVuY3Rpb24oZXZlbnQ6YW55KSB7XG4gIGNvbnNvbGUubG9nKFwicmVxdWVzdDpcIiwgSlNPTi5zdHJpbmdpZnkoZXZlbnQsIHVuZGVmaW5lZCwgMikpO1xuXG4gIC8vIElmIHdlIHBhc3NlZCB0aGUgcGFyYW1ldGVyIHRvIGZhaWwgdGhpcyBzdGVwIFxuICBpZihldmVudC5ydW5fdHlwZSA9PT0gJ2ZhaWxGbGlnaHRzQ29uZmlybWF0aW9uJyl7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoJ0ZhaWxlZCB0byBib29rIHRoZSBmbGlnaHRzJyk7XG4gIH1cblxuICBsZXQgYm9va2luZ0lEID0gJyc7XG4gIGlmICh0eXBlb2YgZXZlbnQuUmVzZXJ2ZUZsaWdodFJlc3VsdCAhPT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgIGJvb2tpbmdJRCA9IGV2ZW50LlJlc2VydmVGbGlnaHRSZXN1bHQuYm9va2luZ19pZDtcbiAgfVxuXG4gIC8vIGNyZWF0ZSBBV1MgU0RLIGNsaWVudHNcbiAgY29uc3QgZHluYW1vID0gbmV3IER5bmFtb0RCKCk7XG5cbiAgdmFyIHBhcmFtcyAgPSB7XG4gICAgVGFibGVOYW1lOiBwcm9jZXNzLmVudi5UQUJMRV9OQU1FLFxuICAgIEtleToge1xuICAgICAgJ3BrJyA6IHtTOiBldmVudC50cmlwX2lkfSxcbiAgICAgICdzaycgOiB7UzogJ0ZMSUdIVCMnK2Jvb2tpbmdJRH1cbiAgICB9LFxuICAgIFwiVXBkYXRlRXhwcmVzc2lvblwiOiBcInNldCB0cmFuc2FjdGlvbl9zdGF0dXMgPSA6Ym9va2VkXCIsXG4gICAgXCJFeHByZXNzaW9uQXR0cmlidXRlVmFsdWVzXCI6IHtcbiAgICAgICAgXCI6Ym9va2VkXCI6IHtcIlNcIjogXCJjb25maXJtZWRcIn1cbiAgICB9XG4gIH1cbiAgXG4gIC8vIENhbGwgRHluYW1vREIgdG8gYWRkIHRoZSBpdGVtIHRvIHRoZSB0YWJsZVxuICBsZXQgcmVzdWx0ID0gYXdhaXQgZHluYW1vLnVwZGF0ZUl0ZW0ocGFyYW1zKS5wcm9taXNlKCkuY2F0Y2goKGVycm9yOiBhbnkpID0+IHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoZXJyb3IpO1xuICB9KTtcblxuICBjb25zb2xlLmxvZygnY29uZmlybWVkIGZsaWdodCBib29raW5nOicpO1xuICBjb25zb2xlLmxvZyhyZXN1bHQpO1xuXG4gIC8vIHJldHVybiBzdGF0dXMgb2Ygb2tcbiAgcmV0dXJuIHtcbiAgICBzdGF0dXM6IFwib2tcIixcbiAgICBib29raW5nX2lkOiBib29raW5nSURcbiAgfVxufTsiXX0=