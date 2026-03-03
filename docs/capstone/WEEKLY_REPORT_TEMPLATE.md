## TruthLens Capstone — Weekly Report Template

**Student**: 102012dl  
**Week**: `YYYY‑WW` (e.g., 2026‑W02)  
**Dates**: `YYYY‑MM‑DD – YYYY‑MM‑DD`

---

### 1. Summary (3–5 речень)

- Коротко: що зроблено цього тижня, з акцентом на **результати**, а не лише на активності.

---

### 2. Work completed

- **Code / Architecture**
  - [ ] Описати ключові зміни в коді (модулі, рефакторинг, нові фічі).
- **ML / Experiments**
  - [ ] Запущені/оновлені ML‑експерименти (ноутбуки, MLflow runs).
  - [ ] Отримані метрики (Accuracy, F1, інші).
- **DevOps / Deploy**
  - [ ] Запуск Docker / CI/CD, виправлені помилки пайплайнів.
- **Documentation**
  - [ ] Оновлені Markdown‑документи (`docs/capstone/*`, README).
  - [ ] Написані/доповнені розділи дипломної (вказати сторінки/розділи).

---

### 3. Issues & Solutions

- **Issue 1**: `…`
  - Impact: `низький / середній / високий`
  - Root cause: `…`
  - Solution / workaround: `…`

- **Issue 2**: `…`
  - …

Якщо критичних проблем немає — написати коротко: «Критичних блокерів не виявлено, були лише дрібні технічні труднощі (описати).»

---

### 4. Next week plan

- **ML / Analytics**
  - [ ] Наприклад: «Довчити модель на ISOT», «Порівняти LogisticRegression vs LinearSVC», «Додати sanity‑чекер».
- **Backend / API**
  - [ ] «Додати новий ендпоінт /news/summary», «Оптимізувати аналіз тексту».
- **UI / UX**
  - [ ] «Завершити екран X у Streamlit/Vite», «Покращити відображення метрик».
- **DevOps**
  - [ ] «Дотюнити GitHub Actions / GitLab CI», «Налаштувати staging‑деплой».
- **Thesis**
  - [ ] «Написати/доповнити розділ …», «Підготувати таблиці/рисунки для розділу 4».

---

### 5. Links to artifacts

- **Repo / Branch**: `https://github.com/102012dl/TruthLens` (branch: main)
- **CI Runs**: `[посилання на останні CI‑пайплайни]`
- **Notebook(s)**:
  - `notebooks/01_isot_fake_news_detection.ipynb`
- **MLflow**:
  - UI: `http://localhost:5000` (локально; скріншоти в `docs/mlflow-screenshots/`)
- **Dashboards / UI**:
  - Streamlit: `http://localhost:8501` (локально)
  - Vite: `http://localhost:5173` (локально)
- **DOCX / Thesis**:
  - `docs/capstone/sources/AS_ACS_CSP_CS_1923_010326.docx` (зберігається вручну)

---

### 6. Checklists

- **Quality**
  - [ ] Всі тести (`pytest`) пройшли перед push.
  - [ ] Запущено `truthlens_full_automation.sh` і `AUDIT_REPORT.md` оновлено.
  - [ ] Перевірено `/health` (локально або в Docker‑деплої).

- **Documentation**
  - [ ] Оновлено `PROJECT_STATUS_MARCH2026.md` (якщо статус суттєво змінився).
  - [ ] Додані/оновлені скріншоти MLflow / UI.

