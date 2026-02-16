"""
TruthLens - API Unit Tests
==========================
Author: 102012dl
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app


class TestAPI:
    """Test suite for FastAPI endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_analyze_endpoint_success(self, client):
        """Test analyze endpoint with valid input."""
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "This is a sample news article about technology advances.",
                "language": "en",
                "detailed": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "credibility_score" in data
        assert 0 <= data["credibility_score"] <= 100
    
    def test_analyze_endpoint_with_url(self, client):
        """Test analyze endpoint with source URL."""
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "Scientists at Reuters report new findings.",
                "url": "https://www.reuters.com/article",
                "language": "en"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["source_name"] is not None
    
    def test_analyze_endpoint_short_text(self, client):
        """Test analyze endpoint with too short text."""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "Short"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_get_sources_endpoint(self, client):
        """Test get known sources endpoint."""
        response = client.get("/api/v1/sources")
        assert response.status_code == 200
        data = response.json()
        assert "reliable_sources" in data
        assert "unreliable_sources" in data
        assert len(data["reliable_sources"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
