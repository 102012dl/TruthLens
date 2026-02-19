from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_read_root():
<<<<<<< HEAD
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TruthLens API is running", "version": "1.0.0"}

def test_analyze_endpoint():
    payload = {"text": "This is a long enough text to be analyzed by the algorithm."}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    assert "score" in response.json()
    assert "risk_level" in response.json()
=======
    """Перевірка доступності сервісу (Health Check)"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active", "service": "TruthLens API"}

def test_analyze_endpoint_valid():
    """Перевірка аналізу тексту (Happy Path)"""
    payload = {"text": "This is a breaking news about aliens landing in New York."}
    response = client.post("/api/v1/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Перевірка структури відповіді
    assert "label" in data
    assert "score" in data
    assert "risk_level" in data
    assert data["model"] == "DistilBERT-v1"
    
    # Перевірка типів даних
    assert isinstance(data["score"], float)
    assert data["label"] in ["FAKE", "REAL"]

def test_analyze_endpoint_empty():
    """Перевірка обробки помилок (Edge Case)"""
    # FastAPI автоматично валідує типи, тому відправляємо пустий json, 
    # щоб отримати помилку валідації (422 Unprocessable Entity)
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422
>>>>>>> 24165e1f4514abcf9f23b7a318beda28e3dc39ca
