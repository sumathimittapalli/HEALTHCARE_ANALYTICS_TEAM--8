import streamlit as st
from utils.healthcare_api_client import predict_xray
from utils.healthcare_api_client import HealthcareAPIClient
from utils.visualization_charts import show_probability_chart

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    layout="centered"
)

st.title("🏥 Healthcare Analytics Dashboard")

# --------------------------------------------------
# Backend Health Check
# --------------------------------------------------
def backend_available():
    result = HealthcareAPIClient.health_check()
    return result.get("status") == "healthy"

if not backend_available():
    st.error("❌ Backend is not running! Please start FastAPI on port 8000.")
    st.stop()

st.success("✅ Backend is running")

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🩻 X-Ray Image Prediction",
    "🩺 Disease Prediction",
    "📊 Patient Readmission Risk"
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
        blood_pressure = st.number_input("Blood Pressure", min_value=0.0, value=120.0)
        sugar = st.number_input("Sugar (mg/dL)", min_value=0.0, value=90.0)
        bmi = st.number_input("BMI", min_value=0.0, value=23.0)
        cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, value=180.0)

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

        if res is None or "error" in res:
            st.error(f"Prediction failed ❌ {res.get('error') if res else ''}")
        else:
            if res.get("status") == "success":
                st.success(f"Prediction: {res.get('prediction')}")
                show_probability_chart(res.get("prediction"))
            else:
                st.error("Prediction failed: " + str(res))

# ==================================================
# TAB 3: Patient Readmission Risk
# ==================================================
with tab3:
    st.subheader("30-Day Readmission Risk Prediction")
    st.write("Enter patient hospitalization details.")

    with st.form("readmission_form"):
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        time_in_hospital = st.number_input("Time in Hospital (days)", min_value=0, value=3)
        medication_count = st.number_input("Medication Count", min_value=0, value=5)

        blood_pressure = st.number_input("Blood Pressure", min_value=1.0, value=120.0)
        cholesterol = st.number_input("Cholesterol", min_value=1.0, value=180.0)
        bmi = st.number_input("BMI", min_value=1.0, value=25.0)

        diabetes = st.selectbox(
            "Diabetes",
            options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        hypertension = st.selectbox(
            "Hypertension",
            options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

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
