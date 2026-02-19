"""
TruthLens fake news classifier — TF-IDF + LogisticRegression + MLflow.

Used by nlp_processor for fake_news_score. Training in notebooks/.
"""

from __future__ import annotations

from typing import Any

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# import mlflow


def load_model() -> Any:
    """Load trained TF-IDF + LogReg from MLflow or disk. Returns (vectorizer, model)."""
    raise NotImplementedError("Load model from MLflow artifact or path")


def predict(text: str) -> float:
    """Return fake news score in [0, 1]. Higher = more likely fake."""
    raise NotImplementedError("Vectorize + model.predict_proba, track with MLflow if needed")
