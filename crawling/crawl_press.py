import json
import os
import time

import requests
from bs4 import BeautifulSoup


def crawl_news_companies(random_id) -> tuple[int, str]:
    url = f"https://media.naver.com/press/{random_id}/ranking?type=popular"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for press_hd_name in soup.find_all("h3", class_="press_hd_name"):
        press_name = press_hd_name.find("a", class_="press_hd_name_link").text.strip()

    return random_id, press_name


def crawl_with_retry(url, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (attempt + 1))


def crawl_top20_news(press_id) -> list[str]:
    url = f"https://media.naver.com/press/{press_id}/ranking"
    try:
        response = crawl_with_retry(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return [link["href"] for link in soup.find_all("a", class_="_es_pc_link")]
    except Exception as e:
        print(f"Error crawling {press_id}: {e}")
        return []


def extract_news_id(url: str) -> str:
    return url.split("/")[5].split("?")[0]


def save_companies_to_file():
    news_company_names = {}
    for i in range(1000):
        time.sleep(0.5)
        num = str(i).zfill(3)
        try:
            press_id, press_name = crawl_news_companies(num)
            news_company_names[press_id] = press_name
            print(f"{num} - {press_name}")
        except:
            print(f"{num} - doent's exist")
            pass

    print("=" * 30)
    print(f"{len(news_company_names)}개 언론사: \n{news_company_names}")

    with open("news_company_names.json", "w", encoding="utf-8") as f:
        json.dump(news_company_names, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    if not os.path.isfile("news_company_names.json"):
        save_companies_to_file()
    print(crawl_top20_news(127))
