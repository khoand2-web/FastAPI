# app/tests/test_basic.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root() -> None:
    """Basic test to check docs route available."""
    r = client.get("/docs")
    assert r.status_code in (200, 307)  # depending on redirect behavior
