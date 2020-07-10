# Polly Pattern

![overview image](img/overview.png)

This is a pattern that integrates the Amazon Polly service into an AWS Lambda Function so that you can translate text into speech using a serverless stack

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| Amazon Polly | [Amazon Polly Site](https://aws.amazon.com/polly/) |
| Pricing | [Polly Pricing](https://aws.amazon.com/polly/pricing/) |
| Permissions | [Polly IAM Permissions](https://docs.aws.amazon.com/polly/latest/dg/api-permissions-reference.html) |
| AWS Blogs | [Giving your content a voice with the Newscaster speaking style from Amazon Polly](https://aws.amazon.com/blogs/machine-learning/giving-your-content-a-voice-with-the-newscaster-speaking-style-from-amazon-polly/) |
| Timothy Mugayi | [Text-to-Speech: Build Apps That Talk With AWS Polly and Node.js](https://medium.com/better-programming/text-to-speech-build-apps-that-talk-with-aws-polly-and-node-js-a9cdab99af04 ) |
| Philip Kiely | [Text-To-Speech With AWS (Part 1)](https://www.smashingmagazine.com/2019/08/text-to-speech-aws/) |

# Available Versions

* [TypeScript](typescript)
* [Python](python)

## What is Included In This Pattern?

After deployment you will have an API Gateway HTTP API configured where all traffic points to a Lambda Function that calls the Polly service.

### API Gateway HTTP API
This is setup with basic settings where all traffic is routed to our Lambda Function

### Lambda Function
Takes in whatever voice you want and whatever text you want, sends it to the Polly service and returns an Audio stream

## Testing The Pattern

After deployment in the deploy logs you will see the url for the API Gateway.

If you open that URL in chrome it will play an audio recording saying &quot;To hear your own script, you need to include text in the message body of your restful request to the API Gateway&quot;

You can customise this message based on how you call the url:

### Changing the voice
You can pick from 3 voices "Matthew" (the default), "Joanna" or "Lupe".

To change voices just add a query param onto your url like:

```
https://{api-url}/?voice=Lupe
https://{api-url}/?voice=Joanna
https://{api-url}/?voice=Matthew
```

### Changing the text
If you use a tool like Postman to send text in the body of a POST request to the url it will use Polly to synthesize your text