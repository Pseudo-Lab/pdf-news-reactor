import requests
import pandas as pd
from bs4 import BeautifulSoup


def parse_reaction_data_from_html(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        editor_info = soup.find("span", class_="byline_s").text.strip().split()
        editor = editor_info[0]
        email = editor_info[2]

        return editor, email

if __name__ == "__main__":
    editor, email = parse_reaction_data_from_html("naver_news.html")
    print(editor, email)