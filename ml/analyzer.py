"""
TruthLens ML analyzer — joblib-based fake news classifier wrapper.

Loads a scikit-learn Pipeline (TF-IDF + LinearSVC or LogisticRegression)
from ``artifacts/best_model.joblib`` and exposes a simple analyze_text()
API for the rest of the system.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import joblib

logger = logging.getLogger(__name__)


DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "best_model.joblib"


@dataclass
class FakeNewsPrediction:
    label: str
    score: float
    raw_score: float | None = None


class TruthLensAnalyzer:
    """High-level wrapper around a sklearn Pipeline for fake news detection."""

    def __init__(self, model_path: Optional[Path] = None) -> None:
        self._model_path: Path = model_path or DEFAULT_MODEL_PATH
        self._pipeline: Any | None = None

    @property
    def pipeline(self) -> Any:
        if self._pipeline is None:
            if not self._model_path.exists():
                msg = f"Model file not found at {self._model_path}"
                logger.warning(msg)
                raise FileNotFoundError(msg)
            try:
                self._pipeline = joblib.load(self._model_path)
                logger.info("Loaded fake news model from %s", self._model_path)
            except Exception as exc:  # pragma: no cover - defensive
                logger.exception("Failed to load model from %s", self._model_path)
                raise RuntimeError(f"Failed to load model: {exc}") from exc
        return self._pipeline

    def predict(self, text: str) -> FakeNewsPrediction:
        """Return structured prediction: label + score in [0, 1]."""
        if not text or not text.strip():
            return FakeNewsPrediction(label="UNKNOWN", score=0.5, raw_score=None)

        pipe = self.pipeline

        # Try to use predict_proba if available (e.g. LogisticRegression).
        label: str
        score: float
        raw_score: float | None = None

        try:
            if hasattr(pipe, "predict_proba"):
                proba = pipe.predict_proba([text])[0]
                # Assume binary [REAL, FAKE] or [FAKE, REAL]; take max prob as score.
                max_p = float(max(proba))
                pred_idx = int(proba.argmax())
                label = "FAKE" if pred_idx == 1 else "REAL"
                score = max_p
                raw_score = max_p
            elif hasattr(pipe, "decision_function"):
                # Typical for LinearSVC
                df = pipe.decision_function([text])[0]
                raw_score = float(df)
                # Map unbounded decision function to [0, 1] with a simple logistic.
                import math

                score = 1.0 / (1.0 + math.exp(-raw_score))
                label = "FAKE" if score >= 0.5 else "REAL"
            else:
                # Fallback: only predict() returning labels.
                pred = pipe.predict([text])[0]
                label = str(pred).upper()
                score = 0.5
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Model inference failed")
            raise RuntimeError(f"Model inference failed: {exc}") from exc

        return FakeNewsPrediction(label=label, score=float(round(score, 4)), raw_score=raw_score)


_analyzer: TruthLensAnalyzer | None = None


def get_analyzer() -> TruthLensAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = TruthLensAnalyzer()
    return _analyzer


def analyze_text(text: str) -> dict[str, Any]:
    """Public API: analyze text and return dict with label and score."""

    pred = get_analyzer().predict(text)
    return {
        "label": pred.label,
        "score": pred.score,
        "raw_score": pred.raw_score,
    }


def run_sanity_checks() -> None:
    """Run quick sanity checks on a couple of hand-crafted examples."""

    examples = [
        ("According to the official report, the policy was announced today.", "REAL"),
        ("SHOCKING SECRET!!! YOU WON'T BELIEVE THIS!!!", "FAKE"),
    ]
    try:
        labels = [analyze_text(text)["label"] for text, _ in examples]
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Sanity checks failed due to model error: %s", exc)
        return

    if len(set(labels)) == 1:
        logger.warning(
            "Sanity check: model returned the same label (%s) for all sanity examples.",
            labels[0],
        )

