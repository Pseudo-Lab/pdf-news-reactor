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