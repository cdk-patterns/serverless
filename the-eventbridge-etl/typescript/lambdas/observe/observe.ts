export {};

/**
 * This is a lambda that subscribes to every eventbridge etl event that is sent and logs them in one place
 */
exports.handler = async (event:any) => {
    console.log(JSON.stringify(event, null, 2));
}