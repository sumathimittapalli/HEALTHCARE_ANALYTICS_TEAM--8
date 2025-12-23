import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

# -----------------------------
# Database URL
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:868859@localhost:5432/disease_db"
)

# -----------------------------
# SQLAlchemy Engine
# -----------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# -----------------------------
# Session Local
# -----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------
# Base class for ORM models
# -----------------------------
Base = declarative_base()

# -----------------------------
# Dependency for FastAPI
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
