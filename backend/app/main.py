from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ----------------------------
# Database
# ----------------------------
from app.database.database import Base, engine
# Patient model imported in routers where needed

# ----------------------------
# Routers
# ----------------------------
from app.api.v1.routers.disease_prediction import router as disease_router
from app.api.v1.routers.readmission_prediction import router as readmission_router

# ----------------------------
# Create DB tables
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI(
    title="Healthcare Analytics API",
    description="Disease Prediction + Patient Readmission Modules",
    version="1.0.0"
)

# ----------------------------
# CORS Middleware (Streamlit)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later (e.g. http://localhost:8501)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Include Routers
# ----------------------------
app.include_router(disease_router, prefix="/api/v1")
app.include_router(readmission_router, prefix="/api/v1")

# ----------------------------
# Health Check
# ----------------------------
@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "Healthcare Analytics API is running",
        "modules": [
            "Disease Prediction",
            "Patient Readmission Risk"
        ]
    }

