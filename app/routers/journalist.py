from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import JournalistScore, JournalistAverageScore
from app.schemas import JournalistRequest, JournalistScoreRequest

router = APIRouter()

@router.post("/api/journalist/validate")
def validate_journalist(request: JournalistRequest, db: Session = Depends(get_db)):
    exists = db.query(JournalistScore).filter_by(journalisturl=request.journalisturl).first() is not None
    return {"exists": exists}

@router.post("/api/journalist/add-score")
def add_journalist_score(request: JournalistScoreRequest, db: Session = Depends(get_db)):
    new_score = JournalistScore(**request.dict())
    db.add(new_score)
    db.commit()
    return {"message": "Score added successfully"}
