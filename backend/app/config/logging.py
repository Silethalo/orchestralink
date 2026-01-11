"""
File contains logging logic.
"""

import logging
from logging.config import dictConfig
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / 'app.log'
ERROR_LOG_FILE = LOGS_DIR / 'error.log'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'default',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOG_FILE,
            'maxBytes': 1 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'default',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file', 'error_file', 'console']
    },
}

def setup_logging():
    """Set up logging configuration."""
    dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info("Logging initialized.")

setup_logging()
