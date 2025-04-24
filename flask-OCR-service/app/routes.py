from flask import Flask, request, jsonify, Blueprint, current_app
from .logger_utils import info, error  # Replace direct logger usage
from PIL import Image
from io import BytesIO
import pytesseract
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

    if 'image' in request.files:
        info("Processing file from form-data")
        file = request.files['image']
        image_bytes = file.read()
    elif request.is_json and 'image' in request.json:
        info("Processing image from JSON payload as byte array")
        # Process image sent as byte array in JSON payload instead of file upload
        byte_array = request.json['image']  # list of ints
        image_bytes = bytes(byte_array)      # converting list of ints to bytes
    else:
        error("No valid image provided in either form-data or JSON payload")
    """ task = process_image.delay(image_bytes)
    extracted_text = task.get(timeout=30) """
    if not image_bytes:
        error("No image bytes found")
        return jsonify({"error": "No image provided"}), 400
    image = Image.open(BytesIO(image_bytes))
    extracted_text = pytesseract.image_to_string(image)
    print(f"Extracted text: {extracted_text}")
    # Send the result to Django backend API at route process_text_from_flask
    
    return jsonify({"sender": "bot", "text": extracted_text})
