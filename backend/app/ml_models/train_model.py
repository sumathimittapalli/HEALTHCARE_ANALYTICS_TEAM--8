import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

CSV_PATH = os.path.join("backend", "app", "ml_models", "disease_dataset.csv")
MODEL_PATH = os.path.join("backend", "app", "ml_models", "disease_model.pkl")

def encode_gender(g):
    return 1 if str(g).lower() in ("male", "m") else 0

def main():
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
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved to:", MODEL_PATH)

if __name__ == "__main__":
    main()
