import boto3
import sys
import base64

polly_c = boto3.client('polly')
translate_c = boto3.client('translate')

def handler(event, context):
    try:
        voice = event["queryStringParameters"]["voice"]
    except KeyError:
        voice = 'Matthew'

    try:
        translate_from = event["queryStringParameters"]["translateFrom"]
    except KeyError:
        translate_from = 'en'

    try:
        translate_to = event["queryStringParameters"]["translateTo"]
    except KeyError:
        translate_to = 'en'
        
    try:
        text = event['body']
    except KeyError:
        text = 'To hear your own script, you need to include text in the message body of your restful request to the API Gateway'
        
    # Only perform a translation if the languages are different
    if translate_to != translate_from:
        text = translate_text(text, translate_from, translate_to)

    speech = convert_text_to_speech(voice, text)
    
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'audio/mpeg' },
        'body': base64.b64encode(speech),
        'isBase64Encoded': True
    }

def translate_text(text, translate_from, translate_to):
    response = translate_c.translate_text(
        Text=text,
        SourceLanguageCode=translate_from,
        TargetLanguageCode=translate_to
    )

    return response['TranslatedText']

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
