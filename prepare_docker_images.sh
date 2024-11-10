#!/bin/bash

# .env 파일 불러오기
if [ -f .env ]; then
  export $(cat .env | xargs)
else
  echo ".env file not found!"
  exit 1
fi

# Docker Hub 로그인
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
if [ $? -ne 0 ]; then
  echo "Docker login failed. Please check your credentials."
  exit 1
fi
echo "Docker login successful."

# Docker 이미지 빌드 및 푸시
docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_USERNAME/create_reaction_topic:$IMAGE_TAG -f python/Dockerfile.create_topic --push python
docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_USERNAME/reaction_producer:$IMAGE_TAG -f python/Dockerfile.producer --push python
docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_USERNAME/reaction_consumer:$IMAGE_TAG -f python/Dockerfile.consumer --push python

# 로그아웃
docker logout

echo "Images have been pushed to Docker Hub with tag $IMAGE_TAG"