# Healthcare Analytics System

A comprehensive healthcare analytics platform that provides disease prediction and patient readmission risk analysis using machine learning models.

## 🏥 Features

- **Disease Risk Prediction**: Predict disease risk based on patient vitals (age, gender, blood pressure, sugar, BMI, cholesterol)
- **Readmission Risk Analysis**: Assess 30-day hospital readmission probability based on patient history
- **Interactive Dashboard**: User-friendly Streamlit interface for healthcare professionals
- **REST API**: FastAPI backend with comprehensive endpoints
- **Real-time Predictions**: Instant ML-powered predictions with confidence scores

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HEALTHCARE_ANALYTICS_TEAM--8
   ```

2. **Install Backend Dependencies**
   ```bash
   pip install -r backend/app/requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   pip install -r frontend/requirements.txt
   ```

4. **Set up Environment Variables**
   - Copy `.env` file and update database credentials if needed
   - Default configuration uses PostgreSQL with credentials: abc/abc/abc

### Running the Application

#### Option 1: Using Startup Scripts (Recommended)

**Start Backend:**
```bash
python start_backend.py
```
- Backend will be available at: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs

**Start Frontend (in a new terminal):**
```bash
python start_frontend.py
```
- Dashboard will be available at: http://localhost:8501

#### Option 2: Manual Startup

**Backend:**
```bash
uvicorn backend.app.healthcare_api:app --host 127.0.0.1 --port 8000 --reload
```

**Frontend:**
```bash
streamlit run frontend/healthcare_dashboard.py --server.port 8501
```

## 📊 Usage

### Web Dashboard
1. Open http://localhost:8501 in your browser
2. Use the **Disease Prediction** tab to assess disease risk
3. Use the **Patient Readmission Risk** tab to predict readmission probability

### API Endpoints

#### Health Check
```bash
GET http://127.0.0.1:8000/
```

#### Disease Prediction
```bash
POST http://127.0.0.1:8000/api/v1/disease/predict
Content-Type: application/json

{
  "age": 45,
  "gender": "male",
  "blood_pressure": 150.0,
  "sugar": 160.0,
  "bmi": 28.5,
  "cholesterol": 240.0
}
```

#### Readmission Prediction
```bash
POST http://127.0.0.1:8000/api/v1/readmission/predict
Content-Type: application/json

{
  "age": 65,
  "time_in_hospital": 5,
  "medication_count": 8,
  "blood_pressure": 145.0,
  "cholesterol": 220.0,
  "bmi": 28.9,
  "diabetes": 1,
  "hypertension": 1
}
```

## 🧠 Machine Learning Models

### Disease Prediction Model
- **Algorithm**: Random Forest Classifier
- **Features**: Age, Gender, Blood Pressure, Sugar, BMI, Cholesterol
- **Output**: Risk Level (High Risk / Low Risk)

### Readmission Prediction Model
- **Algorithm**: Random Forest Classifier
- **Features**: Age, Hospital Stay Duration, Medication Count, Vitals, Comorbidities
- **Output**: Risk Level (High/Low) + Probability Score

## 🏗️ Project Structure

```
├── backend/app/
│   ├── healthcare_api.py              # FastAPI main application
│   ├── api/v1/routers/               # API route handlers
│   ├── models/                       # Database models
│   ├── schemas/                      # Pydantic validation schemas
│   ├── database/                     # Database configuration & operations
│   ├── ml_models/                    # Trained ML models & training scripts
│   └── utils/                        # Utility functions
├── frontend/
│   ├── healthcare_dashboard.py       # Streamlit main application
│   └── utils/                        # Frontend utilities
├── datasets/                         # Training datasets
├── .env                             # Environment configuration
└── start_*.py                       # Startup scripts
```

## 🔧 Development

### Training New Models
```bash
# Train disease prediction model
python backend/app/ml_models/disease_prediction_trainer.py

# Train readmission prediction model
python backend/app/ml_models/readmission_prediction_trainer.py
```

### Database Setup
The application uses PostgreSQL by default. Update `.env` file with your database credentials:
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

## 📈 Model Performance

Both models are trained on healthcare datasets and provide:
- Real-time predictions
- Confidence scores
- Feature importance analysis
- Robust error handling

## 🛡️ Security Features

- Input validation using Pydantic schemas
- CORS middleware for secure frontend-backend communication
- Environment-based configuration
- SQL injection protection via SQLAlchemy ORM

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at http://127.0.0.1:8000/docs
2. Review the project structure in `PROJECT_STRUCTURE.md`
3. Ensure all dependencies are installed correctly

---

**Healthcare Analytics System** - Empowering healthcare decisions with AI 🏥✨