# 🛡️ TruthLens: AI-Powered Information Credibility Analysis Platform

![Status](https://img.shields.io/badge/Status-MVP-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)

> **Capstone Project** | Neoversity | Master of Science in Computer Science  
> **Author:** 102012dl | **Email:** 102012dl@gmail.com

## 🎯 Огляд проєкту
**TruthLens** — це SaaS-платформа для автоматизованого виявлення фейкових новин. Система використовує гібридний ансамбль моделей (TF-IDF + DistilBERT) для оцінки семантичного контексту та надійності джерел.

### 🏗 Архітектура
Проєкт побудований на мікросервісах:
- **Frontend:** Streamlit Dashboard (Port 8501)
- **Backend:** FastAPI Gateway (Port 8000)
- **ML Engine:** PyTorch / HuggingFace
- **MLOps:** MLflow & Docker Compose

## 🚀 Швидкий старт

### Через Docker (Рекомендовано)
```bash
docker-compose up --build -d
```
- **UI:** http://localhost:8501
- **API:** http://localhost:8000/docs

### Локально
```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
streamlit run src/ui/dashboard.py
```

## 📊 Результати
Модель **DistilBERT** досягає **98.5% F1-Score** на датасеті ISOT.

© 2026 TruthLens.
