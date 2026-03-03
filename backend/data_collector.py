"""
TruthLens data collector — NewsAPI, RSS (BBC, Reuters, Ukrinform), web scraping.

All I/O is async. Used by /api/news/search and /api/trends.

This module provides the `NewsCollector` class plus convenience functions
`search_news` and `get_trends` used by the FastAPI layer.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

import httpx

try:  # Optional dependency for HTML parsing
    from bs4 import BeautifulSoup  # type: ignore[reportMissingImports]
except Exception:  # pragma: no cover - optional import
    BeautifulSoup = None  # type: ignore[assignment]

try:  # Optional dependency for RSS parsing
    import feedparser  # type: ignore[reportMissingImports]
except Exception:  # pragma: no cover - optional import
    feedparser = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"
NEWSAPI_DEFAULT_LANGUAGE = "en"
NEWSAPI_DEFAULT_DAYS = 1
NEWSAPI_MAX_RESULTS = 50


RSS_FEEDS: dict[str, str] = {
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Reuters": "http://feeds.reuters.com/reuters/worldNews",
    "Ukrinform": "https://www.ukrinform.net/rss/block-lastnews",
}


MOCK_ARTICLES: list[dict[str, Any]] = [
    {
        "title": "Mock: Ukraine conflict update",
        "url": "https://example.com/mock-ukraine-conflict",
        "published_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
        "source": "MockSource",
        "content": "This is offline mock content about Ukraine used for development.",
        "description": "Offline mock article for TruthLens development.",
    }
]

MOCK_RSS_ENTRIES: list[dict[str, Any]] = [
    {
        "title": "Mock RSS: Global markets react to news",
        "link": "https://example.com/mock-rss-markets",
        "published_at": datetime(2024, 1, 2, tzinfo=timezone.utc),
        "source": "MockRSS",
        "summary": "Offline mock RSS entry for development.",
    }
]

MOCK_SCRAPED_TEXT = (
    "This is offline mock scraped article text used when HTTP access is unavailable. "
    "It allows the rest of the NLP pipeline to function in development mode."
)


@dataclass
class NewsCollector:
    """Asynchronous client for NewsAPI, RSS feeds, and HTML scraping.

    All methods are async and return plain Python dicts/strings to keep the
    FastAPI layer simple and serialization‑friendly.
    """

    newsapi_key: str | None = None

    async def fetch_newsapi(
        self,
        query: str,
        language: str = NEWSAPI_DEFAULT_LANGUAGE,
        days: int = NEWSAPI_DEFAULT_DAYS,
        max_results: int = NEWSAPI_MAX_RESULTS,
    ) -> list[dict[str, Any]]:
        """Query NewsAPI for recent articles matching `query`.

        Args:
            query: Search query or keywords.
            language: ISO language code (e.g. "en", "uk").
            days: Number of recent days to include.
            max_results: Maximum number of articles to return (NewsAPI page size).

        Returns:
            List of article dicts with keys:
            title, url, published_at (datetime|None), source, content, description.

        Notes:
            - If `NEWSAPI_KEY` is missing or any error occurs, returns mock data.
        """

        api_key = self.newsapi_key or os.getenv("NEWSAPI_KEY")
        if not api_key:
            logger.warning("NEWSAPI_KEY not set; using mock NewsAPI articles.")
            return MOCK_ARTICLES.copy()

        from_date = (datetime.now(timezone.utc) - timedelta(days=max(days, 1))).strftime(
            "%Y-%m-%d"
        )

        params = {
            "q": query,
            "language": language,
            "from": from_date,
            "pageSize": max(1, min(max_results, 100)),
            "sortBy": "publishedAt",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    NEWSAPI_ENDPOINT,
                    params=params,
                    headers={"X-Api-Key": api_key},
                )
                resp.raise_for_status()
        except Exception as exc:  # pragma: no cover - network issues
            logger.exception("NewsAPI request failed: %s", exc)
            return MOCK_ARTICLES.copy()

        data = resp.json()
        articles_raw: Iterable[dict[str, Any]] = data.get("articles") or []
        articles: list[dict[str, Any]] = []
        for a in articles_raw:
            published_at_raw = a.get("publishedAt") or a.get("published_at")
            published_at: datetime | None = None
            if isinstance(published_at_raw, str):
                try:
                    published_at = datetime.fromisoformat(
                        published_at_raw.replace("Z", "+00:00")
                    )
                except ValueError:
                    published_at = None
            articles.append(
                {
                    "title": a.get("title") or "",
                    "url": a.get("url"),
                    "published_at": published_at,
                    "source": (a.get("source") or {}).get("name") if isinstance(a.get("source"), dict) else a.get("source"),
                    "content": a.get("content") or "",
                    "description": a.get("description") or "",
                }
            )
        return articles

    async def fetch_rss(self, limit_per_feed: int = 20) -> list[dict[str, Any]]:
        """Parse configured RSS feeds and return recent entries.

        Args:
            limit_per_feed: Maximum entries to take per feed.

        Returns:
            List of entry dicts with keys:
            title, url, published_at (datetime|None), source, summary.

        Notes:
            - On error, returns mock RSS entries.
        """

        if feedparser is None:
            logger.warning("feedparser not installed; using mock RSS entries.")
            return MOCK_RSS_ENTRIES.copy()

        async def _fetch_one(name: str, url: str) -> list[dict[str, Any]]:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                # feedparser is synchronous; run it in a thread.
                parsed = await asyncio.to_thread(feedparser.parse, resp.text)
            except Exception as exc:  # pragma: no cover - network issues
                logger.exception("Failed to fetch RSS for %s: %s", name, exc)
                return []

            out: list[dict[str, Any]] = []
            for entry in parsed.entries[:limit_per_feed]:
                published_at: datetime | None = None
                published_raw = getattr(entry, "published", None) or getattr(
                    entry, "updated", None
                )
                if isinstance(published_raw, str):
                    try:
                        published_at = datetime.fromisoformat(
                            published_raw.replace("Z", "+00:00")
                        )
                    except ValueError:
                        published_at = None

                out.append(
                    {
                        "title": getattr(entry, "title", ""),
                        "url": getattr(entry, "link", None),
                        "published_at": published_at,
                        "source": name,
                        "summary": getattr(entry, "summary", ""),
                    }
                )
            return out

        tasks = [_fetch_one(name, url) for name, url in RSS_FEEDS.items()]
        try:
            results = await asyncio.gather(*tasks)
        except Exception as exc:  # pragma: no cover - unexpected
            logger.exception("RSS aggregation failed: %s", exc)
            return MOCK_RSS_ENTRIES.copy()

        combined: list[dict[str, Any]] = [item for sub in results for item in sub]
        if not combined:
            return MOCK_RSS_ENTRIES.copy()
        return combined

    async def scrape_article(self, url: str, max_chars: int = 5000) -> str:
        """Download and extract main article text from a URL.

        Args:
            url: Article URL.
            max_chars: Maximum number of characters to return.

        Returns:
            Extracted article text (may be empty). On failure, returns mock text.
        """

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                resp.raise_for_status()
        except Exception as exc:  # pragma: no cover - network issues
            logger.exception("Failed to fetch article URL %s: %s", url, exc)
            return MOCK_SCRAPED_TEXT[:max_chars]

        html = resp.text
        try:
            if BeautifulSoup is None:
                logger.warning("BeautifulSoup not installed; using mock scraped text.")
                return MOCK_SCRAPED_TEXT[:max_chars]

            soup = BeautifulSoup(html, "html.parser")
            # Prefer <article> content where possible.
            article_tag = soup.find("article")
            if article_tag:
                text = " ".join(p.get_text(" ", strip=True) for p in article_tag.find_all("p"))
            else:
                # Fallback: concat <p> tags.
                text = " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
            text = text.strip()
        except Exception as exc:  # pragma: no cover - HTML parsing issues
            logger.exception("Failed to parse HTML for URL %s: %s", url, exc)
            return MOCK_SCRAPED_TEXT[:max_chars]

        if not text:
            return MOCK_SCRAPED_TEXT[:max_chars]
        return text[:max_chars]


_collector: NewsCollector | None = None


def get_collector() -> NewsCollector:
    """Return a shared NewsCollector instance (singleton)."""

    global _collector
    if _collector is None:
        _collector = NewsCollector()
    return _collector


async def search_news(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search news from NewsAPI and RSS feeds.

    Args:
        query: Search query or topic.
        limit: Maximum number of articles to return.

    Returns:
        List of articles with fields: title, url, published_at, source, content/summary.

    Notes:
        - Combines NewsAPI and RSS results, then truncates to `limit`.
    """

    collector = get_collector()

    # Fetch NewsAPI articles and RSS entries concurrently.
    newsapi_task = asyncio.create_task(
        collector.fetch_newsapi(query=query, language=NEWSAPI_DEFAULT_LANGUAGE)
    )
    rss_task = asyncio.create_task(collector.fetch_rss())

    newsapi_articles, rss_entries = await asyncio.gather(newsapi_task, rss_task)

    articles: list[dict[str, Any]] = []
    articles.extend(newsapi_articles)
    for e in rss_entries:
        articles.append(
            {
                "title": e.get("title", ""),
                "url": e.get("url"),
                "published_at": e.get("published_at"),
                "source": e.get("source"),
                "content": e.get("summary", ""),
                "description": e.get("summary", ""),
            }
        )

    return articles[: max(1, limit)]


async def get_trends(query: str) -> list[dict[str, Any]]:
    """Get simple TF-IDF keyword trends for the given query.

    This is a lightweight, async-friendly implementation that:
    1. Fetches a small corpus of articles via `search_news`.
    2. Runs a bag‑of‑words TF-IDF over article contents.

    Returns:
        List of dicts with at least a `keyword` key and optional `score`.
    """

    from sklearn.feature_extraction.text import TfidfVectorizer

    articles = await search_news(query=query, limit=30)
    documents = [a.get("content") or a.get("description") or "" for a in articles]
    documents = [d for d in documents if isinstance(d, str) and d.strip()]
    if not documents:
        return []

    vectorizer = TfidfVectorizer(
        max_features=30,
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z\u0400-\u04FF]{3,}\b",
    )
    X = vectorizer.fit_transform(documents)
    scores = X.sum(axis=0).A1
    names = vectorizer.get_feature_names_out()
    indices = scores.argsort()[::-1]

    trends: list[dict[str, Any]] = []
    for idx in indices[:20]:
        if scores[idx] <= 0:
            continue
        trends.append({"keyword": names[idx], "score": float(scores[idx])})
    return trends

