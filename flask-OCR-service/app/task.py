from celery import shared_task
from .logger_utils import info, error  # Replace direct logger usage
import pytesseract
from PIL import Image
from io import BytesIO


@shared_task
def process_image(image_bytes):
    """
    Process the image bytes and extract text using pytesseract.
    """
    try:
        # Convert byte array to PIL Image
        image = Image.open(BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        info(f"Extracted text: {extracted_text}")
        return extracted_text
    except Exception as e:
        error(f"Error processing image: {e}")
        extracted_text = None
        return None
    
