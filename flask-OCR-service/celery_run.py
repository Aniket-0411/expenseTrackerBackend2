from flask import Flask
from celery_app import celery_init_app  # Import the function to initialize Celery
from config import config  # Import configuration settings

flask_app = Flask(__name__)                 # renamed from `app`
flask_app.config.from_object(config)        # Load configuration settings from config.py

print("Initializing Celery...")
print(f"Celery broker URL: {flask_app.config['CELERY']['broker_url']}")
print(f"Celery result backend: {flask_app.config['CELERY']['result_backend']}")

# Initialize Celery with the Flask app
celery_app = celery_init_app(flask_app)

# Expose as 'celery' so `celery -A celery_run worker` finds it
celery = celery_app