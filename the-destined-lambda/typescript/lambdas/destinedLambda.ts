exports.handler = async (event:any, context:any) => {
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
    return "{'value': 'test'}";
  };