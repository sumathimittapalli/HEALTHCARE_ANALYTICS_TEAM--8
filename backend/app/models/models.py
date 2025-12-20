from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base

class DiseaseRecord(Base):
    __tablename__ = "disease_records"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    blood_pressure = Column(Float, nullable=False)
    sugar = Column(Float, nullable=False)
    bmi = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    prediction = Column(String, nullable=False)
