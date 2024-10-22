import redis

CRAWLED_LIST_KEY = "crawled_list"
TASK_LIST_KEY = "task_list"

redis_client = redis.Redis(host="localhost", port=30007, db=0)


redis_client.rpush(TASK_LIST_KEY, "0000283914")

print(redis_client.lrange(TASK_LIST_KEY, 0, -1))

# redis_client.flushall()

import time

time.sleep(10)

redis_client.rpush(TASK_LIST_KEY, "0000283915")
