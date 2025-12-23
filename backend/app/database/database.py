import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------
# Load environment variables (.env)
# ---------------------------------
load_dotenv()

# ---------------------------------
# Database URL
# ---------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:9121665288@localhost:5432/image_db"
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
# FastAPI Dependency
# ---------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
