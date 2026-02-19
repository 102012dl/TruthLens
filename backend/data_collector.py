"""
TruthLens data collector — NewsAPI, RSS (BBC, Reuters, Ukrinform), web scraping.

All I/O is async. Used by /api/news/search and /api/trends.
"""

from __future__ import annotations

from typing import Any

# TODO: NewsAPI, feedparser, aiohttp + BeautifulSoup
# import os
# from newsapi import NewsAPIClient
# import feedparser
# import aiohttp


async def search_news(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """
    Search news from NewsAPI and RSS feeds.

    Returns list of articles with title, url, published_at, source, content/snippet.
    """
    raise NotImplementedError("Data collector: integrate NewsAPI + RSS + env API key")


async def get_trends(query: str) -> list[dict[str, Any]]:
    """Get TF-IDF keyword trends for the given query (e.g. from collected corpus)."""
    raise NotImplementedError("Data collector/trends: integrate with topic_modeler or TF-IDF")
