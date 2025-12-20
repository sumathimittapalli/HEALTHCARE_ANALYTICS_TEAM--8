import streamlit as st
import requests
from utils.api_client import predict_disease_api
from utils.charts import show_probability_chart

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="Disease Prediction", layout="centered")
st.title(" Disease Prediction (Module 1)")
st.write("Enter patient details and get a risk prediction.")

# -----------------------------
# Backend health check
# -----------------------------
def backend_available():
    try:
        r = requests.get("http://127.0.0.1:8000/")
        return r.status_code == 200
    except:
        return False

if not backend_available():
    st.error("Backend is not running! Please start FastAPI on port 8000.")
    st.stop()

# -----------------------------
# Input form
# -----------------------------
with st.form("input_form"):
    age = st.number_input("Age", min_value=0, max_value=120, value=40)
    gender = st.selectbox("Gender", ["male", "female"])
    blood_pressure = st.number_input("Blood Pressure", min_value=0.0, value=120.0)
    sugar = st.number_input("Sugar (mg/dL)", min_value=0.0, value=90.0)
    bmi = st.number_input("BMI", min_value=0.0, value=23.0)
    cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, value=180.0)
    submitted = st.form_submit_button("Predict")

# -----------------------------
# Form submission
# -----------------------------
if submitted:
    # Standardize gender to match backend
    gender_backend = "M" if gender.lower() == "male" else "F"

    payload = {
        "age": int(age),
        "gender": gender_backend,
        "blood_pressure": float(blood_pressure),
        "sugar": float(sugar),
        "bmi": float(bmi),
        "cholesterol": float(cholesterol)
    }

    # Call backend
    res = predict_disease_api(payload)

    if res is None or "error" in res:
        st.error(f"Could not contact backend. {res.get('error') if res else ''}")
    else:
        if res.get("status") == "success":
            st.success(f"Prediction: {res.get('prediction')}")
            show_probability_chart(res.get("prediction"))
        else:
            st.error("Prediction failed: " + str(res))
