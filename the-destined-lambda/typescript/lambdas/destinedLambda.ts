exports.handler = async (event:any, context:any, callback:any) => {
  console.log('Event Received')
  console.log(event);
    //throw new Error('test');
    return {
      source: 'cdkpatterns.the-destined-lambda',
      action: 'message',
      message: 'hello world'
    };
  };