"""
Pytest fixtures for TruthLens — FastAPI test client, mocks.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

# Import app from backend when running from repo root: PYTHONPATH=truthlens or install as package
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from backend.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)
