from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.medicine_model import RecommendationHistory
from app.core.medicine_model_loader import load_medicine_model
import pandas as pd
from app.schemas.medicine_schema import MedicineRequest
from app.schemas.medicine_schema import MedicineCreate
from fastapi import HTTPException
from app.models.medicine_model import RecommendationHistory,Medicine
import json


from typing import List


router = APIRouter()





##recommending medicine based on request


@router.post("/recommend")
def recommend_medicine(
    request: MedicineRequest,
    db: Session = Depends(get_db)
):
    medicines = db.query(Medicine).all()

    if not medicines:
        return []

    # Build DataFrame from DB
    data = []
    for m in medicines:
        data.append({
            "disease": m.disease,
            "medicine": m.medicine,
            "dosage": m.dosage,
            "notes": m.notes,
            "min_age": m.min_age,
            "max_age": m.max_age
        })

    df = pd.DataFrame(data)

    # Load model
    model = load_medicine_model()
    model.df = df

    recommendations = model.recommend(
        disease=request.disease,
        age=request.age,
        allergies=request.allergies or []
    )

    # ✅ STORE recommendation in PostgreSQL
    history = RecommendationHistory(
        disease=request.disease,
        age=request.age,
        allergies=",".join(request.allergies or []),
        recommended_medicines=json.dumps(
            [r["medicine"] for r in recommendations]
        )
    )

    db.add(history)
    db.commit()

    return recommendations



#Adding Medicine
@router.post("/add")
def add_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):
    db_medicine = Medicine(
        disease=medicine.disease.lower(),
        medicine=medicine.medicine,
        dosage=medicine.dosage,
        notes=medicine.notes,
        min_age=medicine.min_age,
        max_age=medicine.max_age
    )

    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    return {
        "message": "Medicine added successfully",
        "id": db_medicine.id
    }
#deleting medicine 
from fastapi import HTTPException

@router.delete("/delete/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    db.delete(medicine)
    db.commit()

    return {
        "message": "Medicine deleted successfully",
        "deleted_id": medicine_id
    }

#Get all medicine list
@router.get("/list")
def list_medicines(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()

    return [
        {
            "disease": m.disease,
            "medicine": m.medicine,
            "dosage": m.dosage,
            "notes": m.notes,
            "min_age": m.min_age,
            "max_age": m.max_age
        }
        for m in medicines
    ]


# SEARCH MEDICINE BY NAME
@router.get("/search")
def search_medicine(name: str, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).filter(
        Medicine.medicine.ilike(f"%{name}%")
    ).all()

    return [
        {
            "disease": m.disease,
            "medicine": m.medicine,
            "dosage": m.dosage,
            "notes": m.notes,
            "min_age": m.min_age,
            "max_age": m.max_age
        }
        for m in medicines
    ]


# SEARCH BY EXACT MEDICINE NAME (your /search/disease logic corrected)
@router.get("/search/disease")
def search_disease(name: str, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).filter(
        Medicine.medicine.ilike(name)
    ).all()

    return [
        {
            "disease": m.disease,
            "medicine": m.medicine,
            "dosage": m.dosage,
            "notes": m.notes,
            "min_age": m.min_age,
            "max_age": m.max_age
        }
        for m in medicines
    ]


# FILTER BY DISEASE
@router.get("/by-disease/{disease}")
def medicines_by_disease(disease: str, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).filter(
        Medicine.disease.ilike(disease)
    ).all()

    return [
        {
            "disease": m.disease,
            "medicine": m.medicine,
            "dosage": m.dosage,
            "notes": m.notes,
            "min_age": m.min_age,
            "max_age": m.max_age
        }
        for m in medicines
    ]




# DOSAGE INFO
@router.get("/{medicine_name}/dosage")
def get_dosage(medicine_name: str, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(
        Medicine.medicine.ilike(medicine_name)
    ).first()

    if not medicine:
        return {"message": "Medicine not found"}

    return {
        "medicine": medicine.medicine,
        "dosage": medicine.dosage,
        "notes": medicine.notes
    }


# DISCLAIMER
@router.get("/disclaimer")
def disclaimer():
    return {
        "warning": "This is not real medical advice. Consult a doctor."
    }


# DATASET STATS
@router.get("/stats")
def dataset_stats(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()

    return {
        "total_records": len(medicines),
        "unique_diseases": len(set(m.disease for m in medicines)),
        "unique_medicines": len(set(m.medicine for m in medicines))
    }
