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

SCORE_FIELDS = ["useful", "touched", "recommend", "analytical", "wow"]


def scores_are_equal(
    existing: JournalistScore, incoming: JournalistScoreRequest
) -> bool:
    return all(
        getattr(existing, field) == getattr(incoming, field) for field in SCORE_FIELDS
    )


def update_score_fields(score_obj: JournalistScore, source: JournalistScoreRequest):
    for field in SCORE_FIELDS:
        setattr(score_obj, field, getattr(source, field))


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
    existing_score = (
        db.query(JournalistScore)
        .filter_by(articleurl=request.articleurl, journalisturl=request.journalisturl)
        .first()
    )

    if existing_score:
        if scores_are_equal(existing_score, request):
            logger.info(
                f"Score is already the latest for journalist: {request.journalisturl}, article: {request.articleurl}"
            )
            message = "Score already up to date"
        else:
            update_score_fields(existing_score, request)
            db.commit()
            logger.info(
                f"Updated score for journalist: {request.journalisturl}, article: {request.articleurl}"
            )
            message = "Score updated successfully"
    else:
        new_score = JournalistScore(
            articleurl=request.articleurl,
            journalisturl=request.journalisturl,
            **{field: getattr(request, field) for field in SCORE_FIELDS},
        )
        db.add(new_score)
        db.commit()
        logger.info(
            f"Added new score for journalist: {request.journalisturl}, article: {request.articleurl}"
        )
        message = "Score added successfully"

    # 평균 점수 재계산
    scores = (
        db.query(JournalistScore).filter_by(journalisturl=request.journalisturl).all()
    )
    count = len(scores)
    avg_score = {
        f"{field}_avg": sum(getattr(s, field) for s in scores) // count
        for field in SCORE_FIELDS
    }

    existing_avg = (
        db.query(JournalistAverageScore)
        .filter_by(journalisturl=request.journalisturl)
        .first()
    )
    if existing_avg:
        for key, value in avg_score.items():
            setattr(existing_avg, key, value)
        logger.info(f"Updated average score for journalist: {request.journalisturl}")
    else:
        new_avg = JournalistAverageScore(
            journalisturl=request.journalisturl, **avg_score
        )
        db.add(new_avg)
        logger.info(f"Created average score for journalist: {request.journalisturl}")

    db.commit()
    return {"message": f"{message} and average updated successfully"}


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
