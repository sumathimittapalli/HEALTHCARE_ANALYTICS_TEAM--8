from pydantic import BaseModel
from typing import List
import pandas as pd

class MedicineRequest(BaseModel):
    disease: str
    age: int
    allergies: List[str]

class MedicineResponse(BaseModel):
    medicine_name: str
    dosage: str
    notes: str


class MedicineCreate(BaseModel):
    disease: str
    medicine: str
    dosage: str
    notes: str
    min_age: int
    max_age: int


class MedicineRecommender:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)

    def recommend(self, disease: str, age: int, allergies: list):
        filtered = self.df[self.df["disease"].str.lower() == disease.lower()]

        if allergies:
            filtered = filtered[
                ~filtered["medicine"].str.lower().isin(
                    [a.lower() for a in allergies]
                )
            ]

        recommendations = []
        for _, row in filtered.iterrows():
            recommendations.append({
                "medicine_name": row["medicine"],
                "dosage": row["dosage"],
                "notes": row["notes"]
            })

        return recommendations
