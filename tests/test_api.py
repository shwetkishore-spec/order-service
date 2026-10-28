"""API tests: check the service end to end through HTTP."""
from app.main import app

client = app.test_client()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_total_endpoint_applies_discount():
    resp = client.get("/total?cart_value=1000")
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 900


def test_total_endpoint_rejects_bad_input():
    assert client.get("/total?cart_value=abc").status_code == 400
