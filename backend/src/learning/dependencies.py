from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from .service import LearningService

def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_learning_service() -> LearningService:
    """Get learning service instance."""
    return LearningService()
