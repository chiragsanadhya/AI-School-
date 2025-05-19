from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# Existing schemas
# ... (keep existing schemas like ChunkMetadata, ChapterProcessResponse, etc.)

class TestAttempt(BaseModel):
    score: float
    total_questions: int
    correct_answers: int
    attempted_at: datetime
    questions_attempted: List[Dict[str, Any]]

class LearningProgressBase(BaseModel):
    chapter_id: str
    is_completed: bool = False
    completion_percentage: float = Field(0.0, ge=0.0, le=100.0)
    completed_sections: int = 0
    test_attempts: int = 0
    highest_score: float = Field(0.0, ge=0.0, le=100.0)
    test_history: List[TestAttempt] = []
    current_streak: int = 0
    longest_streak: int = 0

class LearningProgressCreate(LearningProgressBase):
    pass

class LearningProgressUpdate(BaseModel):
    is_completed: Optional[bool] = None
    completion_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    completed_sections: Optional[int] = None
    test_attempt: Optional[TestAttempt] = None

class LearningProgressResponse(LearningProgressBase):
    id: str
    user_id: str
    last_accessed_at: datetime
    last_streak_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProgressSummary(BaseModel):
    total_chapters: int
    completed_chapters: int
    overall_completion_percentage: float
    current_streak: int
    longest_streak: int
    subject_progress: Dict[str, Dict[str, Any]]  # Subject-wise progress
    recent_test_scores: List[Dict[str, Any]]
    last_activity_date: datetime

class SubjectProgress(BaseModel):
    subject: str
    total_chapters: int
    completed_chapters: int
    completion_percentage: float
    average_test_score: float
    chapters_in_progress: List[Dict[str, Any]]
    recently_completed: List[Dict[str, Any]] 