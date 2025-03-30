import logging
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import JournalistAverageScore, JournalistScore
from app.schemas import JournalistRequest, JournalistScoreRequest

# .env 로딩
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Database initialized successfully")


@app.post("/api/journalist/validate")
def validate_journalist(request: JournalistRequest, db: Session = Depends(get_db)):
    exists = (
        db.query(JournalistScore).filter_by(journalisturl=request.journalisturl).first()
        is not None
    )
    logger.info(
        f"Journalist validation requested: {request.journalisturl}, exists: {exists}"
    )
    return {"exists": exists}


@app.post("/api/journalist/add-score")
def add_journalist_score(
    request: JournalistScoreRequest, db: Session = Depends(get_db)
):
    # 새로운 평가 추가
    new_score = JournalistScore(
        articleurl=request.articleurl,
        journalisturl=request.journalisturl,
        useful=request.useful,
        touched=request.touched,
        recommend=request.recommend,
        analytical=request.analytical,
        wow=request.wow,
    )

    db.add(new_score)
    db.commit()
    logger.info(
        f"New score added for journalist: {request.journalisturl}, article: {request.articleurl}"
    )

    # 평균값 재계산
    scores = (
        db.query(JournalistScore).filter_by(journalisturl=request.journalisturl).all()
    )
    count = len(scores)
    avg_score = {
        "useful_avg": sum(s.useful for s in scores) // count,
        "touched_avg": sum(s.touched for s in scores) // count,
        "recommend_avg": sum(s.recommend for s in scores) // count,
        "analytical_avg": sum(s.analytical for s in scores) // count,
        "wow_avg": sum(s.wow for s in scores) // count,
    }

    # 기존 평균값이 있는지 확인 후 업데이트 또는 추가
    existing_avg = (
        db.query(JournalistAverageScore)
        .filter_by(journalisturl=request.journalisturl)
        .first()
    )
    if existing_avg:
        for key, value in avg_score.items():
            setattr(existing_avg, key, value)
        logger.info(f"Average score updated for journalist: {request.journalisturl}")
    else:
        new_avg_score = JournalistAverageScore(
            journalisturl=request.journalisturl, **avg_score
        )
        db.add(new_avg_score)
        logger.info(
            f"New average score created for journalist: {request.journalisturl}"
        )

    db.commit()
    return {"message": "Score added and average updated successfully"}


@app.post("/api/journalist/average-score")
def get_average_score(request: JournalistRequest, db: Session = Depends(get_db)):
    avg_score = (
        db.query(JournalistAverageScore)
        .filter_by(journalisturl=request.journalisturl)
        .first()
    )

    if not avg_score:
        logger.warning(
            f"Average score requested but not found for journalist: {request.journalisturl}"
        )
        raise HTTPException(status_code=404, detail="Journalist not found")

    logger.info(f"Average score retrieved for journalist: {request.journalisturl}")
    return {
        "journalisturl": avg_score.journalisturl,
        "useful": avg_score.useful_avg,
        "touched": avg_score.touched_avg,
        "recommend": avg_score.recommend_avg,
        "analytical": avg_score.analytical_avg,
        "wow": avg_score.wow_avg,
    }
