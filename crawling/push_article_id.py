import json

import redis

from crawl_press import crawl_top20_news

CRAWLED_LIST_KEY = "crawled_list"
TASK_LIST_KEY = "task_list"

redis_client = redis.Redis(host="localhost", port=30007, db=0)


with open("news_company_names.json", "r", encoding="utf-8") as f:
    news_company_names = json.load(f)

    for press_id in news_company_names:
        top_news_list = crawl_top20_news(press_id)
        news_ids = [news_url.split("/")[5].split("?")[0] for news_url in top_news_list]
        print(f"Collected {len(news_ids)} articles from press {press_id}")

        if top_news_list:
            redis_client.rpush(TASK_LIST_KEY, *news_ids)
            print(f"Total length: {redis_client.llen(TASK_LIST_KEY)}")

print(redis_client.lrange(TASK_LIST_KEY, 0, -1))

# redis_client.flushall()
# print(redis_client.lrange(TASK_LIST_KEY, 0, -1))

# import time

# time.sleep(10)

# redis_client.rpush(TASK_LIST_KEY, "0000283915")
