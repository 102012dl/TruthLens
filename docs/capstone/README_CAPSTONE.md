## TruthLens Capstone — Artifacts Index

Цей документ — «мапа» всіх артефактів Capstone усередині репозиторію TruthLens.

### 1. Код і сервіс

- **Back‑end API**
  - FastAPI додаток для аналізу текстів і новин.
  - Основний модуль: `backend/main.py`
  - Запуск (локально):
    ```bash
    cd truthlens
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```
  - API Docs: `http://localhost:8000/docs`

- **NLP / ML логіка**
  - `backend/nlp_processor.py` — sentiment, NER, keywords, rule‑based fake news.
  - `ml/fake_news_classifier.py` — інтеграція з joblib‑моделлю fake news (TF‑IDF + LinearSVC).
  - `ml/analyzer.py` — високорівнева обгортка (інтерфейс `analyze_text`), якщо використовується.

### 2. NLP/ML ноутбуки

- Папка: `notebooks/`
  - **Основний ноутбук ISOT**:
    - `notebooks/01_isot_fake_news_detection.ipynb` — сценарій тренування та експорту `best_model.joblib`.
    - Якщо фактичний ноутбук має іншу назву (`notebooks_01_isot_fake_news_detection_mlflow.ipynb`), структура пояснена в `NOTEBOOK_INTEGRATION.md`.

### 3. Модельні артефакти

- Папка: `artifacts/`
  - `best_model.joblib` — основна модель fake news (TF‑IDF + LinearSVC).
  - Рекомендація: не зберігати надто великі файли в git; при потребі — описати, як їх відтворити.

### 4. MLflow експерименти

- Локальний бекенд для MLflow:
  - Каталог `./mlruns` (не обов’язково у git).
  - Скрипт запуску UI:
    ```bash
    ~/run_truthlens_mlflow.sh
    # або
    cd truthlens
    mlflow ui --backend-store-uri ./mlruns --host 0.0.0.0 --port 5000
    ```
  - Доступ: `http://localhost:5000`

- **Скріншоти MLflow**
  - Папка: `docs/mlflow-screenshots/`
  - Зберігаються ключові скріни:
    - список експериментів,
    - найкращий run (F1‑score, parameters),
    - порівняння моделей (за потреби).

### 5. Dashboards / UI

- **Streamlit dashboard**
  - Модуль: `frontend/dashboard.py`
  - Запуск (WSL):
    ```bash
    cd ~/truthlens
    streamlit run frontend/dashboard.py --server.port 8501 --server.address 0.0.0.0
    # або використати скрипт:
    ~/run_truthlens_streamlit.sh
    ```
  - URL: `http://localhost:8501`

- **Vite / web‑app frontend**
  - Папка: `web-app/`
  - Запуск:
    ```bash
    cd ~/truthlens/web-app
    npm install        # перший запуск
    npm run dev -- --host 0.0.0.0 --port 5173
    ```
  - URL: `http://localhost:5173`

- **Скріншоти UI**
  - Папка: `docs/screenshots/`
  - Рекомендовані скріни:
    - головний екран дашборду,
    - приклад аналізу тексту,
    - сторінка API docs.

### 6. Capstone‑документація

- Папка: `docs/capstone/`
  - `MENTOR_BRIEFING_SUMMARY.md` — узагальнення 8‑тижневого плану та вимог до артефактів.
  - `PROJECT_STATUS_MARCH2026.md` — поточний статус, TODO, ризики.
  - `THESIS_STRUCTURE.md` — структура дипломної роботи.
  - `WEEKLY_REPORT_TEMPLATE.md` — шаблон тижневого звіту.
  - `NOTEBOOK_INTEGRATION.md` — (буде створено) інструкція з тренування та експорту моделі.

- Папка: `docs/capstone/sources/`
  - Оригінальні DOCX‑файли дипломної/звітності (додаються вручну, не обов’язково в git).

### 7. Як користуватися цим індексом

1. **Для технічної перевірки**:
   - Запустити `truthlens_full_automation.sh` і переконатися, що всі тести пройшли.
   - Перейти за посиланнями на API, UI, MLflow.
2. **Для перевірки ML‑частини**:
   - Переглянути ноутбук(и) в `notebooks/` + скріни з MLflow.
3. **Для перевірки дипломної**:
   - Використати `THESIS_STRUCTURE.md` і тижневі звіти для оцінки прогресу.

