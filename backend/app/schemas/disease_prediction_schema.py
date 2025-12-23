from pydantic import BaseModel, Field

class DiseasePredictionInput(BaseModel):
    age: int = Field(..., ge=0)
    gender: str
    blood_pressure: float
    sugar: float
    bmi: float
    cholesterol: float

class DiseasePredictionOutput(BaseModel):
    prediction: str
    status: str

class DiseasePredictionRecordOut(BaseModel):
    age: int
    gender: str
    blood_pressure: float
    sugar: float
    bmi: float
    cholesterol: float
    prediction: str

    class Config:
        from_attributes = True