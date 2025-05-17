from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChunkMetadata(BaseModel):
    chunk_id: int
    source: str
    chunk_index: int
    extra: Optional[Dict[str, Any]] = None

class ChapterProcessResponse(BaseModel):
    status: str
    chunks: int
    message: str

class ExplanationResponse(BaseModel):
    explanation: str
    audio_path: Optional[str] = None
    audio_played: Optional[bool] = None

class QARequest(BaseModel):
    chapter_id: str
    question: str

class QAResponse(BaseModel):
    answer: str
    context: str
    sources: List[Dict[str, Any]]

class MCQOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class MCQQuestion(BaseModel):
    question: str
    options: MCQOption
    correct_answer: str
    explanation: str

class TestResponse(BaseModel):
    chapter_id: str
    questions: List[MCQQuestion]
    total_questions: int

class ValidateAnswerRequest(BaseModel):
    question: MCQQuestion
    user_answer: str

class ValidateAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
