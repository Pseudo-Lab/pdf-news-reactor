# 실행순서

1. `python crawl_news.py`로 뉴스기사 전체를 html파일로 저장
2. `python push_article_id.py`로 크롤링할 뉴스를 redis list에 추가하기
3. `python preprocessing.py`로 뉴스 작성 기자 정보 추출가능
4. `python api_call.py`로 기사에 대한 리액션 정보 추출가능

## redis이용 방식으로 수정한 구조

- `push_article_id.py` 파일로 임시로 article_id를 list에 추가하도록 해두었습니다.
    - article_id를 수집하는 방식은 자유롭게 구성하면 될것 같습니다.
- `crawl_news.py, api_call.py` 파일로 article_id를 redis에서 꺼내서 처리하는 로직을 작성해보았습니다.