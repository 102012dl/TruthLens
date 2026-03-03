## TruthLens Capstone — Mentor Briefing Summary

**Student**: 102012dl  
**Programme**: Neoversity MSCS DS&DA  
**Project**: TruthLens — AI‑powered information credibility analysis

### 1. 8‑тижневий план (T1–T8, високий рівень)

- **T1 — Repo baseline & audit**
  - Очищення репозиторію (видалення службових / COPY_PASTE_PROMPTS файлів).
  - Вирівнювання GitHub ↔ GitLab (gitlab mirror).
  - Базові тести, автоматизований аудит (`truthlens_full_automation.sh` + `AUDIT_REPORT.md`).

- **T2 — News Collector + Sentiment MVP + deploy fixes**
  - Запуск бекенду (FastAPI) з ендпоінтами `/api/analyze`, `/api/news/search`, `/api/trends`.
  - Асинхронний News Collector (RSS/NewsAPI) + базовий sentiment (HF pipeline) + rule‑based fake‑news heuristic.
  - Налагодження локального деплою (Docker Compose), smoke‑тести (`run_truthlens_docker_smoke.sh`).

- **T3 — Fake News v2 (ML модель) + ноутбук**
  - Навчання TF‑IDF + LinearSVC на ISOT (ноутбук `notebooks/01_isot_fake_news_detection.ipynb`).
  - Експорт `artifacts/best_model.joblib`.
  - Інтеграція моделі у код (модуль `ml/analyzer.py` / `ml/fake_news_classifier.py`) + sanity‑чекер.

- **T4 — MLflow evidence + експерименти**
  - Запис експериментів у MLflow (`./mlruns`).
  - Скриншоти з MLflow → `docs/mlflow-screenshots/`.
  - Опис ML‑пайплайна в документації (метрики, конфігурації, версії).

- **T5 — Frontend (React/Vite) + Streamlit dashboard**
  - Vite‑фронтенд (`web-app/`) як lightweight UI.
  - Streamlit‑дашборд (`frontend/dashboard.py`) для інтерактивного аналізу (вхідний текст → результат моделі).
  - Оновлення README з інструкціями запуску та демо‑сценаріями.

- **T6 — IaC / DevOps + CI/CD**
  - Огляд Dockerfile + docker-compose для прод‑режиму.
  - Перевірка/оновлення GitHub Actions (тести, mirror на GitLab).
  - Документація інфраструктури (topology diagram, опис пайплайнів).

- **T7 — Розділи дипломної 3–5 + артефакти**
  - Розділ 3 (Методи / Архітектура / Реалізація) з посиланням на код/діаграми.
  - Розділ 4 (Результати та обговорення) з таблицями метрик, графіками, скрінами MLflow/dashboards.
  - Розділ 5 (Висновки та подальша робота).

- **T8 — Фінальні правки, презентація та демо**
  - Фінальний технічний аудит (скрипт).
  - Презентація (слайди) + живе демо (API + UI + MLflow).
  - Підготовка пакету артефактів до здачі.

### 2. Обов’язковий «артефакт‑пакет» Capstone

- **1. Репозиторій коду**
  - GitHub: `https://github.com/102012dl/TruthLens`
  - GitLab mirror: `https://gitlab.com/102012dl/TruthLens`
  - Гілка `main` з проходженням тестів (CI).

- **2. Live demo / розгорнутий інстанс (за можливості)**
  - Або Streamlit (локально / хмара), або Vite‑фронтенд + бекенд.
  - Опис сценарію демо в README (кроки для перевірки функціональності).

- **3. ML‑ноутбук(и)**
  - Основний ноутбук ISOT fake‑news detection (`notebooks/01_isot_fake_news_detection.ipynb`).
  - Додаткові ноутбуки (за потреби) — аналіз помилок, абляції, порівняння моделей.

- **4. Модельні артефакти**
  - `artifacts/best_model.joblib` (TF‑IDF + LinearSVC).
  - Опис версій бібліотек і способу завантаження у прод‑коді.

- **5. MLflow evidence**
  - Локальний каталог `./mlruns` (не обов’язково в git, але згаданий у документації).
  - Скриншоти UI → `docs/mlflow-screenshots/`.

- **6. Скриншоти / демо‑матеріали**
  - UI (Streamlit/Vite) → `docs/screenshots/`.
  - API docs (`/docs` FastAPI) → `docs/screenshots/`.
  - Приклади запитів/відповідей.

- **7. Capstone‑документація в репозиторії**
  - Структура дипломної (`docs/capstone/THESIS_STRUCTURE.md`).
  - Статус проєкту (`docs/capstone/PROJECT_STATUS_MARCH2026.md`).
  - Шаблон тижневого звіту (`docs/capstone/WEEKLY_REPORT_TEMPLATE.md`).
  - README для capstone‑артефактів (`docs/capstone/README_CAPSTONE.md`).

