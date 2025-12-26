import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("datasets/medicine_data.csv")

# Select features
features = df[["disease", "min_age", "max_age"]]

# Encode disease
encoder = OneHotEncoder(sparse_output=False)
disease_encoded = encoder.fit_transform(features[["disease"]])

# Combine features
X = pd.concat([
    pd.DataFrame(disease_encoded),
    features[["min_age", "max_age"]].reset_index(drop=True)
], axis=1)

# Save everything needed for inference
model_data = {
    "dataframe": df,
    "encoder": encoder,
    "feature_matrix": X
}

with open("backend/app/ml_models/medicine_ml_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print("✅ Machine Learning model trained and saved")
