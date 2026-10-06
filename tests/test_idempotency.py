import os
import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

API_KEY = os.getenv("API_KEY")


def test_idempotent_request_behavior():
    assert API_KEY is not None, (
        "API_KEY environment variable must be set before running tests"
    )

    unique_value = uuid.uuid4().hex[:8]

    client_id = f"PYTEST_{unique_value}"
    idempotency_key = f"idem-{unique_value}"

    headers = {
        "X-API-Key": API_KEY,
        "X-Idempotency-Key": idempotency_key,
    }

    original_body = {
        "client_id": client_id,
        "request_type": "DATA_EXPORT",
        "priority": "NORMAL",
        "payload": {
            "format": "csv"
        },
    }

    # First request should create a new database record.
    first_response = client.post(
        "/requests",
        headers=headers,
        json=original_body,
    )

    assert first_response.status_code == 201, first_response.json()

    first_data = first_response.json()

    # Exact retry should return the existing request.
    duplicate_response = client.post(
        "/requests",
        headers=headers,
        json=original_body,
    )

    assert duplicate_response.status_code == 200

    duplicate_data = duplicate_response.json()

    assert duplicate_data["request_id"] == first_data["request_id"]

    # Reusing the same key with different request data is a conflict.
    changed_body = {
        "client_id": client_id,
        "request_type": "DATA_EXPORT",
        "priority": "HIGH",
        "payload": {
            "format": "pdf"
        },
    }

    conflict_response = client.post(
        "/requests",
        headers=headers,
        json=changed_body,
    )

    assert conflict_response.status_code == 409