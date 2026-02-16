# TruthLens: NLP News Intelligence Platform 🛡️

![Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Coverage](https://img.shields.io/badge/coverage-85%25-green)

**TruthLens** is a Capstone Project for the Master of Science in Computer Science program. It is an automated SaaS platform designed to detect fake news using advanced NLP techniques (DistilBERT) and MLOps principles.

## 🏗️ Technical Architecture
The project follows a microservice architecture tailored for scalability:
- **Core ML:** PyTorch & HuggingFace Transformers (DistilBERT).
- **Backend:** FastAPI for asynchronous inference.
- **Frontend:** Streamlit for interactive dashboard.
- **MLOps:** MLflow for experiment tracking.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker (optional)

### Installation
```bash
git clone https://github.com/102012dl/TruthLens.git
cd TruthLens
pip install -r requirements.txt
```

### Running the API
```bash
uvicorn src.api.main:app --reload
```
Visit `http://localhost:8000/docs` for Swagger UI.

## 📊 Evaluation
Current model (DistilBERT) achieves **~98.5% Accuracy** on the ISOT dataset.

## 👤 Author
**102012dl**
- Email: 102012dl@gmail.com
