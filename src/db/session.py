from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

# Use DATABASE_URL from config.py (which reads from .env)
DATABASE_URL = settings.DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Define Base class for models
Base = declarative_base()
