import os
import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

API_KEY = os.getenv("API_KEY")


def test_burst_risk_levels_and_blocking():
    assert API_KEY is not None, (
        "API_KEY environment variable must be set before running tests"
    )

    unique_value = uuid.uuid4().hex[:8]
    client_id = f"RISK_{unique_value}"

    body = {
        "client_id": client_id,
        "request_type": "DATA_EXPORT",
        "priority": "NORMAL",
        "payload": {
            "format": "csv"
        },
    }

    expected_risk_levels = [
        "LOW",
        "LOW",
        "LOW",
        "MEDIUM",
        "MEDIUM",
        "MEDIUM",
    ]

    for request_number, expected_risk in enumerate(
        expected_risk_levels,
        start=1,
    ):
        response = client.post(
            "/requests",
            headers={
                "X-API-Key": API_KEY,
                "X-Idempotency-Key": (
                    f"risk-{unique_value}-{request_number}"
                ),
            },
            json=body,
        )

        assert response.status_code == 201, response.json()
        assert response.json()["risk_level"] == expected_risk

    seventh_response = client.post(
        "/requests",
        headers={
            "X-API-Key": API_KEY,
            "X-Idempotency-Key": f"risk-{unique_value}-7",
        },
        json=body,
    )

    assert seventh_response.status_code == 429