export {};
const AWSXRay = require('aws-xray-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let records: any[] = event.Records;
  
  for(let index in records) {

    // Try and get our trace information associated to the right parent
    let traceHeaderStr = records[index].attributes.AWSTraceHeader;
    let traceData = AWSXRay.utils.processTraceData(traceHeaderStr);
    const segment = new AWSXRay.Segment('Logging SQS Message', traceData.Root, traceData.Parent);
    AWSXRay.middleware.resolveSampling(traceData, segment);
    console.log('received message ' + records[index].body);  

    segment.addMetadata("message", records[index].body)

    segment.close();
  }
};