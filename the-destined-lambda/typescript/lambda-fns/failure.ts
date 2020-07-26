export {};

exports.handler = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));
}