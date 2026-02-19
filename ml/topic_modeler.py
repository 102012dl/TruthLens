"""
TruthLens topic modeler — BERTopic for trend extraction.

Used by /api/trends and data_collector.get_trends.
"""

from __future__ import annotations

from typing import Any

# from bertopic import BERTopic
# from sklearn.feature_extraction.text import CountVectorizer


def fit_topic_model(documents: list[str], **kwargs: Any) -> Any:
    """Fit BERTopic on corpus. Optionally log to MLflow."""
    raise NotImplementedError("BERTopic fit, optional MLflow logging")


def get_trends_from_model(model: Any, query: str, top_n: int = 10) -> list[dict[str, Any]]:
    """Return top topics/keywords for query (e.g. transform or find_topics)."""
    raise NotImplementedError("BERTopic transform / find_topics")
