import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Use relative path to datasets folder
CSV_PATH = os.path.join("datasets", "readmission_clean.csv")

def train_readmission_prediction_model():
    """Train and save the readmission prediction model"""
    if not os.path.exists(CSV_PATH):
        print(f"Dataset not found at {CSV_PATH}")
        return

    # Load dataset
    df = pd.read_csv(CSV_PATH)

    # Target encoding - adjust column name based on your actual dataset
    if "readmitted_30_days" in df.columns:
        y = df["readmitted_30_days"].map({"No": 0, "Yes": 1}).fillna(0)
        X = df.drop("readmitted_30_days", axis=1)
    elif "readmitted" in df.columns:
        y = df["readmitted"].map({"No": 0, "Yes": 1, 0: 0, 1: 1}).fillna(0)
        X = df.drop("readmitted", axis=1)
    else:
        print("Target column not found. Expected 'readmitted_30_days' or 'readmitted'")
        return

    # Remove ID columns if present
    if "patient_id" in X.columns:
        X = X.drop("patient_id", axis=1)

    # One-hot encoding for categorical variables
    X = pd.get_dummies(X, drop_first=True)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Save model
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "readmission_prediction_model.pkl"
    )

    joblib.dump(model, MODEL_PATH)
    print("✅ Readmission prediction model saved at:", MODEL_PATH)

if __name__ == "__main__":
    train_readmission_prediction_model()