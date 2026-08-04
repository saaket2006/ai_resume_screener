import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

logger = logging.getLogger("resume_screener")

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    logger.critical("Startup Configuration Failed: DATABASE_URL is not set.")
    raise RuntimeError("DATABASE_URL is not set. A PostgreSQL/Supabase connection is required.")

if not (DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")):
    logger.critical("Startup Configuration Failed: ONLY PostgreSQL (Supabase) is supported. Received: %s", DATABASE_URL)
    raise RuntimeError("Only PostgreSQL (Supabase) connections are allowed. Local SQLite databases are disabled.")

def create_db_engine(url: str):
    return create_engine(url)

# Attempt connection to the configured database. If it fails, fail fast.
try:
    logger.info("Connecting to database: %s", DATABASE_URL)
    engine = create_db_engine(DATABASE_URL)
    # Test connection immediately
    with engine.connect() as conn:
        pass
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.critical("Database connection failed for URL: %s. Application stopping. Error: %s", DATABASE_URL, e)
    raise RuntimeError(f"Database connection failed: {e}") from e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI Dependency to yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
