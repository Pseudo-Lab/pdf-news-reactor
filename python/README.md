# How to use

- 토픽 생성
    - `docker build -t ehddnr/create_reaction_topic -f Dockerfile.create_topic .`
- Producer
    - `docker build -t ehddnr/reaction_producer -f Dockerfile.producer .`
- Consumer
    - `docker build -t ehddnr/reaction_consumer -f Dockerfile.consumer .`

- Dockerhub에 푸시
    - `docker push ehddnr/create_reaction_topic`
    - `docker push ehddnr/reaction_producer`
    - `docker push ehddnr/reaction_consumer`