from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import GatewayRequestModel


def count_recent_requests(
    db: Session,
    client_id: str,
    seconds: int = 60
) -> int:

    cutoff_time = (
        datetime.now(timezone.utc)
        - timedelta(seconds=seconds)
    )

    return (
        db.query(GatewayRequestModel)
        .filter(
            GatewayRequestModel.client_id == client_id,
            GatewayRequestModel.created_at >= cutoff_time
        )
        .count()
    )


def calculate_risk_level(
    db: Session,
    client_id: str
) -> str:

    recent_request_count = count_recent_requests(
        db,
        client_id
    )

    total_with_current_request = (
        recent_request_count + 1
    )

    if total_with_current_request >= 7:
        return "HIGH"

    if total_with_current_request >= 4:
        return "MEDIUM"

    return "LOW"
