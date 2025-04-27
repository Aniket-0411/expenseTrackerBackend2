FROM python:3.11.5-slim

ENV PYHTONUNBUFFERED=1


WORKDIR /app
# Install Tesseract OCR engine
RUN apt-get update && apt-get install -y tesseract-ocr
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=wsgi:flask_app
EXPOSE 5000
CMD ["gunicorn","-w","4","-b","0.0.0.0:5000","wsgi:flask_app"]
