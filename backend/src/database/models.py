from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    learning_progress = relationship("LearningProgress", back_populates="user")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, index=True, nullable=False)
    subject = Column(String, index=True, nullable=False)
    description = Column(String)
    total_sections = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    learning_progress = relationship("LearningProgress", back_populates="chapter")

class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    chapter_id = Column(String, ForeignKey("chapters.id"), nullable=False)
    
    # Progress tracking
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_sections = Column(Integer, default=0)
    
    # Test results
    test_attempts = Column(Integer, default=0)
    highest_score = Column(Float, default=0.0)  # 0.0 to 100.0
    test_history = Column(JSON, default=list)  # List of test attempts with scores and dates
    
    # Streak tracking
    current_streak = Column(Integer, default=0)  # Current consecutive days of learning
    longest_streak = Column(Integer, default=0)  # Longest streak achieved
    last_streak_date = Column(DateTime(timezone=True))  # Last date when streak was updated
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_progress")
    chapter = relationship("Chapter", back_populates="learning_progress")

    class Config:
        orm_mode = True 