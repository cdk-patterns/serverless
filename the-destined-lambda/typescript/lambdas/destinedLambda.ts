exports.handler = async (event:any, context:any, callback:any) => {
    const response = {
        // Event envelope fields
        Source: 'cdkpatterns.the-destined-lambda',
        EventBusName: 'default',
        DetailType: 'event',
        Time: new Date(),
  
        // Main event body
        Detail: JSON.stringify({
          action: 'message',
          message: 'hello world'
        })
    };
    //throw new Error('test');
    return "{'value': 'test'}";
  };