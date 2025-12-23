import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Use relative path to datasets folder
CSV_PATH = os.path.join("datasets", "disease_dataset.csv")
MODEL_PATH = os.path.join("backend", "app", "ml_models", "disease_prediction_model.pkl")

def encode_gender(g):
    return 1 if str(g).lower() in ("male", "m") else 0

def train_disease_prediction_model():
    """Train and save the disease prediction model"""
    if not os.path.exists(CSV_PATH):
        print(f"Dataset not found at {CSV_PATH}")
        return
        
    df = pd.read_csv(CSV_PATH)
    # Expected columns: age, gender, blood_pressure, sugar, bmi, cholesterol, prediction
    df = df.dropna()
    X = pd.DataFrame({
        "age": df["age"],
        "gender_male": df["gender"].apply(encode_gender),
        "blood_pressure": df["blood_pressure"],
        "sugar": df["sugar"],
        "bmi": df["bmi"],
        "cholesterol": df["cholesterol"]
    })
    # Map labels to 0/1
    y = df["prediction"].map(lambda x: 1 if str(x).strip().lower() in ("high risk", "high", "1", "yes") else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("Disease prediction model trained and saved to:", MODEL_PATH)

if __name__ == "__main__":
    train_disease_prediction_model()