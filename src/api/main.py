from fastapi import FastAPI
from pydantic import BaseModel
import random
import time

app = FastAPI(title="TruthLens API", version="2.0.0")

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "active", "service": "TruthLens API"}

@app.post("/api/v1/analyze")
def analyze_text(request: AnalyzeRequest):
    # Simulation of ML processing delay
    time.sleep(0.3)
    
    # Placeholder logic (Replace with DistilBERT inference later)
    fake_prob = random.uniform(0.1, 0.9)
    label = "FAKE" if fake_prob > 0.5 else "REAL"
    risk = "HIGH" if fake_prob > 0.7 else ("MEDIUM" if fake_prob > 0.3 else "LOW")
    
    return {
        "label": label,
        "score": round(fake_prob, 4),
        "risk_level": risk,
        "model": "DistilBERT-v1"
    }
