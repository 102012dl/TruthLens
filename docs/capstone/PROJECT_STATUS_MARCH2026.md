## TruthLens — Project Status (March 2026)

**Student**: 102012dl  
**Programme**: Neoversity MSCS DS&DA  
**Repo**: `github.com/102012dl/TruthLens` (mirrored to GitLab)

### 1. Поточний статус (на березень 2026)

- **Кодова база**
  - Бекенд: FastAPI сервіс з ендпоінтами для аналізу тексту й новин.
  - NLP: `backend/nlp_processor.py` з sentiment (HF), NER (spaCy), keywords (TF‑IDF), rule‑based fake‑news score.
  - ML: модулі в `ml/` (fake news classifier, RAG, topic modeling), базові заготовки для joblib/MLflow інтеграції.
  - Dashboard: Streamlit UI (`frontend/dashboard.py`) з трьома вкладками (News Analysis, Trends, Text Analyzer).
  - Telegram‑бот: MVP у `bot/telegram_bot.py`.

- **Тести**
  - `pytest` покриває:
    - NLP‑процесор (fake_news_score, keywords, sentiment stub).
    - API‑шар (health, analyze, news search).
    - News collector.
  - Поточний статус: **усі тести проходять (18 passed)**.

- **Інфраструктура**
  - Dockerfile + docker-compose для API + допоміжних сервісів.
  - Налаштований GitHub ↔ GitLab mirror (окремий workflow, deploy key).
  - Допоміжні скрипти для аудиту та снапшотів:
    - `truthlens_full_automation.sh` — аудит, тести, git‑стан, `AUDIT_REPORT.md`.
    - `truthlens_release_snapshot.sh` — створення «snapshot» коміту з оновленим звітом.
    - `run_truthlens_frontend.sh`, `run_truthlens_mlflow.sh`, `run_truthlens_docker_smoke.sh`.

### 2. Орієнтовний відсоток виконання

- **Код / Архітектура**: ~70%
  - Основні сервіси існують, працюють і покриті тестами.
  - Потребують шліфування ML‑частина (joblib‑модель) та інтеграція RAG/multi‑agent (опційно).

- **ML‑частина**: ~50–60%
  - Є rule‑based fake news score; існують заготовки для TF‑IDF + LogReg / LinearSVC та MLflow.
  - Потрібно:
    - довести до прод‑стану joblib‑модель (`artifacts/best_model.joblib`),
    - оновити модуль аналізу, щоб використовував саме модель,
    - зафіксувати результати в MLflow і скріншотах.

- **UI / UX**: ~60–70%
  - Streamlit‑дашборд функціональний (новини, тренди, текстовий аналіз).
  - Vite/Web‑додаток є (web‑app/), але потребує завершення та узгодження зі сценарієм Capstone.

- **DevOps / Deploy**: ~50–60%
  - Локальний Docker‑деплой працює (smoke‑тести `/health`).
  - GitHub Actions mirror налаштований; потрібен остаточний огляд, щоб не ламати існуючий CI.

- **Документація / Дипломна**: ~30–40%
  - README наявний, але потребує розширення саме під Capstone.
  - Структура розділів дипломної формалізується в `THESIS_STRUCTURE.md`.
  - Потрібно розвинути розділи 3–5 (методи, результати, висновки) + додатки.

### 3. Критичні TODO (технічні)

1. **Інтегрувати справжню ML‑модель для fake news**
   - Реалізувати завантаження `artifacts/best_model.joblib` (sklearn Pipeline) у `ml/analyzer.py` / `ml/fake_news_classifier.py`.
   - Надати чистий інтерфейс `analyze_text(text)` з `{label, score, notes}`.
   - Додати sanity‑чекер (2–3 відомі приклади; логувати попередження при підозрілих результатах).

2. **Оновити та задокументувати ноутбук ISOT**
   - Переконатися, що `notebooks/01_isot_fake_news_detection.ipynb` існує (або є зрозумілий placeholder).
   - Описати в `NOTEBOOK_INTEGRATION.md`, як запустити тренування й оновити модельний артефакт.

3. **MLflow evidence**
   - Запустити MLflow UI (`run_truthlens_mlflow.sh`), зробити 3–5 ключових скріншотів.
   - Зберегти їх у `docs/mlflow-screenshots/` з осмисленими назвами.

4. **Узгодити UI для демо**
   - Визначитись: основне демо робиться через Streamlit (`frontend/dashboard.py`) чи Vite‑фронтенд.
   - Оновити README та `README_CAPSTONE.md` з чіткими інструкціями запуску обраного UI.

5. **Capstone doc pack**
   - Заповнити статус і плани в `PROJECT_STATUS_MARCH2026.md` (цей файл).
   - Підготувати перші тижневі звіти за шаблоном `WEEKLY_REPORT_TEMPLATE.md`.
   - Вирівняти опис архітектури/ML/деплою з фактичним кодом.

### 4. Ризики

- Часові обмеження:
  - ML‑модель + MLflow + документація можуть вимагати додаткового часу.
- Технічні:
  - Важливість стабільності залежностей (transformers, spacy, scikit‑learn, mlflow).
  - Обмеження ресурсів (CPU/RAM) для навчання моделі.

### 5. Що далі (short‑list)

1. Довести до кінця інтеграцію ML‑моделі fake news у код (`ml/analyzer.py`).
2. Оновити ноутбук + згенерувати MLflow evidence (скріншоти + опис).
3. Дописати/уточнити розділи 3–4 дипломної роботи (методи, результати) з посиланнями на артефакти.

