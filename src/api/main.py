"""
TruthLens - FastAPI Application
===============================
Main API entry point

Author: 102012dl
Email: 102012dl@gmail.com
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import asyncio

from src.ml.analyzer import TruthLensAnalyzer, create_analyzer, AnalysisResult

# ===== Pydantic Models =====

class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint."""
    text: str = Field(..., min_length=10, max_length=50000, 
                      description="Text to analyze")
    url: Optional[str] = Field(None, description="Source URL")
    language: str = Field("en", description="Language code")
    detailed: bool = Field(True, description="Include detailed analysis")

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    environment: str

class AnalyzeResponse(BaseModel):
    """Analysis response model."""
    success: bool
    credibility_score: int
    verdict: str
    sentiment: str
    sentiment_score: float
    bias_level: str
    bias_score: float
    bias_types: List[str]
    manipulative_techniques: List[str]
    manipulation_score: float
    source_credibility: Optional[float]
    source_name: Optional[str]
    key_findings: List[str]
    recommendations: List[str]
    processing_time_ms: int

# ===== Application Setup =====

app = FastAPI(
    title="TruthLens API",
    description="AI-Powered Information Credibility Analysis Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance
analyzer: Optional[TruthLensAnalyzer] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global analyzer
    analyzer = create_analyzer()
    await analyzer.load_models()

# ===== Endpoints =====

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TruthLens API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.post("/api/v1/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text for credibility.
    
    Performs comprehensive analysis including:
    - Credibility scoring (0-100)
    - Sentiment analysis
    - Bias detection
    - Manipulative technique detection
    - Source verification (if URL provided)
    """
    global analyzer
    
    if analyzer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Analyzer not initialized"
        )
    
    try:
        result = await analyzer.analyze(request.text, request.url)
        
        return AnalyzeResponse(
            success=True,
            credibility_score=result.credibility_score,
            verdict=result.verdict,
            sentiment=result.sentiment.value,
            sentiment_score=result.sentiment_score,
            bias_level=result.bias_level,
            bias_score=result.bias_score,
            bias_types=[bt.value for bt in result.bias_types],
            manipulative_techniques=[mt.value for mt in result.manipulative_techniques],
            manipulation_score=result.manipulation_score,
            source_credibility=result.source_credibility,
            source_name=result.source_name,
            key_findings=result.key_findings,
            recommendations=result.recommendations,
            processing_time_ms=result.processing_time_ms
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/api/v1/sources", tags=["Sources"])
async def get_known_sources():
    """Get list of known reliable/unreliable sources."""
    return {
        "reliable_sources": list(TruthLensAnalyzer.RELIABLE_SOURCES.keys()),
        "unreliable_sources": list(TruthLensAnalyzer.UNRELIABLE_SOURCES.keys())
    }

# ===== Error Handlers =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
