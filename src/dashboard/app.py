"""
TruthLens Capstone — lightweight Streamlit demo using real ML model.

Shows:
- Input text → result from analyzer (artifacts/best_model.joblib when available)
- Model metrics block (F1=0.9947, accuracy ~99.42%)
- Optional sentiment stub (placeholder when API not ready)

Run from project root:
  streamlit run src/dashboard/app.py --server.port 8501 --server.address 0.0.0.0
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on path when run via streamlit
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

# Model metrics (from ISOT analysis)
MODEL_F1 = 0.9947
MODEL_ACCURACY = 0.9942


def _get_analyzer_result(text: str) -> dict:
    """Use real joblib model if available, else fallback to heuristic."""
    try:
        from ml.analyzer import analyze_text
        return analyze_text(text)
    except FileNotFoundError:
        # Model not trained yet — minimal rule-based fallback (no heavy deps)
        lower = text.lower()
        score = 0.0
        for phrase in ("shocking", "you won't believe", "!!!", "secret", "exposed"):
            if phrase in lower:
                score += 0.2
        score = min(1.0, round(score, 4))
        label = "FAKE" if score >= 0.5 else "REAL"
        return {"label": label, "score": score, "notes": "Using rule-based heuristic (artifacts/best_model.joblib not found)"}
    except Exception as e:
        return {"label": "ERROR", "score": 0.5, "notes": str(e)}


def main() -> None:
    st.set_page_config(page_title="TruthLens Demo", layout="centered")
    st.title("TruthLens — Fake News Analyzer (Capstone Demo)")

    # Model metrics block
    st.markdown("### Model metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("F1-Score", f"{MODEL_F1:.4f}")
    with col2:
        st.metric("Accuracy", f"{MODEL_ACCURACY:.2%}")
    st.caption("ISOT dataset, TF-IDF + LinearSVC pipeline")

    st.markdown("---")
    st.markdown("### Analyze text")
    text = st.text_area("Enter news text to analyze:", height=150, placeholder="Paste article or headline here...")
    if st.button("Analyze"):
        if not text or not text.strip():
            st.warning("Please enter some text.")
            return
        with st.spinner("Analyzing..."):
            result = _get_analyzer_result(text.strip())
        st.markdown("#### Result")
        label = result.get("label", "N/A")
        score = result.get("score", 0.5)
        notes = result.get("notes", "")
        st.metric("Label", label)
        st.metric("Score (0=REAL, 1=FAKE)", f"{score:.4f}")
        if notes:
            st.info(notes)

    st.markdown("---")
    st.markdown("### Sentiment (placeholder)")
    st.caption("Full sentiment analysis available via API at /api/analyze when backend is running.")


if __name__ == "__main__":
    main()
