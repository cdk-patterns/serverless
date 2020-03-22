"use strict";
/*
* Notice that there is no mention of EventBridge in this file yet it is integrated through lambda destinations
*/
exports.handler = async (event, context, callback) => {
    var _a;
    console.log('Event Received');
    console.log(JSON.stringify(event));
    let records = event.Records;
    //SNS can send multiple records
    for (let index in records) {
        let message = (_a = records[index]) === null || _a === void 0 ? void 0 : _a.Sns.Message;
        if (message == 'please fail') {
            console.log('received failure flag, throwing error');
            throw new Error('test');
        }
    }
    return {
        source: 'cdkpatterns.the-destined-lambda',
        action: 'message',
        message: 'hello world'
    };
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGVzdGluZWRMYW1iZGEuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJkZXN0aW5lZExhbWJkYS50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxDQUFDLE9BQU8sR0FBRyxLQUFLLEVBQUUsS0FBUyxFQUFFLE9BQVcsRUFBRSxRQUFZLEVBQUUsRUFBRTs7SUFDL0QsT0FBTyxDQUFDLEdBQUcsQ0FBQyxnQkFBZ0IsQ0FBQyxDQUFBO0lBQzdCLE9BQU8sQ0FBQyxHQUFHLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDO0lBRW5DLElBQUksT0FBTyxHQUFVLEtBQUssQ0FBQyxPQUFPLENBQUM7SUFFbkMsK0JBQStCO0lBQy9CLEtBQUksSUFBSSxLQUFLLElBQUksT0FBTyxFQUFFO1FBQ3hCLElBQUksT0FBTyxTQUFHLE9BQU8sQ0FBQyxLQUFLLENBQUMsMENBQUUsR0FBRyxDQUFDLE9BQU8sQ0FBQztRQUMxQyxJQUFHLE9BQU8sSUFBSSxhQUFhLEVBQUM7WUFDMUIsT0FBTyxDQUFDLEdBQUcsQ0FBQyx1Q0FBdUMsQ0FBQyxDQUFDO1lBQ3JELE1BQU0sSUFBSSxLQUFLLENBQUMsTUFBTSxDQUFDLENBQUM7U0FDekI7S0FDRjtJQUVELE9BQU87UUFDTCxNQUFNLEVBQUUsaUNBQWlDO1FBQ3pDLE1BQU0sRUFBRSxTQUFTO1FBQ2pCLE9BQU8sRUFBRSxhQUFhO0tBQ3ZCLENBQUM7QUFDSixDQUFDLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyJleHBvcnRzLmhhbmRsZXIgPSBhc3luYyAoZXZlbnQ6YW55LCBjb250ZXh0OmFueSwgY2FsbGJhY2s6YW55KSA9PiB7XG4gIGNvbnNvbGUubG9nKCdFdmVudCBSZWNlaXZlZCcpXG4gIGNvbnNvbGUubG9nKEpTT04uc3RyaW5naWZ5KGV2ZW50KSk7XG5cbiAgbGV0IHJlY29yZHM6IGFueVtdID0gZXZlbnQuUmVjb3JkcztcblxuICAvL1NOUyBjYW4gc2VuZCBtdWx0aXBsZSByZWNvcmRzXG4gIGZvcihsZXQgaW5kZXggaW4gcmVjb3Jkcykge1xuICAgIGxldCBtZXNzYWdlID0gcmVjb3Jkc1tpbmRleF0/LlNucy5NZXNzYWdlO1xuICAgIGlmKG1lc3NhZ2UgPT0gJ3BsZWFzZSBmYWlsJyl7XG4gICAgICBjb25zb2xlLmxvZygncmVjZWl2ZWQgZmFpbHVyZSBmbGFnLCB0aHJvd2luZyBlcnJvcicpO1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCd0ZXN0Jyk7XG4gICAgfVxuICB9XG5cbiAgcmV0dXJuIHtcbiAgICBzb3VyY2U6ICdjZGtwYXR0ZXJucy50aGUtZGVzdGluZWQtbGFtYmRhJyxcbiAgICBhY3Rpb246ICdtZXNzYWdlJyxcbiAgICBtZXNzYWdlOiAnaGVsbG8gd29ybGQnXG4gIH07XG59OyJdfQ==