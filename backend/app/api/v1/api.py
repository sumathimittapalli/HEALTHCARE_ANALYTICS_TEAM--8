from fastapi import APIRouter
from app.api.v1.routers import predictions

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(
    predictions.router,
    prefix="/predictions",
    tags=["X-Ray Prediction"]
)
