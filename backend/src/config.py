import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
AUDIO_DIR = UPLOAD_DIR / "audio"
PDF_DIR = UPLOAD_DIR / "pdfs"

# Create necessary directories
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:bhoomi#123@db.mbkzwmbutivszdlyzfcr.supabase.co:5432/postgres")

# Supabase settings
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://mbkzwmbutivszdlyzfcr.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Must be set in .env

# AI Model settings
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_BASE_URL = "http://localhost:11434"
LLM_MODEL_NAME = "llama3-8b-8192"

# Document processing settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
VECTOR_TABLE_NAME = "document_embeddings"
VECTOR_QUERY_NAME = "match_documents"

# Audio settings
AUDIO_SAMPLE_RATE = 22050

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Must be set in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# API settings
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "AI School"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
