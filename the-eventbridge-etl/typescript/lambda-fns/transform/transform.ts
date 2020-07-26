const AWS = require('aws-sdk')
export{};
AWS.config.region = process.env.AWS_REGION || 'us-east-1'
const eventbridge = new AWS.EventBridge()

exports.handler = async (event:any) => {
    console.log(JSON.stringify(event, null, 2))

    const headers:string = event.detail.headers;
    const data:string = event.detail.data;

    let headerArray = headers.split(',');
    let dataArray = data.split(',');
    let transformedObject:any = {};

    for(let index in headerArray) {
        transformedObject[headerArray[index]] = dataArray[index];
    }

    // Building our transform event for EventBridge
    var params = {
        Entries: [
          {
            DetailType: 'transform',
            EventBusName: 'default',
            Source: 'cdkpatterns.the-eventbridge-etl',
            Time: new Date(),
            // Main event body
            Detail: JSON.stringify({
              status: 'transformed',
              data: transformedObject
            })
          }
        ]
    };
    
    const result = await eventbridge.putEvents(params).promise();
    console.log(result);

}