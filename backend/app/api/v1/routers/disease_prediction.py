from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.disease_schema import DiseaseInput, DiseaseOutput, DiseaseRecordOut
from app.database.connection import SessionLocal
from app.database import crud
from app.utils.preprocess import preprocess_input
import os
import joblib

router = APIRouter(
    prefix="/disease",
    tags=["Disease Prediction"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(
    BASE_DIR, "..", "..", "..", "ml_models", "disease_model.pkl"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

_model = None
try:
    _model = joblib.load(MODEL_PATH)
except Exception:
    _model = None

@router.post("/predict", response_model=DiseaseOutput)
def predict_disease(payload: DiseaseInput, db: Session = Depends(get_db)):
    features = preprocess_input(payload)

    if _model is not None:
        try:
            pred = _model.predict([features])[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model inference error: {e}")
    else:
        pred = 1 if (payload.sugar > 140 or payload.blood_pressure > 160) else 0

    prediction_label = "High Risk" if int(pred) == 1 else "Low Risk"

    crud.save_prediction(db, {
        "age": payload.age,
        "gender": payload.gender,
        "blood_pressure": payload.blood_pressure,
        "sugar": payload.sugar,
        "bmi": payload.bmi,
        "cholesterol": payload.cholesterol,
        "prediction": prediction_label
    })

    return DiseaseOutput(
        prediction=prediction_label,
        status="success"
    )

@router.get("/info")
def disease_info():
    return {
        "model": "Disease Prediction Model",
        "features": ["age", "gender", "blood_pressure", "sugar", "bmi", "cholesterol"]
    }

@router.get("/records", response_model=list[DiseaseRecordOut])
def get_all_disease_records(db: Session = Depends(get_db)):
    """
    Returns all disease prediction records saved via POST
    """
    return crud.get_all_predictions(db)
