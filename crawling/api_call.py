import requests
import json

ARTICLE_ID = "0000283913"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": f"https://n.news.naver.com/mnews/article/449/{ARTICLE_ID}?sid=100",
}

url = f"https://news.like.naver.com/v1/search/contents?q=JOURNALIST%5B75535(period)%5D%7CNEWS%5Bne_449_{ARTICLE_ID}%5D&isDuplication=false&cssIds=MULTI_MOBILE,NEWS_MOBILE"


response = requests.get(url, headers=headers)

# 응답 출력
data = response.json()

reaction_counts = {}

for content in data["contents"]:
    for reaction in content["reactions"]:
        reaction_type = reaction["reactionType"]
        count = reaction["count"]
        if reaction_type in reaction_counts:
            reaction_counts[reaction_type] += count
        else:
            reaction_counts[reaction_type] = count

print(reaction_counts)
