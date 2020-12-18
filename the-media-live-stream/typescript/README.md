# The Media Live Stream

This is an example of how to deploy a Serverless environment to stream live event content.

![architecture](img/the-media-live-stream.png)

## Warnings
1. This CDK stack doesn't automatically start its medialive channel. AWS charges for a medialive "live/started" channel whether you are using it or not, so you must start manually using Console, CLI or SDK. Check prices here: https://aws.amazon.com/medialive/pricing/    
2. This CDK stack is just to demonstrate how to create a Serverless broadcast enviroment, so I wrote using a single channel and 2 high definitions. If you need to deploy it in production, I suggest that you learn more about AWS MediaLive Services here: https://www.aws.training/LearningLibrary?filters=language%3A1&filters=classification%3A75&tab=view_all  
3. Don't forget and leave your medialive channel opened, AWS will charge you!   
4. You can attach a CloudFront to the MediaPackage distribution or set S3 as backup of medialive stream. In the future I'll update this stack.  
5. If you have some doubts about MediaLive Services, feel free to send me a message (https://github.com/leandrodamascena).
6. Before destroying this Stack, you must stop your LiveChannel, otherwise CloudFormation will generate an error.

Let's party! :D

## Stacks

This pattern uses assets, so you must run `cdk bootstrap account/region` before run the other commands. 

Due to this pattern creating the media package and then using the streaming url on a demo webpage, it was split into two stacks. This does not affect the deployment command however and you can still just do:

```bash
npm run deploy
```


### TheMediaLiveStreamStack
This defines all the elements to create the LiveStream channel. The parameters below can be modified to launch this stack:


    "id_channel": "test-channel",  # ChannelId
    "ip_sg_input": "0.0.0.0/0",  # IP Ingress to channel
    "stream_name": "test/channel", # Stream/Key to OBStudio
    "hls_segment_duration_seconds": 5,
    "hls_playlist_window_seconds": 60,
    "hls_max_video_bits_per_second": 2147483647,
    "hls_min_video_bits_per_second": 0,
    "hls_stream_order": "ORIGINAL"


### TheMediaLiveStreamWebsiteStack
This stack deploys the website that is used to test your stream

## Manual Steps After Deployment

This Stack doesn't start your channel automatically due to costs, so open MediaLive in the AWS Console and click the Channels link in the sidebar. Click "test-channel" and now click the orange start button in the top right to start the channel. **Remember to stop your channel after you are done testing as it charges per second**

 Now click Inputs in the sidebar and you should see "input-test-channel" in a list - copy the "Destination A" URL ignoring the "channel" at the end (if the url is rmtp://x.x.x.x/test/channel you copy rmtp://x.x.x.x/test/). Go to OBS Studio and paste this URL (channel is the key). In this example I used OBS Studio, but you can use any type of software that supports RMTP PUSH protocol.

![obs1](img/obs1.png)
![obs2](img/obs2.png)

After that go to AWS Console -> AWS Elemental MediaLive -> Channels -> channel1 and Start the channel.

## Results

I simulated transmitting my screen: D

![live1](img/live1.png)
![live2](img/live2.png)
![live3](img/live3.png)
![live4](img/live4.png)

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`  deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template