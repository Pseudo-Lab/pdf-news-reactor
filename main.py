from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.models import JournalistScore, JournalistAverageScore
from app.schemas import JournalistRequest, JournalistScoreRequest

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/api/journalist/validate")
def validate_journalist(request: JournalistRequest, db: Session = Depends(get_db)):
    exists = db.query(JournalistScore).filter_by(journalisturl=request.journalisturl).first() is not None
    return {"exists": exists}

@app.post("/api/journalist/add-score")
def add_journalist_score(request: JournalistScoreRequest, db: Session = Depends(get_db)):
    # 새로운 평가 추가
    new_score = JournalistScore(
        journalisturl=request.journalisturl,
        useful=request.useful,
        touched=request.touched,
        recommend=request.recommend,
        analytical=request.analytical,
        wow=request.wow
    )
    db.add(new_score)
    db.commit()

    # 평균값 재계산
    scores = db.query(JournalistScore).filter_by(journalisturl=request.journalisturl).all()
    count = len(scores)
    avg_score = {
        "useful_avg": sum(s.useful for s in scores) // count,
        "touched_avg": sum(s.touched for s in scores) // count,
        "recommend_avg": sum(s.recommend for s in scores) // count,
        "analytical_avg": sum(s.analytical for s in scores) // count,
        "wow_avg": sum(s.wow for s in scores) // count,
    }

    # 기존 평균값이 있는지 확인 후 업데이트 또는 추가
    existing_avg = db.query(JournalistAverageScore).filter_by(journalisturl=request.journalisturl).first()
    if existing_avg:
        existing_avg.useful_avg = avg_score["useful_avg"]
        existing_avg.touched_avg = avg_score["touched_avg"]
        existing_avg.recommend_avg = avg_score["recommend_avg"]
        existing_avg.analytical_avg = avg_score["analytical_avg"]
        existing_avg.wow_avg = avg_score["wow_avg"]
    else:
        new_avg_score = JournalistAverageScore(journalisturl=request.journalisturl, **avg_score)
        db.add(new_avg_score)

    db.commit()
    return {"message": "Score added and average updated successfully"}

@app.post("/api/journalist/average-score")
def get_average_score(request: JournalistRequest, db: Session = Depends(get_db)):
    avg_score = db.query(JournalistAverageScore).filter_by(journalisturl=request.journalisturl).first()
    
    if not avg_score:
        raise HTTPException(status_code=404, detail="Journalist not found")

    return {
        "journalisturl": avg_score.journalisturl,
        "useful": avg_score.useful_avg,
        "touched": avg_score.touched_avg,
        "recommend": avg_score.recommend_avg,
        "analytical": avg_score.analytical_avg,
        "wow": avg_score.wow_avg,
    }
