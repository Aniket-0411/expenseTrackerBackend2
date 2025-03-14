from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  # Import requests to send HTTP requests
import easyocr
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})  # Allow only your Django frontend

# Initialize EasyOCR reader once (here, for English)
reader = easyocr.Reader(['en'])

@app.route('/accept_image/', methods=['POST'])
def accept_image():
    # Process the image upload
    file = request.files['image']
    image = Image.open(file.stream)  # Open the uploaded image using Pillow
    image_np = np.array(image)  # Convert to numpy array for EasyOCR

    # Extract text using EasyOCR
    result_list = reader.readtext(image_np, detail=0)  # detail=0 returns only recognized text
    extracted_text = " ".join(result_list)
    result = {"sender": "flask", "message": extracted_text}
    
    # Send the result to Django backend API at route process_text_from_flask
    django_api_url = "http://localhost:8000/get_rasa_response/"
    try:
        response = requests.post(django_api_url, json=result)
        django_response = response.json()
    except Exception as e:
        django_response = {"error": str(e)}
    
    return jsonify(django_response)

if __name__ == '__main__':
    app.run(port=5000)