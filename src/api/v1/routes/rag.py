from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.ml.rag import RAGChatbot

# Define request model
class QueryRequest(BaseModel):
    question: str

# Initialize FastAPI router
router = APIRouter()

@router.get("/")
async def get_rag():
    return {"message": "RAG endpoint - Coming soon"}

# Load RAG chatbot instance
try:
    chatbot = RAGChatbot()
except Exception as e:
    print(f"Warning: RAG Chatbot initialization failed: {e}")
    chatbot = None

@router.post("/chat")
async def chat_with_rag(query: QueryRequest):
    if not chatbot:
        raise HTTPException(status_code=503, detail="RAG service unavailable")
    try:
        response = chatbot.chat(query.question)
        return {"question": query.question, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
