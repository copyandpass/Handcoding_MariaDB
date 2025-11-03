from fastapi.testclient import TestClient
from Handcoding_MariaDB.main import app


def test_read_root():
    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert "손코딩" in resp.json().get("message", "")
