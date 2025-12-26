import streamlit as st
import pandas as pd

from utils.healthcare_api_client import (
    HealthcareAPIClient,
    predict_xray
)
from utils.visualization_charts import show_probability_chart

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    layout="centered"
)

st.title("Healthcare Analytics Dashboard")

# --------------------------------------------------
# Backend Health Check
# --------------------------------------------------
def backend_available():
    result = HealthcareAPIClient.health_check()
    return result.get("status") == "healthy"

if not backend_available():
    st.error("❌ Backend is not running! Please start FastAPI on port 8000.")
    st.stop()

st.success("Backend is running")

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🩻 X-Ray Image Prediction",
    "🧬 Disease Prediction",
    "🏥 Patient Readmission Risk",
    "💊 Medicine Recommendation"
])

# ==================================================
# TAB 1: X-Ray Image Prediction
# ==================================================
with tab1:
    st.subheader("Chest X-Ray Disease Prediction")
    st.write("Upload a chest X-ray image to predict disease.")

    uploaded_file = st.file_uploader(
        "Upload X-ray Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded X-ray", use_column_width=True)

        if st.button("Predict X-Ray"):
            with st.spinner("Predicting X-ray..."):
                result = predict_xray(uploaded_file)

                if "error" in result:
                    st.error(f"Prediction failed ❌ {result['error']}")
                else:
                    st.success("Prediction Completed ✅")
                    st.json(result)

# ==================================================
# TAB 2: Disease Prediction
# ==================================================
with tab2:
    st.subheader("Disease Risk Prediction")
    st.write("Enter patient details to predict disease risk.")

    with st.form("disease_form"):
        age = st.number_input("Age", min_value=0, max_value=120, value=40)
        gender = st.selectbox("Gender", ["male", "female"])
        blood_pressure = st.number_input("Blood Pressure", value=120.0)
        sugar = st.number_input("Sugar (mg/dL)", value=90.0)
        bmi = st.number_input("BMI", value=23.0)
        cholesterol = st.number_input("Cholesterol (mg/dL)", value=180.0)

        submitted = st.form_submit_button("Predict Disease Risk")

    if submitted:
        payload = {
            "age": int(age),
            "gender": "M" if gender.lower() == "male" else "F",
            "blood_pressure": float(blood_pressure),
            "sugar": float(sugar),
            "bmi": float(bmi),
            "cholesterol": float(cholesterol)
        }

        res = HealthcareAPIClient.predict_disease(payload)

        if "error" in res:
            st.error(f"Prediction failed ❌ {res['error']}")
        else:
            st.success(f"Prediction: {res.get('prediction')}")
            show_probability_chart(res.get("prediction"))

# ==================================================
# TAB 3: Patient Readmission Risk
# ==================================================
with tab3:
    st.subheader("30-Day Readmission Risk Prediction")

    with st.form("readmission_form"):
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        time_in_hospital = st.number_input("Time in Hospital (days)", value=3)
        medication_count = st.number_input("Medication Count", value=5)
        blood_pressure = st.number_input("Blood Pressure", value=120.0)
        cholesterol = st.number_input("Cholesterol", value=180.0)
        bmi = st.number_input("BMI", value=25.0)

        diabetes = st.selectbox("Diabetes", [0, 1], format_func=lambda x: "Yes" if x else "No")
        hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "Yes" if x else "No")

        submit = st.form_submit_button("Predict Readmission Risk")

    if submit:
        payload = {
            "age": age,
            "time_in_hospital": time_in_hospital,
            "medication_count": medication_count,
            "blood_pressure": blood_pressure,
            "cholesterol": cholesterol,
            "bmi": bmi,
            "diabetes": diabetes,
            "hypertension": hypertension
        }

        result = HealthcareAPIClient.predict_readmission(payload)

        if "error" in result:
            st.error(f"Prediction failed ❌ {result['error']}")
        else:
            st.success("Prediction Successful 🎯")
            st.metric("Readmission Risk", result.get("readmission_risk"))
            st.metric("Probability", result.get("probability"))

# ==================================================
# TAB 4: Medicine Recommendation
# ==================================================
with tab4:
    st.subheader("Medicine Recommendation System")

    disease = st.text_input("Enter Disease")
    age = st.number_input("Enter Age", min_value=0, max_value=120, value=25)
    allergies_input = st.text_input("Allergies (comma separated)", "")

    if st.button("Get Medicine Recommendations"):
        allergies = [a.strip() for a in allergies_input.split(",") if a.strip()]

        payload = {
            "disease": disease,
            "age": age,
            "allergies": allergies
        }

        result = HealthcareAPIClient.recommend_medicine(payload)

        if "error" in result:
            st.error(result["error"])
        elif result:
            st.success("Recommendations generated successfully")
            st.table(pd.DataFrame(result))
        else:
            st.warning("No medicines found")

    st.caption("⚠️ This is not real medical advice. Consult a doctor.")
