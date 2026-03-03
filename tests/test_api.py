"""
Tests for TruthLens API endpoints — health, analyze, news, trends.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """GET /api/health returns 200 and status ok."""
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "truthlens" in data.get("service", "").lower()


def test_analyze_success(client: TestClient) -> None:
    """POST /api/analyze returns 200 and analysis when nlp_processor succeeds."""
    fake_result = {
        "sentiment": {"label": "3 stars", "score": 0.8, "stars": 3},
        "entities": [{"text": "Paris", "label": "GPE", "start": 0, "end": 5, "language": "en"}],
        "keywords": ["news", "headline"],
        "fake_news_score": 0.1,
    }
    text = "Sample news headline."
    with patch("backend.main.analyze_text", new_callable=AsyncMock, return_value=fake_result):
        r = client.post("/api/analyze", json={"text": text})
    assert r.status_code == 200
    data = r.json()
    assert data["sentiment"]["stars"] == 3
    assert data["fake_news"] == 0.1
    assert data["text_length"] == len(text)
    assert "entities" in data


def test_news_search_success(client: TestClient) -> None:
    """POST /api/news/search returns analyzed articles when NewsCollector succeeds."""
    fake_articles = [
        {
            "title": "Test article",
            "url": "https://example.com/test",
            "published_at": "2024-01-01T00:00:00Z",
            "source": "UnitTest",
            "content": "This is the content of the test article.",
        }
    ]
    fake_analysis = {
        "sentiment": {"label": "4 stars", "score": 0.9, "stars": 4},
        "entities": [],
        "keywords": ["test", "article"],
        "fake_news_score": 0.2,
    }
    with patch("backend.main.search_news", new_callable=AsyncMock, return_value=fake_articles), patch(
        "backend.main.analyze_text", new_callable=AsyncMock, return_value=fake_analysis
    ):
        r = client.post("/api/news/search", json={"query": "Ukraine", "language": "en", "days": 3})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert len(data["articles"]) == 1
    article = data["articles"][0]
    assert article["title"] == "Test article"
    assert article["sentiment"]["stars"] == 4
    assert article["fake_news"] == 0.2
    assert article["text_length"] > 0


def test_trends_success(client: TestClient) -> None:
    """POST /api/trends returns ranked keywords when NewsCollector succeeds."""
    fake_trends = ["war", "ukraine", "nato"]
    with patch("backend.main.get_trends", new_callable=AsyncMock, return_value=fake_trends):
        r = client.post("/api/trends", json={"query": "Ukraine", "language": "en", "days": 7})
    assert r.status_code == 200
    data = r.json()
    assert data["query"].lower() == "ukraine"
    assert data["language"] == "en"
    assert data["days"] == 7
    assert len(data["keywords"]) == len(fake_trends)
    returned_keywords = [k["keyword"] for k in data["keywords"]]
    for kw in fake_trends:
        assert kw in returned_keywords
