const { Polly } = require('aws-sdk');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  let text = event?.body ?? "you need to include text in your message body";
  let voice = event?.queryStringParameters?.voice ?? "Matthew";

  const validVoices = ['Joanna', 'Matthew', 'Lupe'];

  if(!validVoices.includes(voice)){
    sendRes(400, 'Only Joanna, Matthew and Lupe support the newscaster style')
  }

  // create AWS SDK clients
  const polly = new Polly();

  const params = {
    OutputFormat: 'mp3',
    Engine:'neural',
    Text: text,
    TextType:'ssml',
    VoiceId: voice,
  };

  let synthesis = await polly.synthesizeSpeech(params).promise();

  let audioStream = new Buffer(synthesis.AudioStream);
  let base64data = audioStream.toString('base64');

  return sendVoicdRes(200, base64data);
};

const sendVoicdRes = (status:number, body:string) => {
  var response = {
    statusCode: status,
    headers: {
      "Content-Type": "audio/mpeg",
    },
    body: body,
    isBase64Encoded: true
  };
  return response;
};

const sendRes = (status:number, body:string) => {
    var response = {
      statusCode: status,
      headers: {
        "Content-Type": "text/html"
      },
      body: body
    };
    return response;
  };