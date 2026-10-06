from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data
    assert "requests_by_method" in data
    assert "responses_by_status" in data
    assert "average_duration_ms" in data