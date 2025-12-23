from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------
# Database
# --------------------------------
from app.database.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models import xray_prediction  # noqa: F401

# --------------------------------
# Routers
# --------------------------------
from app.api.v1.api import api_router
from app.api.v1.routers.disease_prediction import router as disease_router
from app.api.v1.routers.readmission_prediction import router as readmission_router

# --------------------------------
# Create DB tables
# --------------------------------
Base.metadata.create_all(bind=engine)

# --------------------------------
# FastAPI App
# --------------------------------
app = FastAPI(
    title="Healthcare ML & Analytics System",
    description="X-ray Disease Prediction + Readmission Risk Modules",
    version="1.0.0"
)

# --------------------------------
# CORS Middleware (for Streamlit / Frontend)
# --------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict: http://localhost:8501
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------
# Include Routers
# --------------------------------
app.include_router(api_router)  # existing API v1 router
app.include_router(disease_router, prefix="/api/v1")
app.include_router(readmission_router, prefix="/api/v1")

# --------------------------------
# Health Check
# --------------------------------
@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "Backend is Running",
        "modules": [
            "X-ray Image Classification",
            "Disease Prediction",
            "Patient Readmission Risk"
        ]
    }
