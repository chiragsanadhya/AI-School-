from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Dict, Any, List
from pathlib import Path
import tempfile
import shutil
import os

from .service import LearningService
from .dependencies import get_learning_service

router = APIRouter(prefix="/learning", tags=["learning"])

@router.post("/chapters/process")
async def process_chapter(
    file: UploadFile = File(...),
    metadata: Dict[str, Any] = None,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Process a new chapter PDF and prepare it for learning features."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = Path(temp_file.name)

        try:
            # Process the chapter
            result = await learning_service.process_chapter(temp_path, metadata)
            return result
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chapters/{chapter_id}/ask")
async def ask_chapter_question(
    chapter_id: str,
    question: str,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Ask a question about a specific chapter."""
    try:
        result = await learning_service.get_chapter_answer(question, chapter_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
async def explain_text(
    text: str,
    save_audio: bool = False,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Generate explanation and optionally convert to speech."""
    try:
        result = await learning_service.explain_text(text, save_audio)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chapters/{chapter_id}/test")
async def generate_chapter_test(
    chapter_id: str,
    num_questions: int = 5,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Generate a test for a specific chapter."""
    try:
        result = await learning_service.generate_test(chapter_id, num_questions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test/validate")
async def validate_answer(
    question: Dict[str, Any],
    user_answer: str,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Validate a user's answer to a test question."""
    try:
        result = await learning_service.validate_test_answer(question, user_answer)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_content(
    query: str,
    k: int = 3,
    learning_service: LearningService = Depends(get_learning_service)
):
    """Search for relevant content across chapters."""
    try:
        results = await learning_service.search_chapter_content(query, k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
