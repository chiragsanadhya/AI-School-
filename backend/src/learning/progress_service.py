import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.models import LearningProgress, Chapter, User
from .schemas import LearningProgressUpdate, TestAttempt, UserProgressSummary, SubjectProgress

logger = logging.getLogger(__name__)

class ProgressService:
    def __init__(self, db: Session):
        self.db = db

    def update_progress(self, user_id: str, chapter_id: str, update_data: LearningProgressUpdate) -> LearningProgress:
        """Update learning progress for a user and chapter."""
        try:
            # Get or create progress record
            progress = self.db.query(LearningProgress).filter(
                LearningProgress.user_id == user_id,
                LearningProgress.chapter_id == chapter_id
            ).first()

            if not progress:
                progress = LearningProgress(
                    user_id=user_id,
                    chapter_id=chapter_id
                )
                self.db.add(progress)

            # Update progress fields
            if update_data.is_completed is not None:
                progress.is_completed = update_data.is_completed
            if update_data.completion_percentage is not None:
                progress.completion_percentage = update_data.completion_percentage
            if update_data.completed_sections is not None:
                progress.completed_sections = update_data.completed_sections

            # Update test attempt if provided
            if update_data.test_attempt:
                self._update_test_attempt(progress, update_data.test_attempt)

            # Update streak
            self._update_streak(progress)

            # Update last accessed timestamp
            progress.last_accessed_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(progress)
            return progress

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating progress: {str(e)}")
            raise

    def _update_test_attempt(self, progress: LearningProgress, test_attempt: TestAttempt):
        """Update test attempt history and statistics."""
        # Add to test history
        if not progress.test_history:
            progress.test_history = []
        progress.test_history.append(test_attempt.dict())

        # Update test statistics
        progress.test_attempts += 1
        if test_attempt.score > progress.highest_score:
            progress.highest_score = test_attempt.score

    def _update_streak(self, progress: LearningProgress):
        """Update user's learning streak."""
        now = datetime.utcnow()
        
        if not progress.last_streak_date:
            progress.current_streak = 1
            progress.last_streak_date = now
            return

        # Check if last activity was yesterday
        if (now.date() - progress.last_streak_date.date()) == timedelta(days=1):
            progress.current_streak += 1
            if progress.current_streak > progress.longest_streak:
                progress.longest_streak = progress.current_streak
        # If more than a day has passed, reset streak
        elif (now.date() - progress.last_streak_date.date()) > timedelta(days=1):
            progress.current_streak = 1
        
        progress.last_streak_date = now

    def get_user_progress_summary(self, user_id: str) -> UserProgressSummary:
        """Get overall progress summary for a user."""
        try:
            # Get all progress records for the user
            progress_records = self.db.query(LearningProgress).filter(
                LearningProgress.user_id == user_id
            ).all()

            # Get all chapters
            total_chapters = self.db.query(Chapter).count()
            completed_chapters = sum(1 for p in progress_records if p.is_completed)

            # Calculate overall completion percentage
            if total_chapters > 0:
                overall_completion = sum(p.completion_percentage for p in progress_records) / total_chapters
            else:
                overall_completion = 0.0

            # Get current and longest streak
            current_streak = max((p.current_streak for p in progress_records), default=0)
            longest_streak = max((p.longest_streak for p in progress_records), default=0)

            # Get subject-wise progress
            subject_progress = self._get_subject_progress(progress_records)

            # Get recent test scores
            recent_test_scores = self._get_recent_test_scores(progress_records)

            # Get last activity date
            last_activity = max((p.last_accessed_at for p in progress_records), default=datetime.utcnow())

            return UserProgressSummary(
                total_chapters=total_chapters,
                completed_chapters=completed_chapters,
                overall_completion_percentage=overall_completion,
                current_streak=current_streak,
                longest_streak=longest_streak,
                subject_progress=subject_progress,
                recent_test_scores=recent_test_scores,
                last_activity_date=last_activity
            )

        except Exception as e:
            logger.error(f"Error getting user progress summary: {str(e)}")
            raise

    def _get_subject_progress(self, progress_records: List[LearningProgress]) -> Dict[str, Dict[str, Any]]:
        """Calculate progress for each subject."""
        subject_stats = {}
        
        for progress in progress_records:
            chapter = self.db.query(Chapter).get(progress.chapter_id)
            if not chapter:
                continue

            if chapter.subject not in subject_stats:
                subject_stats[chapter.subject] = {
                    "total_chapters": 0,
                    "completed_chapters": 0,
                    "total_completion": 0.0,
                    "total_score": 0.0,
                    "test_count": 0,
                    "chapters_in_progress": [],
                    "recently_completed": []
                }

            stats = subject_stats[chapter.subject]
            stats["total_chapters"] += 1
            
            if progress.is_completed:
                stats["completed_chapters"] += 1
                stats["recently_completed"].append({
                    "chapter_id": chapter.id,
                    "title": chapter.title,
                    "completed_at": progress.updated_at
                })
            else:
                stats["chapters_in_progress"].append({
                    "chapter_id": chapter.id,
                    "title": chapter.title,
                    "completion_percentage": progress.completion_percentage
                })

            stats["total_completion"] += progress.completion_percentage
            if progress.test_attempts > 0:
                stats["total_score"] += progress.highest_score
                stats["test_count"] += 1

        # Calculate final statistics for each subject
        for subject, stats in subject_stats.items():
            if stats["total_chapters"] > 0:
                stats["completion_percentage"] = stats["total_completion"] / stats["total_chapters"]
            else:
                stats["completion_percentage"] = 0.0

            if stats["test_count"] > 0:
                stats["average_test_score"] = stats["total_score"] / stats["test_count"]
            else:
                stats["average_test_score"] = 0.0

            # Sort and limit recently completed and in-progress chapters
            stats["recently_completed"] = sorted(
                stats["recently_completed"],
                key=lambda x: x["completed_at"],
                reverse=True
            )[:5]
            
            stats["chapters_in_progress"] = sorted(
                stats["chapters_in_progress"],
                key=lambda x: x["completion_percentage"],
                reverse=True
            )

            # Remove temporary fields
            del stats["total_completion"]
            del stats["total_score"]
            del stats["test_count"]

        return subject_stats

    def _get_recent_test_scores(self, progress_records: List[LearningProgress]) -> List[Dict[str, Any]]:
        """Get recent test scores across all chapters."""
        recent_scores = []
        
        for progress in progress_records:
            if not progress.test_history:
                continue

            chapter = self.db.query(Chapter).get(progress.chapter_id)
            if not chapter:
                continue

            # Get the most recent test attempt
            latest_attempt = max(
                progress.test_history,
                key=lambda x: x["attempted_at"]
            )

            recent_scores.append({
                "chapter_id": chapter.id,
                "chapter_title": chapter.title,
                "subject": chapter.subject,
                "score": latest_attempt["score"],
                "attempted_at": latest_attempt["attempted_at"]
            })

        # Sort by attempt date and return most recent 10
        return sorted(
            recent_scores,
            key=lambda x: x["attempted_at"],
            reverse=True
        )[:10]

    def get_subject_progress(self, user_id: str, subject: str) -> SubjectProgress:
        """Get detailed progress for a specific subject."""
        try:
            # Get all chapters for the subject
            chapters = self.db.query(Chapter).filter(
                Chapter.subject == subject
            ).all()

            # Get progress for all chapters in the subject
            progress_records = self.db.query(LearningProgress).filter(
                LearningProgress.user_id == user_id,
                LearningProgress.chapter_id.in_([c.id for c in chapters])
            ).all()

            # Calculate subject statistics
            total_chapters = len(chapters)
            completed_chapters = sum(1 for p in progress_records if p.is_completed)
            
            if total_chapters > 0:
                completion_percentage = sum(p.completion_percentage for p in progress_records) / total_chapters
            else:
                completion_percentage = 0.0

            # Calculate average test score
            test_scores = [p.highest_score for p in progress_records if p.test_attempts > 0]
            average_test_score = sum(test_scores) / len(test_scores) if test_scores else 0.0

            # Get chapters in progress and recently completed
            chapters_in_progress = []
            recently_completed = []

            for progress in progress_records:
                chapter = next(c for c in chapters if c.id == progress.chapter_id)
                if progress.is_completed:
                    recently_completed.append({
                        "chapter_id": chapter.id,
                        "title": chapter.title,
                        "completed_at": progress.updated_at,
                        "highest_score": progress.highest_score
                    })
                else:
                    chapters_in_progress.append({
                        "chapter_id": chapter.id,
                        "title": chapter.title,
                        "completion_percentage": progress.completion_percentage,
                        "last_accessed": progress.last_accessed_at
                    })

            # Sort lists
            recently_completed.sort(key=lambda x: x["completed_at"], reverse=True)
            chapters_in_progress.sort(key=lambda x: x["completion_percentage"], reverse=True)

            return SubjectProgress(
                subject=subject,
                total_chapters=total_chapters,
                completed_chapters=completed_chapters,
                completion_percentage=completion_percentage,
                average_test_score=average_test_score,
                chapters_in_progress=chapters_in_progress,
                recently_completed=recently_completed
            )

        except Exception as e:
            logger.error(f"Error getting subject progress: {str(e)}")
            raise 