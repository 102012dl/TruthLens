"""
Tests for NewsCollector in backend.data_collector — NewsAPI, RSS, scraping.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from backend.data_collector import (
    MOCK_ARTICLES,
    MOCK_RSS_ENTRIES,
    MOCK_SCRAPED_TEXT,
    NewsCollector,
    get_collector,
    get_trends,
    search_news,
)


def test_get_collector_singleton() -> None:
    c1 = get_collector()
    c2 = get_collector()
    assert isinstance(c1, NewsCollector)
    assert c1 is c2


@pytest.mark.asyncio
async def test_fetch_newsapi_uses_mock_when_no_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NEWSAPI_KEY", raising=False)
    collector = NewsCollector(newsapi_key=None)
    articles = await collector.fetch_newsapi(query="test")
    assert isinstance(articles, list)
    # Expect mock data when key is missing.
    assert articles == MOCK_ARTICLES


@pytest.mark.asyncio
async def test_fetch_newsapi_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEWSAPI_KEY", "dummy")
    fake_response = {
        "articles": [
            {
                "title": "NewsAPI test article",
                "url": "https://example.com/newsapi",
                "publishedAt": "2024-01-01T00:00:00Z",
                "source": {"name": "UnitTestSource"},
                "content": "Body",
                "description": "Desc",
            }
        ]
    }

    class FakeResp:
        def __init__(self, data: dict) -> None:
            self._data = data

        def raise_for_status(self) -> None:  # pragma: no cover - trivial
            return None

        def json(self) -> dict:
            return self._data

    async def fake_get(url: str, *args, **kwargs):
        assert "everything" in url
        return FakeResp(fake_response)

    with patch("backend.data_collector.httpx.AsyncClient") as client_cls:
        client = MagicMock()
        client.get = AsyncMock(side_effect=fake_get)
        client_cls.return_value.__aenter__.return_value = client
        collector = NewsCollector()
        articles = await collector.fetch_newsapi(query="test")

    assert len(articles) == 1
    art = articles[0]
    assert art["title"] == "NewsAPI test article"
    assert art["source"] == "UnitTestSource"
    assert art["url"] == "https://example.com/newsapi"


@pytest.mark.asyncio
async def test_fetch_rss_uses_mock_on_error() -> None:
    with patch("backend.data_collector.httpx.AsyncClient") as client_cls:
        client = MagicMock()
        client.get = AsyncMock(side_effect=Exception("network error"))
        client_cls.return_value.__aenter__.return_value = client
        collector = NewsCollector()
        entries = await collector.fetch_rss()
    assert entries == MOCK_RSS_ENTRIES


@pytest.mark.asyncio
async def test_scrape_article_uses_mock_on_error() -> None:
    collector = NewsCollector()
    with patch("backend.data_collector.httpx.AsyncClient") as client_cls:
        client = MagicMock()
        client.get = AsyncMock(side_effect=Exception("network error"))
        client_cls.return_value.__aenter__.return_value = client
        text = await collector.scrape_article("https://example.com/fail")
    assert text == MOCK_SCRAPED_TEXT[: len(text)]


@pytest.mark.asyncio
async def test_scrape_article_parses_html() -> None:
    html = "<html><body><article><p>First paragraph.</p><p>Second paragraph.</p></article></body></html>"

    class FakeResp:
        def __init__(self, text: str) -> None:
            self.text = text

        def raise_for_status(self) -> None:  # pragma: no cover - trivial
            return None

    async def fake_get(url: str, *args, **kwargs):
        return FakeResp(html)

    collector = NewsCollector()
    with patch("backend.data_collector.httpx.AsyncClient") as client_cls:
        client = MagicMock()
        client.get = AsyncMock(side_effect=fake_get)
        client_cls.return_value.__aenter__.return_value = client
        text = await collector.scrape_article("https://example.com/article")

    assert "First paragraph." in text
    assert "Second paragraph." in text


@pytest.mark.asyncio
async def test_search_news_combines_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_newsapi(*args, **kwargs):
        return [{"title": "From NewsAPI", "url": "https://example.com/a", "published_at": None, "source": "NewsAPI", "content": "news", "description": "d"}]

    async def fake_rss(*args, **kwargs):
        return [{"title": "From RSS", "url": "https://example.com/b", "published_at": None, "source": "RSS", "summary": "rss summary"}]

    collector = NewsCollector()
    with patch.object(collector, "fetch_newsapi", new=AsyncMock(side_effect=fake_newsapi)), patch.object(
        collector, "fetch_rss", new=AsyncMock(side_effect=fake_rss)
    ), patch("backend.data_collector.get_collector", return_value=collector):
        articles = await search_news("test", limit=10)

    titles = [a["title"] for a in articles]
    assert "From NewsAPI" in titles
    assert "From RSS" in titles


@pytest.mark.asyncio
async def test_get_trends_returns_keywords(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_search_news(*args, **kwargs):
        return [
            {"content": "machine learning and data science"},
            {"content": "data science and artificial intelligence"},
        ]

    with patch("backend.data_collector.search_news", new=AsyncMock(side_effect=fake_search_news)):
        trends = await get_trends("test")

    assert isinstance(trends, list)
    assert all("keyword" in t for t in trends)
    assert any("data" in t["keyword"] or "science" in t["keyword"] for t in trends)

