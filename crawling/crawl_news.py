import time
import redis
import requests
from bs4 import BeautifulSoup

redis_client = redis.Redis(host="localhost", port=6379, db=0)

CRAWLED_LIST_KEY = "crawled_list"
TASK_LIST_KEY = "task_list"

# User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

error_message = "페이지를 찾을 수 없습니다."


# 크롤링 함수 정의
def crawl_article(article_id, save_html=False):
    url = f"https://n.news.naver.com/mnews/article/449/{article_id}?sid=100"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 페이지 존재 여부 확인
    if error_message in soup.get_text():
        print(f"Failed to fetch article {article_id}: Page not found.")
    else:
        if save_html:
            # HTML 저장
            with open(f"naver_news_{article_id}.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"Article {article_id} saved successfully.")
        else:
            print(f"Article {article_id} fetched successfully, but not saved.")

        # 크롤링된 ID를 Redis의 CRAWLED_LIST에 추가
        redis_client.rpush(CRAWLED_LIST_KEY, article_id)


def main():
    while True:
        task_list = (
            [item.decode("utf-8") for item in redis_client.lrange(TASK_LIST_KEY, 0, -1)]
            if redis_client.exists(TASK_LIST_KEY)
            else []
        )
        crawled_list = (
            [
                item.decode("utf-8")
                for item in redis_client.lrange(CRAWLED_LIST_KEY, 0, -1)
            ]
            if redis_client.exists(CRAWLED_LIST_KEY)
            else []
        )

        if task_list:
            for article_id in task_list:
                if article_id in crawled_list:
                    print(f"Skipping article {article_id} as it is already crawled.")
                    redis_client.lrem(TASK_LIST_KEY, 1, article_id)
                    print(f"Article {article_id} removed from task list.")
                    time.sleep(10)
                    continue

                # 크롤링 수행 (HTML 저장하지 않음)
                crawl_article(article_id, save_html=True)

                # 크롤링 완료 후 대기
                time.sleep(10)
        else:
            print("No tasks found. Sleeping for 10 seconds.")
            time.sleep(10)


if __name__ == "__main__":
    main()
