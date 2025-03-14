FROM python:3.11.5-slim

ENV PYHTONUNBUFFERED=1


WORKDIR /app
# Install Tesseract OCR engine
RUN apt-get update && apt-get install -y tesseract-ocr

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["python", "app.py"]
