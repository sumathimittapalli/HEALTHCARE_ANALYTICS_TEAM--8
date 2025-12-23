from pydantic import BaseModel, conint, confloat

class PatientReadmissionData(BaseModel):
    age: conint(gt=0)
    time_in_hospital: conint(ge=0)
    medication_count: conint(ge=0)
    blood_pressure: confloat(gt=0)
    cholesterol: confloat(gt=0)
    bmi: confloat(gt=0)
    diabetes: conint(ge=0, le=1)
    hypertension: conint(ge=0, le=1)

class PatientReadmissionResponse(BaseModel):
    readmission_risk: str
    probability: float