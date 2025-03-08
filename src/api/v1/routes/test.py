from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.ml.test import SupabaseHandler, MCQGenerator
import os

router = APIRouter()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize handlers
supabase_handler = SupabaseHandler(SUPABASE_URL, SUPABASE_KEY)
mcq_generator = MCQGenerator(GROQ_API_KEY)

class TestRequest(BaseModel):
    topic: str
    num_questions: int = 5

# Fix: Add error handling for missing environment variables
if not all([SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY]):
    raise ValueError("Missing required environment variables")

@router.post("/generate-mcq")
async def generate_mcq(request: TestRequest):
    """Endpoint to generate MCQs for a given topic."""
    context = supabase_handler.fetch_relevant_text(request.topic)
    if not context:
        raise HTTPException(status_code=404, detail="No relevant content found!")
    
    mcqs = mcq_generator.generate_mcqs(context, request.num_questions)
    return {"topic": request.topic, "mcqs": mcqs}
