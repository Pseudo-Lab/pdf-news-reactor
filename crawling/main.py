import requests
from bs4 import BeautifulSoup

ARTICLE_ID = "0000283913"

url = f"https://n.news.naver.com/mnews/article/449/{ARTICLE_ID}?sid=100"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# save the html file
with open("naver_news.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())
