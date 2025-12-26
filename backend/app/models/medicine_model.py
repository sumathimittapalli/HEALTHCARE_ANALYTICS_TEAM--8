
from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String, index=True)
    medicine = Column(String, index=True)
    dosage = Column(String)
    notes = Column(String)
    min_age = Column(Integer)
    max_age = Column(Integer)


class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String)
    age = Column(Integer)
    allergies = Column(String)
    recommended_medicines = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


