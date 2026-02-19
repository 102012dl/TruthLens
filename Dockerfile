# TruthLens backend — Python 3.11, FastAPI + uvicorn
# Build: docker build -t truthlens-backend .
# Run:  docker run -p 8000:8000 --env-file .env truthlens-backend

FROM python:3.11-slim

WORKDIR /app

# System deps for build (optional: for some NLP libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App (truthlens tree)
COPY backend/ ./backend/
COPY ml/      ./ml/

# Default: run API; override for bot or streamlit
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
