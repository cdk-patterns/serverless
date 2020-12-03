# The Predictive Lambda Pattern

![architecture](img/arch.png)

This is a pattern that uses a container inside Lambda to deploy a custom Python ML model to predict the nearest Chipotle restaurant based on your lat/long.

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| AWS Blog | [New for AWS Lambda – Container Image Support](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) |
| AWS Docs | [Lambda now supports container images](https://aws.amazon.com/about-aws/whats-new/2020/12/aws-lambda-now-supports-container-images-as-a-packaging-format/) |
| Yan Cui | [Package your Lambda function as a container image](https://lumigo.io/blog/package-your-lambda-function-as-a-container-image/) |
| Scikit Learn Docs | [User Guide](https://scikit-learn.org/stable/user_guide.html) |
| AWS ECR Gallery | [Python Lambda Image](https://gallery.ecr.aws/lambda/python) |
| Docker Docs | [CLI Reference](https://docs.docker.com/reference/) |

## What's Included In This Pattern?
This pattern uses sklearn to create a custom k nearest neighbour model to predict the nearest Chipotle to a given Latitude and Longitude. The model is deployed inside a container attached to AWS Lambda.

### The Data
If you want to look at the data used for this model you can look at the [jupyter notebook](model/training/Chipotle.ipynb), the raw data came from [kaggle](https://www.kaggle.com/jeffreybraun/chipotle-locations)

### The ML Model
This is a very simple model to demonstrate the concept (I didn't even check the accuracy because it doesn't change the pattern). It uses [sklearn nearest neighbors](https://scikit-learn.org/stable/modules/neighbors.html) to predict the closest Chipotle location to a given lat/long

### Two Docker Containers
I use the Lambda image to train the ML model in one container and then I use a separate container for the deployed Lambda Function. The reason I do this is because it means that you know you have pickled your model in the same environment it will be deployed but you can use things that wont be packaged into your deployed function keeping it as lightweight as possible. You will also have a built container image containing the raw data, the training logic and the trained model. These images could be archived to have a history of your model.

### A Lambda Function
I have this setup with a 15 second timeout and 4GB ram to comfortably run our model

### An API Gateway HTTP API
Setup as a proxy integration, all requests hit the Lambda Function

## How Do I Test This Pattern?

do "npm run deploy" from the base directory and you will have the url for an API Gateway output into the logs or in the CloudFormation console. Open that url in a browser but add "?lat=39.153198&long=-77.066176" to the end and you should get back a prediction.

## How Does It Work?

Most of the logic for this lives in the model folder. There are two Dockerfiles:
- Dockerfile - used by Lambda during the deploy
- TrainingDockerfile - used to spin up the container to train our model

I have added the trained model to version control but if you want to retrain it yourself what you have to do is make sure docker is running and:

```bash
cd model
./trainmodel.sh
```

This uses the Lambda Python image to run the file training/training.py and then copy the chipotle.pkl file out of the container. The requirements.txt is shared between the training container and the deployed container.

The actual logic that runs when we hit our url is in model/deployment/app.py, it unpickles the model, makes a prediction and returns the response as a string.

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `npm run deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
