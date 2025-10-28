FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download all ML models during build
# This caches them in the container image (~1.4GB total)

# 1. Download spaCy model (43MB)
RUN python -m spacy download en_core_web_sm || \
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# 2. Download transformers models (Cardiff RoBERTa ~500MB + sentence-transformers ~80MB)
COPY download_models.py .
RUN python download_models.py && rm download_models.py

# Copy application
COPY src/ ./src/
COPY config/ ./config/
COPY benchmark.py .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
