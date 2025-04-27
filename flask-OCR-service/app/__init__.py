from flask import Flask
# Import CORS for handling cross-origin requests
from flask_cors import CORS, cross_origin
from .utilis import celery_init_app  # Import the function to initialize Celery
from .routes import main
from config import Config  # Import the configuration class


def create_app(config):
    """Create and configure the Flask application."""
    app = Flask(
        __name__, instance_relative_config=True)  # Create Flask app instance
    app.config.from_object(config)  # Load configuration settings

    
    CORS(app, resources={
        r"/*": {
            "origins": [app.config['FRONTEND_URL'], app.config['DJANGO_BACKEND_URL'],"http://localhost:8000"],
        }
    }, supports_credentials=True)  # Enable CORS for the app

    # Initialize Celery with the Flask app
    celery_init_app(app)
    app.register_blueprint(main)  # Register the main blueprint
    return app
