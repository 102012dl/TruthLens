# TruthLens - Copy/Paste Промпти для створення MVP

## Промпт 1: Створення ML/NLP аналізатора

```
Створи Python клас TruthLensAnalyzer для аналізу достовірності інформації.

Клас повинен включати:
1. Credibility Scoring (0-100%) - оцінка достовірності
2. Sentiment Analysis - аналіз тональності (positive, negative, neutral, mixed)
3. Bias Detection - виявлення упередженості (political, emotional, sensationalist)
4. Manipulation Detection - виявлення маніпуляцій (clickbait, emotional_appeal, appeal_to_fear)
5. Source Verification - перевірка джерел за списком надійних/ненадійних
6. Key Findings - генерація висновків
7. Recommendations - рекомендації для користувача

Використовуй dataclasses, Enum, typing. Додай docstrings.
```

---

## Промпт 2: Створення FastAPI Backend

```
Створи FastAPI застосунок для TruthLens API.

Endpoints:
1. POST /api/v1/analyze - аналіз тексту
   - Input: text (required), url (optional), language (default: "en")
   - Output: credibility_score, verdict, sentiment, bias, manipulative_techniques, key_findings, recommendations

2. GET /health - health check

3. GET /api/v1/sources - список надійних/ненадійних джерел

Додай CORS, Pydantic models, error handling, OpenAPI docs.
```

---

## Промпт 3: Створення Telegram бота

```
Створи Telegram бота для TruthLens з використанням aiogram 3.x.

Функції:
1. /start - привітання з inline keyboard
2. /help - довідка
3. /about - про бота
4. Обробка тексту - аналіз та відповідь з результатами
5. Callback handlers для inline buttons

Відповідь повинна включати:
- Оцінку достовірності (з emoji за кольором)
- Вердикт
- Тональність
- Упередженість
- Висновки та рекомендації

Українська мова інтерфейсу.
```

---

## Промпт 4: Створення Next.js Dashboard

```
Створи Next.js 14 дашборд для TruthLens.

Сторінки:
1. / - Landing page (hero, features, pricing, CTA)
2. /analyzer - Чат-інтерфейс для аналізу з demo прикладами
3. /dashboard - Аналітика з Recharts (line, pie, bar charts)
4. /history - Історія аналізів з фільтрами та експортом
5. /settings - Налаштування (тема, мова, план)

Технології:
- TypeScript
- Tailwind CSS
- shadcn/ui компоненти
- Recharts для графіків
- Framer Motion для анімацій
- Dark/Light тема
- Multi-language (UK/EN)
- Responsive design

Credibility Score показуй з кольоровим індикатором (зелений/жовтий/червоний).
```

---

## Промпт 5: CI/CD Pipeline

```
Створи GitHub Actions CI/CD pipeline для TruthLens.

Jobs:
1. lint - Black, isort, flake8, mypy
2. security - Bandit, Safety, Snyk
3. test - pytest з coverage
4. build - Docker build
5. deploy-staging - deploy на staging (develop гілка)
6. deploy-production - deploy на production (main гілка)

Сервіси для тестів: PostgreSQL, Redis.
Додай upload coverage на Codecov.
```

---

## Промпт 6: Повний MVP

```
Створи повний MVP TruthLens - AI-платформу для аналізу достовірності інформації.

Компоненти:
1. ML/NLP Engine (Python) - credibility scoring, sentiment, bias, manipulation detection
2. FastAPI Backend - REST API
3. Telegram Bot (aiogram 3.x) - миттєвий аналіз
4. Next.js Dashboard - візуалізація
5. PostgreSQL + Redis - зберігання даних
6. Docker + CI/CD - інфраструктура

SaaS модель:
- Free: $0 (10 аналізів/день)
- Basic: $19/міс (100 аналізів/день)
- Pro: $49/міс (unlimited)
- Enterprise: $299+/міс (custom)

Це Capstone Project для Neoversity Data Science.
Автор: 102012dl, email: 102012dl@gmail.com
```

---

## Промпт 7: Jupyter Notebook для презентації

```
Створи Jupyter Notebook для презентації TruthLens Capstone Project.

Секції:
1. Вступ та постановка задачі
2. Теоретична частина (NLP, BERT, Sentiment, Bias, RAG)
3. Аналіз ринку ($9.4B, конкуренти)
4. Архітектура рішення
5. ML/NLP Pipeline
6. Реалізація коду (TruthLensAnalyzer клас)
7. Демонстрація (аналіз достовірної та фейкової новини)
8. Бізнес-модель (pricing, фінансові прогнози, капіталізація)
9. Висновки
10. Додатки

Включи візуалізацію з matplotlib.
Готовий для Google Colab.
```

---

**Використовуйте ці промпти в будь-якому AI-інструменті!**
