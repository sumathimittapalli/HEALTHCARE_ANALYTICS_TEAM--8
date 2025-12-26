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
from app.api.v1.routers.medicine_routers import router as medicine_router

# --------------------------------
# Create DB tables (RUN ONCE)
# --------------------------------
Base.metadata.create_all(bind=engine)
print("✅ Database tables created")

# --------------------------------
# FastAPI App
# --------------------------------
app = FastAPI(
    title="Healthcare ML & Medicine Recommendation System",
    description=(
        "X-ray Image Classification, Disease Prediction, "
        "Patient Readmission Risk, and Medicine Recommendation"
    ),
    version="1.0.0"
)

# --------------------------------
# CORS Middleware (Streamlit / Frontend)
# --------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later (e.g., http://localhost:8501)
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
app.include_router(medicine_router, prefix="/medicine", tags=["Medicine"])

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
            "Patient Readmission Risk",
            "Medicine Recommendation"
        ]
    }
