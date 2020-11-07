# The Media Live Stream

This is an example of how to deploy a Serverless environment to stream live event content.

![architecture](img/the-media-live-stream.png)

## Warnings
1 - This CDK stack doesn't automatically start its medialive channel. AWS charges for a medialive "live/started" channel whether you are using it or not, so you must start manually using Console, CLI or SDK. Check prices here: https://aws.amazon.com/medialive/pricing/    
2 - This CDK stack is just to demonstrate how to create a Serverless broadcast enviroment, so I wrote using a single channel and 2 high definitions. If you need to deploy it in production, I suggest that you learn more about AWS MediaLive Services here: https://www.aws.training/LearningLibrary?filters=language%3A1&filters=classification%3A75&tab=view_all  
3 - Don't forget your medialive channel opened, AWS will charge you!   
4 - You can attach a CloudFront to the MediaPackage distribution or set S3 as backup of medialive stream. In the future I'll update this stack.  
5 - If you have some doubts about MediaLive Services, feel free to send me a message. 

Let's party! :D

## Commands

This stack uses assets (CustomResources + SdkCall) so you must run `cdk bootstrap account/region` before run `cdk deploy`.

To deploy this stack run `cdk deploy`. After the deploy you'll see de URL of Bucket to access the website.

## Manual steps

As I said at the beginning, this Stack doesn't start your channel automatically, so go to AWS Console -> AWS Elemental MediaLive -> Inputs -> input-test1 and copy the endpoint URL. Go to OBS Studio and paste this URL (bbb is the key). In this example I used OBS Studio, but you can use any type of software that supports RMTP PUSH protocol.

![obs1](img/obs1.png)
![obs2](img/obs2.png)

After that go to AWS Console -> AWS Elemental MediaLive -> Channels -> channel1 and Start the channel.

## Results

I simulated transmitting my screen: D

![live1](img/live1.png)
![live2](img/live2.png)
![live3](img/live3.png)
![live4](img/live4.png)