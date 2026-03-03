"""
Tests for TruthLens NLPProcessor — sentiment, entities, keywords, fake_news_score.
"""

from __future__ import annotations

import pytest

import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from backend.nlp_processor import (
    NLPProcessor,
    NLPProcessorError,
    DEFAULT_RED_FLAGS,
    MIN_CHARS_FOR_KEYWORDS,
)


# --- fake_news_score (pure heuristic, no models) ---


def test_fake_news_score_empty_returns_zero() -> None:
    processor = NLPProcessor()
    assert processor.fake_news_score("") == 0.0
    assert processor.fake_news_score("   ") == 0.0


def test_fake_news_score_red_flags_increase_score() -> None:
    processor = NLPProcessor()
    normal = "The government announced a new policy today."
    with_flags = "BREAKING! URGENT! Shocking secret exposed. The government announced."
    s0 = processor.fake_news_score(normal)
    s1 = processor.fake_news_score(with_flags)
    assert s1 > s0
    assert 0 <= s0 <= 1 and 0 <= s1 <= 1


def test_fake_news_score_caps_ratio() -> None:
    processor = NLPProcessor()
    lower = "this is a calm headline about the weather."
    all_caps = "THIS IS A CALM HEADLINE ABOUT THE WEATHER."
    sc_lower = processor.fake_news_score(lower)
    sc_caps = processor.fake_news_score(all_caps)
    assert sc_caps > sc_lower


def test_fake_news_score_punctuation() -> None:
    processor = NLPProcessor()
    mild = "Is this true?"
    heavy = "Is this true?!?!?! What?!?!"
    assert processor.fake_news_score(heavy) >= processor.fake_news_score(mild)


def test_fake_news_score_custom_red_flags() -> None:
    processor = NLPProcessor(red_flags=frozenset({"custom_flag"}))
    text_with = "This article contains custom_flag and nothing else."
    text_without = "This article contains nothing suspicious."
    assert processor.fake_news_score(text_with) > processor.fake_news_score(text_without)


def test_fake_news_score_bounded() -> None:
    processor = NLPProcessor()
    assert 0 <= processor.fake_news_score("Normal text.") <= 1
    extreme = "BREAKING!!! URGENT!!! SHOCKING!!! " + "A" * 50
    assert 0 <= processor.fake_news_score(extreme) <= 1.0


# --- extract_keywords (TF-IDF, no HuggingFace/spaCy) ---


def test_extract_keywords_empty_returns_empty() -> None:
    processor = NLPProcessor()
    assert processor.extract_keywords("") == []
    assert processor.extract_keywords("ab") == []  # below min_chars


def test_extract_keywords_short_text_below_min_chars() -> None:
    processor = NLPProcessor()
    assert processor.extract_keywords("Hi there.", min_chars=100) == []


def test_extract_keywords_returns_list_of_strings() -> None:
    processor = NLPProcessor()
    text = (
        "Machine learning is a branch of artificial intelligence. "
        "Machine learning models learn from data. Data is essential for machine learning."
    )
    keywords = processor.extract_keywords(text, top_n=5)
    assert isinstance(keywords, list)
    assert all(isinstance(k, str) for k in keywords)
    assert len(keywords) <= 5
    # "learning" and "machine" should be prominent
    combined = " ".join(k.lower() for k in keywords)
    assert "learning" in combined or "machine" in combined or "data" in combined


def test_extract_keywords_respects_top_n() -> None:
    processor = NLPProcessor()
    # Multiple sentences so TF-IDF has multiple terms; ask for 3.
    text = "Alpha beta gamma. Alpha delta epsilon. Beta gamma delta."
    keywords = processor.extract_keywords(text, top_n=3)
    assert len(keywords) <= 3


# --- extract_entities (requires spaCy or mock) ---


@pytest.mark.skipif(
    True,  # Set to False to run integration tests with real spaCy
    reason="Requires spaCy en_core_web_sm; run with real model for integration",
)
def test_extract_entities_integration() -> None:
    processor = NLPProcessor()
    text = "Barack Obama met with Angela Merkel in Berlin."
    entities = processor.extract_entities(text)
    assert isinstance(entities, list)
    for e in entities:
        assert "text" in e and "label" in e
    texts = [e["text"] for e in entities]
    assert "Barack Obama" in texts or "Obama" in texts
    assert "Berlin" in texts or "Angela Merkel" in texts


def test_extract_entities_empty_returns_empty() -> None:
    processor = NLPProcessor()
    # Avoid loading spaCy by not calling on non-empty; test empty path only.
    assert processor.extract_entities("") == []
    assert processor.extract_entities("   ") == []


# --- analyze_sentiment (mock to avoid downloading BERT) ---


def test_analyze_sentiment_mocked() -> None:
    """Test sentiment with mocked pipeline returning fixed result."""
    from unittest.mock import MagicMock, patch
    processor = NLPProcessor()
    fake_result = [{"label": "4 stars", "score": 0.92}]
    with patch.object(processor, "_get_sentiment_pipeline") as get_pipe:
        get_pipe.return_value = MagicMock(return_value=fake_result)
        out = processor.analyze_sentiment("This product is great.")
    assert out["label"] == "4 stars"
    assert out["score"] == 0.92
    assert out["stars"] == 4


def test_analyze_sentiment_empty_returns_neutral() -> None:
    processor = NLPProcessor()
    out = processor.analyze_sentiment("")
    assert out["label"] == "neutral"
    assert out["score"] == 0.5
    assert out["stars"] == 3


# --- analyze (full pipeline with mocks) ---


def test_analyze_aggregates_all() -> None:
    """Full analyze() returns sentiment, entities, keywords, fake_news_score."""
    from unittest.mock import MagicMock, patch
    processor = NLPProcessor()
    fake_pipe = MagicMock(return_value=[{"label": "3 stars", "score": 0.8}])
    doc = MagicMock()
    doc.ents = []
    en_nlp = MagicMock(return_value=doc)
    with patch.object(processor, "_get_sentiment_pipeline", return_value=fake_pipe), \
         patch.object(processor, "_get_spacy_en", return_value=en_nlp), \
         patch.object(processor, "_get_spacy_uk", return_value=en_nlp):
        text = "A calm article about the economy. No caps or exclamation."
        result = processor.analyze(text)
    assert "sentiment" in result
    assert "entities" in result
    assert "keywords" in result
    assert "fake_news_score" in result
    assert result["sentiment"]["stars"] == 3
    assert isinstance(result["entities"], list)
    assert isinstance(result["keywords"], list)
    assert 0 <= result["fake_news_score"] <= 1


# --- NLPProcessorError and defaults ---


def test_default_red_flags_non_empty() -> None:
    assert len(DEFAULT_RED_FLAGS) > 0
    assert "breaking" in DEFAULT_RED_FLAGS or "BREAKING" in DEFAULT_RED_FLAGS


def test_min_chars_for_keywords_positive() -> None:
    assert MIN_CHARS_FOR_KEYWORDS >= 1
