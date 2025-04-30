from app import create_app
from config import Config

flask_app = create_app(Config)  # Create the Flask app instance
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    # Run the Flask app with the WSGI server
    flask_app.run(host='0.0.0.0', port=5000, debug=True)