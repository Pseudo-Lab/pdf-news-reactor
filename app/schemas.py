from pydantic import BaseModel

# 기자 URL 검증 요청 스키마
class JournalistRequest(BaseModel):
    journalisturl: str

# 기자 평가 점수 추가 요청 스키마
class JournalistScoreRequest(JournalistRequest):
    useful: int
    touched: int
    recommend: int
    analytical: int
    wow: int

# 기자 평균 평가 점수 응답 스키마
class JournalistAverageScore(BaseModel):
    journalisturl: str
    useful: float
    touched: float
    recommend: float
    analytical: float
    wow: float
