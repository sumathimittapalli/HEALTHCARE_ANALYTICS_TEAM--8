from fastapi import APIRouter, HTTPException, Depends
import joblib
import pandas as pd
import os
from sqlalchemy.orm import Session

from app.schemas.patient_readmission_schema import PatientReadmissionData
from app.models.patient_readmission import PatientReadmission
from app.database.database import get_db

router = APIRouter(prefix="/readmission", tags=["Readmission Prediction"])

# ------------------ Load ML Model Safely ------------------

model = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(
    BASE_DIR, "..", "..", "..", "ml_models", "readmission_prediction_model.pkl"
)

if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Model load failed: {e}")
else:
    print("Model file missing or empty")

# ------------------ Column Mapping ------------------

column_mapping = {
    "age": "age",
    "time_in_hospital": "time_in_hospital",
    "medication_count": "num_medications",
    "blood_pressure": "blood_pressure",
    "cholesterol": "cholesterol",
    "bmi": "bmi",
    "diabetes": "diabetes",
    "hypertension": "hypertension",
}

# ------------------ Feature Preparation ------------------

def prepare_features(data: dict):
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="ML model not loaded. Please check model file."
        )

    df = pd.DataFrame([data]).rename(columns=column_mapping)

    for col in model.feature_names_in_:
        if col not in df:
            df[col] = 0

    return df[model.feature_names_in_]

# ------------------ Prediction Logic ------------------

def predict_readmission_risk(df):
    proba = model.predict_proba(df)[0][1]
    risk = "High" if proba >= 0.3 else "Low"

    return {
        "readmission_risk": risk,
        "probability": round(float(proba), 3)
    }

# ------------------ API Endpoint ------------------

@router.post("/predict")
def predict_patient_readmission(
    patient: PatientReadmissionData,
    db: Session = Depends(get_db)
):
    try:
        # Save patient input to database
        record = PatientReadmission(**patient.dict())
        db.add(record)
        db.commit()

        # Prepare features and predict
        df = prepare_features(patient.dict())
        return predict_readmission_risk(df)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
