from celery import shared_task
from .logger_utils import info, error  # Replace direct logger usage
import pytesseract
from PIL import Image
from io import BytesIO


@shared_task
def process_image(request):
    """
    Process the image bytes and extract text using pytesseract.
    """
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
    else:
        error("No valid image provided in either form-data or JSON payload")

    extracted_text = pytesseract.image_to_string(image)
    if not extracted_text:
        extracted_text = "No text found in the image."
    info(f"Extracted text: {extracted_text}")
    data = [{"sender": "bot", "text": extracted_text}]
    return data
