import os
from pathlib import Path

DOCKER_BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define the log directory
log_directory = os.path.join(DOCKER_BASE_DIR, "logs")

# Ensure the log directory exists
Path(log_directory).mkdir(parents=True, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_directory, "info.log"),
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
