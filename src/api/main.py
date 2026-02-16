from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(
    title="TruthLens API",
    description="NLP-powered Fake News Detection API",
    version="1.0.0"
)

class ArticleRequest(BaseModel):
    text: str
    source_url: str | None = None

@app.get("/")
async def root():
    return {"message": "TruthLens API is running", "version": "1.0.0"}

@app.post("/analyze")
async def analyze_article(request: ArticleRequest):
    """
    Analyzes the text and returns a fake news probability score.
    """
    if len(request.text) < 50:
        raise HTTPException(status_code=400, detail="Text too short for analysis")
    
    # Placeholder for ML Inference (Model will be loaded here)
    # In a real scenario, we would load the .pkl model and predict
    
    fake_score = round(random.uniform(0.1, 0.9), 4)
    label = "FAKE" if fake_score > 0.5 else "REAL"
    risk_level = "HIGH" if fake_score > 0.7 else ("MEDIUM" if fake_score > 0.3 else "LOW")

    return {
        "label": label,
        "score": fake_score,
        "risk_level": risk_level,
        "model_version": "distilbert-v1"
    }
