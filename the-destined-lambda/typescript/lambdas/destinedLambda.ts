exports.handler = async (event:any, context:any, callback:any) => {
    //throw new Error('test');
    return JSON.stringify({
      source: 'cdkpatterns.the-destined-lambda',
      action: 'message',
      message: 'hello world'
    });
  };