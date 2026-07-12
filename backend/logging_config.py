import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_level: str = "INFO"):
    # Ensure logs directory exists in the workspace
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(backend_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    # Define formats
    console_format = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%H:%M:%S")
    file_format = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s:%(filename)s:%(lineno)d | %(message)s")

    # Get the app-specific logger
    logger = logging.getLogger("resume_screener")
    logger.setLevel(log_level)
    logger.handlers.clear()  # Clear existing handlers to prevent double logs

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_format)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    # File Handler (rotating logs, max 5MB, keeping 3 backups)
    try:
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
        file_handler.setFormatter(file_format)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
        logger.info(f"Logging initialized. Log file saved at: {log_file}")
    except Exception as e:
        logger.warning(f"Could not create file log handler: {e}")

    # Prevent logs from propagating to the default root logger
    logger.propagate = False
