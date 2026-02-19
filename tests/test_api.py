from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "active"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_valid():
    payload = {"text": "Breaking news about aliens landing in New York City today."}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert "risk_level" in data
    assert data["label"] in ["FAKE", "REAL"]
    assert isinstance(data["score"], float)

def test_analyze_empty():
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422
