import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os

class MedicineRecommender:
    def __init__(self):
        self.model_data = None

    def _load_model(self):
        if self.model_data is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            model_path = os.path.join(
                base_dir,
                "ml_models",
                "medicine_ml_model.pkl"
            )

            with open(model_path, "rb") as f:
                self.model_data = pickle.load(f)

    def recommend(self, disease: str, age: int, allergies: list):
        self._load_model()

        df = self.model_data["dataframe"].copy()
        X = self.model_data["feature_matrix"]

        # ✅ STEP 1: RULE-BASED SAFETY FILTERING
        df = df[df["disease"].str.lower() == disease.lower()]
        df = df[(df["min_age"] <= age) & (df["max_age"] >= age)]

        if allergies:
            df = df[~df["medicine"].str.lower().isin(
                [a.lower() for a in allergies]
            )]

        if df.empty:
            return []

        # ✅ STEP 2: ML RANKING (AGE-ONLY SIMILARITY)
        # Age similarity is what matters now
        age_vector = pd.DataFrame([[age, age]])

        X_filtered = X.loc[df.index][["min_age", "max_age"]]

        similarity = cosine_similarity(age_vector, X_filtered)[0]
        df["similarity_score"] = similarity

        df = df.sort_values(by="similarity_score", ascending=False)

        return (
            df
            .drop(columns=["similarity_score"])
            .head(5)
            .to_dict(orient="records")
        )
