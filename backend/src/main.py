from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from pathlib import Path
from src.auth.dependencies import get_current_user
from src.auth.router import router as auth_router
from src.learning.router import router as learning_router
from src.learning.progress_router import router as progress_router
from src.auth.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI School API",
    description="AI-powered interactive learning platform API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",  # Vite dev server alternative
        "http://localhost:3000",  # React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
PDF_DIR = UPLOAD_DIR / "pdfs"
EMBEDDINGS_DIR = UPLOAD_DIR / "embeddings"

for directory in [UPLOAD_DIR, PDF_DIR, EMBEDDINGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(UPLOAD_DIR)), name="static")

# Initialize settings
settings = get_settings()
logger.info("Initialized settings with Supabase configuration")

# Include routers
app.include_router(learning_router)
app.include_router(auth_router)
app.include_router(progress_router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI School API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
