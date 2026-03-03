"""
TruthLens FastAPI application — "TruthLens API v1.0.0".

Endpoints:
- POST /api/analyze: text → {sentiment, entities, fake_news, text_length}
- POST /api/news/search: {query, language, days} → analyzed articles (limit 10)
- POST /api/trends: {query, language, days} → ranked TF-IDF keywords
- GET /api/health: service status
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.nlp_processor import NLPProcessorError, analyze_text
from backend.data_collector import get_trends, search_news


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown: load models, cleanup resources."""
    # In later phases, this can preload NLP models or warm NewsCollector connections.
    yield
    # Teardown hook if needed.


tags_metadata = [
    {
        "name": "health",
        "description": "Service health and readiness probes.",
    },
    {
        "name": "nlp",
        "description": "NLP analysis for arbitrary text: sentiment, entities, fake news heuristic.",
    },
    {
        "name": "news",
        "description": "News search & analysis using external providers (NewsCollector).",
    },
    {
        "name": "trends",
        "description": "Keyword and topic trends over recent news.",
    },
]


app = FastAPI(
    title="TruthLens API",
    description="TruthLens — SaaS NLP News Intelligence Platform (MVP).",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """Request body for POST /api/analyze."""

    text: str = Field(..., min_length=1, description="Text to analyze")


class AnalyzeResponse(BaseModel):
    """Response for POST /api/analyze."""

    sentiment: dict[str, Any]
    entities: list[dict[str, Any]]
    fake_news: float = Field(..., ge=0.0, le=1.0)
    text_length: int = Field(..., ge=0)


class NewsSearchRequest(BaseModel):
    """Request body for POST /api/news/search."""

    query: str = Field(..., min_length=1, description="Search query or topic.")
    language: str = Field(
        default="en",
        min_length=2,
        max_length=5,
        description="ISO language code (e.g. 'en', 'uk').",
    )
    days: int = Field(
        default=1,
        ge=1,
        le=30,
        description="How many recent days of news to include.",
    )


class AnalyzedArticle(BaseModel):
    """Single analyzed news article with NLP metadata."""

    title: str
    url: str | None = None
    published_at: datetime | None = None
    source: str | None = None
    sentiment: dict[str, Any]
    entities: list[dict[str, Any]]
    fake_news: float = Field(..., ge=0.0, le=1.0)
    text_length: int = Field(..., ge=0)


class NewsSearchResponse(BaseModel):
    """Response body for POST /api/news/search."""

    total: int
    articles: list[AnalyzedArticle]


class TrendsRequest(BaseModel):
    """Request body for POST /api/trends."""

    query: str = Field(..., min_length=1, description="Topic to analyze trends for.")
    language: str = Field(
        default="en",
        min_length=2,
        max_length=5,
        description="ISO language code (e.g. 'en', 'uk').",
    )
    days: int = Field(
        default=7,
        ge=1,
        le=90,
        description="How many recent days of news to analyze for trends.",
    )


class TrendKeyword(BaseModel):
    """Single trend keyword with optional score/weight."""

    keyword: str
    score: float | None = None


class TrendsResponse(BaseModel):
    """Response body for POST /api/trends."""

    query: str
    language: str
    days: int
    keywords: list[TrendKeyword]


def _extract_article_text(article: dict[str, Any]) -> str:
    """Choose the best available text field from a news article.

    Preference order: content → description → snippet/summary → title.
    """

    for key in ("content", "description", "snippet", "summary", "title"):
        value = article.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


@app.get("/api/health", tags=["health"])
async def health() -> dict[str, str]:
    """Service status & basic health information."""

    return {"status": "ok", "service": "truthlens-api"}


@app.post("/api/analyze", response_model=AnalyzeResponse, tags=["nlp"])
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze a single text snippet.

    Returns sentiment, entities, fake_news heuristic score, and text length.
    """

    try:
        result = await analyze_text(request.text)
    except NLPProcessorError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    text_length = len(request.text or "")
    return AnalyzeResponse(
        sentiment=result["sentiment"],
        entities=result["entities"],
        fake_news=result["fake_news_score"],
        text_length=text_length,
    )


@app.post("/api/news/search", response_model=NewsSearchResponse, tags=["news"])
async def news_search(request: NewsSearchRequest) -> NewsSearchResponse:
    """Search recent news and return up to 10 articles with NLP analysis.

    Uses NewsCollector (via ``search_news``) plus ``NLPProcessor`` for per-article analysis.
    """

    try:
        raw_articles = await search_news(query=request.query, limit=10)
    except Exception as exc:  # pragma: no cover - network/service errors
        raise HTTPException(status_code=503, detail=f"News search failed: {exc}") from exc

    analyzed: list[AnalyzedArticle] = []
    for article in raw_articles[:10]:
        body = _extract_article_text(article)
        if not body:
            continue
        try:
            analysis = await analyze_text(body)
        except NLPProcessorError:
            # Skip articles that fail NLP to keep endpoint robust.
            continue

        analyzed.append(
            AnalyzedArticle(
                title=str(article.get("title", "")),
                url=article.get("url"),
                published_at=article.get("published_at"),
                source=(article.get("source") or article.get("source_name")),
                sentiment=analysis["sentiment"],
                entities=analysis["entities"],
                fake_news=analysis["fake_news_score"],
                text_length=len(body),
            )
        )

    return NewsSearchResponse(total=len(analyzed), articles=analyzed)


@app.post("/api/trends", response_model=TrendsResponse, tags=["trends"])
async def trends(request: TrendsRequest) -> TrendsResponse:
    """Return ranked trend keywords for the given query.

    Uses NewsCollector (``get_trends``) which should internally apply TF-IDF / BERTopic.
    """

    try:
        raw_trends = await get_trends(query=request.query)
    except Exception as exc:  # pragma: no cover - network/service errors
        raise HTTPException(status_code=503, detail=f"Trends computation failed: {exc}") from exc

    keywords: list[TrendKeyword] = []
    for item in raw_trends or []:
        if isinstance(item, str):
            keywords.append(TrendKeyword(keyword=item))
        elif isinstance(item, dict):
            kw = (
                item.get("keyword")
                or item.get("term")
                or item.get("token")
                or item.get("word")
            )
            if not kw:
                continue
            score_val = item.get("score") or item.get("weight") or item.get("value")
            score: float | None
            try:
                score = float(score_val) if score_val is not None else None
            except (TypeError, ValueError):
                score = None
            keywords.append(TrendKeyword(keyword=str(kw), score=score))

    return TrendsResponse(
        query=request.query,
        language=request.language,
        days=request.days,
        keywords=keywords,
    )

