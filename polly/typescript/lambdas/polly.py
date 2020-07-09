import boto3
import sys
import base64

polly_c = boto3.client('polly')

def handler(event, context):
    try:
        voice = event["queryStringParameters"]["voice"]
    except KeyError:
        voice = 'Matthew'
        
    try:
        text = event['body']
    except KeyError:
        text = 'you need to include text in your message body'
        
    print(voice)
    print(text)
        
    translation = translate(voice, text)
    
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'audio/mpeg' },
        'body': base64.b64encode(translation),
        'isBase64Encoded': True
    }

def translate(voice, text):
    if voice not in ['Joanna', 'Matthew', 'Lupe']:
        print('Only Joanna, Matthew and Lupe support the newscaster style')
        sys.exit(1)
    response = polly_c.synthesize_speech(
                   VoiceId=voice,
                   Engine='neural',
                   OutputFormat='mp3',
                   TextType='ssml',
                   Text = f'<speak><amazon:domain name="news">{text}></amazon:domain></speak>')

    return response['AudioStream'].read()
    #f = open('newscaster.mp3', 'wb')
    #f.write(response['AudioStream'].read())
    #f.close()
