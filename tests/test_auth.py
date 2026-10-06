import os

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

API_KEY = os.getenv("API_KEY")


def test_missing_api_key_returns_401():
    response = client.get(
        "/requests/pytest-auth-missing"
    )

    assert response.status_code == 401


def test_wrong_api_key_returns_401():
    response = client.get(
        "/requests/pytest-auth-wrong",
        headers={
            "X-API-Key": "definitely-wrong-api-key"
        },
    )

    assert response.status_code == 401


def test_correct_api_key_passes_authentication():
    assert API_KEY is not None, (
        "API_KEY environment variable must be set before running tests"
    )

    response = client.get(
        "/requests/pytest-auth-valid",
        headers={
            "X-API-Key": API_KEY
        },
    )

    assert response.status_code == 404