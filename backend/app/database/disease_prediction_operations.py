from sqlalchemy.orm import Session
from app.models.disease_prediction import DiseasePredictionRecord

def get_all_disease_predictions(db: Session):
    """Get all disease prediction records from database"""
    return db.query(DiseasePredictionRecord).all()

def save_disease_prediction(db: Session, record_data: dict):
    """
    Save disease prediction record to database
    record_data: dict with keys age, gender, blood_pressure, sugar, bmi, cholesterol, prediction
    """
    record = DiseasePredictionRecord(
        age=record_data.get("age"),
        gender=record_data.get("gender"),
        blood_pressure=record_data.get("blood_pressure"),
        sugar=record_data.get("sugar"),
        bmi=record_data.get("bmi"),
        cholesterol=record_data.get("cholesterol"),
        prediction=record_data.get("prediction")
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record