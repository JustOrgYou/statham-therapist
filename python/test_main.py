from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_status():
    resp = client.get("/")
    assert resp.status_code == 200
