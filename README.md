# 🔍 TruthLens - AI-Powered Information Credibility Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-blue.svg)](.github/workflows)
[![Security](https://img.shields.io/badge/Security-Bandit%20%7C%20Snyk-red.svg)](docs/SECURITY.md)

> **Capstone Project | Neoversity | Data Science & Machine Learning**
> 
> Author: 102012dl | Email: 102012dl@gmail.com

## 📋 Зміст

- [Огляд проєкту](#-огляд-проєкту)
- [Архітектура](#-архітектура)
- [Технології](#-технології)
- [Швидкий старт](#-швидкий-старт)
- [ML Pipeline](#-ml-pipeline)
- [API документація](#-api-документація)
- [CI/CD](#-cicd)
- [Security](#-security)
- [Тестування](#-тестування)
- [Deployment](#-deployment)
- [Ліцензія](#-ліцензія)

---

## 🎯 Огляд проєкту

**TruthLens** — це інноваційна SaaS-платформа для аналізу достовірності інформації та виявлення дезінформації, яка поєднує:

- 🤖 **Telegram Bot** для миттєвого аналізу новин
- 🌐 **Web Dashboard** для візуалізації трендів
- 🧠 **ML/NLP Engine** для глибокого аналізу тексту
- 📊 **Analytics Platform** для бізнес-інсайтів

### Ключові можливості

| Feature | Опис |
|---------|------|
| **Credibility Score** | Оцінка достовірності 0-100% з ML алгоритмами |
| **Sentiment Analysis** | Визначення емоційного забарвлення тексту |
| **Bias Detection** | Виявлення політичного та емоційного ухилу |
| **Fact-Checking** | Автоматична перевірка фактів |
| **Source Verification** | Оцінка надійності джерел |
| **Manipulative Techniques** | Виявлення технік маніпуляції |

### Бізнес-модель (SaaS)

| Plan | Ціна/місяць | Ціна/рік | Features |
|------|-------------|----------|----------|
| **Free** | $0 | $0 | 10 аналізів/день |
| **Basic** | $19 | $190 | 100 аналізів/день, API |
| **Pro** | $49 | $490 | Unlimited, Priority |
| **Enterprise** | $299+ | $2,990+ | Custom, White-label |

**Прогнозована капіталізація**: $9-18M через 3 роки

---

## 🏗 Архітектура

```
┌─────────────────────────────────────────────────────────────────┐
│                        TruthLens Platform                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │  Telegram   │   │    Web      │   │    API      │           │
│  │    Bot      │   │  Dashboard  │   │  Clients    │           │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────┐           │
│  │              API Gateway (FastAPI)               │           │
│  │  • Rate Limiting  • Auth  • Validation          │           │
│  └────────────────────────┬────────────────────────┘           │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────┐           │
│  │              ML/NLP Engine                       │           │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │           │
│  │  │  BERT   │ │  spaCy  │ │LangChain│           │           │
│  │  └─────────┘ └─────────┘ └─────────┘           │           │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │           │
│  │  │Sentiment│ │  Bias   │ │  RAG    │           │           │
│  │  │Analysis │ │Detection│ │ System  │           │           │
│  │  └─────────┘ └─────────┘ └─────────┘           │           │
│  └────────────────────────┬────────────────────────┘           │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────┐           │
│  │              Data Layer                          │           │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │           │
│  │  │PostgreSQL│ │  Redis   │ │  S3/Minio│        │           │
│  │  └──────────┘ └──────────┘ └──────────┘        │           │
│  └─────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Технології

### Backend (Python 3.11+)

| Category | Technologies |
|----------|-------------|
| **Framework** | FastAPI 0.109+, aiogram 3.4+ |
| **ML/NLP** | transformers, spaCy, LangChain, scikit-learn |
| **Database** | PostgreSQL 15, Redis 7, SQLAlchemy 2.0 |
| **ML Ops** | MLflow, DVC, Weights & Biases |
| **Testing** | pytest, pytest-cov, pytest-asyncio |

### Frontend (TypeScript)

| Category | Technologies |
|----------|-------------|
| **Framework** | Next.js 14, React 18 |
| **Styling** | Tailwind CSS, shadcn/ui |
| **Charts** | Recharts, Chart.js |
| **State** | Zustand, React Query |

### DevOps & MLOps

| Category | Technologies |
|----------|-------------|
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions, GitLab CI |
| **Monitoring** | Prometheus, Grafana |
| **Security** | Bandit, Snyk, OWASP ZAP |

---

## 🚀 Швидкий старт

### Вимоги

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Встановлення

```bash
# 1. Клонування репозиторію
git clone https://github.com/102012dl/truthlens.git
cd truthlens

# 2. Створення віртуального середовища
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або: .\venv\Scripts\activate  # Windows

# 3. Встановлення залежностей
pip install -r requirements.txt
npm install --prefix web

# 4. Налаштування змінних середовища
cp .env.example .env
# Відредагуйте .env файл

# 5. Запуск бази даних
docker-compose up -d postgres redis

# 6. Міграції
alembic upgrade head

# 7. Запуск застосунку
make dev
```

### Docker запуск

```bash
# Повний запуск всіх сервісів
docker-compose up -d

# Перегляд логів
docker-compose logs -f
```

---

## 🧠 ML Pipeline

### Модель аналізу достовірності

```python
class TruthLensAnalyzer:
    """
    Ensemble ML модель для аналізу достовірності інформації.
    
    Components:
    - BERT: Semantic understanding
    - spaCy: NER, POS tagging
    - Sentiment Model: Emotion detection
    - Bias Classifier: Political/emotional bias
    - Fact-Checker: RAG-based verification
    """
    
    def analyze(self, text: str) -> AnalysisResult:
        # 1. Preprocessing
        cleaned_text = self.preprocess(text)
        
        # 2. Feature extraction
        features = self.extract_features(cleaned_text)
        
        # 3. Ensemble prediction
        credibility = self.credibility_model.predict(features)
        sentiment = self.sentiment_model.predict(features)
        bias = self.bias_model.predict(features)
        
        # 4. Fact-checking (RAG)
        facts = self.fact_checker.verify(text)
        
        return AnalysisResult(
            credibility_score=credibility,
            sentiment=sentiment,
            bias_score=bias,
            facts=facts
        )
```

### MLOps Pipeline

```yaml
# mlops-pipeline.yaml
stages:
  - data_collection
  - preprocessing
  - training
  - evaluation
  - deployment
  - monitoring

data_collection:
  sources:
    - news_apis
    - fact_check_databases
    - social_media
  schedule: "0 */6 * * *"  # Every 6 hours

training:
  model: TruthLensEnsemble
  hyperparameters:
    learning_rate: 0.001
    batch_size: 32
    epochs: 10
  tracking: mlflow

evaluation:
  metrics:
    - accuracy
    - f1_score
    - auc_roc
  threshold: 0.85

deployment:
  strategy: blue_green
  rollback: automatic
```

---

## 📡 API документація

### Endpoints

#### POST /api/analyze

Аналіз тексту на достовірність.

```bash
curl -X POST https://api.truthlens.ai/v1/analyze \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Breaking news: Scientists discover...",
    "language": "en",
    "detailed": true
  }'
```

**Response:**

```json
{
  "id": "analysis_123",
  "credibility_score": 78,
  "verdict": "likely_true",
  "sentiment": {
    "label": "neutral",
    "score": 0.65
  },
  "bias": {
    "level": "low",
    "type": null
  },
  "manipulative_techniques": [],
  "facts": [
    {
      "claim": "Scientists discover...",
      "verified": true,
      "sources": ["nature.com", "sciencedaily.com"]
    }
  ],
  "recommendations": [
    "Information appears credible",
    "Cross-reference with official sources"
  ]
}
```

### Rate Limits

| Plan | Requests/min | Requests/day |
|------|--------------|-------------|
| Free | 5 | 100 |
| Basic | 30 | 1,000 |
| Pro | 100 | 10,000 |
| Enterprise | Custom | Custom |

---

## 🔄 CI/CD

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Bandit
        run: bandit -r src/ -f json -o bandit-report.json
      - name: Run Snyk
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  deploy:
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: echo "Deploying..."
```

---

## 🔒 Security

### Security Checklist

- [x] Input validation & sanitization
- [x] SQL injection protection (SQLAlchemy ORM)
- [x] XSS prevention
- [x] CSRF tokens
- [x] Rate limiting
- [x] API key authentication
- [x] HTTPS/TLS encryption
- [x] Secrets management (env vars)
- [x] Dependency scanning (Snyk)
- [x] Static code analysis (Bandit)
- [x] Container security scanning

### Security Headers

```python
# security.py
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'"
}
```

---

## 🧪 Тестування

```bash
# Запуск всіх тестів
pytest

# З покриттям коду
pytest --cov=src --cov-report=html

# Тільки unit тести
pytest tests/unit/

# Тільки integration тести
pytest tests/integration/

# E2E тести
pytest tests/e2e/
```

### Test Coverage Target: >80%

---

## 📦 Deployment

### Production Deployment

```bash
# 1. Build Docker images
docker-compose -f docker-compose.prod.yml build

# 2. Push to registry
docker push ghcr.io/102012dl/truthlens:latest

# 3. Deploy
kubectl apply -f k8s/
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token | Yes |
| `OPENAI_API_KEY` | OpenAI/LLM API key | Yes |
| `SECRET_KEY` | JWT secret key | Yes |

---

## 📄 Ліцензія

MIT License - див. [LICENSE](LICENSE) файл.

---

## 👨‍💻 Автор

**102012dl**
- Email: 102012dl@gmail.com
- GitHub: [@102012dl](https://github.com/102012dl)
- GitLab: [@102012dl](https://gitlab.com/102012dl)

---

## 🙏 Подяки

- Neoversity за можливість реалізувати цей проєкт
- Ментори програми Data Science & Machine Learning
- Open-source спільнота

---

**© 2024 TruthLens. All rights reserved.**
