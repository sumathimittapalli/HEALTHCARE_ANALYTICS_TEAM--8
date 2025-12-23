from pydantic import BaseModel
from datetime import datetime

class XRayPredictionResponse(BaseModel):
    image_name: str
    prediction: str
    confidence: float
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True
