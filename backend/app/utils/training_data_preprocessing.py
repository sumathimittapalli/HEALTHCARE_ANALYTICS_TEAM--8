import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_training_data(csv_path):
    """
    Preprocess training data for machine learning models.
    Handles data cleaning, feature selection, and train-test split.
    """
    df = pd.read_csv(csv_path)

    # Remove missing values
    df = df.dropna()

    # Example target column - adjust based on your dataset
    if "readmitted" in df.columns:
        y = df["readmitted"]
        X = df.drop(columns=["readmitted"])
    elif "readmitted_30_days" in df.columns:
        y = df["readmitted_30_days"]
        X = df.drop(columns=["readmitted_30_days"])
    else:
        raise ValueError("Target column not found in dataset")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test