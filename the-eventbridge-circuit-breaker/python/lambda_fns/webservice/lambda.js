"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const AWS = require('aws-sdk');
AWS.config.region = process.env.AWS_REGION || 'us-east-1';
const eventbridge = new AWS.EventBridge();
exports.handler = async (event, context) => {
    const ERROR_THRESHOLD = 3;
    const serviceURL = 'www.google.com';
    let response;
    // create AWS SDK clients
    const dynamo = new AWS.DynamoDB();
    const secondsSinceEpoch = Math.round(Date.now() / 1000);
    // We are querying our error Dynamo to count how many errors are in there for www.google.com
    var dynamoParams = {
        ExpressionAttributeValues: {
            ":v1": { "S": serviceURL },
            ":now": { "N": secondsSinceEpoch.toString() }
        },
        KeyConditionExpression: "SiteUrl = :v1 and ExpirationTime > :now",
        IndexName: "UrlIndex",
        TableName: process.env.TABLE_NAME,
    };
    const recentErrors = await dynamo.query(dynamoParams).promise();
    console.log('--- Recent Errors ---');
    console.log(recentErrors.Count);
    console.log(JSON.stringify(recentErrors));
    // If we are within our error threshold, make the http call
    if (recentErrors.Count < ERROR_THRESHOLD) {
        let errorType = '';
        // In here assume we made an http request to google and it was down, 
        // 10 sec hard coded delay for simulation
        const fakeServiceCall = await new Promise((resolve, reject) => {
            console.log('--- Calling Webservice, recent errors below threshold ---');
            setTimeout(function () {
                reject("service timeout exception");
            }, 10000);
        }).catch((reason) => {
            console.log('--- Service Call Failure ---');
            console.log(reason);
            errorType = reason;
        });
        // Building our failure event for EventBridge
        var params = {
            Entries: [
                {
                    DetailType: 'httpcall',
                    EventBusName: 'default',
                    Source: 'cdkpatterns.eventbridge.circuitbreaker',
                    Time: new Date(),
                    // Main event body
                    Detail: JSON.stringify({
                        status: 'fail',
                        siteUrl: serviceURL,
                        errorType: errorType
                    })
                }
            ]
        };
        const result = await eventbridge.putEvents(params).promise();
        console.log('--- EventBridge Response ---');
        console.log(result);
        response = sendRes(500, 'Something appears to be wrong with this service, please try again later');
    }
    else {
        console.log('Circuit currently closed, sending back failure response');
        response = sendRes(500, 'This service has been experiencing issues for a while, we have closed the circuit');
    }
    return response;
};
const sendRes = (status, body) => {
    var response = {
        statusCode: status,
        headers: {
            "Content-Type": "text/html"
        },
        body: body
    };
    return response;
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibGFtYmRhLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsibGFtYmRhLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7O0FBQUEsTUFBTSxHQUFHLEdBQUcsT0FBTyxDQUFDLFNBQVMsQ0FBQyxDQUFBO0FBQzlCLEdBQUcsQ0FBQyxNQUFNLENBQUMsTUFBTSxHQUFHLE9BQU8sQ0FBQyxHQUFHLENBQUMsVUFBVSxJQUFJLFdBQVcsQ0FBQTtBQUN6RCxNQUFNLFdBQVcsR0FBRyxJQUFJLEdBQUcsQ0FBQyxXQUFXLEVBQUUsQ0FBQTtBQUd6QyxPQUFPLENBQUMsT0FBTyxHQUFHLEtBQUssRUFBRSxLQUFTLEVBQUUsT0FBVyxFQUFFLEVBQUU7SUFDakQsTUFBTSxlQUFlLEdBQUcsQ0FBQyxDQUFDO0lBQzFCLE1BQU0sVUFBVSxHQUFHLGdCQUFnQixDQUFDO0lBQ3BDLElBQUksUUFBUSxDQUFDO0lBRWIseUJBQXlCO0lBQ3pCLE1BQU0sTUFBTSxHQUFHLElBQUksR0FBRyxDQUFDLFFBQVEsRUFBRSxDQUFDO0lBQ2xDLE1BQU0saUJBQWlCLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsR0FBRyxFQUFFLEdBQUcsSUFBSSxDQUFDLENBQUM7SUFFeEQsNEZBQTRGO0lBQzVGLElBQUksWUFBWSxHQUFHO1FBQ2pCLHlCQUF5QixFQUFFO1lBQzFCLEtBQUssRUFBRyxFQUFDLEdBQUcsRUFBQyxVQUFVLEVBQUM7WUFDeEIsTUFBTSxFQUFFLEVBQUMsR0FBRyxFQUFDLGlCQUFpQixDQUFDLFFBQVEsRUFBRSxFQUFDO1NBQzFDO1FBQ0Qsc0JBQXNCLEVBQUUseUNBQXlDO1FBQ2pFLFNBQVMsRUFBRSxVQUFVO1FBQ3JCLFNBQVMsRUFBRSxPQUFPLENBQUMsR0FBRyxDQUFDLFVBQVU7S0FDakMsQ0FBQztJQUVILE1BQU0sWUFBWSxHQUFHLE1BQU0sTUFBTSxDQUFDLEtBQUssQ0FBQyxZQUFZLENBQUMsQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUVoRSxPQUFPLENBQUMsR0FBRyxDQUFDLHVCQUF1QixDQUFDLENBQUM7SUFDckMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxZQUFZLENBQUMsS0FBSyxDQUFDLENBQUM7SUFDaEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUM7SUFFMUMsMkRBQTJEO0lBQzNELElBQUcsWUFBWSxDQUFDLEtBQUssR0FBRyxlQUFlLEVBQUM7UUFDdEMsSUFBSSxTQUFTLEdBQUcsRUFBRSxDQUFDO1FBRW5CLHFFQUFxRTtRQUNyRSx5Q0FBeUM7UUFDekMsTUFBTSxlQUFlLEdBQUcsTUFBTSxJQUFJLE9BQU8sQ0FBQyxDQUFDLE9BQU8sRUFBRSxNQUFNLEVBQUUsRUFBRTtZQUM1RCxPQUFPLENBQUMsR0FBRyxDQUFDLDJEQUEyRCxDQUFDLENBQUM7WUFDekUsVUFBVSxDQUFFO2dCQUNWLE1BQU0sQ0FBQywyQkFBMkIsQ0FBQyxDQUFBO1lBQ3JDLENBQUMsRUFBRSxLQUFLLENBQUMsQ0FBQTtRQUNYLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxDQUFDLE1BQU0sRUFBQyxFQUFFO1lBQ2pCLE9BQU8sQ0FBQyxHQUFHLENBQUMsOEJBQThCLENBQUMsQ0FBQztZQUM1QyxPQUFPLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1lBQ3BCLFNBQVMsR0FBRyxNQUFNLENBQUM7UUFDckIsQ0FBQyxDQUFDLENBQUM7UUFFSCw2Q0FBNkM7UUFDN0MsSUFBSSxNQUFNLEdBQUc7WUFDWCxPQUFPLEVBQUU7Z0JBQ1A7b0JBQ0UsVUFBVSxFQUFFLFVBQVU7b0JBQ3RCLFlBQVksRUFBRSxTQUFTO29CQUN2QixNQUFNLEVBQUUsd0NBQXdDO29CQUNoRCxJQUFJLEVBQUUsSUFBSSxJQUFJLEVBQUU7b0JBQ2hCLGtCQUFrQjtvQkFDbEIsTUFBTSxFQUFFLElBQUksQ0FBQyxTQUFTLENBQUM7d0JBQ3JCLE1BQU0sRUFBRSxNQUFNO3dCQUNkLE9BQU8sRUFBRSxVQUFVO3dCQUNuQixTQUFTLEVBQUUsU0FBUztxQkFDckIsQ0FBQztpQkFDSDthQUNGO1NBQ0YsQ0FBQztRQUVGLE1BQU0sTUFBTSxHQUFHLE1BQU0sV0FBVyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUU3RCxPQUFPLENBQUMsR0FBRyxDQUFDLDhCQUE4QixDQUFDLENBQUE7UUFDM0MsT0FBTyxDQUFDLEdBQUcsQ0FBQyxNQUFNLENBQUMsQ0FBQTtRQUNuQixRQUFRLEdBQUcsT0FBTyxDQUFDLEdBQUcsRUFBRSx5RUFBeUUsQ0FBQyxDQUFDO0tBQ3BHO1NBQU07UUFDTCxPQUFPLENBQUMsR0FBRyxDQUFDLHlEQUF5RCxDQUFDLENBQUM7UUFDdkUsUUFBUSxHQUFHLE9BQU8sQ0FBQyxHQUFHLEVBQUUsbUZBQW1GLENBQUMsQ0FBQztLQUM5RztJQUVELE9BQU8sUUFBUSxDQUFDO0FBQ2xCLENBQUMsQ0FBQTtBQUVELE1BQU0sT0FBTyxHQUFHLENBQUMsTUFBVSxFQUFFLElBQVEsRUFBRSxFQUFFO0lBQ3ZDLElBQUksUUFBUSxHQUFHO1FBQ1gsVUFBVSxFQUFFLE1BQU07UUFDbEIsT0FBTyxFQUFFO1lBQ0wsY0FBYyxFQUFFLFdBQVc7U0FDOUI7UUFDRCxJQUFJLEVBQUUsSUFBSTtLQUNiLENBQUM7SUFDRixPQUFPLFFBQVEsQ0FBQztBQUNsQixDQUFDLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyJjb25zdCBBV1MgPSByZXF1aXJlKCdhd3Mtc2RrJylcclxuQVdTLmNvbmZpZy5yZWdpb24gPSBwcm9jZXNzLmVudi5BV1NfUkVHSU9OIHx8ICd1cy1lYXN0LTEnXHJcbmNvbnN0IGV2ZW50YnJpZGdlID0gbmV3IEFXUy5FdmVudEJyaWRnZSgpXHJcbmV4cG9ydCB7fTtcclxuXHJcbmV4cG9ydHMuaGFuZGxlciA9IGFzeW5jIChldmVudDphbnksIGNvbnRleHQ6YW55KSA9PiB7XHJcbiAgY29uc3QgRVJST1JfVEhSRVNIT0xEID0gMztcclxuICBjb25zdCBzZXJ2aWNlVVJMID0gJ3d3dy5nb29nbGUuY29tJztcclxuICBsZXQgcmVzcG9uc2U7XHJcblxyXG4gIC8vIGNyZWF0ZSBBV1MgU0RLIGNsaWVudHNcclxuICBjb25zdCBkeW5hbW8gPSBuZXcgQVdTLkR5bmFtb0RCKCk7XHJcbiAgY29uc3Qgc2Vjb25kc1NpbmNlRXBvY2ggPSBNYXRoLnJvdW5kKERhdGUubm93KCkgLyAxMDAwKTtcclxuXHJcbiAgLy8gV2UgYXJlIHF1ZXJ5aW5nIG91ciBlcnJvciBEeW5hbW8gdG8gY291bnQgaG93IG1hbnkgZXJyb3JzIGFyZSBpbiB0aGVyZSBmb3Igd3d3Lmdvb2dsZS5jb21cclxuICB2YXIgZHluYW1vUGFyYW1zID0ge1xyXG4gICAgRXhwcmVzc2lvbkF0dHJpYnV0ZVZhbHVlczoge1xyXG4gICAgIFwiOnYxXCI6ICB7XCJTXCI6c2VydmljZVVSTH0sXHJcbiAgICAgXCI6bm93XCI6IHtcIk5cIjpzZWNvbmRzU2luY2VFcG9jaC50b1N0cmluZygpfVxyXG4gICAgfSwgXHJcbiAgICBLZXlDb25kaXRpb25FeHByZXNzaW9uOiBcIlNpdGVVcmwgPSA6djEgYW5kIEV4cGlyYXRpb25UaW1lID4gOm5vd1wiLCBcclxuICAgIEluZGV4TmFtZTogXCJVcmxJbmRleFwiLFxyXG4gICAgVGFibGVOYW1lOiBwcm9jZXNzLmVudi5UQUJMRV9OQU1FLFxyXG4gICB9O1xyXG5cclxuICBjb25zdCByZWNlbnRFcnJvcnMgPSBhd2FpdCBkeW5hbW8ucXVlcnkoZHluYW1vUGFyYW1zKS5wcm9taXNlKCk7XHJcbiAgXHJcbiAgY29uc29sZS5sb2coJy0tLSBSZWNlbnQgRXJyb3JzIC0tLScpO1xyXG4gIGNvbnNvbGUubG9nKHJlY2VudEVycm9ycy5Db3VudCk7XHJcbiAgY29uc29sZS5sb2coSlNPTi5zdHJpbmdpZnkocmVjZW50RXJyb3JzKSk7XHJcbiAgXHJcbiAgLy8gSWYgd2UgYXJlIHdpdGhpbiBvdXIgZXJyb3IgdGhyZXNob2xkLCBtYWtlIHRoZSBodHRwIGNhbGxcclxuICBpZihyZWNlbnRFcnJvcnMuQ291bnQgPCBFUlJPUl9USFJFU0hPTEQpe1xyXG4gICAgbGV0IGVycm9yVHlwZSA9ICcnO1xyXG4gICAgXHJcbiAgICAvLyBJbiBoZXJlIGFzc3VtZSB3ZSBtYWRlIGFuIGh0dHAgcmVxdWVzdCB0byBnb29nbGUgYW5kIGl0IHdhcyBkb3duLCBcclxuICAgIC8vIDEwIHNlYyBoYXJkIGNvZGVkIGRlbGF5IGZvciBzaW11bGF0aW9uXHJcbiAgICBjb25zdCBmYWtlU2VydmljZUNhbGwgPSBhd2FpdCBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XHJcbiAgICAgIGNvbnNvbGUubG9nKCctLS0gQ2FsbGluZyBXZWJzZXJ2aWNlLCByZWNlbnQgZXJyb3JzIGJlbG93IHRocmVzaG9sZCAtLS0nKTtcclxuICAgICAgc2V0VGltZW91dCggZnVuY3Rpb24oKSB7XHJcbiAgICAgICAgcmVqZWN0KFwic2VydmljZSB0aW1lb3V0IGV4Y2VwdGlvblwiKVxyXG4gICAgICB9LCAxMDAwMCkgXHJcbiAgICB9KS5jYXRjaCgocmVhc29uKT0+IHtcclxuICAgICAgY29uc29sZS5sb2coJy0tLSBTZXJ2aWNlIENhbGwgRmFpbHVyZSAtLS0nKTtcclxuICAgICAgY29uc29sZS5sb2cocmVhc29uKTtcclxuICAgICAgZXJyb3JUeXBlID0gcmVhc29uO1xyXG4gICAgfSk7XHJcbiAgXHJcbiAgICAvLyBCdWlsZGluZyBvdXIgZmFpbHVyZSBldmVudCBmb3IgRXZlbnRCcmlkZ2VcclxuICAgIHZhciBwYXJhbXMgPSB7XHJcbiAgICAgIEVudHJpZXM6IFtcclxuICAgICAgICB7XHJcbiAgICAgICAgICBEZXRhaWxUeXBlOiAnaHR0cGNhbGwnLFxyXG4gICAgICAgICAgRXZlbnRCdXNOYW1lOiAnZGVmYXVsdCcsXHJcbiAgICAgICAgICBTb3VyY2U6ICdjZGtwYXR0ZXJucy5ldmVudGJyaWRnZS5jaXJjdWl0YnJlYWtlcicsXHJcbiAgICAgICAgICBUaW1lOiBuZXcgRGF0ZSgpLFxyXG4gICAgICAgICAgLy8gTWFpbiBldmVudCBib2R5XHJcbiAgICAgICAgICBEZXRhaWw6IEpTT04uc3RyaW5naWZ5KHtcclxuICAgICAgICAgICAgc3RhdHVzOiAnZmFpbCcsXHJcbiAgICAgICAgICAgIHNpdGVVcmw6IHNlcnZpY2VVUkwsXHJcbiAgICAgICAgICAgIGVycm9yVHlwZTogZXJyb3JUeXBlXHJcbiAgICAgICAgICB9KVxyXG4gICAgICAgIH1cclxuICAgICAgXVxyXG4gICAgfTtcclxuICBcclxuICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IGV2ZW50YnJpZGdlLnB1dEV2ZW50cyhwYXJhbXMpLnByb21pc2UoKTtcclxuICBcclxuICAgIGNvbnNvbGUubG9nKCctLS0gRXZlbnRCcmlkZ2UgUmVzcG9uc2UgLS0tJylcclxuICAgIGNvbnNvbGUubG9nKHJlc3VsdCkgIFxyXG4gICAgcmVzcG9uc2UgPSBzZW5kUmVzKDUwMCwgJ1NvbWV0aGluZyBhcHBlYXJzIHRvIGJlIHdyb25nIHdpdGggdGhpcyBzZXJ2aWNlLCBwbGVhc2UgdHJ5IGFnYWluIGxhdGVyJyk7XHJcbiAgfSBlbHNlIHtcclxuICAgIGNvbnNvbGUubG9nKCdDaXJjdWl0IGN1cnJlbnRseSBjbG9zZWQsIHNlbmRpbmcgYmFjayBmYWlsdXJlIHJlc3BvbnNlJyk7XHJcbiAgICByZXNwb25zZSA9IHNlbmRSZXMoNTAwLCAnVGhpcyBzZXJ2aWNlIGhhcyBiZWVuIGV4cGVyaWVuY2luZyBpc3N1ZXMgZm9yIGEgd2hpbGUsIHdlIGhhdmUgY2xvc2VkIHRoZSBjaXJjdWl0Jyk7XHJcbiAgfVxyXG5cclxuICByZXR1cm4gcmVzcG9uc2U7XHJcbn1cclxuXHJcbmNvbnN0IHNlbmRSZXMgPSAoc3RhdHVzOmFueSwgYm9keTphbnkpID0+IHtcclxuICB2YXIgcmVzcG9uc2UgPSB7XHJcbiAgICAgIHN0YXR1c0NvZGU6IHN0YXR1cyxcclxuICAgICAgaGVhZGVyczoge1xyXG4gICAgICAgICAgXCJDb250ZW50LVR5cGVcIjogXCJ0ZXh0L2h0bWxcIlxyXG4gICAgICB9LFxyXG4gICAgICBib2R5OiBib2R5XHJcbiAgfTtcclxuICByZXR1cm4gcmVzcG9uc2U7XHJcbn07XHJcbiJdfQ==