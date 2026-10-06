from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import GatewayRequestModel
from app.schemas import GatewayRequest


def create_request_record(
    db: Session,
    request: GatewayRequest,
    idempotency_key: str,
    risk_level: str
) -> GatewayRequestModel:

    request_record = GatewayRequestModel(
        request_id=str(uuid4()),
        client_id=request.client_id,
        idempotency_key=idempotency_key,
        request_type=request.request_type.value,
        priority=request.priority.value,
        risk_level=risk_level,
        payload=request.payload,
        status="RECEIVED"
    )

    db.add(request_record)
    db.commit()
    db.refresh(request_record)

    return request_record


def get_request_by_id(
    db: Session,
    request_id: str
) -> GatewayRequestModel | None:

    return (
        db.query(GatewayRequestModel)
        .filter(
            GatewayRequestModel.request_id == request_id
        )
        .first()
    )

def get_request_by_idempotency_key(
    db: Session,
    client_id: str,
    idempotency_key: str
) -> GatewayRequestModel | None:

    return (
        db.query(GatewayRequestModel)
        .filter(
            GatewayRequestModel.client_id == client_id,
            GatewayRequestModel.idempotency_key == idempotency_key
        )
        .first()
    )