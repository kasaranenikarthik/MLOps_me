from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path


LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_rotating_handler():
    return RotatingFileHandler(
    LOG_DIR / "rotating.log",
    maxBytes=5000000, # 5 MB
    backupCount=5,
    encoding="utf-8"
    )


def get_timed_rotating_handler():
    return TimedRotatingFileHandler(
    LOG_DIR / "timed.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
    )