from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class PatientReadmission(Base):
    __tablename__ = "patient_readmissions"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    time_in_hospital = Column(Integer)
    medication_count = Column(Integer)
    blood_pressure = Column(Float)
    cholesterol = Column(Float)
    bmi = Column(Float)
    diabetes = Column(Integer)
    hypertension = Column(Integer)