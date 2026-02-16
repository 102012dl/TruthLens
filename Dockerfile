# Multi-stage build for optimized size
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/

# Expose ports for API (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Command is overriden by docker-compose usually, but default to API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
