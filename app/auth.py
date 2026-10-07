import os
import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def verify_api_key(
    api_key: str | None = Security(api_key_header)
) -> str:

    expected_api_key = os.getenv("API_KEY")

    if not expected_api_key:
        raise RuntimeError(
            "API_KEY environment variable is not set"
        )

    if (
        api_key is None
        or not secrets.compare_digest(
            api_key,
            expected_api_key
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

    return api_key
