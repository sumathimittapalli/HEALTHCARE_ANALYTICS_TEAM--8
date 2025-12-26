import pandas as pd
import os

from backend.app.database.database import SessionLocal
from backend.app.models.medicine_model import Medicine

def seed_database():
    # 🔹 Get project root directory
    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
    # base_dir → backend/

    project_root = os.path.dirname(base_dir)
    # project_root → medicine_recommendation/

    csv_path = os.path.join(
        project_root,
        "datasets",
        "medicine_data.csv"
    )

    df = pd.read_csv(csv_path)

    db = SessionLocal()

    for _, row in df.iterrows():
        medicine = Medicine(
            disease=row["disease"].lower(),
            medicine=row["medicine"],
            dosage=row["dosage"],
            notes=row["notes"],
            min_age=int(row["min_age"]),
            max_age=int(row["max_age"])
        )
        db.add(medicine)

    db.commit()
    db.close()

    print("✅ CSV data successfully loaded into PostgreSQL")

if __name__ == "__main__":
    seed_database()
