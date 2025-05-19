from fastapi import Depends
from .service import LearningService

def get_learning_service() -> LearningService:
    """Get learning service instance."""
    return LearningService()
