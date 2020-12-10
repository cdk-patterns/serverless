# The Predictive Lambda Pattern

![architecture](img/arch.png)

This is a pattern that uses a container inside Lambda to deploy a custom Python ML model to predict the nearest Chipotle restaurant based on your lat/long.

Some Useful References:

| Author        | Link           |
| ------------- | ------------- |
| AWS Blog | [New for AWS Lambda – Container Image Support](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) |
| AWS Docs | [Lambda now supports container images](https://aws.amazon.com/about-aws/whats-new/2020/12/aws-lambda-now-supports-container-images-as-a-packaging-format/) |
| Julian Wood | [Working with lambda layers and extensions in container images](https://aws.amazon.com/blogs/compute/working-with-lambda-layers-and-extensions-in-container-images/) |
| Michael Hart | [Using container images with aws lambda](https://hichaelmart.medium.com/using-container-images-with-aws-lambda-7ffbd23697f1) |
| Yan Cui | [Package your Lambda function as a container image](https://lumigo.io/blog/package-your-lambda-function-as-a-container-image/) |
| Scikit Learn Docs | [User Guide](https://scikit-learn.org/stable/user_guide.html) |
| AWS ECR Gallery | [Python Lambda Image](https://gallery.ecr.aws/lambda/python) |
| Docker Docs | [CLI Reference](https://docs.docker.com/reference/) |


# Available Versions

* [TypeScript](typescript)
* [Python](python)

## Desconstructing The Predictive Lambda
If you want a walkthrough of the theory, the code and finally a demo of the deployed implementation check out:

[![Alt text](https://img.youtube.com/vi/FgP6zetWSXY/0.jpg)](https://www.youtube.com/watch?v=FgP6zetWSXY)


## What's Included In This Pattern?
This pattern uses sklearn to create a custom k nearest neighbour model to predict the nearest Chipotle to a given Latitude and Longitude. The model is deployed inside a container attached to AWS Lambda.

### The Data
If you want to look at the data used for this model you can look at the [jupyter notebook](typescript/model/training/Chipotle.ipynb), the raw data came from [kaggle](https://www.kaggle.com/jeffreybraun/chipotle-locations)

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

## Deep Dive WalkThrough

There are 3 separate processes included in this pattern

1. A scripted process to train and export a ML model from inside the Lambda Python image for runtime compatibility
2. A Dockerfile to take that exported model and use it inside a containerised lambda function
3. A CDK implementation to deploy an API Gateway and the above Lambda

### Model Training - Completely Optional

> I have included a pre-trained model in this pattern so you only need to do this if you want to understand how I did it or you want to try it with your own model.

If you look inside the model folder there is a shell script called trainmodel.sh, running this script (making sure you have docker started) will completely retrain the model.

```bash
cd model
./trainmodel.sh
```

The code in this shell script looks worse than it is

```bash
#Using the named TrainingDockerfile, build this image and tag it as chipotle
docker build . -f TrainingDockerfile -t chipotle
#We need the image id, so query docker for an image tagged with chipotle
IMAGE_ID=$(docker images -q chipotle)
#Start the image as a background process named training
docker run -d --name 'training' ${IMAGE_ID} 'app.handler'
#Copy the trained model out of the container
docker cp training:/var/task/chipotle.pkl chipotle.pkl
#stop the running instance and delete it
docker kill training && docker rm training
```

The next place to look is TrainingDockerfile

```docker
# Use the python lambda image from AWS ECR
FROM public.ecr.aws/lambda/python:3.6
# Put these 3 files inside the container
COPY training/training.py requirements.txt training/chipotle_stores.csv ./
# Install python dependencies
RUN pip3 install -r requirements.txt
# Run the training logic
RUN python3 training.py
```

If you want to look at the data inside chipotle_stores.csv you can look at the [jupyter notebook](typescript/model/training/Chipotle.ipynb), the raw data came from [kaggle](https://www.kaggle.com/jeffreybraun/chipotle-locations)

The training logic inside training/training.py loads chipotle_stores.csv into Python, cleans it up and then trains/exports a model. The training/export logic is

```python
#train model
model = KNeighborsClassifier(n_neighbors=2, weights="distance", algorithm="auto")
model.fit(train_set_no_labels, train_set_labels)

#export model
joblib.dump(model, 'chipotle.pkl')
```

### Containerised Lambda Function

Most of the logic to make this happen is in model/Dockerfile

```docker
FROM public.ecr.aws/lambda/python:3.6
# copy our function logic, requirements and model into the container
COPY deployment/app.py requirements.txt chipotle.pkl ./
# install the dependencies
RUN pip3 install -r requirements.txt
# the lambda handler is located inside app.py as a method called lambdaHandler
CMD ["app.lambdaHandler"]
```

The actual lambda handler code inside deployment/app.py is the same as any other lambda function

```python
import joblib

def lambdaHandler(event, context):
    model = joblib.load('chipotle.pkl')

    try:
        latitude = event["queryStringParameters"]['lat']
    except KeyError:
        latitude = 0

    try:
        longitude = event["queryStringParameters"]['long']
    except KeyError:
        longitude = 0

    prediction = model.predict([[latitude,longitude]])
    prediction = prediction.tolist()
    return {'body': str(prediction[0]), 'statusCode': 200}
```

### CDK Infra Logic

The relevant piece of CDK is that instead of the normal way of creating our function, we use lambda.DockerImageFunction and ask CDK to build our container from the model folder

```typescript
// defines an AWS Lambda resource
const predictiveLambda = new lambda.DockerImageFunction(this, 'PredictiveLambda', {
    code: lambda.DockerImageCode.fromImageAsset(path.join(__dirname, '../model')),
    memorySize:4096,
    timeout: cdk.Duration.seconds(15)
})
```
