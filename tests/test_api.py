"""
Tests for TruthLens API endpoints — health, analyze, news, trends.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """GET /api/health returns 200 and status ok."""
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "truthlens" in data.get("service", "").lower()


def test_analyze_not_implemented(client: TestClient) -> None:
    """POST /api/analyze returns 501 until nlp_processor is wired."""
    r = client.post("/api/analyze", json={"text": "Sample news headline."})
    assert r.status_code == 501


def test_news_search_not_implemented(client: TestClient) -> None:
    """POST /api/news/search returns 501 until data_collector is wired."""
    r = client.post("/api/news/search", json={"query": "Ukraine", "limit": 5})
    assert r.status_code == 501


def test_trends_not_implemented(client: TestClient) -> None:
    """POST /api/trends returns 501 until trends pipeline is wired."""
    r = client.post("/api/trends", json={"query": "election"})
    assert r.status_code == 501
