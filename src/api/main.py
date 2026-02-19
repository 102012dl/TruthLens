<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
=======
from fastapi import FastAPI
>>>>>>> 24165e1f4514abcf9f23b7a318beda28e3dc39ca
from pydantic import BaseModel
import random
import time

<<<<<<< HEAD
app = FastAPI(
    title="TruthLens API",
    version="2.0.0",
    description="Backend for Fake News Detection"
)

class AnalyzeRequest(BaseModel):
    text: str
    source: str | None = None
=======
app = FastAPI(title="TruthLens API", version="2.0.0")

class AnalyzeRequest(BaseModel):
    text: str
>>>>>>> 24165e1f4514abcf9f23b7a318beda28e3dc39ca

@app.get("/")
def health_check():
    return {"status": "active", "service": "TruthLens API"}

@app.post("/api/v1/analyze")
def analyze_text(request: AnalyzeRequest):
<<<<<<< HEAD
    # Simulation of ML Inference delay
    time.sleep(0.5)
    
    # Placeholder Logic (To be replaced by model.predict)
    # Simulating DistilBERT confidence
    fake_prob = random.uniform(0.0, 1.0)
    
=======
    # Simulation of ML processing delay
    time.sleep(0.3)
    
    # Placeholder logic (Replace with DistilBERT inference later)
    fake_prob = random.uniform(0.1, 0.9)
>>>>>>> 24165e1f4514abcf9f23b7a318beda28e3dc39ca
    label = "FAKE" if fake_prob > 0.5 else "REAL"
    risk = "HIGH" if fake_prob > 0.7 else ("MEDIUM" if fake_prob > 0.3 else "LOW")
    
    return {
        "label": label,
        "score": round(fake_prob, 4),
        "risk_level": risk,
<<<<<<< HEAD
        "model": "DistilBERT-finetuned-v1",
        "processing_time": "0.52s"
=======
        "model": "DistilBERT-v1"
>>>>>>> 24165e1f4514abcf9f23b7a318beda28e3dc39ca
    }
