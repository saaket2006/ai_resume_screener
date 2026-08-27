import os
from typing import List, Set
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Settings
    API_TITLE: str = os.getenv("API_TITLE", "Nipun API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(",") if origin.strip()
    ]
    
    # Rate Limiting
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "5/minute")
    
    # File Upload Limits
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", str(5 * 1024 * 1024))) # Default 5MB
    
    ALLOWED_EXTENSIONS: Set[str] = {
        ext.strip().lower() for ext in os.getenv("ALLOWED_EXTENSIONS", ".pdf,.docx,.doc").split(",") if ext.strip()
    }
    
    # Log Level
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # JWT Authentication Settings
    JWT_SECRET: str = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES", "1440")) # Default 24 hours
    FIREBASE_PROJECT_ID: str = os.getenv("VITE_FIREBASE_PROJECT_ID", "ai-resume-screener-69d23")


settings = Settings()

if not settings.JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is not set. It is required for security.")
