from kafka import KafkaProducer
import json

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['broker-1:9092', 'broker-2:9092', 'broker-3:9092'],
    value_serializer=json_serializer
)

def send_message(topic, message):
    producer.send(topic, message)
    producer.flush()

# # 예제 메시지 전송
# cnt = 1
# while True:
#     import time
#     time.sleep(1)
#     
#     cnt += 1



import time
import redis
import requests
import json

# Redis 설정
redis_client = redis.Redis(host="redis", port=6379, db=0)
TASK_LIST_KEY = "task_list"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "*/*",
}


def get_article_reactions(article_id):
    # URL 생성
    url = f"https://news.like.naver.com/v1/search/contents?q=JOURNALIST%5B75535(period)%5D%7CNEWS%5Bne_449_{article_id}%5D&isDuplication=false&cssIds=MULTI_MOBILE,NEWS_MOBILE"
    headers["Referer"] = (
        f"https://n.news.naver.com/mnews/article/449/{article_id}?sid=100"
    )

    # 요청 보내기
    response = requests.get(url, headers=headers)

    # 응답 처리
    data = response.json()
    reaction_counts = {}

    # 반응 수 계산
    for content in data.get("contents", []):
        for reaction in content.get("reactions", []):
            reaction_type = reaction.get("reactionType")
            count = reaction.get("count", 0)
            reaction_counts[reaction_type] = (
                reaction_counts.get(reaction_type, 0) + count
            )

    return reaction_counts


def main():
    while True:
        # Redis에서 작업 ID 가져오기
        article_id = redis_client.lpop(TASK_LIST_KEY)

        if article_id:
            # 바이트형 데이터를 문자열로 변환
            article_id = article_id.decode("utf-8")

            # article_id에 대한 반응 수 가져오기
            reaction_counts = get_article_reactions(article_id)
            send_message('reaction', reaction_counts)

            # 작업 간 대기 시간
            time.sleep(10)
        else:
            print("No tasks found. Sleeping for 10 seconds.")
            time.sleep(10)


if __name__ == "__main__":
    main()
