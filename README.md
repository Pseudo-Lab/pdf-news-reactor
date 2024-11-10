# Prepare docker images(Option)

- 기존 docker hub 이미지를 이용할 수 있으나 개인 docker hub를 이용하고 싶은 경우 혹은 이미지 재구축 시 진행
- `.env_example` 파일을 참고하여 `.env` 파일 생성 및 docker login 정보 입력
- `bash prepare_docker_images.sh`

# How to use

- 시작하기: `bash start.sh`
- 끝내기: `bash terminate.sh`

## 구조

- `bash start.sh` 명령으로 실행된 Redis, Kafka (Broker, Producer, Consumer)

## Clickhouse

- 쿼리해보기
```sql
select * from reaction_table
settings stream_like_engine_allow_direct_select = 1
```
```sql
select * from local_table
```