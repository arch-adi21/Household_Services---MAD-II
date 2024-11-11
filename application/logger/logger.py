import logging
import logging.config
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(pathname)s - %(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
        },
        'standard': {
            'format': '%(asctime)s - %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'level': 'DEBUG',
            'filename': 'logs/app.log',
            'mode': 'w',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['file_handler', 'console'],
        'level': 'DEBUG',
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Create and export a logger instance for reuse
logger = logging.getLogger(__name__)
