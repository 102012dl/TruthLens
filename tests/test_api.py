from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TruthLens API is running", "version": "1.0.0"}

def test_analyze_endpoint():
    payload = {"text": "This is a long enough text to be analyzed by the algorithm."}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    assert "score" in response.json()
    assert "risk_level" in response.json()
