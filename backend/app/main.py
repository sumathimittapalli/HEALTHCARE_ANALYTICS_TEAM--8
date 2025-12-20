from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.disease_prediction import router as disease_router
from app.database.connection import Base, engine

# Create DB tables (if not exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Analytics API",
    description="Disease Prediction Module (Diabetes/Heart/Liver) - Module 1",
    version="1.0.0"
)

# ----------------------------
# CORS middleware for Streamlit
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. Later restrict to Streamlit URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your disease prediction router
app.include_router(disease_router)

# Health check endpoint
@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Healthcare Analytics API is running"}
