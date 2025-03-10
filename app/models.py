from sqlalchemy import Column, Integer, String
from app.database import Base

class JournalistScore(Base):
    __tablename__ = "journalist_scores"

    id = Column(Integer, primary_key=True, index=True)
    journalisturl = Column(String, index=True)
    useful = Column(Integer)
    touched = Column(Integer)
    recommend = Column(Integer)
    analytical = Column(Integer)
    wow = Column(Integer)

class JournalistAverageScore(Base):
    __tablename__ = "journalist_avg_scores"

    id = Column(Integer, primary_key=True, index=True)
    journalisturl = Column(String, unique=True, index=True)
    useful_avg = Column(Integer)
    touched_avg = Column(Integer)
    recommend_avg = Column(Integer)
    analytical_avg = Column(Integer)
    wow_avg = Column(Integer)