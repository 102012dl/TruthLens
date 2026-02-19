from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio
from src.ml.analyzer import TruthLensAnalyzer

app = FastAPI(
    title="TruthLens API",
    version="2.0.0",
    description="AI-Powered Information Credibility Analysis"
)

analyzer = TruthLensAnalyzer()

class AnalyzeRequest(BaseModel):
    text: str
    source: Optional[str] = None
    url: Optional[str] = None

@app.get("/")
def root():
    return {"status": "active", "service": "TruthLens API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/analyze")
def analyze(request: AnalyzeRequest):
    if not request.text or len(request.text) < 10:
        raise HTTPException(status_code=422, detail="Text too short")
    result = asyncio.run(analyzer.analyze(request.text, url=request.url))
    return {
        "label": "FAKE" if result.credibility_score < 50 else "REAL",
        "score": round(result.credibility_score / 100, 2),
        "risk_level": result.verdict,
        "sentiment": result.sentiment.value,
        "bias_level": result.bias_level,
        "manipulative_techniques": [t.value for t in result.manipulative_techniques],
        "key_findings": result.key_findings,
        "recommendations": result.recommendations,
        "model": "TruthLens-v2.0"
    }
