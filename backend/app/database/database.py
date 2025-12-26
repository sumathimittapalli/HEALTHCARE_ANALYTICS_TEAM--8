import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------
# Load environment variables
# ---------------------------------
load_dotenv()

# ---------------------------------
# Database URL (from .env or fallback)
# ---------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Vijayram7@localhost:5432/Healthcare"
)

# ---------------------------------
# SQLAlchemy Engine
# ---------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# ---------------------------------
# Session Factory
# ---------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------
# Base class for ORM models
# ---------------------------------
Base = declarative_base()

# ---------------------------------
# FastAPI DB Dependency
# ---------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
