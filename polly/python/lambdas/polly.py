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
        text = 'To hear your own script, you need to include text in the message body of your restful request to the API Gateway'
        
    speech = convert_text_to_speech(voice, text)
    
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'audio/mpeg' },
        'body': base64.b64encode(speech),
        'isBase64Encoded': True
    }

def convert_text_to_speech(voice, text):
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
