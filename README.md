# TruthLens — AI-Powered Information Credibility Analysis

**Capstone Project** | Neoversity MSCS DS&DA | Author: 102012dl

TruthLens is a SaaS platform for automated news credibility analysis, fake news detection, and sentiment analysis using NLP and ML pipelines.

---

## Quickstart

### 1. Clone and setup

```bash
git clone https://github.com/102012dl/TruthLens.git
cd TruthLens
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

Create `.env` (see `.env.example`):

```bash
# Optional: API keys for news collection
NEWSAPI_KEY=your_key
OPENAI_API_KEY=your_key   # for RAG / CrewAI if used

# Optional: model path override
FAKE_NEWS_MODEL_PATH=artifacts/best_model.joblib
```

### 3. Run API

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 4. Run Streamlit dashboard (Capstone demo)

```bash
streamlit run src/dashboard/app.py --server.port 8501 --server.address 0.0.0.0
```

- Demo: http://localhost:8501

Or use the full news dashboard:

```bash
streamlit run frontend/dashboard.py --server.port 8501 --server.address 0.0.0.0
```

---

## Capstone artifacts index

All Capstone deliverables, docs, and run instructions are indexed in:

- **[docs/capstone/README_CAPSTONE.md](docs/capstone/README_CAPSTONE.md)** — "Where everything is"

Includes: notebook, API docs, dashboards, MLflow screenshots, demo screenshots, thesis structure, weekly report template.

---

## MLflow evidence

MLflow experiments and metrics are stored in `./mlruns`. Screenshots for the thesis are saved in:

- **docs/mlflow-screenshots/** — F1, accuracy, experiment runs, model comparison

To view MLflow UI locally:

```bash
mlflow ui --backend-store-uri ./mlruns --host 0.0.0.0 --port 5000
```

Then open http://localhost:5000 and capture screenshots for the capstone report.

---

## Project structure

```
TruthLens/
├── backend/          # FastAPI app, NLP processor
├── frontend/         # Streamlit news dashboard
├── src/dashboard/    # Lightweight Capstone demo (fake news analyzer)
├── ml/               # ML pipeline (analyzer, fake_news_classifier, RAG, CrewAI)
├── notebooks/       # ISOT training, MLflow experiments
├── artifacts/       # best_model.joblib (TF-IDF + LinearSVC)
├── docs/
│   ├── capstone/    # Capstone docs, thesis structure, weekly reports
│   ├── mlflow-screenshots/
│   └── screenshots/
├── tests/
└── requirements.txt
```

---

## Model training

Train the fake news model and export `artifacts/best_model.joblib`:

1. Run the notebook: `notebooks/01_isot_fake_news_detection.ipynb` (or `notebooks_01_isot_fake_news_detection_mlflow.ipynb`)
2. Log experiments to MLflow (`./mlruns`)
3. Export `joblib.dump(pipeline, "artifacts/best_model.joblib")`

See **[docs/capstone/NOTEBOOK_INTEGRATION.md](docs/capstone/NOTEBOOK_INTEGRATION.md)** for full instructions.

---

## Tests

```bash
pytest -q
```

---

## License

MIT
