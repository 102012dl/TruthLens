"""
TruthLens FastAPI application — MVP API endpoints.

Endpoints: POST /api/analyze, POST /api/news/search, POST /api/trends, GET /api/health.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Placeholder until nlp_processor and data_collector are implemented
# from backend.nlp_processor import analyze_text
# from backend.data_collector import search_news, get_trends


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown: load models, cleanup."""
    yield
    # Teardown if needed


app = FastAPI(
    title="TruthLens API",
    description="MVP SaaS NLP News Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response schemas ---


class AnalyzeRequest(BaseModel):
    """Request body for POST /api/analyze."""

    text: str = Field(..., min_length=1, description="Text to analyze")


class AnalyzeResponse(BaseModel):
    """Response for POST /api/analyze."""

    sentiment: dict[str, Any]
    entities: list[dict[str, Any]]
    fake_news_score: float
    keywords: list[str]


class NewsSearchRequest(BaseModel):
    """Request body for POST /api/news/search."""

    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)


class NewsSearchResponse(BaseModel):
    """Response for POST /api/news/search."""

    articles: list[dict[str, Any]]


class TrendsRequest(BaseModel):
    """Request body for POST /api/trends."""

    query: str = Field(..., min_length=1)


class TrendsResponse(BaseModel):
    """Response for POST /api/trends."""

    trends: list[dict[str, Any]]


# --- Endpoints ---


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Service status. MVP: always healthy."""
    return {"status": "ok", "service": "truthlens-api"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze text: sentiment, NER, keywords, fake news score."""
    # TODO: call nlp_processor.analyze_text(request.text)
    raise HTTPException(status_code=501, detail="Not implemented: integrate nlp_processor")


@app.post("/api/news/search", response_model=NewsSearchResponse)
async def news_search(request: NewsSearchRequest) -> NewsSearchResponse:
    """Search news and return articles with NLP analysis."""
    # TODO: call data_collector.search_news + nlp analysis
    raise HTTPException(status_code=501, detail="Not implemented: integrate data_collector")


@app.post("/api/trends", response_model=TrendsResponse)
async def trends(request: TrendsRequest) -> TrendsResponse:
    """TF-IDF keyword trends for query."""
    # TODO: call data_collector / topic_modeler for trends
    raise HTTPException(status_code=501, detail="Not implemented: integrate trends pipeline")
