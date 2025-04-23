import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
if os.environ.get("FLASK_ENV") is None:
    os.environ.setdefault("FLASK_ENV", "development")

app = Celery('celeryapp', broker=os.environ.get("CELERY_BROKER_URL"), backend=os.environ.get("CELERY_RESULT_BACKEND"))


USE_DJANGO_CONFIG = os.environ.get("USE_DJANGO_CONFIG", "False").lower() == "true"
if USE_DJANGO_CONFIG:
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
else:
    app.config_from_object('flaskapp.config', namespace='CELERY')
    app.autodiscover_tasks(['flaskapp.tasks'])

