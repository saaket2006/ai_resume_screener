import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

logger = logging.getLogger("resume_screener")

DATABASE_URL = settings.DATABASE_URL

# Safe fallback/resolution for local SQLite development
if not DATABASE_URL:
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, "resume_screener.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    logger.info("DATABASE_URL not configured. Defaulting to persistent SQLite: %s", DATABASE_URL)
elif DATABASE_URL.startswith("sqlite:///"):
    # Extract path and make it absolute if it is relative
    path = DATABASE_URL[10:]
    if not os.path.isabs(path):
        db_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.basename(path) or "resume_screener.db"
        if filename == "sql_app.db":
            filename = "resume_screener.db"
        db_path = os.path.abspath(os.path.join(db_dir, filename))
        DATABASE_URL = f"sqlite:///{db_path}"
        logger.info("Resolved relative SQLite URL to absolute path: %s", DATABASE_URL)

def create_db_engine(url: str):
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
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
