from pydantic import BaseModel, Field

class DiseaseInput(BaseModel):
    age: int = Field(..., ge=0)
    gender: str
    blood_pressure: float
    sugar: float
    bmi: float
    cholesterol: float

class DiseaseOutput(BaseModel):
    prediction: str
    status: str

class DiseaseRecordOut(BaseModel):
    age: int
    gender: str
    blood_pressure: float
    sugar: float
    bmi: float
    cholesterol: float
    prediction: str

    class Config:
        orm_mode = True
