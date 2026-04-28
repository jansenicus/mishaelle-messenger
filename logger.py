# logger.py
import logging

def setup_logger(level=logging.INFO, log_file=None):
    """
    Configure logging for the project.
    - level: logging level (INFO, DEBUG, WARNING, etc.)
    - log_file: optional path to log file (if None, logs only to console)
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )

    # Silence overly noisy libraries if needed
    logging.getLogger("telethon").setLevel(level)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logging.getLogger("mishaelle")
