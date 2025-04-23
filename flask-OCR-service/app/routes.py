from flask import Flask, request, jsonify, Blueprint, current_app
from .logger_utils import info, error  # Replace direct logger usage
#------tasks--------
from .task import process_image

main = Blueprint('main', __name__)

@main.route('/test/', methods=['GET'])
def test():
    # test config.py is working and get CELERY settings
    celery = current_app.config['CELERY']
    broker_url = celery['broker_url']
    print(f"Broker URL: {broker_url}")
    result_backend = celery['result_backend']
    
    return jsonify({"status": "Flask is running"})

@main.route('/accept_image/', methods=['POST'])
def accept_image():
    # Process the image upload
    info("Image received and starting text extraction with pytesseract...")
    info(f"Request content type: {request.content_type}")
    
    data = process_image.delay(request)  # Call the Celery task asynchronously
    # Send the result to Django backend API at route process_text_from_flask

    return jsonify({"data": data})
