# core/config.py
from pydantic import PostgresDsn, validator
from typing import Optional, Dict, Any
import secrets
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    # Project Metadata
    PROJECT_NAME: str = "AI School"
    PROJECT_DESCRIPTION: str = "Interactive Learning Platform"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Database Configuration
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    # Security Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # ML Model Configurations
    GROQ_API_KEY: str
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "ollama/llama2"
    OLLAMA_HOST: str = "http://localhost:11434"
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",    # React default port
        "http://localhost:5173",    # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        
        username = info.data.get("DATABASE_USERNAME")
        password = info.data.get("DATABASE_PASSWORD")
        host = info.data.get("DATABASE_HOSTNAME")
        port = info.data.get("DATABASE_PORT")
        db = info.data.get("DATABASE_NAME")
        
        return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db}"
    
    @field_validator("SUPABASE_URL", "SUPABASE_KEY", "GROQ_API_KEY", mode="before")
    def validate_required_keys(cls, v: Optional[str], info) -> str:
        if not v:
            raise ValueError(f"{info.field_name} must be provided")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()