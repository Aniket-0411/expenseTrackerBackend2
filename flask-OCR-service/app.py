from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests  # Import requests to send HTTP requests
import pytesseract
from PIL import Image
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})  # Allow only your Django frontend

@app.route('/accept_image/', methods=['POST'])
def accept_image():
    # Process the image upload
    # Replace print with:
    logger.info("Image received and starting text extraction with pytesseract...")
    file = request.files['image']
    image = Image.open(file.stream)  # Open the uploaded image using Pillow
    # Extract text using pytesseract
    extracted_text = pytesseract.image_to_string(image)
    result = {"sender": "flask", "message": extracted_text}
    # Send the result to Django backend API at route process_text_from_flask
    url = os.environ.get("DJANGO_API_URL")
    django_api_url = url + "/get_rasa_response/"
    try:
        response = requests.post(django_api_url, json=result)
        django_response = response.json()
    except Exception as e:
        django_response = {"error": str(e)}
    logger.info("Text extraction and response from Django API complete.")
    return jsonify(django_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)