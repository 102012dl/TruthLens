# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

TruthLens is an AI-powered fake-news / credibility analysis platform. It has two independently runnable frontends and a Python backend API. See `README.md` for full architecture.

### Services

| Service | Command | Port | Notes |
|---|---|---|---|
| **FastAPI API** | `uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000` | 8000 | Core backend; no database required at runtime (analyzer is in-memory) |
| **React Web App** | `npm run dev` (from `web-app/`) | 5173 | Needs `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` env vars for full functionality; renders without them but Supabase features (history) will fail |
| **Streamlit Dashboard** | `streamlit run dashboard/app.py` | 8501 | Optional; minimal stub |

### Running tests

- **Python:** `python3 -m pytest tests/ -v` from repo root (18 tests; uses `pytest-asyncio` with `asyncio_mode = auto` configured in `pytest.ini`)
- **Web-app lint:** `npx eslint .` from `web-app/`
- **Web-app type check:** `npx tsc -b` from `web-app/`

### Non-obvious caveats

- The FastAPI API does **not** connect to PostgreSQL at runtime. The `TruthLensAnalyzer` in `src/ml/analyzer.py` is entirely in-memory (keyword/regex heuristics). PostgreSQL is only needed when running via `docker-compose`.
- `~/.local/bin` must be on `PATH` for `uvicorn`, `streamlit`, and other pip-installed CLI tools to be found.
- The web-app uses `npm` (has `package-lock.json`), not pnpm or yarn.
- `python` is not aliased on this VM; use `python3` explicitly.
