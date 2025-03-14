FROM python:3.10.6-slim

# ...existing configuration...
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app

# Expose ports for Django, Rasa server, and Rasa Actions
EXPOSE 8000 5005 5055

# Start all services via the start.py script
CMD ["python", "start.py"]
