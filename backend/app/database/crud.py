from sqlalchemy.orm import Session
from app.models.models import DiseaseRecord

def get_all_predictions(db: Session):
    return db.query(DiseaseRecord).all()


def save_prediction(db: Session, record_data: dict):
    """
    record_data: dict with keys age, gender, blood_pressure, sugar, bmi, cholesterol, prediction
    """
    rec = DiseaseRecord(
        age=record_data.get("age"),
        gender=record_data.get("gender"),
        blood_pressure=record_data.get("blood_pressure"),
        sugar=record_data.get("sugar"),
        bmi=record_data.get("bmi"),
        cholesterol=record_data.get("cholesterol"),
        prediction=record_data.get("prediction")
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
