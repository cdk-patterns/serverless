export {};
const AWSXRay = require('aws-xray-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let records: any[] = event.Records;
  
  for(let index in records) {

    let traceHeaderStr = records[index].attributes.AWSTraceHeader;
    const traceData = AWSXRay.utils.processTraceData(traceHeaderStr);
    const segment = new AWSXRay.Segment("SQS", traceData.Root, traceData.Parent);
    const subscriberSegment = segment.addNewSubsegment('Logging SQS Message');
    console.log('received message ' + records[index].body);  

    subscriberSegment.addMetadata("message", records[index].body)
  }
};