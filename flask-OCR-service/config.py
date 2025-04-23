from dotenv import load_dotenv
import os
load_dotenv() 

class config():
    """Configuration class for the Flask application."""
    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:8000')
    frontend_url2 = os.environ.get('FRONTEND_URL2', 'http://localhost:8000')
    CELERY = {
        'broker_url': os.environ.get('CELERY_BROKER_URL'),
        'result_backend': os.environ.get('CELERY_RESULT_BACKEND'),
        'task_ignore_result': True,
    }
