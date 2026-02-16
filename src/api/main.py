from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

app = FastAPI(
    title="TruthLens API",
    version="2.0.0",
    description="Backend for Fake News Detection"
)

class AnalyzeRequest(BaseModel):
    text: str
    source: str | None = None

@app.get("/")
def health_check():
    return {"status": "active", "service": "TruthLens API"}

@app.post("/api/v1/analyze")
def analyze_text(request: AnalyzeRequest):
    # Simulation of ML Inference delay
    time.sleep(0.5)
    
    # Placeholder Logic (To be replaced by model.predict)
    # Simulating DistilBERT confidence
    fake_prob = random.uniform(0.0, 1.0)
    
    label = "FAKE" if fake_prob > 0.5 else "REAL"
    risk = "HIGH" if fake_prob > 0.7 else ("MEDIUM" if fake_prob > 0.3 else "LOW")
    
    return {
        "label": label,
        "score": round(fake_prob, 4),
        "risk_level": risk,
        "model": "DistilBERT-finetuned-v1",
        "processing_time": "0.52s"
    }
