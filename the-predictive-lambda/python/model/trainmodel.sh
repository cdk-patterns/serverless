docker build . -f TrainingDockerfile -t chipotle
IMAGE_ID=$(docker images -q chipotle)
docker run -d --name 'training' ${IMAGE_ID} 'app.handler'
docker cp training:/var/task/chipotle.pkl chipotle.pkl
docker kill training && docker rm training