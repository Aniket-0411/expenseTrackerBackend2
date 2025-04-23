from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests  # Import requests to send HTTP requests
import pytesseract
from PIL import Image
import logging
from config import config  # Import configuration settings
from io import BytesIO  # Added import for handling byte arrays
from logger_utils import info, error  # Replace direct logger usage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config.from_object(config)  # Load configuration settings

CORS(app, resources={r"/*": {"origins": [app.config['frontend_url'], app.config['frontend_url2']], 
                            "methods": ["POST", "GET", "OPTIONS"],
                            "allow_headers": ["Content-Type", "Authorization"]}})

@app.route('/test/', methods=['GET'])
def test():
    # Test endpoint to check if Flask is running
    return jsonify({"status": "Flask is running"})

@app.route('/accept_image/', methods=['POST'])
def accept_image():
    # Process the image upload
    info("Image received and starting text extraction with pytesseract...")
    info(f"Request content type: {request.content_type}")
    
    if 'image' in request.files:
        info("Processing file from form-data")
        file = request.files['image']
        image = Image.open(file.stream)  # Open the uploaded image using Pillow
    elif request.is_json and 'image' in request.json:
        info("Processing image from JSON payload as byte array")
        # Process image sent as byte array in JSON payload instead of file upload
        byte_array = request.json['image']  # list of ints
        image_bytes = bytes(byte_array)      # converting list of ints to bytes
        image = Image.open(BytesIO(image_bytes))
        # check image opened
        if image is None:
            error("Failed to open image from byte array")
            return jsonify({"error": "Failed to open image"}), 400
    else:
        error("No valid image provided in either form-data or JSON payload")
        return jsonify({"error": "No image provided"}), 400

    extracted_text = pytesseract.image_to_string(image)
    if not extracted_text:
        extracted_text = "No text found in the image."
    info(f"Extracted text: {extracted_text}")
    data = [{"sender": "bot", "text": extracted_text}]
    # Send the result to Django backend API at route process_text_from_flask

    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)