from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import joblib

from app.schemas.disease_prediction_schema import DiseasePredictionInput, DiseasePredictionOutput, DiseasePredictionRecordOut
from app.database.database import SessionLocal
from app.database import disease_prediction_operations
from app.utils.disease_preprocessing import preprocess_disease_input

router = APIRouter(
    prefix="/disease",
    tags=["Disease Prediction"]
)

# ----------------------------
# DB Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Load ML Model
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(
    BASE_DIR, "..", "..", "..", "ml_models", "disease_prediction_model.pkl"
)

try:
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None

# ----------------------------
# Routes
# ----------------------------
@router.post("/predict", response_model=DiseasePredictionOutput)
def predict_disease(payload: DiseasePredictionInput, db: Session = Depends(get_db)):

    features = preprocess_disease_input(payload)

    if model:
        try:
            pred = model.predict([features])[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        pred = 1 if (payload.sugar > 140 or payload.blood_pressure > 160) else 0

    prediction_label = "High Risk" if int(pred) == 1 else "Low Risk"

    disease_prediction_operations.save_disease_prediction(db, {
        "age": payload.age,
        "gender": payload.gender,
        "blood_pressure": payload.blood_pressure,
        "sugar": payload.sugar,
        "bmi": payload.bmi,
        "cholesterol": payload.cholesterol,
        "prediction": prediction_label
    })

    return DiseasePredictionOutput(
        prediction=prediction_label,
        status="success"
    )

@router.get("/info")
def disease_info():
    return {
        "model": "Disease Prediction Model",
        "features": ["age", "gender", "blood_pressure", "sugar", "bmi", "cholesterol"]
    }

@router.get("/records", response_model=list[DiseasePredictionRecordOut])
def get_all_disease_records(db: Session = Depends(get_db)):
    return disease_prediction_operations.get_all_disease_predictions(db)

