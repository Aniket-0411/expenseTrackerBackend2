from app import create_app
from config import Config

flask_app = create_app(Config)  # Create the Flask app instance
celery_app = flask_app.extensions["celery"]