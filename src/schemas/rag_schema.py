from pydantic import BaseModel

class RAGQueryRequest(BaseModel):
    """Schema for RAG query input."""
    query: str
