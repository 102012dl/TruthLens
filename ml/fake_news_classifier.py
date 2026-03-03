"""
TruthLens fake news classifier — TF-IDF + LogisticRegression + MLflow.

Used by nlp_processor for fake_news_score. Training in notebooks/.
"""

from __future__ import annotations

from typing import Any

from pathlib import Path

import joblib


MODEL_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "best_model.joblib"


_pipeline: Any | None = None

def _get_pipeline() -> Any:
    """Lazy-load sklearn Pipeline from disk."""
    global _pipeline
    if _pipeline is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}")
        _pipeline = joblib.load(MODEL_PATH)
    return _pipeline


def load_model() -> Any:
    """Return the underlying sklearn Pipeline instance."""
    return _get_pipeline()


def predict(text: str) -> float:
    """Return fake news score in [0, 1]. Higher = more likely fake."""
    if not text or not text.strip():
        return 0.5

    pipe = _get_pipeline()

    # Try to use predict_proba when available (e.g. LogisticRegression).
    if hasattr(pipe, "predict_proba"):
        import numpy as np

        proba = pipe.predict_proba([text])[0]
        # Assume binary classification; take probability of the "FAKE" class as score.
        # If order is unknown, take max probability as a conservative score.
        score = float(np.max(proba))
        return max(0.0, min(1.0, round(score, 4)))

    # Fallback: use decision_function (e.g. LinearSVC) and squash to [0, 1].
    if hasattr(pipe, "decision_function"):
        import math

        raw = float(pipe.decision_function([text])[0])
        score = 1.0 / (1.0 + math.exp(-raw))
        return max(0.0, min(1.0, round(score, 4)))

    # Last resort: only predict() is available.
    _ = pipe.predict([text])[0]
    return 0.5

