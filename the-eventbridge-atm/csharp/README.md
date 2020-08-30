
# The EventBridge ATM

This is an example CDK stack to deploy the code from this blogpost by [James Beswick](https://twitter.com/jbesw)- https://aws.amazon.com/blogs/compute/integrating-amazon-eventbridge-into-your-serverless-applications/

In this example, a banking application for automated teller machine (ATM) produces events about transactions. It sends the events to EventBridge, which then uses rules defined by the application to route accordingly. There are three downstream services consuming a subset of these events.

![Architecture](img/amazon-eventbridge-custom-application-2.png)

## When You Would Use This Pattern

EventBridge is an awesome centralised service for routing events between various consumers based on rules. You could set up an EventBridge within your domain and then accessing events within that domain is as easy as a rule in EventBridge, this significantly cuts down on the number of coupled interactions you have between your various services.

## How to test pattern 

After deployment you will have an api gateway where hitting any endpoint triggers the events to be sent to EventBridge defined in lambdas/atmProducer/events.js

* All Approved transactions go to consumer 1
* NY Transactions go to consumer 2
* Declined transactions go to consumer 3

## Useful commands

* `dotnet build src` compile this app
* `cdk deploy`       deploy this stack to your default AWS account/region
* `cdk diff`         compare deployed stack with current state
* `cdk synth`        emits the synthesized CloudFormation template

## Deploy with AWS Cloud9

* Create an **Ubuntu** AWS Cloud9 EC2 development environment
* Add the Microsoft repository
    ```
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
    ```
    ```
    sudo dpkg -i packages-microsoft-prod.deb
    ```
* Install the .NET Core SDK
    ```
    sudo apt-get update; \
    sudo apt-get install -y apt-transport-https && \
    sudo apt-get update && \
    sudo apt-get install -y dotnet-sdk-3.1
    ```
* Clone the CDK Patterns repo
    ```
    git clone https://github.com/cdk-patterns/serverless.git
    ```
* Change directory
    ```
    cd serverless/the-eventbridge-atm/csharp
    ```
* Build the project to see if .NET Core has been setup correctly (optional)
    ```
    dotnet build src
    ```
* Deploy the stack
    ```
    cdk deploy
    ```
