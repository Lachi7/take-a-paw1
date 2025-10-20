FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src .

# Create non-root user for security
RUN useradd -m -u 1000 petapp
USER petapp

# Environment variables for production
ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

# Use gunicorn for production instead of python app.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]