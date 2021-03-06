# The State Machine

This is an example CDK stack to deploy The State Machine stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#statemachine

You would use this pattern if you can do your processing asynchronously and you need to have different flows in your logic.

![Architecture](img/the-state-machine-arch.png)

### Stepfunction Logic
![Architecture](img/statemachine.png)


### Testing It Out

After deployment you should have a proxy api gateway where any url hits a lambda which triggers a step function. You can pass in a queryparameter like '?flavour=pepperoni' or '?flavour=pineapple'.

If you pass in pineapple or hawaiian you should see the step function flow fail when you check it via the console.


# Useful commands

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
    cd serverless/the-scalable-webhook/csharp
    ```
* Build the project to see if .NET Core has been setup correctly (optional)
    ```
    dotnet build src
    ```
* Deploy the stack
    ```
    cdk deploy
    ```
