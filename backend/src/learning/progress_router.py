from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database.database import get_db
from ..auth.dependencies import get_current_user
from ..auth.schemas import UserResponse
from .progress_service import ProgressService
from .schemas import (
    LearningProgressUpdate,
    LearningProgressResponse,
    UserProgressSummary,
    SubjectProgress
)

router = APIRouter(prefix="/progress", tags=["progress"])

def get_progress_service(db: Session = Depends(get_db)) -> ProgressService:
    """Get progress service instance."""
    return ProgressService(db)

@router.put("/chapters/{chapter_id}", response_model=LearningProgressResponse)
async def update_chapter_progress(
    chapter_id: str,
    update_data: LearningProgressUpdate,
    current_user: UserResponse = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Update learning progress for a specific chapter."""
    try:
        progress = progress_service.update_progress(
            user_id=current_user.id,
            chapter_id=chapter_id,
            update_data=update_data
        )
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", response_model=UserProgressSummary)
async def get_progress_summary(
    current_user: UserResponse = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Get overall learning progress summary for the current user."""
    try:
        summary = progress_service.get_user_progress_summary(current_user.id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/subjects/{subject}", response_model=SubjectProgress)
async def get_subject_progress(
    subject: str,
    current_user: UserResponse = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Get detailed progress for a specific subject."""
    try:
        progress = progress_service.get_subject_progress(current_user.id, subject)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/subjects", response_model=Dict[str, Dict[str, Any]])
async def get_all_subjects_progress(
    current_user: UserResponse = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Get progress summary for all subjects."""
    try:
        summary = progress_service.get_user_progress_summary(current_user.id)
        return summary.subject_progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 