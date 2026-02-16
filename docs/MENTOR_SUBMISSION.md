# 🎓 TruthLens - Документація для Ментора

## Capstone Project | Neoversity | Data Science & Machine Learning

---

**Студент:** 102012dl  
**Email:** 102012dl@gmail.com  
**Дата:** Лютий 2026  

---

## 📋 Зміст проєкту

### 1. Файли проєкту

```
truthless_github_package/
├── README.md                    # Основна документація
├── requirements.txt             # Python залежності
├── pyproject.toml               # Конфігурація проєкту
├── Dockerfile                   # Docker образ
├── docker-compose.yml           # Docker Compose
├── Makefile                     # Команди автоматизації
├── .env.example                 # Змінні середовища
├── .gitignore                   # Git ignore
├── LICENSE                      # MIT ліцензія
│
├── src/                         # Вихідний код
│   ├── ml/                      # ML/NLP модуль
│   │   └── analyzer.py          # Основний аналізатор
│   ├── api/                     # FastAPI backend
│   │   └── main.py              # API endpoints
│   └── bot/                     # Telegram bot
│       └── main.py              # aiogram 3.x bot
│
├── tests/                       # Тести
│   ├── test_analyzer.py         # Unit тести аналізатора
│   └── test_api.py              # API тести
│
├── notebooks/                   # Jupyter notebooks
│   └── TruthLens_Capstone_Project.ipynb  # 📓 Основний notebook
│
├── scripts/                     # Скрипти
│   └── init-db.sql              # Ініціалізація БД
│
├── docs/                        # Документація
│   ├── SECURITY.md              # Security policy
│   └── MENTOR_SUBMISSION.md     # Цей файл
│
└── .github/workflows/           # CI/CD
    ├── ci.yml                   # Основний pipeline
    └── security.yml             # Security scanning
```

---

## 🎯 Мета проєкту

**TruthLens** - AI-платформа для аналізу достовірності інформації та виявлення дезінформації.

### Ключові функції:

1. **Credibility Scoring** - оцінка достовірності (0-100%)
2. **Sentiment Analysis** - аналіз тональності
3. **Bias Detection** - виявлення упередженості
4. **Manipulation Detection** - виявлення маніпуляцій
5. **Source Verification** - перевірка джерел

---

## 🛠 Технології

| Категорія | Технології |
|----------|------------|
| **Backend** | Python 3.11, FastAPI, aiogram 3.x |
| **ML/NLP** | BERT, spaCy, LangChain, scikit-learn |
| **Frontend** | Next.js 14, React, TypeScript |
| **Database** | PostgreSQL 15, Redis 7 |
| **DevOps** | Docker, GitHub Actions |
| **MLOps** | MLflow, DVC |

---

## 🚀 Швидкий старт

### Варіант 1: Jupyter Notebook (Google Colab)

1. Відкрийте `notebooks/TruthLens_Capstone_Project.ipynb`
2. Завантажте в Google Colab
3. Виконайте всі комірки

### Варіант 2: Локальний запуск

```bash
# Клонування
git clone https://github.com/102012dl/truthlens.git
cd truthlens

# Встановлення
make install

# Запуск тестів
make test

# Запуск API
make dev
```

### Варіант 3: Docker

```bash
docker-compose up -d
```

---

## 📊 Бізнес-модель (SaaS)

| Plan | Ціна/міс | Ціна/рік |
|------|---------|----------|
| Free | $0 | $0 |
| Basic | $19 | $19