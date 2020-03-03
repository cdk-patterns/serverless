export {};

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let records: any[] = event.Records;
  
  for(let index in records) {
    let payload = records[index].body;
    console.log('received message ' + payload);
  }
};