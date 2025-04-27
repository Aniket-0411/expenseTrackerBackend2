from dotenv import load_dotenv
import os
load_dotenv() 

class Config:
    """Configuration class for the Flask application."""
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://django:8000')
    DJANGO_BACKEND_URL = os.environ.get('DJANGO_BACKEND_URL')
    CELERY = {
        'broker_url': os.environ.get('CELERY_BROKER_URL'),
        'result_backend': os.environ.get('CELERY_RESULT_BACKEND'),
        'task_ignore_result': True,
    }
