## TruthLens — Notebook & Model Integration

Цей документ описує, як пов’язані між собою ноутбуки, MLflow та модельний артефакт `artifacts/best_model.joblib`, що використовується у прод‑коді.

### 1. Основний ноутбук ISOT

- Рекомендований файл:
  - `notebooks/01_isot_fake_news_detection.ipynb`
- Якщо фактичний ноутбук з експериментами вже існує під іншою назвою (наприклад,  
  `notebooks/notebooks_01_isot_fake_news_detection_mlflow.ipynb`), то:
  - можна:
    - або перейменувати його відповідно,
    - або створити легкий wrapper‑ноутбук `01_isot_fake_news_detection.ipynb`, який імпортує/пояснює існуючий.

### 2. Кроки тренування моделі

1. **Підготовка середовища**
   ```bash
   cd truthlens
   python -m venv .venv
   source .venv/bin/activate  # або .venv\Scripts\activate у Windows
   pip install -r requirements.txt
   ```

2. **Запуск Jupyter / VS Code / інший інструмент**
   - Відкрити папку `truthlens/`.
   - Запустити ноутбук `notebooks/01_isot_fake_news_detection.ipynb`.

3. **Логіка ноутбука (рекомендований сценарій)**
   - Завантаження датасету ISOT (True/Fake news).
   - Попередня обробка (чистка тексту, train/test split).
   - Побудова sklearn‑Pipeline:
     - `TfidfVectorizer` (word‑level, n‑grams, стоп‑слова).
     - `LinearSVC` або LogisticRegression як класифікатор.
   - Оцінка моделі:
     - Accuracy, Precision, Recall, F1‑score.
     - Конфузійна матриця.
   - Логування в MLflow:
     - `mlflow.log_params`, `mlflow.log_metrics`.
     - `mlflow.sklearn.log_model` (опційно).

4. **Експорт модельного артефакту**
   - Після вибору найкращої моделі:
     ```python
     import joblib
     from pathlib import Path

     artifacts_dir = Path("artifacts")
     artifacts_dir.mkdir(exist_ok=True)
     joblib.dump(best_pipeline, artifacts_dir / "best_model.joblib")
     ```
   - Переконатися, що `artifacts/best_model.joblib` існує й має адекватний розмір (десятки мегабайт максимум).

### 3. Інтеграція моделі у код

- В ML‑модулі (наприклад, `ml/analyzer.py` або `ml/fake_news_classifier.py`) використовується:
  ```python
  from pathlib import Path
  import joblib

  DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "best_model.joblib"

  def load_model(path: Path | None = None):
      mp = path or DEFAULT_MODEL_PATH
      pipeline = joblib.load(mp)
      return pipeline
  ```

- Високорівнева функція `analyze_text(text: str) -> dict`:
  - Завантажує pipeline (кешовано).
  - Виконує `predict` / `decision_function` або `predict_proba`.
  - Повертає:
    ```python
    {
      "label": "FAKE" or "REAL",
      "score": float,   # наприклад, ймовірність або нормований score
      "details": {...}  # додаткові поля за потреби
    }
    ```

### 4. Sanity‑чекер (обов’язково для прод‑режиму)

- У модулі аналізу бажано додати просту функцію:
  ```python
  def run_sanity_checks():
      samples = [
          ("Official government press release about policy.", "REAL"),
          ("SHOCKING SECRET! You won't believe this!!!", "FAKE"),
      ]
      preds = [analyze_text(t)["label"] for t, _ in samples]
      if len(set(preds)) == 1:
          logger.warning("Sanity check: model predicts one label for all test samples.")
  ```

- Цю функцію можна викликати:
  - один раз при завантаженні моделі (лог для дев‑режиму),
  - або вручну під час налагодження.

### 5. MLflow + скріншоти для диплома

- Після запуску експериментів:
  ```bash
  ~/run_truthlens_mlflow.sh
  # UI: http://localhost:5000
  ```
- Зробити скріншоти:
  - сторінки з найкращим run (F1 ≈ 0.9947, accuracy ≈ 0.9942),
  - списку експериментів,
  - порівняння кількох моделей (якщо є).
- Зберегти їх у `docs/mlflow-screenshots/` (імена файлів: `mlflow_best_run.png`, `mlflow_experiments_overview.png`, тощо).

