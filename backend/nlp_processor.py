"""
TruthLens NLP processor — sentiment, NER, keywords, fake news scoring.

Uses: HuggingFace (nlptown/bert-base-multilingual-uncased-sentiment),
      spaCy (en_core_web_sm, uk_core_news_sm), scikit-learn TF-IDF.
"""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# Default red-flag phrases that often appear in sensational/fake news (EN/UA).
DEFAULT_RED_FLAGS: frozenset[str] = frozenset({
    "breaking", "urgent", "shocking", "you won't believe", "doctors hate",
    "secret", "exposed", "they don't want you to know", "viral", "must read",
    "breaking news", "just in", "alert", "critical", "confirmed",
    "терміново", "екстрено", "шокуюче", "таємниця", "розкрито", "важливо",
})

# Minimum text length for TF-IDF keyword extraction (avoid empty or tiny docs).
MIN_CHARS_FOR_KEYWORDS = 10


class NLPProcessorError(Exception):
    """Raised when NLP processing fails (model load, inference, etc.)."""


class NLPProcessor:
    """
    NLP pipeline: sentiment (BERT), NER (spaCy), keywords (TF-IDF), fake-news heuristic.
    Heavy models are lazy-loaded. Sync inference runs in thread pool to avoid blocking.
    """

    def __init__(
        self,
        red_flags: frozenset[str] | None = None,
        sentiment_model: str = "nlptown/bert-base-multilingual-uncased-sentiment",
    ) -> None:
        """
        Args:
            red_flags: Phrases that increase fake_news_score. Defaults to DEFAULT_RED_FLAGS.
            sentiment_model: HuggingFace model for sentiment (default: 5-star BERT).
        """
        self._red_flags = red_flags if red_flags is not None else DEFAULT_RED_FLAGS
        self._sentiment_model_id = sentiment_model
        self._sentiment_pipeline: Any = None
        self._spacy_en: Any = None
        self._spacy_uk: Any = None
        self._tfidf: Any = None

    def _get_sentiment_pipeline(self) -> Any:
        """Lazy-load HuggingFace sentiment pipeline."""
        if self._sentiment_pipeline is None:
            try:
                from transformers import pipeline
                self._sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=self._sentiment_model_id,
                    truncation=True,
                    max_length=512,
                )
            except Exception as e:
                logger.exception("Failed to load sentiment model %s", self._sentiment_model_id)
                raise NLPProcessorError(f"Sentiment model load failed: {e}") from e
        return self._sentiment_pipeline

    def _get_spacy_en(self) -> Any:
        """Lazy-load spaCy en_core_web_sm."""
        if self._spacy_en is None:
            try:
                import spacy
                self._spacy_en = spacy.load("en_core_web_sm")
            except OSError:
                # Model not installed; try downloading.
                import spacy
                from spacy.cli import download
                download("en_core_web_sm")
                self._spacy_en = spacy.load("en_core_web_sm")
            except Exception as e:
                logger.exception("Failed to load spaCy en_core_web_sm")
                raise NLPProcessorError(f"spaCy en load failed: {e}") from e
        return self._spacy_en

    def _get_spacy_uk(self) -> Any:
        """Lazy-load spaCy uk_core_news_sm."""
        if self._spacy_uk is None:
            try:
                import spacy
                self._spacy_uk = spacy.load("uk_core_news_sm")
            except OSError:
                import spacy
                from spacy.cli import download
                download("uk_core_news_sm")
                self._spacy_uk = spacy.load("uk_core_news_sm")
            except Exception as e:
                logger.exception("Failed to load spaCy uk_core_news_sm")
                raise NLPProcessorError(f"spaCy uk load failed: {e}") from e
        return self._spacy_uk

    def _is_likely_ukrainian(self, text: str) -> bool:
        """Heuristic: presence of Cyrillic suggests Ukrainian (or other Cyrillic lang)."""
        return bool(re.search(r"[\u0400-\u04FF]", text))

    def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """
        Run BERT 5-star sentiment on text.

        Args:
            text: Input (will be truncated to model max length).

        Returns:
            Dict with keys: label (str, e.g. "1 star".."5 stars"),
                            score (float 0..1), stars (int 1..5).

        Raises:
            NLPProcessorError: If model load or inference fails.
        """
        if not text or not text.strip():
            return {"label": "neutral", "score": 0.5, "stars": 3}
        try:
            pipe = self._get_sentiment_pipeline()
            result = pipe(text.strip()[:512])[0]
            # nlptown model returns label like "1 star", "2 stars", ..., "5 stars"
            label = result.get("label", "3 stars")
            score = float(result.get("score", 0.5))
            stars = 3
            for i in range(1, 6):
                if str(i) in label:
                    stars = i
                    break
            return {"label": label, "score": score, "stars": stars}
        except Exception as e:
            logger.exception("Sentiment analysis failed")
            raise NLPProcessorError(f"Sentiment analysis failed: {e}") from e

    def extract_entities(self, text: str) -> list[dict[str, Any]]:
        """
        Extract named entities using spaCy (en or uk by heuristic).

        Args:
            text: Input text.

        Returns:
            List of dicts with keys: text, label, start, end (and optionally language).
        """
        if not text or not text.strip():
            return []
        try:
            if self._is_likely_ukrainian(text):
                nlp = self._get_spacy_uk()
                lang = "uk"
            else:
                nlp = self._get_spacy_en()
                lang = "en"
            doc = nlp(text.strip())
            out: list[dict[str, Any]] = []
            for ent in doc.ents:
                out.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "language": lang,
                })
            return out
        except NLPProcessorError:
            raise
        except Exception as e:
            logger.exception("Entity extraction failed")
            raise NLPProcessorError(f"Entity extraction failed: {e}") from e

    def extract_keywords(
        self,
        text: str,
        top_n: int = 10,
        min_chars: int = MIN_CHARS_FOR_KEYWORDS,
    ) -> list[str]:
        """
        Extract top keywords using TF-IDF over sentences.

        Splits text into sentences, vectorizes with TfidfVectorizer (word level),
        and returns the top_n token (keyword) names by max TF-IDF.

        Args:
            text: Input document.
            top_n: Maximum number of keywords to return.
            min_chars: Skip extraction if text length is below this.

        Returns:
            List of keyword strings (no duplicates, order by importance).
        """
        if not text or len(text.strip()) < min_chars:
            return []
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            # Sentence split (simple: by .!? and newlines).
            raw = text.strip()
            sentences = [s.strip() for s in re.split(r"[.!?\n]+", raw) if s.strip()]
            if not sentences:
                return []
            vectorizer = TfidfVectorizer(
                max_features=top_n * 3,
                stop_words="english",
                lowercase=True,
                token_pattern=r"(?u)\b[a-zA-Z\u0400-\u04FF]{2,}\b",
            )
            X = vectorizer.fit_transform(sentences)
            # Sum TF-IDF per term across sentences, then sort.
            sums = X.sum(axis=0).A1
            names = vectorizer.get_feature_names_out()
            indices = sums.argsort()[::-1]
            seen: set[str] = set()
            keywords: list[str] = []
            for i in indices:
                if len(keywords) >= top_n or sums[i] <= 0:
                    break
                w = names[i]
                if w not in seen:
                    seen.add(w)
                    keywords.append(w)
            return keywords[:top_n]
        except Exception as e:
            logger.exception("Keyword extraction failed")
            raise NLPProcessorError(f"Keyword extraction failed: {e}") from e

    def fake_news_score(
        self,
        text: str,
        red_flags: frozenset[str] | None = None,
    ) -> float:
        """
        Rule-based heuristic fake news score in [0, 1]. Higher = more suspicious.

        Uses: red-flag phrases (case-insensitive), caps ratio, exclamation/question density.

        Args:
            text: Input text.
            red_flags: Override default red-flag set for this call.

        Returns:
            Float in [0, 1].
        """
        flags = red_flags if red_flags is not None else self._red_flags
        if not text or not text.strip():
            return 0.0
        raw = text.strip()
        lower = raw.lower()
        score = 0.0

        # Red-flag phrase count (cap contribution per phrase).
        for phrase in flags:
            if phrase.lower() in lower:
                score += 0.15
        score = min(score, 0.5)  # Cap phrase contribution at 0.5

        # Caps ratio: proportion of letters that are uppercase.
        letters = [c for c in raw if c.isalpha()]
        if letters:
            caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
            # Strong penalty for ALL CAPS or very high caps.
            if caps_ratio >= 0.9:
                score += 0.35
            elif caps_ratio >= 0.5:
                score += 0.2
            elif caps_ratio >= 0.3:
                score += 0.1
        score = min(score, 0.85)

        # Punctuation: multiple ! or ? in short span.
        exclam = len(re.findall(r"!+", raw))
        quest = len(re.findall(r"\?+", raw))
        punct_score = (exclam * 0.05) + (quest * 0.02)
        punct_score = min(punct_score, 0.2)
        score += punct_score

        return min(1.0, round(score, 4))

    def analyze(self, text: str) -> dict[str, Any]:
        """
        Run full pipeline: sentiment, entities, keywords, fake_news_score.

        Args:
            text: Input text.

        Returns:
            Dict with keys: sentiment, entities, keywords, fake_news_score.
        """
        sentiment = self.analyze_sentiment(text)
        entities = self.extract_entities(text)
        keywords = self.extract_keywords(text)
        fake_news_score = self.fake_news_score(text)
        return {
            "sentiment": sentiment,
            "entities": entities,
            "keywords": keywords,
            "fake_news_score": fake_news_score,
        }


# Singleton for use by API (lazy init).
_processor: NLPProcessor | None = None


def get_processor() -> NLPProcessor:
    """Return shared NLPProcessor instance."""
    global _processor
    if _processor is None:
        _processor = NLPProcessor()
    return _processor


async def analyze_text(text: str) -> dict[str, Any]:
    """
    Run full NLP pipeline on text (async; runs sync pipeline in thread pool).

    Returns:
        sentiment: dict with label/score/stars
        entities: list of {text, label, start, end, language}
        keywords: list of str
        fake_news_score: float [0, 1]
    """
    processor = get_processor()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, processor.analyze, text)
